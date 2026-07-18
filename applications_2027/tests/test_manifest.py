import json
import unittest
from collections import Counter
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
