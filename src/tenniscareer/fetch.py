"""Download the raw JS files of a player from tennisabstract.com."""

import requests

BASE_URL = "https://www.tennisabstract.com/jsmatches"
HEADERS = {"User-Agent": "Mozilla/5.0 (tenniscareer; STAT 159 homework)"}
TIMEOUT = 30


class PlayerNotFoundError(ValueError):
    """Raised when tennisabstract.com has no data for the requested player."""


def _download(url):
    """Return the text of a URL, or None if the page does not exist."""
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.text


def download_profile_js(key, name):
    """Download <key>.js: player info (date of birth) and recent matches."""
    text = _download(f"{BASE_URL}/{key}.js")
    if text is None:
        raise PlayerNotFoundError(
            f"No player named {name!r} was found on tennisabstract.com "
            f"(looked for '{key}'). Check the spelling and use the full "
            "name, e.g. 'Serena Williams'."
        )
    return text


def download_career_js(key):
    """Download <key>Career.js (older matches); '' if there is no such file."""
    return _download(f"{BASE_URL}/{key}Career.js") or ""
