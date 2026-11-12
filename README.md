# tenniscareer

STAT 159 (Fall 2026), HW3. A small Python package that downloads the career
matches of a tennis player from [tennisabstract.com](https://www.tennisabstract.com)
and draws a scatter plot like the New York Times chart of Serena Williams
that we reproduced in HW2: the player's age on the x-axis, and the difference
between the player's age and the opponent's age on the y-axis, with wins and
losses in different colors.

## Installation

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-johhh-wei.git
```

It needs Python 3.9 or later and installs `pandas`, `matplotlib` and `requests`.

## Usage

The package has two public functions.

```python
import matplotlib.pyplot as plt
from tenniscareer import get_player_matches, plot_age_gap

# Serena Williams data and plot
serena = get_player_matches("serena williams")
plot_age_gap(serena, title="Serena Williams")
plt.show()

# Rafael Nadal data and plot
rafa = get_player_matches("Rafael Nadal")
plot_age_gap(rafa)

# raises PlayerNotFoundError with a message saying the player was not found
unknown_player = get_player_matches("GastonSanchez")
```

### `get_player_matches(name)`

`name` can be written as `"serena williams"`, `"Serena Williams"` or
`"SerenaWilliams"`. The function returns a pandas data frame with one row per
singles match, sorted by date. As in HW2, matches that were never played
(walkovers and defaults, where the score has no games) are dropped, and
retirements are kept:

| column | description |
|---|---|
| `date` | start date of the tournament |
| `tournament`, `surface`, `round`, `score` | match information |
| `opponent` | name of the opponent |
| `result` | `"Win"` or `"Loss"` |
| `player_age` | age of the player, in years |
| `opponent_age` | age of the opponent, in years |
| `age_diff` | `player_age - opponent_age` (positive when the opponent is younger) |

If tennisabstract.com has no player with that name, the function raises
`PlayerNotFoundError` (a subclass of `ValueError`) with a message that
includes the name that was typed and the key that was looked up.

### `plot_age_gap(matches, title="", ax=None)`

Takes the data frame from `get_player_matches()` and returns a matplotlib
`Axes`. Matches with an unknown opponent age are left out of the plot.

## Where the data comes from

For each player the package reads two files:

- `jsmatches/<Player>.js` has the player's date of birth (`var dob`) and the
  most recent matches (`var matchmx`);
- `jsmatches/<Player>Career.js` has the earlier matches (`var morematchmx`).
  Players with a short career do not have this file, and that is fine.

For male players the files on tennisabstract.com stop in 2018 (for example,
Rafael Nadal's last match in them is from August 2018), so the data frame and
the plot only go up to that point.

The files of female and male players are different. In the files of female
players each match has the opponent's date of birth, so the opponent's age is
computed from it. In the files of male players the opponent's age is already
there. The cleaning code looks at the value itself (8 digits or a decimal
number) so the same function works for both.

## Package layout

```
src/tenniscareer/
    names.py     "serena williams" -> "SerenaWilliams"
    fetch.py     downloads the JS files (the only code that uses the network)
    clean.py     JS text -> match records -> clean data frame
    matches.py   get_player_matches()
    plot.py      plot_age_gap()
tests/
    data/        mock FemalePlayerCareer.js and MalePlayerCareer.js
```

## Tests

The tests never contact tennisabstract.com. They use the mock JS content
from the assignment (in `tests/data/`) and replace the download functions
where needed.

```bash
git clone https://github.com/UCB-stat159-f26/hw03-johhh-wei.git
cd hw03-johhh-wei
pip install -e ".[test]"
pytest
```

## Reflections

The biggest change from HW2 was moving from scripts to functions that other
people call. In HW2 my scripts only had to work for Serena, so things like her
date of birth and the file name were written directly in the code. Here every
one of those became either an argument or something the code has to find by
itself, and that is how I noticed that the player's date of birth is not in
the Career file at all but in the other JS file of the player.

The female and male files being different was the part I spent the most time
on. My first idea was to find out the player's gender and have two cleaning
functions. In the end it was simpler to check the value of each record,
because a date of birth is always 8 digits and an age is a decimal number.

Keeping every function under 20 lines meant that I could check each step
(build the name, download, extract the records, clean, plot) one at a time
with simple code. It also made testing much easier, because the functions
that parse and clean the text do not download anything, so I could test them
with the mock files and never touch the website.

I also learned the packaging side: the `src/` layout, `pyproject.toml`, and
that `pip install git+https://...` only works when the dependencies and the
package location are declared correctly.

One limitation I know about is that a name typed without spaces and all in
lower case (for example "serenawilliams") cannot be split into first and last
name, so it will not be found.

AI use is described in `ai_documentation.txt`.
