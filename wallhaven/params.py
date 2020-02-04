from typing import Union, Dict, Iterable

from wallhaven.exceptions import OptionError
from .utils.params import create_search_query


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
        }

    def reset_params(self):
        """
            Reset parameters.
        """
        self.params = {
            "categories": "111",
            "purity": "100",
            "sorting": "date_added",
            "order": "desc",
            "topRange": "1M",  # Only works if 'sorting' is set to 'toplist'
            "page": "1",
            "q": "",
        }

    def get_params(self) -> Union[Dict[str, str], Dict]:
        """ Return the current parameters. """
        return self.params

    def set_categories(
        self,
        general: Union[bool, str, int] = True,
        anime: Union[bool, str, int] = True,
        people: Union[bool, str, int] = True,
    ) -> None:
        """
            Turn categories on (True, "1", 1) or off (False, "0", 0).
            At least 1 (one) category is needed.

            :param general: Includes general images. Neither anime nor people.
            :param anime: Includes anime related images.
            :param people: Includes images of people.
        """

        # Available categories.
        categories = [general, anime, people]

        # raise TypeError if category is not a boolean, a string, or an integer.
        for category in categories:
            if (
                not isinstance(category, bool)
                and not isinstance(category, str)
                and not isinstance(category, int)
            ):
                raise TypeError(
                    f"ERROR! -> Expected `bool`, `str` or `int`. Found: {type(category)}"
                )

        # Check if the user chose at least one category.
        if not any(categories):
            raise OptionError("At least one (1) category must be included.")

        # Convert category to "1" or "0".
        category_string = "".join([str(int(category)) for category in categories])

        # Set category.
        self.params["categories"] = category_string

    def set_purity(
        self,
        sfw: Union[bool, str, int] = True,
        sketchy: Union[bool, str, int] = False,
        nsfw: Union[bool, str, int] = False,
    ) -> None:
        """
            Turn purities on (True, "1", 1) or off (False, "0", 0).
            At least 1 (one) purity is needed. NSFW requires a valid API key.

            :param sfw: Includes safe-for-work images.
            :param sketchy: Includes sketchy (not quite sfw not quite nsfw) images.
            :param nsfw: Includes not-safe-for-work (mature) images.
        """

        # Available purity.
        purity_list = [sfw, sketchy, nsfw]

        # raise TypeError if purity is not a boolean, a string, or an integer.
        for purity in purity_list:
            if (
                not isinstance(purity, bool)
                and not isinstance(purity, str)
                and not isinstance(purity, int)
            ):
                raise TypeError(
                    f"ERROR! -> Expected `bool`, `str` or `int`. Found: {type(purity)}"
                )

        # Check if the user chose at least one purity.
        if not any(purity_list):
            raise OptionError("ERROR! -> At least one (1) purity must be included.")

        # Convert purity to "1" and "0".
        purity_string = "".join([str(int(purity)) for purity in purity_list])

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
            - Toplist Beta
        """

        # Check if sorting is not a string.
        if not isinstance(sorting, str):
            raise TypeError(f"ERROR! -> Expected `str`. Found: {type(sorting)}")

        # List of available sortings.
        available_sortings = [
            "date_added",
            "relevance",
            "random",
            "views",
            "favorites",
            "toplist",
            "toplist_beta",
        ]

        # Transforms `sorting`.
        # Date Added -> date_added
        sorting = sorting.lower().replace(" ", "_")

        # Check for exact matches.
        if sorting not in available_sortings:
            raise OptionError("ERROR! -> Invalid sorting: " + sorting)

        self.params["sorting"] = sorting

    def set_range(self, top_range: str = "Last Month") -> None:
        """
            Set the time range. Sorting MUST be toplist for this to work.

            :param top_range: Range.

            Available ranges:
            - Last Day (or 1d)
            - Last Three Days (or 3d)
            - Last Week (or 1w)
            - Last Month (or 1M)
            - Last Three Months (3M)
            - Last 6 Months (6M)
            - Last Year (1y)
        """

        if not isinstance(top_range, str):
            raise TypeError(f"ERROR! -> Expected `str`. Found: {type(top_range)}")

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
            if top_range == value:
                break
        else:
            raise OptionError(f"ERROR! -> Invalid range: {top_range}")

        self.params["topRange"] = top_range

    def set_sorting_order(self, order: str = "Descending") -> None:
        """
            Set the sorting order.

            :param order: Sorting order. Can be either Descending or Ascending.
        """

        # Check if order is not a string.
        if not isinstance(order, str):
            raise TypeError(f"Expected `str`. Found: {type(order)}")

        # Map all possible orders.
        order_mapping = {"descending": "desc", "ascending": "asc"}

        # Transforms `order` in a string that can match the mapping keys or values.
        order = order.lower().replace(" ", "_")

        # Check if `order` is in the mapping.
        for key, value in order_mapping.items():
            if order == key:
                order = value
                break
            if order == value:
                break

        # Runs if `order` is not in the mapping.
        else:
            raise OptionError(f"ERROR! -> Invalid order: {order}")

        # Set the order if nothing went wrong.
        self.params["order"] = order

    def set_page(self, page_number: Union[str, int] = "1") -> None:
        """
            Defines what page number to request.

            :param page_number: Page.
        """

        # Check `page_number` type.
        # raises TypeError if `page_number` is not a string nor a integer.
        if not isinstance(page_number, str) and not isinstance(page_number, int):
            raise TypeError(
                f"ERROR! -> Expected type `str` or `int`. Found: {type(page_number)}"
            )

        # Convert to string in case `page_number` is an integer.
        page = str(page_number)
        if not page.isnumeric():
            raise TypeError("ERROR! -> Page needs to be a numeric value.")

        # Set page.
        self.params["page"] = page_number

    def set_search_query(self, query: str = "") -> None:
        """
            Set the search query in the parameters.
            Overwrites the last search query (including tags and others filters).

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
            raise TypeError(f"Expected `str`. Found: {type(query)}")

        # Searching for a keyword is the same as searching for a tag.
        # Here we loop through each word and check if the user
        # wants to add or exclude them.
        # If there's a plus sign preceding the word, include it.
        # Else, exclude it.

        # Split words on spaces.
        # Stores them in a dictionary of tags.
        for word in query.split(" "):
            # By default, a word with no signal is the same as
            # including a tag.
            if word[0] not in ["+", "-"]:
                self.filters["tags"]["included"].append(word.lower())
            elif word[0] == "+":
                self.filters["tags"]["included"].append(word.lower())
            else:
                self.filters["tags"]["excluded"].append(word.lower())

        # Get tags
        include = self.filters["tags"]["included"]
        exclude = self.filters["tags"]["excluded"]

        # Set search query
        self.params["q"] = create_search_query(include, exclude)

    def clear_search_query(self) -> None:
        """
            Clear search query, including tags and other filters.
        """

        # Reset search query
        self.params["q"] = ""

        # Reset tags
        self.filters["tags"]["included"].clear()
        self.filters["tags"]["excluded"].clear()

    def include_tags(self, tags: Iterable[str]) -> None:
        """
            Include tags. Only show images with matching tags.

            :param tags: An iterable of tags.
        """

        # Check if `tags` is not an iterable (excluding strings).
        if not isinstance(tags, Iterable) or isinstance(tags, str):
            raise TypeError(f"ERROR! -> Expected `Iterable[str]`. Found: {type(tags)}")

        # Check if `tags` if empty.
        if not tags:
            raise OptionError(f"Can't include tags from: {tags}")

        # Add tags to filters.
        for tag in tags:
            if tag.lower() not in self.filters["tags"]["included"]:
                self.filters["tags"]["included"].append(tag.lower())

        # Get tags
        include = self.filters["tags"]["included"]
        exclude = self.filters["tags"]["excluded"]

        # Set tags to search query.
        self.params["q"] = create_search_query(include, exclude)

    def exclude_tags(self, tags: Iterable[str]) -> None:
        """
            Exclude tags. Only show images with no matching tags.

            :param tags: An iterable of tags.
        """

        # Check if `tags` is not an iterable (excluding strings).
        if not isinstance(tags, Iterable) or isinstance(tags, str):
            raise TypeError(f"ERROR! -> Expected `Iterable[str]`. Found: {type(tags)}")

        # Check if `tags` is empty.
        if not tags:
            raise OptionError(f"Can't exclude tags from: {tags}")

        # Add tags to filters.
        for tag in tags:
            if tag.lower() not in self.filters["tags"]["excluded"]:
                self.filters["tags"]["excluded"].append(tag.lower())

        # Get tags
        include = self.filters["tags"]["included"]
        exclude = self.filters["tags"]["excluded"]

        # Set tags to search query.
        self.params["q"] = create_search_query(include, exclude)

    def filter_wallpapers_by_user(self, username: str) -> None:
        """
            Only returns images by `username`.

            :param username: Username
        """

        # Check if `username` is not a string.
        if not isinstance(username, str):
            raise TypeError(
                f"ERROR! -> Invalid username. Expected `str`. Found: {type(username)}"
            )

        # Check if `username` is only white spaces.
        if not username:
            raise OptionError("ERROR! -> Username cannot be blank.")

        # End with space to allow more filters.
        self.params["q"] += f"@{username} "
