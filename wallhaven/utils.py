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
