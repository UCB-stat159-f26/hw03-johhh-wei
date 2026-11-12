import matplotlib

matplotlib.use("Agg")

import pandas as pd
import pytest

from tenniscareer.clean import clean_matches, extract_matches
from tenniscareer.plot import plot_age_gap


def test_plot_draws_one_group_of_points_per_result(male_js):
    rafa = clean_matches(extract_matches(male_js), pd.Timestamp("1986-06-03"))
    ax = plot_age_gap(rafa, title="Rafael Nadal")
    sizes = sorted(len(points.get_offsets()) for points in ax.collections)
    assert sizes == [1, 2]
    assert ax.get_title(loc="left") == "Rafael Nadal"


def test_plot_rejects_wrong_data_frame():
    with pytest.raises(ValueError):
        plot_age_gap(pd.DataFrame({"x": [1, 2]}))
