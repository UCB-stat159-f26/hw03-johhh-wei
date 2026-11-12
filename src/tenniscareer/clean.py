"""Turn the raw JS files from tennisabstract.com into a clean data frame.

Nothing in this module touches the network, so it can be tested offline.
"""

import json
import re

import pandas as pd

# position of the fields we keep in each match record
FIELDS = {"date": 0, "tournament": 1, "surface": 2, "outcome": 4,
          "round": 8, "score": 9, "opponent": 11, "opponent_info": 16}
RESULTS = {"W": "Win", "L": "Loss"}
DAYS_PER_YEAR = 365.25
COLUMNS = ["date", "tournament", "surface", "round", "score", "opponent",
           "result", "player_age", "opponent_age", "age_diff"]


def extract_dob(js_text):
    """Find the player's date of birth (`var dob = 19810926;`)."""
    found = re.search(r"var\s+dob\s*=\s*['\"]?(\d{8})", js_text)
    if found is None:
        raise ValueError("could not find the player's date of birth")
    return pd.to_datetime(found.group(1), format="%Y%m%d")


def extract_matches(js_text):
    """Return the match records stored in a JS file as a list of lists.

    Reads both `var matchmx = [...]` and `var morematchmx = [...]`.
    """
    arrays = re.findall(r"var\s+(?:more)?matchmx\s*=\s*(\[\s*\[.*?\]\s*\])",
                        js_text, flags=re.DOTALL)
    return [record for array in arrays for record in json.loads(array)]


def _years_between(start, end):
    """Number of years (possibly fractional) from start to end."""
    return (end - start).dt.days / DAYS_PER_YEAR


def _opponent_age(info, match_date):
    """Age of the opponent on the day of the match.

    Files of female players store the opponent's date of birth (YYYYMMDD);
    files of male players already store the opponent's age.
    """
    is_dob = info.str.fullmatch(r"\d{8}")
    birth = pd.to_datetime(info.where(is_dob), format="%Y%m%d", errors="coerce")
    age = pd.to_numeric(info.where(~is_dob), errors="coerce")
    return age.fillna(_years_between(birth, match_date))


def _was_played(matches):
    """True for matches with a result and at least one game in the score.

    Walkovers ("W/O") and defaults ("DEF") were never played, so they are
    dropped; retirements ("RET") are kept.
    """
    has_result = matches["outcome"].isin(list(RESULTS))
    has_games = matches["score"].str.contains(r"\d", na=False)
    return has_result & has_games


def _raw_table(records):
    """Keep only the fields we need from the match records."""
    rows = [[record[i] for i in FIELDS.values()] for record in records]
    return pd.DataFrame(rows, columns=list(FIELDS), dtype="string")


def clean_matches(records, dob):
    """Build the clean data frame from match records and the player's dob.

    One row per match that was played, sorted by date, with the player's
    age, the opponent's age and their difference (player minus opponent).
    """
    matches = _raw_table(records)
    matches = matches[_was_played(matches)].copy()
    matches["date"] = pd.to_datetime(matches["date"], format="%Y%m%d")
    matches["result"] = matches["outcome"].map(RESULTS)
    matches["player_age"] = _years_between(pd.Timestamp(dob), matches["date"])
    matches["opponent_age"] = _opponent_age(matches["opponent_info"], matches["date"])
    matches["age_diff"] = matches["player_age"] - matches["opponent_age"]
    matches = matches.drop_duplicates(["date", "round", "opponent"])
    return matches.sort_values("date", kind="stable")[COLUMNS].reset_index(drop=True)
