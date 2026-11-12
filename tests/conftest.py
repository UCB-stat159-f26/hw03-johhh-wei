"""Shared fixtures: mock JS content, so tests never hit the live server."""

from pathlib import Path

import pytest

DATA = Path(__file__).parent / "data"


@pytest.fixture
def female_js():
    return (DATA / "FemalePlayerCareer.js").read_text()


@pytest.fixture
def male_js():
    return (DATA / "MalePlayerCareer.js").read_text()
