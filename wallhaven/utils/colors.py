CLEAR = "\033[00m"
RED = "\033[091m"


def error(message: str) -> str:
    return RED + str(message) + CLEAR
