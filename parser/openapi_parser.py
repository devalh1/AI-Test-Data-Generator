
from pathlib import Path
import yaml


def load_openapi_spec(file_path):
    """Load an OpenAPI YAML file into Python data."""
    file_path = Path(file_path)

    with file_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def extract_operations(spec):
    """Extract endpoint paths, methods, and request schemas."""
    operations = []
    paths = spec.get("paths", {})

    http_methods = {
        "get", "post", "put", "patch",
        "delete", "options", "head", "trace"
    }

    for path, methods in paths.items():
        for method, details in methods.items():

            if method.lower() not in http_methods:
                continue

            request_body = details.get("requestBody", {})
            content = request_body.get("content", {})
            json_content = content.get("application/json", {})
            schema = json_content.get("schema", {})

            operations.append({
                "path": path,
                "method": method.upper(),
                "summary": details.get("summary", ""),
                "request_schema": schema
            })

    return operations


if __name__ == "__main__":
    sample_file = (
        Path(__file__).resolve().parent.parent
        / "sample_data"
        / "openapi"
        / "demo_api.yaml"
    )

    spec = load_openapi_spec(sample_file)
    operations = extract_operations(spec)

    for operation in operations:
        print(f"\n{operation['method']} {operation['path']}")
        print(f"Summary: {operation['summary']}")
        print(f"Schema: {operation['request_schema']}")
