"""Turn a player's name into the key used in tennisabstract.com URLs."""

import re


def _capitalize_first(word):
    """Upper-case the first letter and leave the rest untouched."""
    return word[:1].upper() + word[1:]


def player_key(name):
    """Convert a player's name into a tennisabstract key.

    "serena williams", "Serena Williams" and "SerenaWilliams" all give
    "SerenaWilliams".
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string, e.g. 'Serena Williams'")
    words = re.findall(r"[A-Za-z]+", name)
    if not words:
        raise ValueError(f"{name!r} is not a valid player name")
    return "".join(_capitalize_first(word) for word in words)
