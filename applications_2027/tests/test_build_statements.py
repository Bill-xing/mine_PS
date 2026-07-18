import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

from scripts import build_statements as builder
from scripts.build_statements import (
    compose_plain,
    compile_program,
    generate_program,
    latex_escape,
    load_manifest,
    main,
    output_stem,
    render_entry,
    tex_to_plain,
)


class BuilderTests(unittest.TestCase):
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

    def test_output_stem_marks_only_provisional_outputs(self):
        self.assertEqual("cuhk-robotics-provisional", output_stem(self.program))
        ready = dict(self.program, output_status="application_ready")
        self.assertEqual("cuhk-robotics", output_stem(ready))

    def test_latex_escape_protects_every_metadata_metacharacter(self):
        self.assertEqual(
            r"R\&D \% \#1\_lab \$5 \{safe\} x\^{}2",
            latex_escape("R&D % #1_lab $5 {safe} x^2"),
        )

    def test_tex_to_plain_accepts_only_plain_paragraph_escapes(self):
        self.assertEqual(
            "The recorded rate was 93.60% in R&D work.",
            tex_to_plain(r"The recorded rate was 93.60\% in R\&D work."),
        )
        with self.assertRaises(ValueError):
            tex_to_plain(r"\textbf{Unsupported markup}")

    def test_tex_to_plain_rejects_every_other_backslash_escape(self):
        unsupported = (
            r"escaped \# hash",
            r"escaped \_ underscore",
            r"escaped \$ dollar",
            r"escaped \{ brace",
            r"escaped \} brace",
            r"escaped \^{} caret",
            "dangling backslash \\",
        )
        for text in unsupported:
            with self.subTest(text=text), self.assertRaises(ValueError):
                tex_to_plain(text)

    def test_tex_to_plain_rejects_unescaped_latex_special_characters(self):
        unsupported = (
            "96.8%",
            "R&D",
            "item #1",
            "raw_name",
            "$x^2$",
            "{group}",
            "a^2",
            "non~breaking",
        )
        for text in unsupported:
            with self.subTest(text=text), self.assertRaises(ValueError):
                tex_to_plain(text)

    def test_render_entry_selects_exact_base_and_module(self):
        entry = render_entry(self.program)
        self.assertIn(r"\SetBaseContentPath{content/base/robotics_embodied_ai}", entry)
        self.assertIn(r"\SetUniContentPath{content/programs/cuhk/robotics}", entry)
        self.assertIn(r"\SetProgramName{MSc in Robotics}", entry)

    def test_render_entry_separates_base_and_module_with_explicit_paragraph(self):
        entry = render_entry(self.program)
        self.assertIn(
            "\\input{\\GetBaseContentPath}\n"
            "\\par\n"
            "\\input{\\GetUniContentPath}\n",
            entry,
        )

    def test_render_entry_uses_only_declared_compressed_derivative(self):
        derivative = dict(
            self.program,
            compressed_derivative=(
                "content/derivatives/ntu/robotics_intelligent_systems.tex"
            ),
        )
        entry = render_entry(derivative)

        self.assertIn(
            "\\input{content/derivatives/ntu/robotics_intelligent_systems}\n",
            entry,
        )
        self.assertNotIn("content/base/robotics_embodied_ai", entry)
        self.assertNotIn("content/programs/cuhk/robotics", entry)
        self.assertEqual(1, entry.count("\\input{"))

    def test_render_entry_matches_template_and_escapes_metadata(self):
        program = dict(
            self.program,
            program="MSc in AI & Robotics_1",
            university="University #1",
            university_abbr="U$1",
        )
        self.assertEqual(
            "\\documentclass{easier_ps}\n"
            "\\SetStudentName{Jianming Xing}\n"
            "\\SetProgramName{MSc in AI \\& Robotics\\_1}\n"
            "\\SetUniversityName{University \\#1}\n"
            "\\SetUniversityAbbr{U\\$1}\n"
            "\\SetBaseContentPath{content/base/robotics_embodied_ai}\n"
            "\\SetUniContentPath{content/programs/cuhk/robotics}\n"
            "\\begin{document}\n"
            "\\thispagestyle{firstpageheader}\n"
            "\\input{\\GetBaseContentPath}\n"
            "\\par\n"
            "\\input{\\GetUniContentPath}\n"
            "\\end{document}\n",
            render_entry(program),
        )

    def test_compose_plain_preserves_paragraph_order(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = root / "base.tex"
            module = root / "module.tex"
            base.write_text("Base one.\n\nBase two.\n", encoding="utf-8")
            module.write_text("Fit one.\n\nFit two.\n", encoding="utf-8")
            self.assertEqual(
                "Base one.\n\nBase two.\n\nFit one.\n\nFit two.\n",
                compose_plain(base, module),
            )

    def test_compose_plain_converts_only_supported_canonical_escapes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = root / "base.tex"
            module = root / "module.tex"
            base.write_text(r"A 93.60\% result.", encoding="utf-8")
            module.write_text(r"R\&D fit.", encoding="utf-8")
            self.assertEqual(
                "A 93.60% result.\n\nR&D fit.\n",
                compose_plain(base, module),
            )

    def test_load_manifest_returns_program_list(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "config").mkdir()
            (root / "config" / "programs.json").write_text(
                json.dumps({"applicant": {"name": "Ignored"}, "programs": [self.program]}),
                encoding="utf-8",
            )
            with mock.patch.object(builder, "ROOT", root):
                self.assertEqual([self.program], load_manifest())

    def test_generate_program_writes_entry_and_status_aware_markdown(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = root / "content" / "base" / "robotics_embodied_ai.tex"
            module = root / self.program["program_module"]
            base.parent.mkdir(parents=True)
            module.parent.mkdir(parents=True)
            base.write_text("Base paragraph.\n", encoding="utf-8")
            module.write_text("CUHK R\\&D fit.\n", encoding="utf-8")

            with mock.patch.object(builder, "ROOT", root):
                generate_program(self.program)

            self.assertEqual(
                render_entry(self.program),
                (root / "statements" / "cuhk-robotics.tex").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertEqual(
                "Base paragraph.\n\nCUHK R&D fit.\n",
                (
                    root
                    / "output"
                    / "markdown"
                    / "cuhk-robotics-provisional.md"
                ).read_text(encoding="utf-8"),
            )

    def test_generate_program_uses_derivative_for_portal_markdown(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            derivative_program = dict(
                self.program,
                key="ntu-robotics-intelligent-systems",
                school="ntu",
                university="Nanyang Technological University, Singapore",
                university_abbr="NTU",
                program="MSc in Robotics and Intelligent Systems",
                compressed_derivative=(
                    "content/derivatives/ntu/robotics_intelligent_systems.tex"
                ),
            )
            base = root / "content" / "base" / "robotics_embodied_ai.tex"
            module = root / derivative_program["program_module"]
            derivative = root / derivative_program["compressed_derivative"]
            base.parent.mkdir(parents=True)
            module.parent.mkdir(parents=True)
            derivative.parent.mkdir(parents=True)
            base.write_text("Long base paragraph.\n", encoding="utf-8")
            module.write_text("Long NTU module.\n", encoding="utf-8")
            derivative.write_text(
                "NTU portal response one.\n\nNTU portal response two.\n",
                encoding="utf-8",
            )

            with mock.patch.object(builder, "ROOT", root):
                entry_path, markdown_path = generate_program(derivative_program)

            self.assertEqual(
                "NTU portal response one.\n\nNTU portal response two.\n",
                markdown_path.read_text(encoding="utf-8"),
            )
            entry = entry_path.read_text(encoding="utf-8")
            self.assertEqual(1, entry.count("\\input{"))
            self.assertIn(
                r"\input{content/derivatives/ntu/robotics_intelligent_systems}",
                entry,
            )

    def test_generate_program_without_derivative_keeps_base_module_composition(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = root / "content" / "base" / "robotics_embodied_ai.tex"
            module = root / self.program["program_module"]
            base.parent.mkdir(parents=True)
            module.parent.mkdir(parents=True)
            base.write_text("Canonical base.\n", encoding="utf-8")
            module.write_text("Canonical CUHK module.\n", encoding="utf-8")

            with mock.patch.object(builder, "ROOT", root):
                entry_path, markdown_path = generate_program(self.program)

            self.assertEqual(
                "Canonical base.\n\nCanonical CUHK module.\n",
                markdown_path.read_text(encoding="utf-8"),
            )
            self.assertIn(
                "\\input{\\GetBaseContentPath}\n"
                "\\par\n"
                "\\input{\\GetUniContentPath}\n",
                entry_path.read_text(encoding="utf-8"),
            )

    def test_compile_program_uses_exact_latexmk_contract_and_copies_pdf(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            entry_path = root / "statements" / "cuhk-robotics.tex"
            build_dir = root / "build" / "cuhk-robotics"
            built_pdf = build_dir / "cuhk-robotics-provisional.pdf"
            entry_path.parent.mkdir(parents=True)
            build_dir.mkdir(parents=True)
            entry_path.write_text("entry", encoding="utf-8")
            built_pdf.write_bytes(b"compiled pdf")

            with (
                mock.patch.object(builder, "ROOT", root),
                mock.patch.object(builder.subprocess, "run") as run,
            ):
                compile_program(self.program)

            run.assert_called_once_with(
                [
                    "latexmk",
                    "-xelatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    f"-outdir={build_dir}",
                    "-jobname=cuhk-robotics-provisional",
                    str(entry_path),
                ],
                cwd=root,
                check=True,
            )
            self.assertEqual(
                b"compiled pdf",
                (
                    root / "output" / "pdf" / "cuhk-robotics-provisional.pdf"
                ).read_bytes(),
            )

    def test_cli_defaults_to_generating_and_compiling_every_program(self):
        second = dict(
            self.program,
            key="polyu-robotics",
            output_status="application_ready",
        )
        programs = [self.program, second]
        with (
            mock.patch.object(builder, "load_manifest", return_value=programs),
            mock.patch.object(builder, "generate_program") as generate,
            mock.patch.object(builder, "compile_program") as compile_pdf,
        ):
            main([])

        self.assertEqual([mock.call(p) for p in programs], generate.call_args_list)
        self.assertEqual([mock.call(p) for p in programs], compile_pdf.call_args_list)

    def test_cli_only_and_no_pdf_select_one_program_without_compiling(self):
        second = dict(
            self.program,
            key="polyu-robotics",
            output_status="application_ready",
        )
        with (
            mock.patch.object(
                builder, "load_manifest", return_value=[self.program, second]
            ),
            mock.patch.object(builder, "generate_program") as generate,
            mock.patch.object(builder, "compile_program") as compile_pdf,
        ):
            main(["--only", "polyu-robotics", "--no-pdf"])

        generate.assert_called_once_with(second)
        compile_pdf.assert_not_called()

    def test_cli_rejects_an_unknown_only_key(self):
        with mock.patch.object(builder, "load_manifest", return_value=[self.program]):
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main(["--only", "not-a-program"])


if __name__ == "__main__":
    unittest.main()
