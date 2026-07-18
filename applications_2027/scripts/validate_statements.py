#!/usr/bin/env python3
"""Validate canonical statement prose and generated portfolio outputs."""

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

if __package__:
    from .build_statements import compose_plain, output_stem, tex_to_plain
else:  # Direct execution from applications_2027/scripts.
    from build_statements import compose_plain, output_stem, tex_to_plain


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_DIRECTION_COUNTS = Counter(
    {
        "robotics_embodied_ai": 6,
        "computer_science_ai": 14,
        "mechanical_smart_manufacturing": 5,
    }
)
EXPECTED_SCHOOL_COUNTS = Counter(
    {"cuhk": 5, "hkust": 5, "polyu": 5, "cityu": 4, "nus": 3, "ntu": 3}
)


SCHOOL_MARKERS = {
    "cuhk": ("CUHK", "Chinese University of Hong Kong"),
    "hkust": ("HKUST", "Hong Kong University of Science and Technology"),
    "polyu": ("PolyU", "Hong Kong Polytechnic University"),
    "cityu": ("CityUHK", "City University of Hong Kong"),
    "nus": ("NUS", "National University of Singapore"),
    "ntu": ("NTU", "Nanyang Technological University"),
}

WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:[.'-][A-Za-z0-9]+)*")
PLACEHOLDER_PATTERNS = (
    ("Target University", re.compile(r"\bTarget\s+University\b", re.IGNORECASE)),
    ("Student Name Here", re.compile(r"\bStudent\s+Name\s+Here\b", re.IGNORECASE)),
    ("Program Name Here", re.compile(r"\bProgram\s+Name\s+Here\b", re.IGNORECASE)),
    ("TBD", re.compile(r"\bTBD\b", re.IGNORECASE)),
    ("TODO", re.compile(r"\bTODO\b", re.IGNORECASE)),
    ("FIXME", re.compile(r"\bFIXME\b", re.IGNORECASE)),
    ("lorem ipsum", re.compile(r"\blorem\s+ipsum\b", re.IGNORECASE)),
    ("square-bracket token", re.compile(r"\[[^\]\n]*\]")),
    ("angle-bracket token", re.compile(r"<[^>\n]*>")),
)


@dataclass(frozen=True)
class ValidationIssue:
    """One validation failure tied to a program key and named check."""

    program_key: str
    check: str
    message: str


def word_count(text):
    """Count English tokens, keeping decimals and hyphenated terms intact."""
    return len(WORD_PATTERN.findall(text))


def placeholder_errors(text):
    """Return descriptions of template placeholders found in text."""
    return [label for label, pattern in PLACEHOLDER_PATTERNS if pattern.search(text)]


def _contains_marker(text, marker):
    marker_parts = marker.split()
    if not marker_parts:
        return False
    flexible_marker = r"\s+".join(re.escape(part) for part in marker_parts)
    pattern = rf"(?<![A-Za-z0-9]){flexible_marker}(?![A-Za-z0-9])"
    return re.search(pattern, text, re.IGNORECASE) is not None


def contamination_errors(text, own_school):
    """Return target-school markers that do not belong to own_school."""
    errors = []
    for school, markers in SCHOOL_MARKERS.items():
        if school == own_school:
            continue
        for marker in markers:
            if _contains_marker(text, marker):
                errors.append(f"mentions {school} via {marker!r}")
    return errors


def canonical_errors(text):
    """Return a builder-consistent error for unsupported canonical markup."""
    try:
        tex_to_plain(text)
    except ValueError as error:
        return [str(error)]
    return []


def school_marker_errors(text):
    """Return every target-school marker present in text."""
    errors = []
    for school, markers in SCHOOL_MARKERS.items():
        for marker in markers:
            if _contains_marker(text, marker):
                errors.append(f"mentions {school} via {marker!r}")
    return errors


def own_school_errors(text, program):
    """Require a program module to name its own school."""
    markers = list(SCHOOL_MARKERS.get(program.get("school"), ()))
    markers.extend((program.get("university_abbr", ""), program.get("university", "")))
    if any(marker and _contains_marker(text, marker) for marker in markers):
        return []
    return ["program module does not mention its university"]


def limit_errors(text, official_limit):
    """Enforce the default word range or a declared official maximum."""
    if official_limit is None:
        count = word_count(text)
        if 850 <= count <= 950:
            return []
        return [f"word count {count} is outside the default 850-950 range"]

    if not isinstance(official_limit, dict):
        return ["official_limit must be an object or null"]
    maximum = official_limit.get("max")
    if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum <= 0:
        return ["official_limit.max must be a positive integer"]

    unit = official_limit.get("unit")
    if unit == "words":
        count = word_count(text)
        if maximum >= 850:
            upper_bound = min(950, maximum)
            if 850 <= count <= upper_bound:
                return []
            return [
                f"word count {count} is outside the required 850-{upper_bound} range"
            ]
        if 1 <= count <= maximum:
            return []
        if count == 0:
            return ["word-limited statement must be nonempty"]
        return [f"words count {count} exceeds official maximum {maximum}"]
    elif unit == "characters":
        includes_spaces = official_limit.get("includes_spaces")
        if not isinstance(includes_spaces, bool):
            return [
                "character official_limit must declare includes_spaces as a boolean"
            ]
        body = text.strip()
        count = (
            len(body)
            if includes_spaces
            else sum(not character.isspace() for character in body)
        )
        if count == 0:
            return ["character-limited statement must be nonempty"]
        if count <= maximum:
            return []
        return [f"characters count {count} exceeds official maximum {maximum}"]
    else:
        return [f"unsupported official_limit unit: {unit!r}"]


def output_path(program, kind, root=None):
    """Return a generated Markdown or PDF path with the correct status suffix."""
    root = ROOT if root is None else Path(root)
    extensions = {"markdown": "md", "pdf": "pdf"}
    if kind not in extensions:
        raise ValueError(f"unsupported output kind: {kind}")
    return root / "output" / kind / f"{output_stem(program)}.{extensions[kind]}"


def normalize_text(text):
    """Compatibility-normalize, lowercase, and remove non-alphanumeric characters."""
    normalized = unicodedata.normalize("NFKC", text)
    return "".join(
        character for character in normalized.lower() if character.isalnum()
    )


def _strip_pdf_layout_artifacts(text, program):
    """Remove exact EasierPS header lines and isolated trailing page numbers."""
    header_lines = {
        "Personal Statement",
        "Jianming Xing",
        program["university"],
        program["university_abbr"],
        program["program"],
    }
    cleaned_pages = []
    for page in text.split("\f"):
        lines = page.splitlines()
        while lines:
            while lines and not lines[0].strip():
                lines.pop(0)
            if lines and lines[0].strip() in header_lines:
                lines.pop(0)
                continue
            break

        while lines and not lines[-1].strip():
            lines.pop()
        if lines and re.fullmatch(r"[0-9]+", lines[-1].strip()):
            lines.pop()
        while lines and not lines[-1].strip():
            lines.pop()
        cleaned_pages.append("\n".join(lines))
    return "\n".join(cleaned_pages)


def load_manifest(root=None):
    """Load program records from the portfolio manifest."""
    root = ROOT if root is None else Path(root)
    data = json.loads((root / "config" / "programs.json").read_text(encoding="utf-8"))
    return data["programs"]


def manifest_errors(programs):
    """Validate global portfolio counts independently of content selection."""
    errors = []
    keys = [program.get("key") for program in programs]
    if len(programs) != 25:
        errors.append(
            ValidationIssue(
                "manifest",
                "manifest_count",
                f"expected 25 programs, found {len(programs)}",
            )
        )
    if len(set(keys)) != len(keys):
        errors.append(
            ValidationIssue(
                "manifest", "unique_keys", "manifest program keys are not unique"
            )
        )

    direction_counts = Counter(program.get("direction") for program in programs)
    if direction_counts != EXPECTED_DIRECTION_COUNTS:
        errors.append(
            ValidationIssue(
                "manifest",
                "direction_distribution",
                f"expected {dict(EXPECTED_DIRECTION_COUNTS)}, found {dict(direction_counts)}",
            )
        )

    school_counts = Counter(program.get("school") for program in programs)
    if school_counts != EXPECTED_SCHOOL_COUNTS:
        errors.append(
            ValidationIssue(
                "manifest",
                "school_distribution",
                f"expected {dict(EXPECTED_SCHOOL_COUNTS)}, found {dict(school_counts)}",
            )
        )

    for program in programs:
        program_key = program.get("key", "manifest")
        if "compressed_derivative" not in program:
            errors.append(
                ValidationIssue(
                    program_key,
                    "compressed_derivative_field",
                    "manifest record is missing compressed_derivative",
                )
            )
            continue
        derivative = program["compressed_derivative"]
        if derivative is not None and not isinstance(derivative, str):
            errors.append(
                ValidationIssue(
                    program_key,
                    "compressed_derivative_type",
                    "compressed_derivative must be a string path or null",
                )
            )
        elif isinstance(derivative, str):
            errors.extend(
                _content_issues(
                    program_key,
                    "compressed_derivative_path",
                    derivative_path_errors(derivative),
                )
            )
            expected_limit = {
                "unit": "characters",
                "max": 2000,
                "includes_spaces": True,
            }
            if program.get("official_limit") != expected_limit:
                errors.append(
                    ValidationIssue(
                        program_key,
                        "compressed_derivative_limit",
                        "compressed derivatives require the exact 2,000-character including-spaces limit",
                    )
                )
    return errors


def _content_issues(program_key, check, messages):
    return [ValidationIssue(program_key, check, message) for message in messages]


def derivative_path_errors(value):
    """Return schema errors for a compressed-derivative source path."""
    if not isinstance(value, str) or not value:
        return ["compressed_derivative must be a nonempty string path"]
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return ["compressed_derivative must be a safe relative path"]
    if path.suffix != ".tex" or path.parts[:2] != ("content", "derivatives"):
        return [
            "compressed_derivative must be a .tex file below content/derivatives"
        ]
    return []


def validate_program(program, root=None, require_pdfs=False):
    """Validate one program's canonical sources and generated outputs."""
    root = ROOT if root is None else Path(root)
    program_key = program["key"]
    base_path = root / "content" / "base" / f"{program['direction']}.tex"
    module_path = root / program["program_module"]
    errors = []

    source_paths = (("base", base_path), ("module", module_path))
    plain_text = {}
    for source_name, path in source_paths:
        if not path.is_file():
            errors.append(
                ValidationIssue(
                    program_key,
                    f"{source_name}_exists",
                    f"missing canonical source: {path}",
                )
            )
            continue
        raw_text = path.read_text(encoding="utf-8")
        markup_errors = canonical_errors(raw_text)
        if markup_errors:
            errors.extend(
                _content_issues(
                    program_key,
                    "canonical_prose",
                    [f"{source_name} {message}" for message in markup_errors],
                )
            )
            continue
        plain_text[source_name] = tex_to_plain(raw_text).strip()

    body = None
    long_form_body = None
    if set(plain_text) == {"base", "module"}:
        long_form_body = compose_plain(base_path, module_path)
        errors.extend(
            _content_issues(
                program_key,
                "base_school_markers",
                school_marker_errors(plain_text["base"]),
            )
        )
        errors.extend(
            _content_issues(
                program_key,
                "placeholders",
                placeholder_errors(long_form_body),
            )
        )
        errors.extend(
            _content_issues(
                program_key,
                "own_school",
                own_school_errors(plain_text["module"], program),
            )
        )
        errors.extend(
            _content_issues(
                program_key,
                "cross_school_contamination",
                contamination_errors(long_form_body, program["school"]),
            )
        )

        derivative = program.get("compressed_derivative")
        long_form_check = (
            "long_form_length"
            if derivative is not None
            else "word_or_character_limit"
        )
        errors.extend(
            _content_issues(
                program_key,
                long_form_check,
                limit_errors(
                    long_form_body,
                    None if derivative is not None else program.get("official_limit"),
                ),
            )
        )

        if derivative is None:
            body = long_form_body
        elif not isinstance(derivative, str):
            errors.append(
                ValidationIssue(
                    program_key,
                    "derivative_path",
                    "compressed_derivative must be a string path",
                )
            )
        else:
            path_errors = derivative_path_errors(derivative)
            errors.extend(
                _content_issues(program_key, "derivative_path", path_errors)
            )
            if not path_errors:
                derivative_path = root / derivative
                if not derivative_path.is_file():
                    errors.append(
                        ValidationIssue(
                            program_key,
                            "derivative_exists",
                            f"missing canonical derivative: {derivative_path}",
                        )
                    )
                else:
                    raw_derivative = derivative_path.read_text(encoding="utf-8")
                    markup_errors = canonical_errors(raw_derivative)
                    if markup_errors:
                        errors.extend(
                            _content_issues(
                                program_key,
                                "derivative_canonical_prose",
                                markup_errors,
                            )
                        )
                    else:
                        derivative_plain = tex_to_plain(raw_derivative).strip()
                        body = f"{derivative_plain}\n"
                        errors.extend(
                            _content_issues(
                                program_key,
                                "derivative_placeholders",
                                placeholder_errors(body),
                            )
                        )
                        errors.extend(
                            _content_issues(
                                program_key,
                                "derivative_own_school",
                                own_school_errors(derivative_plain, program),
                            )
                        )
                        errors.extend(
                            _content_issues(
                                program_key,
                                "derivative_cross_school_contamination",
                                contamination_errors(body, program["school"]),
                            )
                        )
                        errors.extend(
                            _content_issues(
                                program_key,
                                "word_or_character_limit",
                                limit_errors(body, program.get("official_limit")),
                            )
                        )

    if body is not None:
        markdown_path = output_path(program, "markdown", root)
        if not markdown_path.is_file():
            errors.append(
                ValidationIssue(
                    program_key,
                    "markdown_exists",
                    f"missing generated Markdown: {markdown_path}",
                )
            )
        elif markdown_path.read_text(encoding="utf-8") != body:
            errors.append(
                ValidationIssue(
                    program_key,
                    "markdown_parity",
                    f"generated Markdown differs from canonical body: {markdown_path}",
                )
            )

    if require_pdfs:
        pdf_path = output_path(program, "pdf", root)
        if not pdf_path.is_file():
            errors.append(
                ValidationIssue(
                    program_key,
                    "pdf_exists",
                    f"missing generated PDF: {pdf_path}",
                )
            )
        elif body is not None:
            try:
                result = subprocess.run(
                    ["pdftotext", str(pdf_path), "-"],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except (OSError, subprocess.CalledProcessError) as error:
                errors.append(
                    ValidationIssue(
                        program_key,
                        "pdftotext",
                        f"could not extract PDF text: {error}",
                    )
                )
            else:
                extracted_body = _strip_pdf_layout_artifacts(result.stdout, program)
                if normalize_text(body) not in normalize_text(extracted_body):
                    errors.append(
                        ValidationIssue(
                            program_key,
                            "pdf_text_parity",
                            "normalized PDF extraction does not contain canonical body",
                        )
                    )

    return errors


def _plural(count, singular, plural=None):
    if count == 1:
        return singular
    return plural if plural is not None else f"{singular}s"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-pdfs",
        action="store_true",
        help="also require status-aware PDFs and extracted-text parity",
    )
    parser.add_argument(
        "--only",
        action="append",
        metavar="KEY",
        help="validate one program key; may be supplied more than once",
    )
    args = parser.parse_args(argv)

    try:
        programs = load_manifest()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"[manifest] load_manifest: {error}", file=sys.stderr)
        print("FAIL: 1 error, 0 programs", file=sys.stderr)
        return 1

    errors = manifest_errors(programs)
    if args.only:
        programs_by_key = {program.get("key"): program for program in programs}
        selected = []
        selected_keys = set()
        for requested_key in args.only:
            if requested_key in selected_keys:
                continue
            selected_keys.add(requested_key)
            program = programs_by_key.get(requested_key)
            if program is None:
                errors.append(
                    ValidationIssue(
                        requested_key,
                        "selection",
                        "unknown program key",
                    )
                )
            else:
                selected.append(program)
    else:
        selected = programs

    passing_keys = []
    for program in selected:
        program_errors = validate_program(program, require_pdfs=args.require_pdfs)
        errors.extend(program_errors)
        if not program_errors:
            passing_keys.append(program["key"])

    for program_key in passing_keys:
        print(f"PASS: {program_key}")

    if errors:
        for error in errors:
            print(
                f"[{error.program_key}] {error.check}: {error.message}",
                file=sys.stderr,
            )
        error_count = len(errors)
        program_count = len(selected)
        print(
            f"FAIL: {error_count} {_plural(error_count, 'error')}, "
            f"{program_count} {_plural(program_count, 'program')}",
            file=sys.stderr,
        )
        return 1

    print(f"PASS: {len(selected)} programs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
