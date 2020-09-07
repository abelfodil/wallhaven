# An attempt to map all errors that can raised by the Wallhaven API.
HTTP_ERROR_CODES = {
    401: ("Unauthorized", "API key is missing or incorrect."),
    404: (
        "Not Found",
        "The URI requested is invalid or the resource requested, "
        "such as a wallpaper, does not exist.",
    ),
    429: (
        "Too Many Requests",
        "A request could not be served due to the application's "
        "rate limit having been exhausted for the resource.",
    ),
}


class WallhavenException(Exception):
    """Base exception class for wallhaven."""

    pass


class APIException(WallhavenException):
    """Exception due to an error response from Wallhaven API."""

    def __init__(self, status_code: int):
        self.status_code = status_code

    def __str__(self):
        error = HTTP_ERROR_CODES.get(self.status_code)

        # An error we couldn't map.
        if error is None:
            return f"{self.status_code} Something went wrong!"

        return f"{self.status_code} {error[0]}: {error[1]}"
