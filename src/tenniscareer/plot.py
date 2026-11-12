"""Scatter plot of a player's age against the age gap to each opponent."""

import matplotlib.pyplot as plt

COLORS = {"Win": "#4a90c2", "Loss": "#e8743b"}
REQUIRED = ["player_age", "age_diff", "result"]


def _check_columns(matches):
    """Fail early if the data frame is not the one we expect."""
    missing = [column for column in REQUIRED if column not in matches]
    if missing:
        raise ValueError(f"matches is missing the column(s): {missing}; "
                         "use the data frame from get_player_matches()")


def _style_axes(ax, title):
    """Labels, reference line and a light NYT-like look."""
    ax.axhline(0, color="0.4", linewidth=0.8, zorder=1)
    ax.set_xlabel("Player's age (years)")
    ax.set_ylabel("Player's age minus opponent's age (years)")
    ax.set_title(title, loc="left")
    ax.grid(axis="y", color="0.9", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, title=None)


def plot_age_gap(matches, title="", ax=None):
    """Plot player's age (x) vs. age difference with the opponent (y).

    Points above zero are matches against younger opponents. Wins and
    losses have different colors. Returns the matplotlib Axes.
    """
    _check_columns(matches)
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5.5))
    for result, color in COLORS.items():
        subset = matches[matches["result"] == result]
        ax.scatter(subset["player_age"], subset["age_diff"], s=14, alpha=0.6,
                   color=color, linewidths=0, label=result, zorder=2)
    _style_axes(ax, title)
    return ax
