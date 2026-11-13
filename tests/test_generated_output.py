
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


if __name__ == "__main__":
    unittest.main()
