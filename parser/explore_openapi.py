from pathlib import Path
import yaml

# Locate the YAML file
file_path = (
    Path(__file__).resolve().parent.parent
    / "sample_data"
    / "openapi"
    / "demo_api.yaml"
)

# Load the YAML file
with file_path.open("r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

# Print endpoint paths and their HTTP methods
for path in data["paths"]:
    print(path)

    for method in data["paths"][path]:
        print(" ", method)