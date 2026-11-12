import pytest

from tenniscareer.names import player_key


@pytest.mark.parametrize("name", ["serena williams", "Serena Williams",
                                  "SerenaWilliams", "  serena   williams "])
def test_player_key_accepts_different_spellings(name):
    assert player_key(name) == "SerenaWilliams"


def test_player_key_drops_hyphens():
    assert player_key("felix auger-aliassime") == "FelixAugerAliassime"


@pytest.mark.parametrize("name", ["", "   ", "123"])
def test_player_key_rejects_names_without_letters(name):
    with pytest.raises(ValueError):
        player_key(name)


def test_player_key_rejects_non_strings():
    with pytest.raises(TypeError):
        player_key(42)
