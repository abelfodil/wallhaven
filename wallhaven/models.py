from typing import Dict, Any
import json

from wallhaven.utils import dict_to_string


class WallhavenModel:
    """Base class from which all models will inherit."""

    def __init__(self, **kwargs):
        self._default_params = {}

        # This will be populated when `new_from_dict` is called.
        self._json = None

    def __repr__(self):
        """Return a string that can be converted into an instance with `eval`."""
        return "{class_name}({attributes})".format(
            class_name=self.__class__.__name__,
            attributes=dict_to_string(self.as_dict()),
        )

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()

    def __ne__(self, other):
        return not self.__eq__(other)

    def as_dict(self) -> Dict[str, Any]:
        """Return the instance as a dictionary."""
        data: Dict[str, Any] = {}

        for key, value in self._default_params.items():

            # If the value is a list, we check each item in this list
            # for a function called 'as_dict', meaning they are subclasses of
            # WallhavenModel. If the item is not a subclass of WallhavenModel,
            # we append the value directly.
            # E.g. Wallpapers have a list of Tags and a list of Colors.
            # Each tag is a subclass of WallhavenModel, whereas each color is
            # just a string.
            if isinstance(getattr(self, key, None), list):
                data[key] = []
                for subobj in getattr(self, key, None):
                    if getattr(subobj, "as_dict", None):
                        data[key].append(subobj.as_dict())
                    else:
                        data[key].append(subobj)

            # Not a list, but still a subclass of WallhavenModel and we can
            # assign the data[key] directly with key.as_dict().
            # An example being an Uploader object.
            elif getattr(getattr(self, key, None), "as_dict", None):
                data[key] = getattr(self, key).as_dict()

            # If the value doesn't have an `as_dict` method, meaning is not a subclass
            # of WallhavenModel, we can asign the value directly.
            else:
                data[key] = getattr(self, key, None)

        return data

    def as_json(self, **kwargs) -> str:
        """Return the instance as a JSON string.

        Args:
            kwargs: Additional parameters that ``json.dumps`` takes.

        Returns:
            A valid JSON string.
        """
        return json.dumps(self.as_dict(), **kwargs)

    @classmethod
    def new_from_dict(cls, data: Dict[str, Any]) -> "WallhavenModel":
        """Return a new instance based on a JSON dict.

        Parameters:
            data (Dict[str, Any]): A JSON dict.
        """
        # Create new instance
        c = cls(**data)

        # Save original data in a hidden variable just in case.
        c._json = data

        return c


class Wallpaper(WallhavenModel):
    """Model class that represents wallhaven's wallpaper."""

    def __init__(self, **kwargs):
        self._default_params = {
            "id": None,
            "purity": None,
            "url": None,
            "short_url": None,
            "uploader": None,
            "views": None,
            "favorites": None,
            "source": None,
            "purity": None,
            "category": None,
            "dimension_x": None,
            "dimension_y": None,
            "resolution": None,
            "ratio": None,
            "file_size": None,
            "file_type": None,
            "created_at": None,
            "colors": None,
            "path": None,
            "thumbs": None,
            "tags": None,
        }

        for param, default in self._default_params.items():
            setattr(self, param, kwargs.get(param, default))

        if "uploader" in kwargs:
            self.uploader = Uploader.new_from_dict(kwargs["uploader"])

        if "tags" in kwargs:
            self.tags = [Tag.new_from_dict(tag) for tag in kwargs["tags"]]

    def __str__(self):
        return (
            "Wallpaper(id={0.id}, url={0.url}, file_type={0.file_type}, "
            "purity={0.purity}, resolution={0.resolution})".format(self)
        )


class Uploader(WallhavenModel):
    """Model class that represents an uploader."""

    def __init__(self, **kwargs):
        self._default_params = {"username": None, "group": None, "avatar": None}

        for param, default in self._default_params.items():
            setattr(self, param, kwargs.get(param, default))


class Tag(WallhavenModel):
    """Model class that represents a wallpapers' tags."""

    def __init__(self, **kwargs):
        self._default_params = {
            "id": None,
            "name": None,
            "alias": None,
            "category_id": None,
            "category": None,
            "purity": None,
            "created_at": None,
        }

        for param, default in self._default_params.items():
            setattr(self, param, kwargs.get(param, default))


class SearchResults(WallhavenModel):
    """A class that represents the API search results."""

    def __init__(self, **kwargs):
        self._default_params = {"data": None, "meta": None}

        for param, default in self._default_params.items():
            setattr(self, param, kwargs.get(param, default))

        if "data" in kwargs:
            self.data = [Wallpaper.new_from_dict(wall) for wall in kwargs["data"]]

        if "meta" in kwargs:
            self.meta = Meta.new_from_dict(kwargs["meta"])

    def __str__(self):
        return "SearchResults(data={data}, meta={meta})".format(
            data=[str(wall) for wall in self.data], meta=self.meta
        )


class Meta(WallhavenModel):
    """Model class that represents the API search results' meta information."""

    def __init__(self, **kwargs):
        self._default_params = {
            "current_page": None,
            "last_page": None,
            "per_page": None,
            "total": None,
            "query": None,
            "seed": None,
            "url": None,
        }

        for param, default in self._default_params.items():
            setattr(self, param, kwargs.get(param, default))


class Settings(WallhavenModel):
    """Model class that represents an user's settings."""

    def __init__(self, **kwargs):
        self._default_params = {
            "thumb_size": None,
            "per_page": None,
            "purity": None,
            "categories": None,
            "resolutions": None,
            "aspect_ratios": None,
            "toplist_range": None,
            "tag_blacklist": None,
            "user_blacklist": None,
        }

        for param, default in self._default_params.items():
            setattr(self, param, kwargs.get(param, default))


class Collection(WallhavenModel):
    def __init__(self, **kwargs):
        self._default_params = {
            "id": None,
            "label": None,
            "views": None,
            "public": None,
            "count": None,
        }

        for param, default in self._default_params.items():
            setattr(self, param, kwargs.get(param, default))


class CollectionData(WallhavenModel):
    def __init__(self, **kwargs):
        self._default_params = {"data": None, "meta": None}

        for param, default in self._default_params.items():
            setattr(self, param, kwargs.get(param, default))

        if "data" in kwargs:
            self.data = [Wallpaper.new_from_dict(w) for w in kwargs["data"]]

        if "meta" in kwargs:
            self.meta = Meta.new_from_dict(kwargs["meta"])
