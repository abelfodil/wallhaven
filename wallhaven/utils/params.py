from typing import List


def prepare_tags(operation: str, tags: List[str]) -> List[str]:
    """
        Add `operation` to the beginning of each item in `tags`.
    """
    prepared = []
    for tag in tags:
        if tag[0] == operation:
            prepared.append(tag)
        else:
            prepared.append(operation + tag)
    return prepared


def create_search_query(include: List[str], exclude: List[str]) -> str:
    """
        Create search query using the included and excluded tags.
    """

    # Prepare tags. Add signs (+ or -) to them.
    include = prepare_tags("+", include)
    exclude = prepare_tags("-", exclude)

    # Merge tags. Excluded tags must at the beginning.
    tags = exclude + include

    # Sort and reverse list before returning.
    # This ensures the excluded tags will be at the beginning of the list.
    # Returns a string containing all the tags.
    return "".join(sorted(tags, reverse=True))
