from typing import Union, List

from wallhaven.utils import request_url, get_url_for_route
from wallhaven.models import (
    Tag,
    Wallpaper,
    Settings,
    Collection,
    CollectionData,
)


# TODO Logging.
# TODO Maybe stop using `isinstance` to check types and just use try/except.


def get_wallpaper_info(id: str) -> Wallpaper:
    """
    Return wallpaper information.

    :param id: Wallpaper ID, e.g "13vym3".
    :rtype: Returns an instance of `wallhaven.models.Wallpaper`.
    """

    if not isinstance(id, str):
        raise TypeError(f"Expected type `str` for `id`. Got {type(id)}")

    # Get the correct url.
    url = get_url_for_route("wallpaper").format(id=id)

    # Request API
    response = request_url(url, timeout=10)

    # Get the raw data
    data = response.json()["data"]

    # Return an instance of Wallpaper.
    return Wallpaper.from_data(data)


def get_tag_info(id: Union[str, int]) -> Tag:
    """
    Return tag information

    :param id: Tag ID as either an integer or a string.
    :rtype: An instance of `wallhaven.models.Tag`.
    """

    if not isinstance(id, str) and not isinstance(id, int):
        raise TypeError(f"Expected type `str` or `int` for id. Got {type(id)}")

    # Get the correct url
    url = get_url_for_route("tag").format(id=id)

    # Request the API with a 10s timeout.
    response = request_url(url, timeout=10)

    data = response.json()["data"]

    return Tag.from_data(data)


def get_user_settings(api_key: str) -> Settings:
    """
    Return user settings.

    :param api_key: An API key from Wallhaven.
    :rtype: An instance of `wallhaven.models.Settings`.
    """

    # Only allows strings to be used as an API KEY.
    if not isinstance(api_key, str):
        raise TypeError(f"Expected type `str` for api_key. Got {type(api_key)}")

    # Doesn't allow empty strings though.
    if not api_key:
        raise ValueError("You need an API key to request user settings.")

    # Get the url for settings.
    url = get_url_for_route("settings")

    # Make a request passing the URL as a parameter.
    response = request_url(url, timeout=10, params={"apikey": api_key})

    # Get the settings data.
    data = response.json()["data"]

    return Settings.from_data(data)


def get_user_collections_from_apikey(api_key: str) -> List[Collection]:
    """
    Return all (public and private) collections from an user.

    :param api_key: The API key provided by Wallhaven.
    :rtype: A list of `wallhaven.models.Collection`.
    """

    # Get the correct url.
    url = get_url_for_route("collections_apikey")

    # Make a request passing the API key as a parameter.
    response = request_url(url, timeout=10, params={"apikey": api_key})

    # Get the data
    data = response.json()["data"]

    # Return a list with all the collections.
    return [Collection.from_data(collection) for collection in data]


def get_user_collections_from_username(username: str) -> List[Collection]:
    """
    Return only the user's public collections.

    :param username: Wallhaven username.
    :rtype: A list of `wallhaven.models.Collection`.
    """
    if not isinstance(username, str):
        raise TypeError(f"Expected type `str` for username. Got {type(username)}")

    url = get_url_for_route("collections_username").format(username=username)

    response = request_url(url, timeout=10)

    data = response.json()["data"]

    # Return a list with all the user's public collections.
    return [Collection.from_data(collection) for collection in data]


def get_collection_data(
    username: str, collection_id: Union[int, str]
) -> CollectionData:
    """
    Return data from an user's collection. This includes wallpapers and 
    metadata for pagination.

    :param username: Collection's owner username.
    :param collection: Collection id.
    :rtype: An instance of `wallhaven.models.CollectionData`.
    """
    if not isinstance(username, str):
        raise TypeError(f"Expected type `str` for username. Got {type(username)}")

    if not isinstance(collection_id, str) and not isinstance(collection_id, int):
        raise TypeError(
            f"Expected type `str` or `int` for collection_id. Got {type(collection_id)}"
        )

    # Get the correct url
    url = get_url_for_route("collection_wallpapers").format(
        username=username, id=collection_id
    )

    # Make a request
    response = request_url(url, timeout=10)

    # Get data. This time we don't access the 'data' key because
    # we will also need the 'meta' key for pagination information.
    data = response.json()

    # Add missing information to data. The user will be able to use
    # this url for pagination.
    # TODO Maybe create a class that handles pagination?
    data["meta"]["url"] = url

    return CollectionData.from_data(data)
