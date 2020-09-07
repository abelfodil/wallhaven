from typing import Dict, Any


def dict_to_string(data: Dict[str, Any]) -> str:
    """Convert a dictionary into a string. The string is formatted as key=value."""
    result = ""

    for key, value in data.items():
        # Add quotes if it's a string.
        if isinstance(value, str):
            result += "{key}='{value}', ".format(key=key, value=value)
        else:
            result += "{key}={value}, ".format(key=key, value=value)

    # Return the result without the last space and comma.
    return result[:-2]
