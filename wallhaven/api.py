from typing import Union

from wallhaven.utils import request_url, get_url_for_route
from wallhaven.models import Tag, Wallpaper, Uploader


def get_wallpaper_info(id: str) -> Wallpaper:
    """
    Return wallpaper information from `id`.
    """

    if not isinstance(id, str):
        raise TypeError("Expected type `str` for `id`. Found {}".format(type(id)))

    # Get the correct url.
    url = get_url_for_route("wallpaper").format(id=id)

    # Request API
    response = request_url(url, timeout=10)

    # Get the raw data
    data = response.json()["data"]

    # Pop tags and uploader from data and instanciate them.
    # This is probably the only place where we'll need to do this
    # instead of using the data directly.
    tags = [Tag(**tag) for tag in data.pop("tags")]
    uploader = Uploader(**data.pop("uploader"))

    # Return all the data as a namedtuple object
    return Wallpaper(**data, tags=tags, uploader=uploader)


def get_tag_info(id: Union[str, int]) -> Tag:
    """
    Return tag information from `id`.
    """

    if not isinstance(id, str) and not isinstance(id, int):
        raise TypeError(
            "Expected type `str` or `int` for id. Found {}".format(type(id))
        )

    # Get the correct url
    url = get_url_for_route("tag").format(id=id)

    # Request the API with a 10s timeout.
    response = request_url(url, timeout=10)

    # Return tag data.
    return Tag(**response.json()["data"])
