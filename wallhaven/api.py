from wallhaven.utils import request_url


def get_wallpaper_info(id: str) -> dict:
    """
    Return wallpaper information from `id`.
    """

    if not isinstance(id, str):
        raise TypeError("Expected type `str` for `id`. Found {}".format(type(id)))

    # Get the correct url.
    url = "https://wallhaven.cc/api/v1/w/{id}".format(id=id)

    # Request API
    response = request_url(url, timeout=10)

    # Return data
    return response.json()["data"]
