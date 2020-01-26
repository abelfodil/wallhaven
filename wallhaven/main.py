import json
from typing import Union

import requests

from exceptions import *


class Wallhaven:

    BASE_URL = "https://wallhaven.cc/api/v1/"
    WALLPAPER_URL = BASE_URL + "w/"  # + wallpaper ID
    TAG_URL = BASE_URL + "tag/"  # + tag id
    SETTINGS_URL = BASE_URL + "settings"  # ?apikey
    COLLECTIONS_URL = (
        BASE_URL + "collections/"
    )  # apikey (for self) or usename (for other users)

    def __init__(self, api_key=None):
        self.api_key = api_key

    @staticmethod
    def _request(url, **kwargs) -> requests.Response:
        return requests.get(url, **kwargs)

    def get_wallpaper_info(self, wallpaper_id: Union[str, int]) -> json:
        """ Return wallpaper metadata in JSON format. 
        @param wallpaper_id: Wallpaper ID in a string format. Example: 'r25peq'
        """
        url = self.WALLPAPER_URL + str(wallpaper_id)

        params = {"apikey": self.api_key}
        response = self._request(url, timeout=10, params=params)

        if response.status_code == 401:
            if self.api_key is None:
                raise ApiKeyError("You need an API key to access NSFW wallpapers.")
            else:
                raise ApiKeyError("Invalid API key.")

        if not response.ok:
            raise RequestError("Error requesting server: " + url)

        return response.json()["data"]

    def get_tag_info(self, tag_id: Union[str, int]) -> json:
        """ Return tag metadata in JSON format. 
        @param tag_id: Tag id. 
        """

        url = self.TAG_URL + str(tag_id)
        response = self._request(url, timeout=10)
        if response.status_code == 404:
            raise PageNotFoundError("Tag does not exist.")

        if not response.ok:
            raise RequestError("Error requesting server: " + url)

        return response.json()["data"]

    def get_user_settings(self) -> json:
        """ Return user settings in a JSON format. An API key must be provided."""
        if self.api_key is None:
            raise ApiKeyError("Missing API key")

        params = {"apikey": self.api_key}
        response = self._request(self.SETTINGS_URL, params=params, timeout=10)
        if response.status_code == 404:
            raise RequestError("Invalid API key.")
        if not response.ok:
            raise RequestError("Error requesting user settings.")

        return response.json()["data"]

    def get_collection_from_username(self, username: str) -> json:
        """ Return user's public collection in JSON format. 
        @param username: Collection's owner.
        """

        url = self.COLLECTIONS_URL + str(username)
        response = self._request(url, timeout=10)
        if response.status_code == 404:
            raise PageNotFoundError("User doesn't exist.")
        if not response.ok:
            raise RequestError("Error requesting server: " + url)

        return response.json()["data"]

    def get_collection_from_apikey(self) -> json:
        """ Return user collection in JSON format. 
        An API key must be provided for this to work.
        """

        if self.api_key is None:
            raise ApiKeyError("Missing API key.")

        params = {"apikey": self.api_key}
        response = self._request(self.COLLECTIONS_URL, params=params, timeout=10)
        if response.status_code == 401:
            raise ApiKeyError("Invalid API key.")
        if not response.ok:
            raise RequestError("Error requesting user's collection.")

        return response.json()["data"]

