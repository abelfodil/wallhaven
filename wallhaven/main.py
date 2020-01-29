from typing import Union, Dict, List

import requests

from wallhaven.exceptions import ApiKeyError, PageNotFoundError
from wallhaven.params import Parameters


class Wallhaven:
    """
        A Python wrapper around the Wallhaven API.

        Sample usage:
        from wallhaven import Wallhaven

        wallhaven = Wallhaven()
        data = wallhaven.get_wallpaper_info(wallpaper_id)
    """

    BASE_URL = "https://wallhaven.cc/api/v1/"
    WALLPAPER_URL = BASE_URL + "w/"  # + wallpaper ID
    TAG_URL = BASE_URL + "tag/"  # + tag id
    SETTINGS_URL = BASE_URL + "settings"  # ?apikey
    COLLECTIONS_URL = BASE_URL + "collections/"  # apikey or usename
    SEARCH_URL = BASE_URL + "search/"

    def __init__(self, api_key=None):
        self.api_key = api_key

    @staticmethod
    def _request(url: str, **kwargs) -> requests.Response:
        """
            Perform a request at url.

            :param url: Url.
            :param **kwargs: Additional keyword arguments `requests` take.
        """

        # Use session for multiple requests to the same server.
        # It will speed up your requests.
        # Using a context manager will automatically close the session.
        with requests.Session() as session:
            return session.get(url, **kwargs)

    def get_wallpaper_info(self, wallpaper_id: Union[str, int]) -> Dict:
        """
            Return wallpaper metadata from `wallpaper_id`

            :param wallpaper_id: Wallpaper ID in a string format.
        """
        url = self.WALLPAPER_URL + str(wallpaper_id)

        # Request url.
        response = self._request(url, timeout=10)

        # Unauthorized. API key is wrong or inexistent.
        # If user is unauthorized, is either because he tried to access
        # something without an API key, or the API key is not valid.
        if response.status_code == 401:
            if self.api_key is None:
                raise ApiKeyError(
                    "ERROR! -> You need an API key to access NSFW wallpapers."
                )
            raise ApiKeyError("ERROR! -> Invalid API key.")

        # Return data
        return response.json()["data"]

    def get_tag_info(self, tag_id: str) -> Dict:
        """
            Return tag metadata from `tag_id`.

            :param tag_id: Tag id.
        """

        # Only allow strings
        if not isinstance(tag_id, str):
            raise TypeError(f"ERROR! -> Expected type `str`. Found: {type(tag_id)}")

        # Format URL and make a request.
        url = self.TAG_URL + str(tag_id)
        response = self._request(url, timeout=10)

        # Tag ID doesn't exist.
        if response.status_code == 404:
            raise PageNotFoundError("ERROR! -> Tag does not exist.")

        # Return data
        return response.json()["data"]

    def get_user_settings(self) -> Dict:
        """
            Return user settings. A valid API key must be provided.
        """

        # Check if API key exists.
        if self.api_key is None:
            raise ApiKeyError("ERROR! -> Missing API key")

        # Add key to `params`.
        params = {"apikey": self.api_key}

        # Request url.
        response = self._request(self.SETTINGS_URL, params=params, timeout=10)

        # Page is not found if API key is INVALID.
        if response.status_code == 404:
            raise ApiKeyError("ERROR! -> API key is not valid!")

        # Return data if no errors occurred.
        return response.json()["data"]

    def get_collections_from_username(self, username: str) -> List:
        """
            Return user's public collection from `username`.

            :param username: Collection's owner.
        """

        # Format URL and make request.
        url = self.COLLECTIONS_URL + str(username)
        response = self._request(url, timeout=10)

        # Invalid username.
        if response.status_code == 404:
            raise PageNotFoundError("ERROR! -> Invalid username.")

        # Return data if no errors occurred.
        return response.json()["data"]

    def get_collections_from_apikey(self) -> List:
        """
            Return user collection. A valid API key must be provided.
        """

        # Check if API key exists.
        if self.api_key is None:
            raise ApiKeyError("ERROR! -> Missing API key.")

        # Add key to `params`.
        params = {"apikey": self.api_key}
        response = self._request(self.COLLECTIONS_URL, params=params, timeout=10)

        # Unauthorized if API key is not valid.
        if response.status_code == 401:
            raise ApiKeyError("ERROR! -> Invalid API key.")

        # Return data if no errors occurred.
        return response.json()["data"]

    def get_wallpapers_from_user_collection(
        self, username: str, collection_id: Union[int, str], limit: int = 0
    ) -> List:
        """
            Return wallpapers from a user's collection.

            :param username: Collections' Owner.
            :param collection_id: Collection id.
            :param limit. Limit the amount of wallpapers returned.
        """

        if not isinstance(username, str):
            raise TypeError(
                f"ERROR! -> Invalid username. Expected type `str`. Found: {type(username)}"
            )

        if not isinstance(collection_id, int) and not isinstance(collection_id, str):
            raise TypeError(
                f"ERROR! -> Invalid collection id. Expected type `str` or `int`. Found: {type(collection_id)}"
            )

        if not isinstance(limit, int):
            raise TypeError(
                f"ERROR! -> Invalid limit. Expected type `int`. Found: {type(limit)}"
            )

        # Format URL. Default page is 1.
        url = self.COLLECTIONS_URL + username + "/" + str(collection_id)
        response = self._request(url, timeout=10)

        # User not found;
        if response.status_code == 404:
            raise PageNotFoundError("ERROR! -> User not found.")

        # Get list of wallpapers.
        data = response.json()["data"]

        # Data is empty if collection doesn't exist.
        if not data:
            return data

        # Return the amount of wallpapers defined by limit
        # if limit is greater than, or equal to, data.
        if limit and len(data) >= limit:
            return data[0:limit]

        # Get amount of pages and wallpapers.
        meta = response.json()["meta"]

        # Start from page 2
        page = 2

        # Another list to store all wallpapers.
        wallpapers = data.copy()
        while True:
            # Meta has the total amount of pages needed to request all walls.
            # There are 24 wallpapers per page.
            # If page is 3 and `meta["last_page"]` is 2, there are no more pages.
            if page > meta["last_page"]:
                break

            # Request images and get data.
            # We know `data` is never going to be empty
            # because of the page check.
            response = self._request(url, timeout=10, params={"page": page})
            data = response.json()["data"]

            # Loops through data.
            for wall in data:
                if not limit:
                    wallpapers.append(wall)
                elif len(wallpapers) >= limit:
                    break

            # Increment page.
            page += 1

        # Return amount of wallpapers.
        return wallpapers

    def search(self, parameters: Union[Dict[str, str], Parameters]) -> Dict:
        """
            Search wallpapers using the defined parameters.

            :param parameters: Parameters to filter wallpapers.
        """

        # Search only works with a dictionary of parameters.

        # Check if `parameters` is not a dict.
        if not isinstance(parameters, dict) and isinstance(parameters, Parameters):
            # Get a dictionary with parameters.
            # Also possible to use `parameters.params`.
            params = parameters.get_params()
        elif not isinstance(parameters, Parameters):
            raise TypeError(
                f"ERROR! -> Invalid parameters. Expected type `Dict` or `Parameters`. Found: {type(parameters)}"
            )

        # Check if API key exists.
        if self.api_key is not None:
            params["apikey"] = self.api_key

        # Make request.
        response = self._request(self.SEARCH_URL, params=params, timeout=10)

        # Return an empty list if API key is invalid (or missing)
        # and NSFW is set to True.
        return response.json()["data"]
