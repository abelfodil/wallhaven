# Wallhaven
A Python wrapper around the Wallhaven API.

## Installation
You can install it using pip
```
pip install wallhaven
```

## Usage
```python
from wallhaven import Wallhaven

# Instanciate it.
# For some operations, an API key must be provided.
wallhaven = Wallhaven(api_key)

# Get wallpaper metadata
data = wallhaven.get_wallpaper_info(wallpaper_id="r25peq") # Example id

# Get tag metadata
data = wallhaven.get_tag_info(tag_id=tag_id)

# Get user settings.
# An API key must be provided.
data = wallhaven.get_user_settings()

# Get the user's public collection
data = wallhaven.get_collection_from_username(username=username)

# Get the user's public and private collection.
# An API key must be provided.
data = wallhaven.get_collection_from_apikey()

# Get wallpapers from a user's collection.
# By default, this will return ALL wallpapers.
# You can specify a limit.
data = wallhaven.get_wallpapers_from_collection(username, collection_id, limit=25)
```

Example of data returned from `wallhaven.get_wallpaper_info('r25peq')`
```json
{
  "id": "r25peq",
  "url": "https://wallhaven.cc/w/r25peq",
  "short_url": "https://whvn.cc/r25peq",
  "uploader": {
    "username": "NinjaFace",
    "group": "User",
    "avatar": {
      "200px": "https://wallhaven.cc/images/user/avatar/200/56820_48fd0a9fe541.jpg",
      "128px": "https://wallhaven.cc/images/user/avatar/128/56820_48fd0a9fe541.jpg",
      "32px": "https://wallhaven.cc/images/user/avatar/32/56820_48fd0a9fe541.jpg",
      "20px": "https://wallhaven.cc/images/user/avatar/20/56820_48fd0a9fe541.jpg"
    }
  },
  "views": 822,
  "favorites": 14,
  "source": "https://www.deviantart.com/jim373/art/Food-for-the-Soul-808251562",
  "purity": "sfw",
  "category": "general",
  "dimension_x": 3840,
  "dimension_y": 2160,
  "resolution": "3840x2160",
  "ratio": "1.78",
  "file_size": 13313317,
  "file_type": "image/png",
  "created_at": "2020-01-02 21:08:37",
  "colors": [
    "#000000",
    "#424153",
    "#333399",
    "#663399",
    "#660000"
  ],
  "path": "https://w.wallhaven.cc/full/r2/wallhaven-r25peq.png",
  "thumbs": {
    "large": "https://th.wallhaven.cc/lg/r2/r25peq.jpg",
    "original": "https://th.wallhaven.cc/orig/r2/r25peq.jpg",
    "small": "https://th.wallhaven.cc/small/r2/r25peq.jpg"
  },
  "tags": [
    {
      "id": 713,
      "name": "neon",
      "alias": "neon light, neon lights",
      "category_id": 4,
      "category": "Miscellaneous",
      "purity": "sfw",
      "created_at": "2014-03-05 02:13:24"
    },
    {
      "id": 1018,
      "name": "flowers",
      "alias": "flower",
      "category_id": 42,
      "category": "Plants",
      "purity": "sfw",
      "created_at": "2014-03-27 09:42:03"
    },
    {
      "id": 479,
      "name": "digital art",
      "alias": "Cgi, Digital 2D, digital artwork, digital compositions, graphic, graphics, Motion Design",
      "category_id": 25,
      "category": "Digital",
      "purity": "sfw",
      "created_at": "2014-02-17 08:14:11"
    }
  ]
}
```

## Search
You can also search for wallpapers.
```python
from wallhaven import Wallhaven, Parameters

# API key is only needed for NSFW images.
wallhaven = Wallhaven()

# Choose parameters for the wallpapers.
params = Parameters()
params.set_categories(general=True, anime=True, people=False)
params.set_sorting("Toplist")
params.set_range("Last Three Days") # or set_range("3d")

# Search for keywords
params.set_search_query("Music")

# Filter tags
params.include_tags(["guitar"])
params.exclude_tags(["car"])

# Filter by user
params.filter_by_user(username)

# Search for wallpapers using chosen parameters.
data = wallhaven.search(params=params)
```

Each page contains 24 wallpapers.
Search will return a list of dictionaries with the wallpapers' metadata.

**Default parameters:**
- **Categories:** General, Anime, and People.
- **Purity:** SFW
- **Sorting:** Date Added
- **Range**: Last Month  (Ignored if 'Sorting' is not "Toplist")
- **Order**: Descending
- **Page**: 1
  
For more information about the API, visit the [official documentation](https://wallhaven.cc/help/api).

# Methods
### Class `Wallhaven`

- `def __init__(self, api_key=None)`  
- `def _request(self, url, **kwargs) -> requests.Response`  
- `def get_wallpaper_info(self, wallpaper_id: Union[str, int]) -> Dict[str, Union[str, int, Dict[str, str], List[str], List[Dict[str, str]]]]`
- `def get_tag_info(self, tag_id: Union[str, int]) -> Dict[str, str]` 
- `def get_user_settings(self) -> Dict[str, Union[str, List[str]]]`
  - An API key must be provided.  
- `def_get_collection_from_username(self, username: str) -> List[Dict[str, Union[str, int]]]`
- `def get_collection_from_apikey(self) -> List[Dict[str, Union[str, int]]]`
  - An API key must be provided.
- `def search(self, params: Dict[str, str]) -> List[Dict[str, Union[str, List[str], Dict[str, str]]]]`
  - An API key must be provided (Only for NSFW wallpapers).

### Class `Parameters`

- `def __init__(self)`  
- `def reset_parameters(self) -> None`
  * Reset parameters to default.
- `def reset_filters(self) -> None`
  * Reset all filters.
- `def get_params(self) -> Dict[str, str]`
  * Return current parameters.
- `def get_filters(self) -> Dict[str, Union[str, Dict[str, List[str]]]]`
  * Return current filters.
- `def set_categories(self, general: bool = True, anime: bool = True, people: bool = True) -> None`
- `def set_purity(self, sfw: bool = True, sketchy: bool = False, nsfw: bool = False) -> None`
- `def set_sorting(self, sorting: str = "Date Added") -> None`
- `def set_range(self, top_range: str = "Last Month") -> None`
- `def set_sorting_order(self, order: str = "Descending") -> None`
- `def set_page(self, page_number: Union[str, int]) -> None`
- `def set_search_query(self, query: str = "") -> None`
- `def clear_search_query(self, include_filters: bool = False) -> None`
  * Clear only the search query. May also clear filters.
- `def include_tags(self, tags: List[str]) -> None`
- `def exclude_tags(self, tags: List[str]) -> None`
- `def filter_by_user(self, username: str) -> None`
  * Only return wallpapers by this user.
