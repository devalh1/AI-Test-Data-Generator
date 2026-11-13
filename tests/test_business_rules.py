
import unittest

from generator.business_rule_generator import (
    apply_business_rules,
    generate_business_rule_tests,
    validate_business_rules
)

class TestBusinessRules(unittest.TestCase):

    def setUp(self):
        self.schema = {
            "x-business-rules": [
                {
                    "name": "savings_minimum_balance",
                    "when": {
                        "field": "account_type",
                        "equals": "savings"
                    },
                    "then": {
                        "field": "balance",
                        "minimum": 1000
                    }
                },
                {
                    "name": "current_minimum_balance",
                    "when": {
                        "field": "account_type",
                        "equals": "current"
                    },
                    "then": {
                        "field": "balance",
                        "minimum": 5000
                    }
                }
            ]
        }

    def test_savings_balance_correction(self):
        data = {
            "account_type": "savings",
            "balance": 500
        }

        result = apply_business_rules(self.schema, data)

        self.assertEqual(result["balance"], 1000)

    def test_current_balance_correction(self):
        data = {
            "account_type": "current",
            "balance": 2000
        }

        result = apply_business_rules(self.schema, data)

        self.assertEqual(result["balance"], 5000)

    def test_valid_balance_unchanged(self):
        data = {
            "account_type": "savings",
            "balance": 3000
        }

        result = apply_business_rules(self.schema, data)

        self.assertEqual(result["balance"], 3000)

    def test_original_data_unchanged(self):
        data = {
            "account_type": "current",
            "balance": 1000
        }

        apply_business_rules(self.schema, data)

        self.assertEqual(data["balance"], 1000)


    def test_generated_business_rule_cases(self):
        base_data = {
            "full_name": "Test User",
            "age": 25,
            "email": "test@example.com",
            "account_type": "savings",
            "balance": 1000
        }

        cases = generate_business_rule_tests(
            self.schema,
            base_data
        )

        self.assertEqual(len(cases), 4)

        expected_cases = {
            ("savings", 999, "invalid"),
            ("savings", 1000, "valid"),
            ("current", 4999, "invalid"),
            ("current", 5000, "valid")
        }

        actual_cases = {
            (
                case["request_body"]["account_type"],
                case["request_body"]["balance"],
                case["expected"]
            )
            for case in cases
        }

        self.assertEqual(actual_cases, expected_cases)


    def test_business_rule_validation(self):
        test_cases = [
            ("savings", 0, False),
            ("savings", 999, False),
            ("savings", 1000, True),
            ("current", 0, False),
            ("current", 4999, False),
            ("current", 5000, True),
        ]

        for account_type, balance, expected in test_cases:
            with self.subTest(
                account_type=account_type,
                balance=balance
            ):
                data = {
                    "account_type": account_type,
                    "balance": balance
                }

                result = validate_business_rules(
                    self.schema,
                    data
                )

                self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
