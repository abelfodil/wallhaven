from typing import List, Dict


def make_query(filters: Dict) -> str:
    """
        Get all filters set by the user and puts them in
        the right order in a string.

        :param filters: A dictionary with filters defined
        in the `Parameters` class.
    """
    query = ""

    # Check tags
    if filters["id"]:  # Search by exact tag.
        query += "id:" + filters["id"]
    else:
        for tag in filters["tags"]["excluded"]:
            query += "-" + tag
        for tag in filters["tags"]["included"]:
            query += "+" + tag

    # Check keyword
    if filters["keyword"]:
        query += filters["keyword"]

    # Check user.
    if filters["username"]:
        query += " @" + filters["username"]

    # Check file type
    if filters["type"]:
        query += " type:" + filters["type"]

    # Check for similar images.
    if filters["like"]:
        query += " like:" + filters["like"]

    return query


def get_str_from_bool(values: List[bool]) -> str:
    """
        Return a string from a list of booleans.
        [True, True, False] -> "110"

        :param values: List of booleans.
    """
    return "".join(str(int(value)) for value in values)
