from pathlib import Path
from parser.openapi_parser import load_openapi_spec, extract_operations

# Locate the sample OpenAPI file
file_path = Path("sample_data/openapi/demo_api.yaml")

# Load the specification
spec = load_openapi_spec(file_path)

# Extract the API operations
operations = extract_operations(spec)

# Display the results
print("Total API operations:", len(operations))

for operation in operations:
    print(f"{operation['method']} {operation['path']}")