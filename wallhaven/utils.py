from typing import Dict, Any

import requests

from wallhaven.exceptions import WallhavenException
from wallhaven.routes import ROUTES


def request_url(url: str, **kwargs) -> requests.Response:
    """
    Request `url` and check for HTTP errors using `requests.Response.raise_for_status`.
    """
    response = requests.get(url, **kwargs)

    # check for errors
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise WallhavenException(e)

    # Return response if no errors occurred
    return response


def get_url_for_route(route: str) -> str:
    """
    Return url for `route`.
    """

    # raise an exception if the route doesn't exist.
    try:
        url = ROUTES[route]
    except KeyError:
        raise WallhavenException("Invalid route: " + route)

    return url


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
