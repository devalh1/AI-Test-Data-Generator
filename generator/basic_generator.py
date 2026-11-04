
import random
import string
from faker import Faker
from generator.context_generator import generate_contextual_request

fake = Faker("en_IN")


def generate_realistic_string(field_name, field_schema):
    """Generate realistic data based on a field's name."""

    field_name = field_name.lower()

    generators = {
        "name": fake.name,
        "full_name": fake.name,
        "first_name": fake.first_name,
        "last_name": fake.last_name,
        "username": fake.user_name,
        "city": fake.city,
        "email": fake.email,
        "phone": fake.msisdn,
        "phone_number": fake.msisdn,
        "company": fake.company,
        "address": fake.street_address,
        "product_name": lambda: random.choice([
            "Wireless Mouse",
            "Mechanical Keyboard",
            "USB-C Hub",
            "Laptop Stand",
            "Bluetooth Speaker"
        ])
    }

    generator = generators.get(field_name)

    if generator is None:
        return None

    min_length = field_schema.get("minLength", 0)
    max_length = field_schema.get("maxLength")

    # Try generating a value that respects schema constraints.
    for _ in range(30):
        value = generator()

        if len(value) < min_length:
            continue

        if max_length is not None and len(value) > max_length:
            continue

        return value

    # If realistic data cannot satisfy constraints,
    # fall back to generic generation.
    return None


def generate_value(field_schema, field_name=""):
    """Generate data using field meaning and schema constraints."""

    if "enum" in field_schema:
        values = field_schema["enum"]

        if not values:
            raise ValueError("Enum must contain at least one value")

        return random.choice(values)

    field_type = field_schema.get("type", "string")

    if field_type == "string":
        realistic = generate_realistic_string(
            field_name, field_schema
        )

        if realistic is not None:
            return realistic

        if field_schema.get("format") == "email":
            for _ in range(30):
                email = fake.email()
                if (
                    len(email) >= field_schema.get("minLength", 0)
                    and len(email) <= field_schema.get("maxLength", float("inf"))
                ):
                    return email

            raise ValueError(
                f"Cannot generate email for {field_name} "
                "within the specified length constraints"
            )

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
            generate_value(items_schema, field_name)
            for _ in range(item_count)
        ]

    elif field_type == "object":
        properties = field_schema.get("properties", {})

        return {
            name: generate_value(schema, name)
            for name, schema in properties.items()
        }

    return None


def generate_request_data(schema):
    """Generate a request body with consistent related fields."""
    return generate_contextual_request(schema, generate_value)