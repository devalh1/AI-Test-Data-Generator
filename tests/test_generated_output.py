
import json
import subprocess
import sys
import unittest
from pathlib import Path

from generator.business_rule_generator import validate_business_rules
from parser.openapi_parser import load_openapi_spec


class TestGeneratedOutput(unittest.TestCase):

    def test_valid_cases_follow_business_rules(self):
        spec = load_openapi_spec(
            "sample_data/openapi/banking_api.yaml"
        )

        schema = spec["paths"]["/accounts"]["post"][
            "requestBody"
        ]["content"]["application/json"]["schema"]


        subprocess.run(
            [
                sys.executable,
                "-m",
                "generator.generate_endpoint_tests",
                "--spec",
                "sample_data/openapi/banking_api.yaml"
            ],
            check=True,
            capture_output=True,
            text=True
        )

        output_file = Path("output/generated_test_cases.json")

        self.assertTrue(
            output_file.exists(),
            "Generated JSON not found. Run the generator first."
        )

        with output_file.open() as f:
            results = json.load(f)

        checked = 0

        for endpoint in results:
            for case in endpoint["test_cases"]:
                if case["expected"] != "valid":
                    continue

                checked += 1

                with self.subTest(
                    test_type=case["test_type"],
                    field=case["field"]
                ):
                    self.assertTrue(
                        validate_business_rules(
                            schema,
                            case["request_body"]
                        ),
                        f"Business rule violated: {case}"
                    )

        self.assertGreater(
            checked,
            0,
            "No valid cases were checked."
        )

    def test_negative_minimum_metadata(self):
        # Regenerate the test cases
        subprocess.run(
            [
                sys.executable,
                "-m",
                "generator.generate_endpoint_tests",
                "--spec",
                "sample_data/openapi/banking_api.yaml"
            ],
            check=True,
            capture_output=True,
            text=True
        )

        # Read the generated output
        output_file = Path("output/generated_test_cases.json")

        with output_file.open() as f:
            results = json.load(f)

        # Collect negative minimum-boundary cases
        cases = {
            case["field"]: case
            for endpoint in results
            for case in endpoint["test_cases"]
            if case["test_type"] == "negative_below_min"
        }

        # Verify both expected cases exist
        self.assertIn("age", cases)
        self.assertIn("balance", cases)

        # Verify failure explanations
        for field in ("age", "balance"):
            with self.subTest(field=field):
                self.assertTrue(cases[field]["failure_reason"])

        # Verify overlapping business-rule violations
        self.assertIs(
            cases["age"]["overlapping_business_rule_violation"],
            False
        )

        self.assertIs(
            cases["balance"]["overlapping_business_rule_violation"],
            True
        )


if __name__ == "__main__":
    unittest.main()
