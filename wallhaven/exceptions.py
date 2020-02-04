class ApiKeyError(Exception):
    """
        An error that occurs when the API key is missing or not valid.
    """

    pass


class PageNotFoundError(Exception):
    """
        An error that occurs when the requested page is not found.
    """

    pass
