from typing import Union, List, Optional, Dict, Any

import requests

from wallhaven.models import (
    Tag,
    Wallpaper,
    Settings,
    Collection,
    CollectionData,
    SearchResults,
)
from wallhaven.exceptions import WallhavenException, APIException


class Api:
    """
    An interface into the Wallhaven API.

    Args:
        api_key (str, optional): A unique identifier to authenticate a wallhaven user.
            You can get one at: https://wallhaven.cc/settings/account
        timeout (int, optional): How long to wait for the server to send data
            before giving up

    Usage:
        import wallhaven

        api = wallhaven.Api(api_key=KEY)

        # Request a wallpaper.
        wallpaper = api.get_wallpaper(id=ID)

        # Search for wallpapers.
        result = api.search()

        for wall in result.data:
            print(wall.id)
    """

    def __init__(
        self, api_key: Optional[str] = None, timeout: Optional[int] = None,
    ):
        self.timeout = timeout
        self.api_key = api_key

        self.base_url = "https://wallhaven.cc/api/v1"

        # API key will be used as an URL parameter if it exists.
        self.params: Dict[str, Any] = {}

        if self.api_key:
            self.params = {"apikey": self.api_key}

        self.session = requests.Session()

    def _call(self, url: str, **kwargs) -> requests.Response:
        """Internal call. Make a GET request to `url`.

        Args:
            url (str): Web location to request.
            kwargs (dict, optional): Optional arguments that `requests` takes.

        Returns:
            :class: requests.Response
        """
        response = self.session.get(url, timeout=self.timeout, **kwargs)
        if not response.ok:
            raise APIException(response.status_code)

        return response

    @staticmethod
    def _parse_response(
        response: requests.Response, **kwargs
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """Try to parse the response as json.

        Args:
            response (requests.Response): Response object to parse.
            kwargs (dict, optional): Optional arguments that `json.loads` takes.

        Raises:
            WallhavenException: When the response body does not contain valid json.

        Returns:
            data (list, dict): A json object or an array of json objects.
        """
        try:
            data = response.json(**kwargs)
        except ValueError as e:
            raise WallhavenException("Error parsing response: {}".format(e))

        # If `meta` is not present, we only care about `data`.
        if "meta" not in data:
            return data["data"]

        # Add final url to metadata. This will probably be needed in the future.
        data["meta"]["url"] = response.url

        # Add params to

        return data

    def get_wallpaper(
        self, id: str, as_json: bool = False
    ) -> Union[Wallpaper, Dict[str, Any]]:
        """Return wallpaper metadata from `id`.

        Args:
            id (str): Wallpaper ID, e.g "13vym3".
            as_json (bool): Whether or not to return data as json.

        Raises:
            APIException: For HTTP errors 401, 404 and 429.

        Returns:
            An instance of `wallhaven.models.Wallpaper` or a json object.
        """
        url = self.base_url + "/w/" + id

        # API key is needed for NSFW wallpapers.
        response = self._call(url, params=self.params)
        json_data = self._parse_response(response)

        return json_data if as_json else Wallpaper.new_from_dict(json_data)

    def get_tag(
        self, id: Union[str, int], as_json: bool = False
    ) -> Union[Tag, Dict[str, Any]]:
        """Return tag metadata from `id`.

        Args:
            id (int, str): Tag ID, e.g 123 or '123'.
            as_json (bool): Whether or not to return data as json.

        Raises:
            APIException: For HTTP errors 401, 404 and 429.

        Returns:
            An instance of `wallhaven.models.Tag` or a json object.
        """
        url = self.base_url + "/tag/" + str(id)

        # API key is not needed even for NSFW tags.
        response = self._call(url)
        json_data = self._parse_response(response)

        return json_data if as_json else Tag.new_from_dict(json_data)

    def get_user_settings(
        self, as_json: bool = False
    ) -> Union[Settings, Dict[str, Any]]:
        """
        Return user settings from `api_key`.

        Args:
            as_json (bool): Whether or not to return data as json.

        Raises:
            WallhavenException: If API key is non-existent.
            APIException: For HTTP errors 401, 404 and 429.

        Returns:
            An instance of `wallhaven.models.Settings` or a json object.
        """
        if not self.api_key:
            raise WallhavenException("You need an API key to continue this operation.")

        url = self.base_url + "/settings"
        response = self._call(url, params=self.params)
        json_data = self._parse_response(response)

        return json_data if as_json else Settings.new_from_dict(json_data)

    def get_collections_from_apikey(
        self, as_json: bool = False
    ) -> Union[List[Collection], Dict[str, Any]]:
        """
        Return all (public and private) collections from an user.

        Args:
            as_json (bool): Whether or not to return data as json.

        Raises:
            WallhavenException: If API key is non-existent.
            APIException: For HTTP errors 401, 404 and 429.

        Returns:
            A list of `wallhaven.models.Collection` instances or a list of json objects.
        """
        if not self.api_key:
            raise WallhavenException("You need an API key to continue this operation.")

        url = self.base_url + "/collections"
        response = self._call(url, params=self.params)
        json_data = self._parse_response(response)

        return (
            json_data if as_json else [Collection.new_from_dict(c) for c in json_data]
        )

    def get_collections_from_username(
        self, username: str, as_json: bool = False
    ) -> Union[List[Collection], Dict[str, Any]]:
        """Return onlu public collections from an user.

        Args:
            username (str): Username from Wallhaven
            as_json (bool): Whether or not to return data as json.

        Raises:
            APIException: For HTTP errors 401, 404 and 429.

        Returns:
            A list of `wallhaven.models.Collection` instances or a list of json objects.
        """
        url = self.base_url + "/collections/" + username

        response = self._call(url)
        json_data = self._parse_response(response)

        return (
            json_data if as_json else [Collection.new_from_dict(c) for c in json_data]
        )

    def get_collection_data(
        self, username: str, collection_id: Union[str, int], as_json: bool = False
    ) -> Union[CollectionData, Dict[str, Any]]:
        """Return collection metadata, i.e wallpapers and metadata for pagination.

        Args:
            username (str): Username from Wallhaven
            collection_id (str, int): The collection id.
            as_json (bool): Whether or not to return data as json.

        Raises:
            APIException: For HTTP errors 401, 404 and 429.

        Returns:
            An instance of `wallhaven.models.CollectionData` or a json object
        """
        url = self.base_url + "/collections/" + username + "/" + str(collection_id)
        response = self._call(url)
        json_data = self._parse_response(response)

        return json_data if as_json else CollectionData.new_from_dict(json_data)

    def search(self, as_json: bool = False) -> Union[SearchResults, Dict[str, Any]]:
        """Search for wallpapers. If an API key is provided, searches will be performed
        with that user's browsing settings and default filters.

        With no additional parameters the search will display the latest SFW wallpapers.
        See: https://wallhaven.cc/help/api for more information on default parameters.

        Args:
            as_json (bool): Whether or not to return data as json.

        Raises:
            APIException: For HTTP errors 401, 404 and 429.

        Returns:
            An instance of `wallhaven.models.SearchResults` or a json dictionary.
        """
        url = self.base_url + "/search"
        response = self._call(url)
        json_data = self._parse_response(response)

        return json_data if as_json else SearchResults.new_from_dict(json_data)
