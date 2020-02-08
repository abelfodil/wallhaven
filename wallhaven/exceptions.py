class ApiKeyError(Exception):
    """
    An error that occurs when the API key is missing or not valid.
    """


class PageNotFoundError(Exception):
    """
    An error that occurs when the requested page is not found.
    """


class RequestLimitError(Exception):
    """
    An error that occurs when the user reaches the request limit.
    Limit is 45 requests per minute.
    """
