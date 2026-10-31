from pathlib import Path
import yaml

file_path = (
    Path(__file__).resolve().parent.parent
    / "sample_data"
    / "openapi"
    / "demo_api.yaml"
)

with file_path.open("r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

paths = data.get("paths", {})

for path, methods in paths.items():
    print(f"\nEndpoint: {path}")

    for method, details in methods.items():
        request_body = details.get("requestBody")

        if not request_body:
            continue

        content = request_body.get("content", {})
        json_content = content.get("application/json", {})
        schema = json_content.get("schema", {})
        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])

        print(f"  Method: {method.upper()}")
        print("  Properties:")

        for name, field_details in properties.items():
            field_type = field_details.get("type", "unknown")
            field_format = field_details.get("format", "N/A")
            is_required = name in required_fields

            constraints = {
                key: value
                for key, value in field_details.items()
                if key not in ("type", "format", "description")
            }

            print(f"    Name: {name}")
            print(f"      Type: {field_type}")
            print(f"      Format: {field_format}")
            print(f"      Required: {is_required}")
            print(f"      Constraints: {constraints}")