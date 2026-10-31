
from pathlib import Path
import json

from parser.openapi_parser import load_openapi_spec, extract_operations
from generator.test_case_generator import generate_string_test_cases


project_root = Path(__file__).resolve().parent.parent

file_path = (
    project_root
    / "sample_data"
    / "openapi"
    / "demo_api.yaml"
)

spec = load_openapi_spec(file_path)
operations = extract_operations(spec)

found = False

for operation in operations:
    if operation["method"] != "POST":
        continue

    schema = operation["request_schema"]

    for field_name, field_schema in schema.get("properties", {}).items():
        if field_schema.get("type") != "string":
            continue

        if not (
            "minLength" in field_schema
            or "maxLength" in field_schema
        ):
            continue

        found = True

        print(f"\nEndpoint: {operation['method']} {operation['path']}")
        print(f"Field: {field_name}")
        print(json.dumps(
            generate_string_test_cases(field_schema),
            indent=2
        ))

if not found:
    print("No string fields with length constraints were found.")
