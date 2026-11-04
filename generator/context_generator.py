
import re
import unicodedata
from faker import Faker

fake = Faker("en_IN")


def normalize_text(value):
    """Convert text into lowercase ASCII letters and numbers."""
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", value.lower())


def generate_person_context():
    """Generate related information for one fictional person."""
    first_name = fake.first_name()
    last_name = fake.last_name()

    full_name = f"{first_name} {last_name}"

    first = normalize_text(first_name)
    last = normalize_text(last_name)

    username = f"{first}{last}"
    email = f"{first}.{last}@example.com"

    return {
        "name": full_name,
        "full_name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email
    }


def generate_contextual_request(schema, generate_value):
    """Generate a request body with consistent person-related fields."""
    properties = schema.get("properties", {})
    context = generate_person_context()
    request_data = {}

    for field_name, field_schema in properties.items():
        field_type = field_schema.get("type", "string")

        if field_type == "string" and field_name in context:
            candidate = context[field_name]

            min_length = field_schema.get("minLength", 0)
            max_length = field_schema.get("maxLength")

            valid_length = (
                len(candidate) >= min_length
                and (
                    max_length is None
                    or len(candidate) <= max_length
                )
            )

            allowed_values = field_schema.get("enum")

            valid_enum = (
                allowed_values is None
                or candidate in allowed_values
            )

            if valid_length and valid_enum:
                request_data[field_name] = candidate
                continue

        request_data[field_name] = generate_value(
            field_schema, field_name
        )

    return request_data
