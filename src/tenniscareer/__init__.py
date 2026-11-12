"""tenniscareer: career matches of tennis players and an age-gap plot."""

from .fetch import PlayerNotFoundError
from .matches import get_player_matches
from .plot import plot_age_gap

__all__ = ["get_player_matches", "plot_age_gap", "PlayerNotFoundError"]
__version__ = "0.1.0"
