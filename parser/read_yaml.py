from pathlib import Path
import yaml

# Locate the YAML file
file_path = (
    Path(__file__).resolve().parent.parent
    / "sample_data"
    / "openapi"
    / "product.yaml"
)

# Read the file
with file_path.open("r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

print(type(data["product"]))
print(data["product"]["name"])
for color in data["product"]["colors"]:
    print(color)
print(len(data["product"]["colors"]))
print(type(data["product"]["price"]))

print(type(data["product"]["available"]))

print(type(data["product"]["colors"]))