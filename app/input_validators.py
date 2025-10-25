from .exceptions import ValidationError


def validate_numbers(a_str: str, b_str: str, max_value: float) -> tuple[float, float]:
    """Validate user inputs, ensuring they are numeric and within allowed magnitude."""
    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError:
        raise ValidationError("Inputs must be numeric")

    for name, v in (("a", a), ("b", b)):
        if abs(v) > max_value:
            raise ValidationError(f"{name} exceeds maximum allowed magnitude {max_value}")

    return a, b
