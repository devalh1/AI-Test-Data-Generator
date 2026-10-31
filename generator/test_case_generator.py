
def generate_string_test_cases(field_schema):
    """Generate positive, negative, and boundary test cases for strings."""

    min_length = field_schema.get("minLength", 0)
    max_length = field_schema.get("maxLength")

    if max_length is not None and min_length > max_length:
        raise ValueError("minLength cannot exceed maxLength")

    test_cases = []

    # 1. Positive test case
    valid_length = max(min_length, 4)

    if max_length is not None:
        valid_length = min(valid_length, max_length)

    test_cases.append({
        "type": "positive",
        "value": "a" * valid_length,
        "expected": "valid"
    })

    # 2. Minimum-length boundary
    if "minLength" in field_schema:
        test_cases.append({
            "type": "boundary_min",
            "value": "a" * min_length,
            "expected": "valid"
        })

    # 3. Negative case: one character below minimum
    if min_length > 0:
        test_cases.append({
            "type": "negative_too_short",
            "value": "a" * (min_length - 1),
            "expected": "invalid"
        })

    # 4. Maximum-length boundary
    if max_length is not None:
        test_cases.append({
            "type": "boundary_max",
            "value": "a" * max_length,
            "expected": "valid"
        })

        # 5. Negative case: one character above maximum
        test_cases.append({
            "type": "negative_too_long",
            "value": "a" * (max_length + 1),
            "expected": "invalid"
        })

    return test_cases
