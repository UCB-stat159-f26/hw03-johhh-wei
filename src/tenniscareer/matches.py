"""Public function to get the career matches of a player."""

from .clean import clean_matches, extract_dob, extract_matches
from .fetch import download_career_js, download_profile_js
from .names import player_key


def get_player_matches(name):
    """Get the career matches of a player from tennisabstract.com.

    `name` can be written like "serena williams", "Serena Williams" or
    "SerenaWilliams". Returns a data frame with one row per match, ready
    for plot_age_gap(). Raises PlayerNotFoundError for an unknown player.
    """
    key = player_key(name)
    profile_js = download_profile_js(key, name)
    career_js = download_career_js(key)
    records = extract_matches(career_js) + extract_matches(profile_js)
    return clean_matches(records, extract_dob(profile_js))
