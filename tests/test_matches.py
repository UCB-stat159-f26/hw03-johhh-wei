"""get_player_matches() with the downloads replaced by mock content."""

import pytest

import tenniscareer
from tenniscareer import fetch, matches


class FakeResponse:
    def __init__(self, status_code, text=""):
        self.status_code = status_code
        self.text = text

    def raise_for_status(self):
        pass


def test_get_player_matches_combines_profile_and_career(monkeypatch, female_js):
    profile_js = 'var dob = 19810926;\nvar matchmx = [];\n'
    monkeypatch.setattr(matches, "download_profile_js", lambda key, name: profile_js)
    monkeypatch.setattr(matches, "download_career_js", lambda key: female_js)
    serena = tenniscareer.get_player_matches("serena williams")
    assert len(serena) == 3
    assert serena["opponent"].iloc[0] == "Anne Miller"


def test_unknown_player_gives_meaningful_error(monkeypatch):
    monkeypatch.setattr(fetch.requests, "get", lambda *a, **k: FakeResponse(404))
    with pytest.raises(tenniscareer.PlayerNotFoundError, match="Gaston Sanchez"):
        tenniscareer.get_player_matches("Gaston Sanchez")


def test_missing_career_file_is_not_an_error(monkeypatch):
    monkeypatch.setattr(fetch.requests, "get", lambda *a, **k: FakeResponse(404))
    assert fetch.download_career_js("NewPlayer") == ""
