import json
from typing import Union, Dict, List

from .utils.params import get_str_from_bool, make_query
from .utils.colors import RED, CLEAR


class Parameters:
    """
    Usage:
    from wallhaven import Wallhaven, Parameters
    walhaven = Wallhaven()

    params = Parameters()
    params.set_categories(general=True, anime=False, people=False)
    params.set_sorting(sorting="toplist")
    params.set_range("Last Three Days")
    data = wallhaven.search(params=params)
    """

    def __init__(self):
        # Reset parameters.
        self.reset_params()

        # Search filters.
        self.filters = {
            "tags": {"included": [], "excluded": []},
            "id": "",
            "like": "",
            "username": "",
            "type": "",
            "keyword": "",
        }

    def __str__(self):
        return json.dumps(self.get_params(), indent=2)

    def reset_params(self) -> None:
        """
            Reset parameters to their default state
        """
        self.params = {
            "categories": "111",
            "purity": "100",
            "sorting": "date_added",
            "order": "desc",
            "topRange": "1M",  # Range is ignored if 'sorting' is not toplist
            "page": "1",
            "q": "",
        }

    def reset_filters(self) -> None:
        """
           Reset all filters chosen by the user
        """
        self.filters.clear()

    def get_params(self) -> Dict[str, str]:
        """
            Return the current parameters.
        """
        return self.params

    def get_filters(self) -> Dict[str, Union[str, Dict[str, List]]]:
        """
           Return the current filters
        """
        return self.filters

    def set_categories(
        self, general: bool = True, anime: bool = True, people: bool = True,
    ) -> None:
        """
            Turn categories on (True, "1", 1) or off (False, "0", 0).
            At least 1 (one) category is needed.

            :param general: Includes general images. Neither anime nor people.
            :param anime: Includes anime related images.
            :param people: Includes images of people.
        """

        # Available categories.
        category_dict = {"general": general, "anime": anime, "people": people}

        # raise TypeError if category is not a boolean, a string, or an integer.
        for name, category in category_dict.items():
            if not isinstance(category, bool):
                raise TypeError(f"{RED}Invalid type for argument '{category}'{CLEAR}")

        # Check if the user chose at least one category.
        if not any(category_dict.values()):
            raise ValueError("At least one (1) category must be included.")

        # Convert category to "1" or "0".
        category_string = get_str_from_bool(category_dict.values())

        # Set category.
        self.params["categories"] = category_string

    def set_purity(
        self, sfw: bool = True, sketchy: bool = False, nsfw: bool = False
    ) -> None:
        """
            Turn purities on (True) or off (False).
            At least 1 (one) purity is needed. NSFW requires a valid API key.

            :param sfw: Includes safe-for-work images.
            :param sketchy: Includes sketchy (not quite sfw not quite nsfw) images.
            :param nsfw: Includes not-safe-for-work (mature) images.
        """

        # Available purity.
        purity_dict = {"sfw": sfw, "sketchy": sketchy, "nsfw": nsfw}

        # raise TypeError if purity is not a boolean, a string, or an integer.
        for name, purity in purity_dict.items():
            if not isinstance(purity, bool):
                raise TypeError(f"{RED}Invalid type for argument '{name}'{CLEAR}")

        # Check if the user chose at least one purity.
        if not any(purity_dict.values()):
            raise ValueError(f"{RED}At least one (1) purity must be included{CLEAR}")

        # Convert purity to "1" and "0".
        purity_string = get_str_from_bool(purity_dict.values())

        # Set purity.
        self.params["purity"] = purity_string

    def set_sorting(self, sorting: str = "Date Added") -> None:
        """
            Set the method of sorting results.

            :param sorting: Sorting method.

            Available methods:
            - Date Added
            - Relevance (related to search query)
            - Random
            - Views
            - Favorites
            - Toplist
        """

        # Check if sorting is not a string.
        if not isinstance(sorting, str):
            raise TypeError(f"{RED}Invalid type for argument 'sorting'{CLEAR}")

        # List of available sortings.
        available_sortings = [
            "date_added",
            "relevance",
            "random",
            "views",
            "favorites",
            "toplist",
        ]

        # Transforms `sorting`.
        # Date Added -> date_added
        sorting = sorting.lower().replace(" ", "_")

        # Check for exact matches.
        if sorting not in available_sortings:
            raise ValueError(f"{RED}{sorting} is not a valid option{CLEAR}")

        # Set sorting
        self.params["sorting"] = sorting

    def set_range(self, top_range: str = "Last Month") -> None:
        """
            Set the time range. Sorting MUST be toplist for this to work.

            :param top_range: Range.

            Available ranges:
            - Last Day (or 1d)
            - Last Three Days (or 3d)
            - Last Week (or 1w)
            - Last Month (or 1m)
            - Last Three Months (3M)
            - Last 6 Months (6M)
            - Last Year (1y)
        """

        if not isinstance(top_range, str):
            raise TypeError(f"{RED}Invalid type for argument 'top_range'{CLEAR}")

        # Map ranges.
        # Values are case-sensitive.
        range_mapping = {
            "last_day": "1d",
            "last_three_days": "3d",
            "last_week": "1w",
            "last_month": "1M",
            "last_three_months": "3M",
            "last_six_weeks": "6M",
            "last_year": "1y",
        }

        # Transforms `top_range` in a string that can match the mapping keys.
        # Last Month -> last_month
        top_range = top_range.lower().replace(" ", "_")

        # Check if `top_range` is either the key or the value.
        # Allows `top_range` to be "Last Month" or "1M".
        for key, value in range_mapping.items():
            if top_range == key:
                top_range = value
                break
            if top_range == value.lower():
                top_range = value
                break
        else:
            raise ValueError(f"{RED}{top_range} is not a valid option{CLEAR}")

        # Set range if range is valid.
        self.params["topRange"] = top_range

    def set_sorting_order(self, order: str = "Descending") -> None:
        """
            Set the sorting order.

            :param order: Sorting order. Can be either Descending or Ascending.
        """

        # Check if order is not a string.
        if not isinstance(order, str):
            raise TypeError(f"{RED}Invalid type for argument 'order'{CLEAR}")

        # Map all possible orders.
        order_mapping = {"descending": "desc", "ascending": "asc"}

        # Transforms `order` in a string that can match the mapping keys or values.
        order = order.lower()

        # Check if `order` is in the mapping.
        for key, value in order_mapping.items():
            if order == value:
                break
            if order == key:
                order = value
                break
        else:
            raise ValueError(f"{RED}{order} is not a valid option for 'order'{CLEAR}")

        # Set the order if nothing went wrong.
        self.params["order"] = order

    def set_page(self, page_number: Union[str, int] = "1") -> None:
        """
            Defines what page number to request.

            :param page_number: Page.
        """

        # Check `page_number` type.
        # 'page_number can only be of type str or int.
        if not isinstance(page_number, str) and not isinstance(page_number, int):
            raise TypeError(f"{RED}Invalid type for argument 'page_number'{CLEAR}")

        # Convert to string in case `page_number` is an integer.
        page = str(page_number)
        if not page.isnumeric():
            raise TypeError(f"{RED}Page needs to be a numeric value{CLEAR}")

        # Set page.
        self.params["page"] = page_number

    def set_search_query(self, query: str = "") -> None:
        """
            Set the search query in the parameters.
            Can also be used to include filters.
            Filter must be separated with spaces.

            :param query: Search query.

            Current filters:
            tagname (normal query) -> Search for a tag/keyword.
            -tagname -> Exclude a tag/keyword.
            +tag1 +tag2 -> Must have tag1 and tag2.
            +tag1 -tag2 -> Must have tag1 and NOT tag2.
            @username -> User uploads
            id:123 -> Exact tag search
            type:{png/jpg} -> Search for file type (jpg = jpeg)
            like:<wallpaper-id> -> Find wallpaper with similar tags.
        """

        if not isinstance(query, str):
            raise TypeError(f"{RED}Invalid type for argument 'query'{CLEAR}")

        # Split words on spaces.
        # Loop through each word and try to check if there a filter involved.
        for word in query.split(" "):
            # @ to only include user uploads
            if word[0] == "@":
                self.filters["username"] = word[1:]

            # Search for a specific tag. Can't be used with other tags.
            elif word[0:2] == "id":
                self.filters["id"] = word[3:]

            # Search for file extension. JPG or PNG
            elif word[0:4] == "type":
                self.filters["type"] = word[5:]

            # Search for similar wallpapers.
            elif word[0:4] == "like":
                self.filters["like"] = word[5:]

            # Include tag
            elif word[0] == "+":
                self.filters["tags"]["included"].append(word.lower()[1:])

            # Exclude tag
            elif word[0] == "-":
                self.filters["tags"]["excluded"].append(word.lower()[1:])

            # Search for a keyword.
            else:
                self.filters["keyword"] += word  # Add keywords to string of keywords

        # Get tags
        # include = self.filters["tags"]["included"]
        # exclude = self.filters["tags"]["excluded"]

        # Set search query
        # self.params["q"] = create_search_query(include, exclude)
        self.params["q"] = make_query(self.filters)

    def clear_search_query(self, clean_filters=False) -> None:
        """
            Clear search query. May also clear filters.
        """

        # Reset search query
        self.params["q"] = ""
        self.filters["keyword"] = ""

        # Reset filters
        if clean_filters:
            self.filters.clear()

    def include_tags(self, tags: List[str]) -> None:
        """
            Include tags. Only show images with matching tags.

            :param tags: An iterable of tags.
        """

        # Check if `tags` is not an iterable (excluding strings).
        if not isinstance(tags, List):
            raise TypeError(f"{RED}Invalid type for argument 'tags'{CLEAR}")

        # Check if `tags` if empty.
        if not tags:
            raise ValueError(f"{RED}Can't find tags in: {tags}{CLEAR}")

        # Add tags to filters.
        for tag in tags:
            if tag.lower() not in self.filters["tags"]["included"]:
                self.filters["tags"]["included"].append(tag.lower())

        # Set tags to search query.
        self.params["q"] = make_query(self.filters)

    def exclude_tags(self, tags: List[str]) -> None:
        """
            Exclude tags. Only show images with no matching tags.

            :param tags: An iterable of tags.
        """

        # Check if `tags` is not an iterable (excluding strings).
        if not isinstance(tags, List):
            raise TypeError("{RED}Invalid type for argument 'tags'{CLEAR}")

        # Check if `tags` is empty.
        if not tags:
            raise ValueError(f"{RED}Can't find tags in: {tags}{CLEAR}")

        # Add tags to filters.
        for tag in tags:
            if tag.lower() not in self.filters["tags"]["excluded"]:
                self.filters["tags"]["excluded"].append(tag.lower())

        # Set tags to search query.
        self.params["q"] = make_query(self.filters)

    def filter_wallpapers_by_user(self, username: str) -> None:
        """
            Only returns images by `username`.

            :param username: Username
        """

        # Check if `username` is not a string.
        if not isinstance(username, str):
            raise TypeError(f"{RED}Invalid type for argument 'username'{CLEAR}")

        # Check if `username` is only white spaces.
        if not username:
            raise ValueError(f"{RED}Username cannot be blank{CLEAR}")

        # Add filter
        self.filters["username"] = username

        # Set filter.
        self.params["q"] = make_query(self.filters)
