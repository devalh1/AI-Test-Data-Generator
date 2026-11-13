
from copy import deepcopy


def apply_business_rules(schema, request_data):
    corrected_data = deepcopy(request_data)

    rules = schema.get("x-business-rules", [])

    for rule in rules:
        condition = rule["when"]
        requirement = rule["then"]

        condition_field = condition["field"]
        condition_value = condition["equals"]

        target_field = requirement["field"]
        minimum = requirement["minimum"]

        # Apply the rule only when its condition matches
        if corrected_data.get(condition_field) == condition_value:
            current_value = corrected_data.get(target_field)

            if current_value is None or current_value < minimum:
                corrected_data[target_field] = minimum

    return corrected_data

def generate_business_rule_tests(schema, base_data):
    test_cases = []

    rules = schema.get("x-business-rules", [])

    for rule in rules:
        rule_name = rule["name"]

        condition = rule["when"]
        requirement = rule["then"]

        condition_field = condition["field"]
        condition_value = condition["equals"]

        target_field = requirement["field"]
        minimum = requirement["minimum"]


        # Create a valid boundary test
        valid_request = deepcopy(base_data)

        valid_request[condition_field] = condition_value
        valid_request[target_field] = minimum

        test_cases.append({
            "test_type": "boundary_business_rule",
            "rule": rule_name,
            "field": target_field,
            "request_body": valid_request,
            "expected": "valid"
        })

        # Create a request that violates the business rule
        request_body = deepcopy(base_data)

        request_body[condition_field] = condition_value
        request_body[target_field] = minimum - 1

        test_cases.append({
            "test_type": "negative_business_rule",
            "rule": rule_name,
            "field": target_field,
            "request_body": request_body,
            "expected": "invalid"
        })

    return test_cases

def validate_business_rules(schema, request_data):
    rules = schema.get("x-business-rules", [])

    for rule in rules:
        condition = rule["when"]
        requirement = rule["then"]

        condition_field = condition["field"]
        condition_value = condition["equals"]

        target_field = requirement["field"]
        minimum = requirement["minimum"]

        if request_data.get(condition_field) == condition_value:
            actual_value = request_data.get(target_field)

            if actual_value is None:
                return False

            if not isinstance(actual_value, (int, float)):
                return False

            if isinstance(actual_value, bool):
                return False

            if actual_value < minimum:
                return False

    return True


def validate_business_rules(schema, request_data):
    rules = schema.get("x-business-rules", [])

    for rule in rules:
        condition = rule["when"]
        requirement = rule["then"]

        condition_field = condition["field"]
        condition_value = condition["equals"]

        target_field = requirement["field"]
        minimum = requirement["minimum"]

        if request_data.get(condition_field) == condition_value:
            actual_value = request_data.get(target_field)

            if actual_value is None:
                return False

            if isinstance(actual_value, bool) or not isinstance(
                actual_value, (int, float)
            ):
                return False

            if actual_value < minimum:
                return False

    return True
