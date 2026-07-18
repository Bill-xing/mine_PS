#!/usr/bin/env python3
"""Generate statement entry files, plain Markdown, and compiled PDFs."""

import argparse
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_manifest():
    """Return the program records from the portfolio manifest."""
    data = json.loads(
        (ROOT / "config" / "programs.json").read_text(encoding="utf-8")
    )
    return data["programs"]


def output_stem(program):
    """Return the status-aware output filename stem for a program."""
    if program["output_status"] == "provisional":
        return f"{program['key']}-provisional"
    return program["key"]


def latex_escape(text):
    """Escape LaTeX metacharacters in entry-point metadata."""
    escapes = {
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "$": r"\$",
        "{": r"\{",
        "}": r"\}",
        "^": r"\^{}",
    }
    return "".join(escapes.get(character, character) for character in text)


def tex_to_plain(text):
    """Convert canonical prose to plain text, rejecting LaTeX markup."""
    plain = []
    index = 0
    while index < len(text):
        character = text[index]
        if character != "\\":
            if character in "%&#_$^{}~":
                raise ValueError(
                    "Canonical prose may contain only escaped percent and ampersand signs"
                )
            plain.append(character)
            index += 1
            continue

        if index + 1 >= len(text) or text[index + 1] not in "%&":
            raise ValueError(
                "Canonical prose may contain only escaped percent and ampersand signs"
            )
        plain.append(text[index + 1])
        index += 2
    return "".join(plain)


def compose_plain(base_path, module_path):
    """Compose base prose followed by program-specific prose."""
    base = tex_to_plain(base_path.read_text(encoding="utf-8")).strip()
    module = tex_to_plain(module_path.read_text(encoding="utf-8")).strip()
    return f"{base}\n\n{module}\n"


def render_entry(program):
    base = f"content/base/{program['direction']}"
    module = str(Path(program["program_module"]).with_suffix(""))
    return (
        "\\documentclass{easier_ps}\n"
        f"\\SetStudentName{{{latex_escape('Jianming Xing')}}}\n"
        f"\\SetProgramName{{{latex_escape(program['program'])}}}\n"
        f"\\SetUniversityName{{{latex_escape(program['university'])}}}\n"
        f"\\SetUniversityAbbr{{{latex_escape(program['university_abbr'])}}}\n"
        f"\\SetBaseContentPath{{{base}}}\n"
        f"\\SetUniContentPath{{{module}}}\n"
        "\\begin{document}\n"
        "\\thispagestyle{firstpageheader}\n"
        "\\input{\\GetBaseContentPath}\n"
        "\\par\n"
        "\\input{\\GetUniContentPath}\n"
        "\\end{document}\n"
    )


def generate_program(program):
    """Write one LaTeX entry point and its matching plain Markdown body."""
    statements_dir = ROOT / "statements"
    markdown_dir = ROOT / "output" / "markdown"
    statements_dir.mkdir(parents=True, exist_ok=True)
    markdown_dir.mkdir(parents=True, exist_ok=True)

    entry_path = statements_dir / f"{program['key']}.tex"
    markdown_path = markdown_dir / f"{output_stem(program)}.md"
    base_path = ROOT / "content" / "base" / f"{program['direction']}.tex"
    module_path = ROOT / program["program_module"]

    entry_path.write_text(render_entry(program), encoding="utf-8")
    markdown_path.write_text(
        compose_plain(base_path, module_path), encoding="utf-8"
    )
    return entry_path, markdown_path


def compile_program(program):
    """Compile one generated entry and copy only its final PDF to output."""
    entry_path = ROOT / "statements" / f"{program['key']}.tex"
    build_dir = ROOT / "build" / program["key"]
    pdf_dir = ROOT / "output" / "pdf"
    build_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)

    command = [
        "latexmk",
        "-xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-outdir={build_dir}",
        f"-jobname={output_stem(program)}",
        str(entry_path),
    ]
    subprocess.run(command, cwd=ROOT, check=True)
    destination = pdf_dir / f"{output_stem(program)}.pdf"
    shutil.copy2(
        build_dir / f"{output_stem(program)}.pdf",
        destination,
    )
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", metavar="KEY", help="build only one program key")
    parser.add_argument(
        "--no-pdf", action="store_true", help="generate source files without compiling"
    )
    args = parser.parse_args(argv)

    programs = load_manifest()
    if args.only:
        selected = [program for program in programs if program["key"] == args.only]
        if not selected:
            parser.error(f"unknown program key: {args.only}")
    else:
        selected = programs

    for program in selected:
        generate_program(program)
        if not args.no_pdf:
            compile_program(program)


if __name__ == "__main__":
    main()
