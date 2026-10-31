
from pathlib import Path
import json

from parser.openapi_parser import load_openapi_spec, extract_operations
from generator.basic_generator import generate_request_data


project_root = Path(__file__).resolve().parent.parent

file_path = (
    project_root
    / "sample_data"
    / "openapi"
    / "demo_api.yaml"
)

spec = load_openapi_spec(file_path)
operations = extract_operations(spec)

for operation in operations:
    if operation["method"] == "POST" and operation["request_schema"]:
        request_data = generate_request_data(
            operation["request_schema"]
        )

        print(f"Endpoint: {operation['method']} {operation['path']}")
        print("Generated request body:")
        print(json.dumps(request_data, indent=2))
        break
else:
    print("No POST operation with a request schema was found.")
