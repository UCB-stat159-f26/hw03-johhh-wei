import pandas as pd
import pytest

from tenniscareer.clean import (COLUMNS, clean_matches, extract_dob,
                                extract_matches)

SERENA_DOB = pd.Timestamp("1981-09-26")
NADAL_DOB = pd.Timestamp("1986-06-03")


def test_extract_matches_reads_every_record(female_js, male_js):
    assert len(extract_matches(female_js)) == 3
    assert len(extract_matches(male_js)) == 3


def test_extract_matches_keeps_raw_fields(female_js):
    first = extract_matches(female_js)[0]
    assert first[0] == "19951030"
    assert first[11] == "Anne Miller"


def test_extract_matches_handles_closing_bracket_on_its_own_line():
    js_text = 'var matchmx = [["20200101", "A"],\n["20200108", "B"]\n   ];\n'
    assert len(extract_matches(js_text)) == 2


def test_extract_matches_without_matches_is_empty():
    assert extract_matches("") == []
    assert extract_matches("var fullname = 'Nobody';") == []


def test_extract_dob():
    assert extract_dob("var dob = 19810926;\nvar ht = 175;") == SERENA_DOB


def test_extract_dob_missing_raises():
    with pytest.raises(ValueError):
        extract_dob("var ht = 175;")


def test_clean_matches_columns_and_size(female_js):
    serena = clean_matches(extract_matches(female_js), SERENA_DOB)
    assert list(serena.columns) == COLUMNS
    assert len(serena) == 3


def test_clean_matches_parses_dates_and_results(female_js):
    serena = clean_matches(extract_matches(female_js), SERENA_DOB)
    assert serena["date"].iloc[0] == pd.Timestamp("1995-10-30")
    assert serena["result"].tolist() == ["Loss", "Loss", "Loss"]


def test_female_opponent_age_comes_from_date_of_birth(female_js):
    serena = clean_matches(extract_matches(female_js), SERENA_DOB).iloc[0]
    # Serena was 14.09 and Anne Miller (born 1977-01-19) was 18.78
    assert serena["player_age"] == pytest.approx(14.09, abs=0.01)
    assert serena["opponent_age"] == pytest.approx(18.78, abs=0.01)
    assert serena["age_diff"] == pytest.approx(-4.69, abs=0.01)


def test_male_opponent_age_is_used_as_given(male_js):
    rafa = clean_matches(extract_matches(male_js), NADAL_DOB)
    assert rafa["opponent_age"].iloc[0] == pytest.approx(22.264202601)
    assert rafa["player_age"].iloc[0] == pytest.approx(15.27, abs=0.01)


def test_male_results_and_sorting(male_js):
    rafa = clean_matches(extract_matches(male_js), NADAL_DOB)
    assert rafa["date"].is_monotonic_increasing
    assert sorted(rafa["result"]) == ["Loss", "Loss", "Win"]


def test_missing_opponent_info_gives_missing_age(male_js):
    records = extract_matches(male_js)
    records[0][16] = ""
    rafa = clean_matches(records, NADAL_DOB)
    assert rafa["opponent_age"].isna().sum() == 1


def test_duplicated_records_are_dropped(female_js):
    records = extract_matches(female_js)
    serena = clean_matches(records + records, SERENA_DOB)
    assert len(serena) == 3


def test_records_without_result_are_dropped(female_js):
    records = extract_matches(female_js)
    records[0][4] = ""
    assert len(clean_matches(records, SERENA_DOB)) == 2


@pytest.mark.parametrize("score", ["W/O", "DEF", ""])
def test_matches_that_were_not_played_are_dropped(female_js, score):
    records = extract_matches(female_js)
    records[0][9] = score
    assert len(clean_matches(records, SERENA_DOB)) == 2


def test_retirements_are_kept(female_js):
    records = extract_matches(female_js)
    records[0][9] = "6-1 2-0 RET"
    assert len(clean_matches(records, SERENA_DOB)) == 3
