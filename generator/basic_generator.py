
import random
import string


def generate_value(field_schema):
    """Generate a value based on a field's schema."""

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
        return []

    elif field_type == "object":
        return {}

    return None


def generate_request_data(schema):
    """Generate a complete request body from schema properties."""

    request_data = {}
    properties = schema.get("properties", {})

    for name, field_schema in properties.items():
        request_data[name] = generate_value(field_schema)

    return request_data
