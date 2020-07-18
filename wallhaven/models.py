from typing import List, Dict

import attr


@attr.s(frozen=True)
class Tag:
    id: int = attr.ib()
    name: str = attr.ib()
    alias: str = attr.ib()
    category_id: int = attr.ib()
    category: str = attr.ib()
    purity: str = attr.ib()
    created_at: str = attr.ib()

    @classmethod
    def from_data(cls, data) -> "Tag":
        """
        Return an instance of "Tag" from a given data.

        :param data: Tag information in JSON format.
        """
        return cls(**data)


@attr.s(frozen=True)
class Uploader:
    username: str = attr.ib()
    group: str = attr.ib()
    avatar: str = attr.ib()

    @classmethod
    def from_data(cls, data) -> "Uploader":
        """
        Return an instance of `Uploader` from a given data.

        :param data: Uploader data in JSON format.
        """
        return cls(**data)


@attr.s(frozen=True)
class Wallpaper:
    id: str = attr.ib()
    url: str = attr.ib()
    short_url: str = attr.ib()
    uploader: Uploader = attr.ib()
    views: int = attr.ib()
    favorites: int = attr.ib()
    source: str = attr.ib()
    purity: str = attr.ib()
    category: str = attr.ib()
    dimension_x: int = attr.ib()
    dimension_y: int = attr.ib()
    resolution: str = attr.ib()
    ratio: str = attr.ib()
    file_size: int = attr.ib()
    file_type: str = attr.ib()
    created_at: str = attr.ib()
    colors: List[str] = attr.ib()
    path: str = attr.ib()
    thumbs: Dict[str, str] = attr.ib()
    tags: List[Tag] = attr.ib()

    @classmethod
    def from_data(cls, data) -> "Wallpaper":
        """
        Return an instance of `Wallpaper` from a given data.

        :param data: Wallpaper information in JSON format.
        """

        # Get tags
        tags = [Tag.from_data(tag) for tag in data.pop("tags")]

        # Get uploader
        uploader = Uploader.from_data(data.pop("uploader"))

        # Add them back to data.
        data["tags"] = tags
        data["uploader"] = uploader

        # Return an instance of wallpaper
        return cls(**data)

    @classmethod
    def from_collection_data(cls, data) -> "Wallpaper":
        """
        Return an instance of `Wallpaper` from a given collection data.
        The wallpaper information returned by the collection has neither
        tags nor an uploader.

        :param data: Wallpaper information in JSON format.
        """

        # Add tags and uploader to data.
        data["tags"] = None
        data["uploader"] = None

        return cls(**data)


@attr.s(frozen=True)
class Settings:
    thumb_size: str = attr.ib()
    per_page: str = attr.ib()
    purity: List[str] = attr.ib()
    categories: List[str] = attr.ib()
    resolutions: List[str] = attr.ib()
    aspect_ratios: List[str] = attr.ib()
    toplist_range: str = attr.ib()
    tag_blacklist: List[str] = attr.ib()
    user_blacklist: List[str] = attr.ib()

    @classmethod
    def from_data(cls, data) -> "Settings":
        """
        Return an instance of `Settings` from a given data.

        :param data: Settings information in JSON format.
        """
        return cls(**data)


@attr.s(frozen=True)
class Collection:
    id: int = attr.ib()
    label: str = attr.ib()
    views: int = attr.ib()
    public: int = attr.ib()
    count: int = attr.ib()

    @classmethod
    def from_data(cls, data) -> "Collection":
        """
        Return an instance of `Collection` from a given data.

        :param data: Collection information in JSON format.
        """
        return cls(**data)


@attr.s(frozen=True)
class CollectionData:
    data: List[Wallpaper] = attr.ib()
    current_page: int = attr.ib()
    last_page: int = attr.ib()
    per_page: int = attr.ib()
    total: int = attr.ib()
    url: str = attr.ib()

    @classmethod
    def from_data(cls, data) -> "CollectionData":
        """
        Return an instance of `CollectionData` from a given data.

        :param data: Collection data (wallpapers and pagination) in JSON format.
        """
        # Get wallpapers removing 'data' from the dictionary.
        walls = [Wallpaper.from_collection_data(wall) for wall in data.pop("data")]
        meta = data["meta"]
        # I think this is a good way to do this, but mypy disagrees.
        # It still works but this may change this in the future.
        return cls(
            data=walls,
            current_page=meta["current_page"],
            last_page=meta["last_page"],
            per_page=meta["per_page"],
            total=meta["total"],
            url=meta["url"],
        )
