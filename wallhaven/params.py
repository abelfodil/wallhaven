from typing import Union, Dict

from wallhaven.exceptions import *


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
        self.defaultParameters()

    def defaultParameters(self):
        """ Reset parameters. """
        self.params = {
            "categories": "111",
            "purity": "100",
            "sorting": "date_added",
            "order": "desc",
            "topRange": "1M",  # Only works if 'sorting' is set to 'toplist'
            "page": "1",
            "q": "",
        }

    def get_params(self) -> Dict[str, str]:
        """ Return the current parameters. """
        return self.params

    def set_categories(
        self,
        general: Union[bool, str, int] = True,
        anime: Union[bool, str, int] = True,
        people: Union[bool, str, int] = True,
    ) -> None:
        """ Turn categories on(True) or off(False). At least 1 (one) category is needed."""
        categories = [general, anime, people]

        if not any(categories):
            raise InvalidOptionError("At least one (1) category must be included.")

        category_string = "".join([str(int(category)) for category in categories])
        self.params["categories"] = category_string

    def set_purity(
        self,
        sfw: Union[bool, str, int] = True,
        sketchy: Union[bool, str, int] = False,
        nsfw: Union[bool, str, int] = False,
    ) -> None:
        """ Turn purities on(True) or off(False). At least 1 (one) purity is needed. 
        NSFW requires a valid API key."""
        purity_list = [sfw, sketchy, nsfw]

        if not any(purity_list):
            raise InvalidOptionError("At least one (1) purity must be included.")

        purity_string = "".join([str(int(purity)) for purity in purity_list])
        self.params["purity"] = purity_string

    def set_sorting(self, sorting: str = "Date Added") -> None:
        """ Set the method of sorting results. """
        available_sortings = [
            "date_added",
            "relevance",
            "random",
            "views",
            "favorites",
            "toplist",
            "toplist_beta",
        ]
        sorting = sorting.lower().replace(" ", "_")
        if sorting not in available_sortings:
            raise InvalidOptionError("Invalid sorting: " + sorting)

        self.params["sorting"] = sorting

    def set_range(self, top_range: str = "Last Month") -> None:
        """ Set the time range. Sorting MUST be toplist for this to work. """
        range_mapping = {
            "last_day": "1d",
            "last_three_days": "3d",
            "last_week": "1w",
            "last_month": "1M",
            "last_three_months": "3M",
            "last_six_weeks": "6M",
            "last_year": "1y",
        }

        top_range = top_range.lower().replace(" ", "_")
        for key, value in range_mapping.items():
            if top_range in key:
                top_range = value
                break
            elif top_range in value:
                break
            else:
                continue
        else:
            raise InvalidOptionError("Invalid range.")

        self.params["topRange"] = top_range

    def set_sorting_order(self, order: str = "Descending") -> None:
        """ Set the sorting order. """
        order_mapping = {"descending": "desc", "ascending": "asc"}
        order = order.lower().replace(" ", "_")

        for key, value in order_mapping.items():
            if order in key:
                order = value
                break
            elif order in value:
                break
            else:
                continue
        else:
            raise InvalidOptionError("Invalid order.")

        self.params["order"] = order

    def set_page(self, page_number: Union[str, int] = "1") -> None:
        """ Defines what page number to request. """
        page = str(page_number)
        if not page.isnumeric():
            raise InvalidOptionError("Invalid page. Must be a number!")

        self.params["page"] = page_number

    def set_search_query(self, query: str = ""):
        """ Set the search query in the parameters."""
        query = str(query)

        self.params["q"] = query
