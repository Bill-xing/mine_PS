import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from scripts.build_statements import compose_plain

from scripts.validate_statements import (
    ValidationIssue,
    canonical_errors,
    contamination_errors,
    limit_errors,
    load_manifest,
    main,
    manifest_errors,
    normalize_text,
    output_path,
    own_school_errors,
    placeholder_errors,
    school_marker_errors,
    validate_program,
    word_count,
)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.program = {
            "key": "cuhk-robotics",
            "school": "cuhk",
            "university": "The Chinese University of Hong Kong",
            "university_abbr": "CUHK",
            "program": "MSc in Robotics",
            "direction": "robotics_embodied_ai",
            "program_module": "content/programs/cuhk/robotics.tex",
            "academic_year": "2026/27",
            "verification_status": "latest_official_prior_cycle",
            "output_status": "provisional",
            "official_limit": None,
            "compressed_derivative": None,
        }

    def write_valid_program(self, root, program=None):
        program = self.program if program is None else program
        base_path = root / "content" / "base" / f"{program['direction']}.tex"
        module_path = root / program["program_module"]
        base_path.parent.mkdir(parents=True, exist_ok=True)
        module_path.parent.mkdir(parents=True, exist_ok=True)
        base_path.write_text(
            "real-robot " + "evidence " * 847,
            encoding="utf-8",
        )
        module_path.write_text("CUHK fit.", encoding="utf-8")
        markdown_path = output_path(program, "markdown", root)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(
            compose_plain(base_path, module_path), encoding="utf-8"
        )
        return base_path, module_path, markdown_path

    def test_word_count_handles_hyphenated_terms_and_percentages(self):
        self.assertEqual(7, word_count("A real-robot policy reduced drops by 27.15%."))

    def test_validator_imports_through_applications_package_from_repo_root(self):
        repo_root = Path(__file__).resolve().parents[2]
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "from applications_2027.scripts.validate_statements import word_count; "
                "assert word_count('one two') == 2",
            ],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_placeholder_scan_rejects_template_language(self):
        errors = placeholder_errors("I am applying to Target University.")
        self.assertTrue(errors)
        self.assertFalse(placeholder_errors("I am applying to CUHK."))

    def test_contamination_scan_rejects_another_school(self):
        errors = contamination_errors(
            "CUHK's program fits me, and HKUST is also excellent.",
            own_school="cuhk",
        )
        self.assertTrue(errors)

    def test_contamination_scan_accepts_only_own_school(self):
        self.assertFalse(
            contamination_errors(
                "CUHK's robotics curriculum connects learning and control.",
                own_school="cuhk",
            )
        )

    def test_contamination_scan_matches_flexible_marker_whitespace(self):
        errors = contamination_errors(
            "Hong Kong   University\nof Science and Technology offers this course.",
            own_school="cuhk",
        )
        self.assertTrue(errors)

    def test_own_school_scan_matches_flexible_marker_whitespace(self):
        module = "Chinese University\n   of Hong Kong is a strong fit."
        self.assertFalse(own_school_errors(module, self.program))

    def test_canonical_scan_matches_builder_plain_prose_rules(self):
        self.assertFalse(canonical_errors(r"A 96.80\% result from R\&D."))
        self.assertTrue(canonical_errors(r"A \textbf{formatted} claim."))
        self.assertTrue(canonical_errors("A raw 96.80% result."))

    def test_placeholder_scan_rejects_every_declared_token_form(self):
        for placeholder in (
            "Student Name Here",
            "Program Name Here",
            "TBD",
            "TODO",
            "FIXME",
            "lorem ipsum",
            "[SCHOOL]",
            "<PROGRAM>",
        ):
            with self.subTest(placeholder=placeholder):
                self.assertTrue(placeholder_errors(f"Apply to {placeholder}."))

    def test_school_marker_scan_uses_token_boundaries(self):
        self.assertFalse(school_marker_errors("A bonus eventually arrived."))
        self.assertTrue(school_marker_errors("NUS offers this curriculum."))

    def test_own_school_scan_accepts_abbreviation_or_full_name(self):
        self.assertFalse(own_school_errors("CUHK is a strong fit.", self.program))
        self.assertFalse(
            own_school_errors(
                "The Chinese University of Hong Kong is a strong fit.", self.program
            )
        )
        self.assertTrue(own_school_errors("This program is a strong fit.", self.program))

    def test_default_and_official_word_limits_are_enforced(self):
        self.assertTrue(limit_errors("word " * 849, None))
        self.assertFalse(limit_errors("word " * 850, None))
        self.assertFalse(limit_errors("word " * 950, None))
        self.assertTrue(limit_errors("word " * 951, None))
        official = {"unit": "words", "max": 2}
        self.assertFalse(limit_errors("one two", official))
        self.assertTrue(limit_errors("one two three", official))

    def test_official_character_limit_respects_space_declaration(self):
        without_spaces = {"unit": "characters", "max": 4, "includes_spaces": False}
        with_spaces = {"unit": "characters", "max": 4, "includes_spaces": True}
        self.assertFalse(limit_errors("ab cd", without_spaces))
        self.assertTrue(limit_errors("ab cd", with_spaces))

    def test_loose_official_word_max_keeps_default_word_range(self):
        official = {"unit": "words", "max": 1000}
        self.assertTrue(limit_errors("", official))
        self.assertFalse(limit_errors("word " * 850, official))
        self.assertFalse(limit_errors("word " * 950, official))
        self.assertTrue(limit_errors("word " * 999, official))

    def test_intersecting_and_compressed_official_word_limits(self):
        intersecting = {"unit": "words", "max": 900}
        self.assertTrue(limit_errors("word " * 849, intersecting))
        self.assertFalse(limit_errors("word " * 850, intersecting))
        self.assertFalse(limit_errors("word " * 900, intersecting))
        self.assertTrue(limit_errors("word " * 901, intersecting))

        compressed = {"unit": "words", "max": 400}
        self.assertTrue(limit_errors("", compressed))
        self.assertFalse(limit_errors("word " * 400, compressed))
        self.assertTrue(limit_errors("word " * 401, compressed))

    def test_official_character_limit_requires_nonempty_body(self):
        official = {"unit": "characters", "max": 5, "includes_spaces": True}
        self.assertTrue(limit_errors("", official))
        self.assertTrue(limit_errors("   ", official))
        self.assertFalse(limit_errors("abcde", official))
        self.assertTrue(limit_errors("abcdef", official))

    def test_output_path_uses_status_aware_stem(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(
                root / "output" / "markdown" / "cuhk-robotics-provisional.md",
                output_path(self.program, "markdown", root),
            )
            ready = dict(self.program, output_status="application_ready")
            self.assertEqual(
                root / "output" / "pdf" / "cuhk-robotics.pdf",
                output_path(ready, "pdf", root),
            )

    def test_pdf_normalization_removes_all_non_alphanumeric_characters(self):
        self.assertEqual("realrobot2715", normalize_text("Real-robot: 27.15%!"))

    def test_pdf_normalization_decomposes_common_latin_ligatures(self):
        ligatures = {
            "\ufb00": "ff",
            "\ufb01": "fi",
            "\ufb02": "fl",
            "\ufb03": "ffi",
            "\ufb04": "ffl",
            "\ufb05": "st",
            "\ufb06": "st",
        }
        for glyph, letters in ligatures.items():
            with self.subTest(glyph=glyph):
                self.assertEqual(letters, normalize_text(glyph))

    def test_manifest_scan_accepts_the_exact_portfolio_distribution(self):
        self.assertFalse(manifest_errors(load_manifest()))

    def test_manifest_scan_rejects_count_and_distribution_drift(self):
        errors = manifest_errors(load_manifest()[:-1])
        checks = {error.check for error in errors}
        self.assertEqual(
            {"manifest_count", "direction_distribution", "school_distribution"},
            checks,
        )

    def test_manifest_scan_rejects_duplicate_keys_even_at_count_25(self):
        programs = load_manifest()
        errors = manifest_errors(programs[:-1] + [programs[0]])
        self.assertIn("unique_keys", {error.check for error in errors})

    def test_program_scan_accepts_valid_sources_and_exact_markdown(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_valid_program(root)
            self.assertFalse(validate_program(self.program, root=root))

    def test_program_scan_reports_each_missing_canonical_source(self):
        with tempfile.TemporaryDirectory() as temp:
            errors = validate_program(self.program, root=Path(temp))
        self.assertEqual(
            {"base_exists", "module_exists"}, {error.check for error in errors}
        )

    def test_program_scan_rejects_noncanonical_latex(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base_path, _, _ = self.write_valid_program(root)
            base_path.write_text(r"A \textbf{formatted} claim.", encoding="utf-8")
            errors = validate_program(self.program, root=root)
        self.assertIn("canonical_prose", {error.check for error in errors})

    def test_program_scan_rejects_placeholders_and_school_names_in_base(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base_path, _, _ = self.write_valid_program(root)
            base_path.write_text(
                "Target University CUHK " + "evidence " * 846,
                encoding="utf-8",
            )
            errors = validate_program(self.program, root=root)
        checks = {error.check for error in errors}
        self.assertIn("placeholders", checks)
        self.assertIn("base_school_markers", checks)

    def test_program_scan_requires_own_school_and_rejects_other_school(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, module_path, _ = self.write_valid_program(root)
            module_path.write_text("HKUST fit.", encoding="utf-8")
            errors = validate_program(self.program, root=root)
        checks = {error.check for error in errors}
        self.assertIn("own_school", checks)
        self.assertIn("cross_school_contamination", checks)

    def test_program_scan_enforces_body_length(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base_path, _, _ = self.write_valid_program(root)
            base_path.write_text("evidence " * 10, encoding="utf-8")
            errors = validate_program(self.program, root=root)
        self.assertIn("word_or_character_limit", {error.check for error in errors})

    def test_program_scan_rejects_nonidentical_markdown(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, _, markdown_path = self.write_valid_program(root)
            markdown_path.write_text("Almost the same body.\n", encoding="utf-8")
            errors = validate_program(self.program, root=root)
        self.assertIn("markdown_parity", {error.check for error in errors})

    def test_program_scan_selects_derivative_for_limit_and_output_parity(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            program = dict(
                self.program,
                key="ntu-robotics-intelligent-systems",
                school="ntu",
                university="Nanyang Technological University, Singapore",
                university_abbr="NTU",
                program="MSc in Robotics and Intelligent Systems",
                compressed_derivative=(
                    "content/derivatives/ntu/robotics_intelligent_systems.tex"
                ),
                official_limit={
                    "unit": "characters",
                    "max": 2000,
                    "includes_spaces": True,
                },
            )
            base_path, module_path, markdown_path = self.write_valid_program(
                root, program
            )
            module_path.write_text("NTU long-form fit.", encoding="utf-8")
            derivative_path = root / program["compressed_derivative"]
            derivative_path.parent.mkdir(parents=True)
            derivative_path.write_text(
                "NTU derivative paragraph one.\n\nNTU derivative paragraph two.\n",
                encoding="utf-8",
            )
            markdown_path.write_text(
                "NTU derivative paragraph one.\n\nNTU derivative paragraph two.\n",
                encoding="utf-8",
            )
            long_form_characters = len(compose_plain(base_path, module_path).strip())

            errors = validate_program(program, root=root)

        self.assertFalse(errors)
        self.assertGreater(
            long_form_characters,
            program["official_limit"]["max"],
        )

    def test_program_scan_requires_declared_derivative_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            program = dict(
                self.program,
                compressed_derivative="content/derivatives/ntu/missing.tex",
                official_limit={
                    "unit": "characters",
                    "max": 2000,
                    "includes_spaces": True,
                },
            )
            self.write_valid_program(root, program)
            errors = validate_program(program, root=root)

        self.assertIn("derivative_exists", {error.check for error in errors})

    def test_program_scan_rejects_noncanonical_derivative(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            program = dict(
                self.program,
                compressed_derivative="content/derivatives/ntu/bad.tex",
                official_limit={
                    "unit": "characters",
                    "max": 2000,
                    "includes_spaces": True,
                },
            )
            _, _, markdown_path = self.write_valid_program(root, program)
            derivative_path = root / program["compressed_derivative"]
            derivative_path.parent.mkdir(parents=True)
            derivative_path.write_text(
                r"CUHK \textbf{formatted} derivative.", encoding="utf-8"
            )
            markdown_path.write_text("unused\n", encoding="utf-8")
            errors = validate_program(program, root=root)

        self.assertIn(
            "derivative_canonical_prose", {error.check for error in errors}
        )

    def test_program_scan_applies_content_checks_to_derivative(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            program = dict(
                self.program,
                compressed_derivative="content/derivatives/ntu/bad_content.tex",
                official_limit={
                    "unit": "characters",
                    "max": 2000,
                    "includes_spaces": True,
                },
            )
            _, _, markdown_path = self.write_valid_program(root, program)
            derivative_path = root / program["compressed_derivative"]
            derivative_path.parent.mkdir(parents=True)
            derivative_path.write_text(
                "Target University and HKUST are alternatives.", encoding="utf-8"
            )
            markdown_path.write_text(
                "Target University and HKUST are alternatives.\n", encoding="utf-8"
            )
            errors = validate_program(program, root=root)

        checks = {error.check for error in errors}
        self.assertIn("derivative_placeholders", checks)
        self.assertIn("derivative_own_school", checks)
        self.assertIn("derivative_cross_school_contamination", checks)

    def test_program_scan_keeps_default_long_form_word_gate_for_derivative(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            program = dict(
                self.program,
                compressed_derivative="content/derivatives/ntu/short.tex",
                official_limit={
                    "unit": "characters",
                    "max": 2000,
                    "includes_spaces": True,
                },
            )
            base_path, _, markdown_path = self.write_valid_program(root, program)
            base_path.write_text("too short", encoding="utf-8")
            derivative_path = root / program["compressed_derivative"]
            derivative_path.parent.mkdir(parents=True)
            derivative_path.write_text("CUHK derivative.", encoding="utf-8")
            markdown_path.write_text("CUHK derivative.\n", encoding="utf-8")
            errors = validate_program(program, root=root)

        self.assertIn("long_form_length", {error.check for error in errors})

    def test_program_scan_requires_status_aware_pdf(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_valid_program(root)
            errors = validate_program(self.program, root=root, require_pdfs=True)
        self.assertIn("pdf_exists", {error.check for error in errors})

    def test_program_scan_accepts_normalized_pdftotext_body(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base_path, module_path, _ = self.write_valid_program(root)
            pdf_path = output_path(self.program, "pdf", root)
            pdf_path.parent.mkdir(parents=True)
            pdf_path.write_bytes(b"pdf")
            body = compose_plain(base_path, module_path)
            extracted = "Personal Statement\n" + body.replace(
                "real-robot", "real-\nrobot"
            )
            completed = mock.Mock(stdout=extracted)
            with mock.patch(
                "scripts.validate_statements.subprocess.run", return_value=completed
            ) as run:
                errors = validate_program(self.program, root=root, require_pdfs=True)

            self.assertFalse(errors)
            run.assert_called_once_with(
                ["pdftotext", str(pdf_path), "-"],
                check=True,
                capture_output=True,
                text=True,
            )

    def test_program_scan_strips_known_two_page_layout_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base_path, module_path, _ = self.write_valid_program(root)
            pdf_path = output_path(self.program, "pdf", root)
            pdf_path.parent.mkdir(parents=True)
            pdf_path.write_bytes(b"pdf")
            body = compose_plain(base_path, module_path)
            split_at = body.index("evidence", len(body) // 2)
            first_page_body = body[:split_at]
            second_page_body = body[split_at:]
            extracted = (
                "Personal Statement\n"
                "Jianming Xing\n\n"
                "The Chinese University of Hong Kong\n"
                "MSc in Robotics\n\n"
                f"{first_page_body}\n"
                "1\n\n\f"
                "Jianming Xing\n\n"
                "CUHK\n\n"
                f"{second_page_body}\n"
                "2\n\f"
            )
            with mock.patch(
                "scripts.validate_statements.subprocess.run",
                return_value=mock.Mock(stdout=extracted),
            ):
                errors = validate_program(self.program, root=root, require_pdfs=True)

        self.assertFalse(errors)

    def test_program_scan_rejects_pdf_without_full_canonical_body(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_valid_program(root)
            pdf_path = output_path(self.program, "pdf", root)
            pdf_path.parent.mkdir(parents=True)
            pdf_path.write_bytes(b"pdf")
            with mock.patch(
                "scripts.validate_statements.subprocess.run",
                return_value=mock.Mock(stdout="CUHK evidence only"),
            ):
                errors = validate_program(self.program, root=root, require_pdfs=True)
        self.assertIn("pdf_text_parity", {error.check for error in errors})

    def test_cli_repeatable_only_keeps_global_checks_and_requested_order(self):
        second = dict(self.program, key="hkust-ai", school="hkust")
        programs = [self.program, second]
        stdout = io.StringIO()
        with (
            mock.patch(
                "scripts.validate_statements.load_manifest", return_value=programs
            ),
            mock.patch(
                "scripts.validate_statements.manifest_errors", return_value=[]
            ) as global_scan,
            mock.patch(
                "scripts.validate_statements.validate_program", return_value=[]
            ) as program_scan,
            redirect_stdout(stdout),
        ):
            status = main(
                [
                    "--only",
                    "hkust-ai",
                    "--only",
                    "cuhk-robotics",
                    "--require-pdfs",
                ]
            )

        self.assertEqual(0, status)
        global_scan.assert_called_once_with(programs)
        self.assertEqual(
            [
                mock.call(second, require_pdfs=True),
                mock.call(self.program, require_pdfs=True),
            ],
            program_scan.call_args_list,
        )
        self.assertEqual(
            "PASS: hkust-ai\nPASS: cuhk-robotics\nPASS: 2 programs\n",
            stdout.getvalue(),
        )

    def test_cli_without_only_validates_every_manifest_program(self):
        second = dict(self.program, key="hkust-ai", school="hkust")
        programs = [self.program, second]
        stdout = io.StringIO()
        with (
            mock.patch(
                "scripts.validate_statements.load_manifest", return_value=programs
            ),
            mock.patch("scripts.validate_statements.manifest_errors", return_value=[]),
            mock.patch(
                "scripts.validate_statements.validate_program", return_value=[]
            ) as program_scan,
            redirect_stdout(stdout),
        ):
            status = main([])

        self.assertEqual(0, status)
        self.assertEqual(
            [
                mock.call(self.program, require_pdfs=False),
                mock.call(second, require_pdfs=False),
            ],
            program_scan.call_args_list,
        )
        self.assertTrue(stdout.getvalue().endswith("PASS: 2 programs\n"))

    def test_cli_prints_key_and_check_to_stderr_and_returns_one(self):
        error = ValidationIssue(
            "cuhk-robotics", "markdown_parity", "generated body differs"
        )
        stderr = io.StringIO()
        with (
            mock.patch(
                "scripts.validate_statements.load_manifest",
                return_value=[self.program],
            ),
            mock.patch("scripts.validate_statements.manifest_errors", return_value=[]),
            mock.patch(
                "scripts.validate_statements.validate_program", return_value=[error]
            ),
            redirect_stderr(stderr),
        ):
            status = main(["--only", "cuhk-robotics"])

        self.assertEqual(1, status)
        self.assertIn("[cuhk-robotics] markdown_parity", stderr.getvalue())
        self.assertTrue(stderr.getvalue().endswith("FAIL: 1 error, 1 program\n"))

    def test_cli_rejects_unknown_only_key_with_exit_one(self):
        stderr = io.StringIO()
        with (
            mock.patch(
                "scripts.validate_statements.load_manifest",
                return_value=[self.program],
            ),
            mock.patch("scripts.validate_statements.manifest_errors", return_value=[]),
            mock.patch("scripts.validate_statements.validate_program") as program_scan,
            redirect_stderr(stderr),
        ):
            status = main(["--only", "missing-program"])

        self.assertEqual(1, status)
        program_scan.assert_not_called()
        self.assertIn("[missing-program] selection", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
