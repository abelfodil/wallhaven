from collections import namedtuple


Wallpaper = namedtuple(
    "Wallpaper",
    [
        "id",
        "url",
        "short_url",
        "uploader",
        "views",
        "favorites",
        "source",
        "purity",
        "category",
        "dimension_x",
        "dimension_y",
        "resolution",
        "ratio",
        "file_size",
        "file_type",
        "created_at",
        "colors",
        "path",
        "thumbs",
        "tags",
    ],
)

Tag = namedtuple(
    "Tag", ["id", "name", "alias", "category_id", "category", "purity", "created_at"]
)

Uploader = namedtuple("Uploader", ["username", "group", "avatar"])
