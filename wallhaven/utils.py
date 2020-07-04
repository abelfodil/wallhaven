import requests

from wallhaven.exceptions import WallhavenException


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
