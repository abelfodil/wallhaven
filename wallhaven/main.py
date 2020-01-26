import json

import requests

from exceptions import *


class Wallhaven:

    BASE_URL = "https://wallhaven.cc/api/v1/"
    WALLPAPER_URL = BASE_URL + "w/"  # Wallpaper ID

    def __init__(self, api_key=None):
        self.api_key = api_key

    @staticmethod
    def _request(url, **kwargs) -> requests.Response:
        return requests.get(url, **kwargs)

    def get_wallpaper_info(self, wallpaper_id: str) -> json:
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

