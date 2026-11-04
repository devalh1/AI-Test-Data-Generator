
import random
import string


def generate_value(field_schema):
    """Generate a value based on an OpenAPI field schema."""

    # Enum takes priority over normal type generation.
    if "enum" in field_schema:
        enum_values = field_schema["enum"]

        if not enum_values:
            raise ValueError("Enum must contain at least one value")

        return random.choice(enum_values)

    field_type = field_schema.get("type", "string")

    if field_type == "string":

        if field_schema.get("format") == "email":
            return "alex@example.com"

        min_length = field_schema.get("minLength", 1)
        max_length = field_schema.get("maxLength", 12)

        if min_length > max_length:
            raise ValueError("minLength cannot exceed maxLength")

        length = min(max(8, min_length), max_length)
        characters = string.ascii_letters + string.digits

        return "".join(random.choices(characters, k=length))

    elif field_type == "integer":

        minimum = field_schema.get("minimum", 0)
        maximum = field_schema.get("maximum", 100)

        if minimum > maximum:
            raise ValueError("minimum cannot exceed maximum")

        return random.randint(minimum, maximum)

    elif field_type == "number":

        minimum = field_schema.get("minimum", 0)
        maximum = field_schema.get("maximum", 100)

        if minimum > maximum:
            raise ValueError("minimum cannot exceed maximum")

        return round(random.uniform(minimum, maximum), 2)

    elif field_type == "boolean":
        return random.choice([True, False])

    elif field_type == "array":

        items_schema = field_schema.get("items", {})

        min_items = field_schema.get("minItems", 1)
        max_items = field_schema.get("maxItems", 3)

        if min_items > max_items:
            raise ValueError("minItems cannot exceed maxItems")

        item_count = random.randint(min_items, max_items)

        return [
            generate_value(items_schema)
            for _ in range(item_count)
        ]

    elif field_type == "object":

        properties = field_schema.get("properties", {})

        return {
            name: generate_value(property_schema)
            for name, property_schema in properties.items()
        }

    return None


def generate_request_data(schema):
    """Generate a complete request body from schema properties."""

    request_data = {}
    properties = schema.get("properties", {})

    for name, field_schema in properties.items():
        request_data[name] = generate_value(field_schema)

    return request_data
