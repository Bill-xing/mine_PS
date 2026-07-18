import json
import unittest
from collections import Counter
from pathlib import Path

from scripts.build_statements import tex_to_plain


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "config" / "programs.json"
EASIER_PS_PATH = Path(__file__).resolve().parents[1] / "easier_ps.cls"
MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
PROGRAMS = MANIFEST["programs"]

REQUIRED_FIELDS = {
    "key",
    "school",
    "university",
    "university_abbr",
    "program",
    "direction",
    "program_module",
    "academic_year",
    "verification_status",
    "output_status",
    "official_limit",
    "compressed_derivative",
}
ALLOWED_OUTPUT_STATUSES = {"application_ready", "provisional"}
EASIER_PS_INTERFACES = {
    "SetStudentName",
    "SetProgramName",
    "SetUniversityName",
    "SetUniversityAbbr",
    "SetBaseContentPath",
    "SetUniContentPath",
    "firstpageheader",
}


class ManifestTests(unittest.TestCase):
    def test_easier_ps_layout_snapshot_exposes_expected_interfaces(self):
        self.assertTrue(EASIER_PS_PATH.is_file())

        class_text = EASIER_PS_PATH.read_text(encoding="utf-8")
        for interface in EASIER_PS_INTERFACES:
            with self.subTest(interface=interface):
                self.assertIn(interface, class_text)

        self.assertIn(r"\fancyhead[R]{\@UniversityAbbr}", class_text)
        self.assertIn(
            r"\makebox[\textwidth][r]{\@UniversityName}",
            class_text,
        )

    def test_has_expected_applicant_metadata(self):
        self.assertEqual(
            MANIFEST["applicant"],
            {"name": "Jianming Xing", "intake": "Fall 2027"},
        )

    def test_has_exactly_25_unique_program_keys(self):
        keys = [program["key"] for program in PROGRAMS]

        self.assertEqual(len(keys), 25)
        self.assertEqual(len(set(keys)), 25)

    def test_has_expected_direction_counts(self):
        counts = Counter(program["direction"] for program in PROGRAMS)

        self.assertEqual(
            counts,
            Counter(
                {
                    "robotics_embodied_ai": 6,
                    "computer_science_ai": 14,
                    "mechanical_smart_manufacturing": 5,
                }
            ),
        )

    def test_has_expected_school_counts(self):
        counts = Counter(program["school"] for program in PROGRAMS)

        self.assertEqual(
            counts,
            Counter(
                {
                    "cuhk": 5,
                    "hkust": 5,
                    "polyu": 5,
                    "cityu": 4,
                    "nus": 3,
                    "ntu": 3,
                }
            ),
        )

    def test_programs_have_exact_fields_and_allowed_output_statuses(self):
        for program in PROGRAMS:
            with self.subTest(program=program.get("key")):
                self.assertEqual(set(program), REQUIRED_FIELDS)
                self.assertIn(program["output_status"], ALLOWED_OUTPUT_STATUSES)

    def test_output_status_distribution_matches_current_verification(self):
        self.assertEqual(
            Counter(program["output_status"] for program in PROGRAMS),
            Counter({"provisional": 17, "application_ready": 8}),
        )

    def test_ntu_ris_preserves_official_source_conflict_status(self):
        ris = next(
            program
            for program in PROGRAMS
            if program["key"] == "ntu-robotics-intelligent-systems"
        )

        self.assertEqual("January 2027", ris["academic_year"])
        self.assertEqual("official_sources_conflict", ris["verification_status"])
        self.assertEqual("provisional", ris["output_status"])

    def test_only_three_ntu_programs_declare_character_limited_derivatives(self):
        expected = {
            "ntu-robotics-intelligent-systems": (
                "content/derivatives/ntu/robotics_intelligent_systems.tex"
            ),
            "ntu-computer-control-automation": (
                "content/derivatives/ntu/computer_control_automation.tex"
            ),
            "ntu-signal-processing-machine-learning": (
                "content/derivatives/ntu/signal_processing_machine_learning.tex"
            ),
        }
        declared = {
            program["key"]: program["compressed_derivative"]
            for program in PROGRAMS
            if program["compressed_derivative"] is not None
        }

        self.assertEqual(expected, declared)
        for program in PROGRAMS:
            with self.subTest(program=program["key"]):
                derivative = program["compressed_derivative"]
                if program["key"] in expected:
                    self.assertIsInstance(derivative, str)
                    derivative_path = MANIFEST_PATH.parent.parent / derivative
                    self.assertTrue(derivative_path.is_file())
                    self.assertEqual(
                        {
                            "unit": "characters",
                            "max": 2000,
                            "includes_spaces": True,
                        },
                        program["official_limit"],
                    )
                    character_count = len(
                        tex_to_plain(
                            derivative_path.read_text(encoding="utf-8")
                        ).strip()
                    )
                    self.assertGreaterEqual(character_count, 1850)
                    self.assertLessEqual(character_count, 1950)
                else:
                    self.assertIsNone(derivative)


if __name__ == "__main__":
    unittest.main()
