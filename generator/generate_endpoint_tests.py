
from pathlib import Path
import json

from copy import deepcopy

from parser.openapi_parser import load_openapi_spec, extract_operations
from generator.basic_generator import generate_request_data, generate_value
from generator.test_case_generator import generate_string_test_cases

# 1. Locate the project and load the OpenAPI specification
project_root = Path(__file__).resolve().parent.parent

spec_path = (
    project_root
    / "sample_data"
    / "openapi"
    / "demo_api.yaml"
)

spec = load_openapi_spec(spec_path)
operations = extract_operations(spec)

# 2. Store all generated test cases here
all_results = []
total_test_cases = 0


for operation in operations:
    # Generate request-body tests for POST endpoints
    if operation["method"] != "POST":
        continue

    schema = operation["request_schema"]

    if not schema:
        continue

    properties = schema.get("properties", {})
    required_fields = schema.get("required", [])

    base_data = generate_request_data(schema)
    test_cases = []

    # A. Positive request
    test_cases.append({
        "test_type": "positive",
        "field": None,
        "request_body": deepcopy(base_data),
        "expected": "valid"
    })

    for field_name, field_schema in properties.items():
        field_type = field_schema.get("type")

        # B. String length tests
        if field_type == "string":
            if (
                "minLength" in field_schema
                or "maxLength" in field_schema
            ):
                field_cases = generate_string_test_cases(field_schema)

                for case in field_cases:
                    if case["type"] == "positive":
                        continue

                    request_body = deepcopy(base_data)
                    request_body[field_name] = case["value"]

                    test_cases.append({
                        "test_type": case["type"],
                        "field": field_name,
                        "request_body": request_body,
                        "expected": case["expected"]
                    })

        # C. Integer boundary tests
        elif field_type == "integer":
            minimum = field_schema.get("minimum")
            maximum = field_schema.get("maximum")

            if minimum is not None:
                cases = [
                    ("boundary_min", minimum, "valid"),
                    ("negative_below_min", minimum - 1, "invalid")
                ]

                for case_type, value, expected in cases:
                    request_body = deepcopy(base_data)
                    request_body[field_name] = value

                    test_cases.append({
                        "test_type": case_type,
                        "field": field_name,
                        "request_body": request_body,
                        "expected": expected
                    })

            if maximum is not None:
                cases = [
                    ("boundary_max", maximum, "valid"),
                    ("negative_above_max", maximum + 1, "invalid")
                ]

                for case_type, value, expected in cases:
                    request_body = deepcopy(base_data)
                    request_body[field_name] = value

                    test_cases.append({
                        "test_type": case_type,
                        "field": field_name,
                        "request_body": request_body,
                        "expected": expected
                    })
        
        # Generate negative test cases for enum fields
        if "enum" in field_schema:
            allowed_values = field_schema["enum"]

            if allowed_values:
                invalid_value = "__invalid_enum_value__"

                while invalid_value in allowed_values:
                    invalid_value += "_x"

                request_body = deepcopy(base_data)
                request_body[field_name] = invalid_value

                test_cases.append({
                    "test_type": "negative_invalid_enum",
                    "field": field_name,
                    "request_body": request_body,
                    "expected": "invalid"
                })

        # Generate boundary and negative cases for arrays
        if field_type == "array":
            min_items = field_schema.get("minItems")
            max_items = field_schema.get("maxItems")
            items_schema = field_schema.get("items", {})

            if min_items is not None and min_items > 0:
                request_body = deepcopy(base_data)
                request_body[field_name] = [
                    generate_value(items_schema)
                    for _ in range(min_items - 1)
                ]

                test_cases.append({
                    "test_type": "negative_below_min_items",
                    "field": field_name,
                    "request_body": request_body,
                    "expected": "invalid"
                })

            if max_items is not None:
                request_body = deepcopy(base_data)
                request_body[field_name] = [
                    generate_value(items_schema)
                    for _ in range(max_items + 1)
                ]

                test_cases.append({
                    "test_type": "negative_above_max_items",
                    "field": field_name,
                    "request_body": request_body,
                    "expected": "invalid"
                })

        # D. Invalid email test
        if field_schema.get("format") == "email":
            request_body = deepcopy(base_data)
            request_body[field_name] = "not-an-email"

            test_cases.append({
                "test_type": "negative_invalid_email",
                "field": field_name,
                "request_body": request_body,
                "expected": "invalid"
            })

    # E. Missing required-field tests
    for field_name in required_fields:
        request_body = deepcopy(base_data)
        request_body.pop(field_name, None)

        test_cases.append({
            "test_type": "negative_missing_required",
            "field": field_name,
            "request_body": request_body,
            "expected": "invalid"
        })

    # F. Add this endpoint and its cases to the complete results
    all_results.append({
        "endpoint": operation["path"],
        "method": operation["method"],
        "test_case_count": len(test_cases),
        "test_cases": test_cases
    })

    total_test_cases += len(test_cases)


# 3. Create the output folder and save the JSON file
output_dir = project_root / "output"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "generated_test_cases.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(all_results, file, indent=2, ensure_ascii=False)


# 4. Print a short summary
print("\nTest case generation complete!")
print("-" * 35)

for result in all_results:
    print(
        f"{result['method']} {result['endpoint']}: "
        f"{result['test_case_count']} test cases"
    )

print("-" * 35)
print(f"Total test cases: {total_test_cases}")
print(f"Saved to: {output_file}")
