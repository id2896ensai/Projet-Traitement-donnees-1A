import pytest
from datetime import date
from Model.match import Match
from Model.sport import Sport


@pytest.fixture
def sport():
    return Sport("Football", "Collectif", 11, "Jeu de ballon", True)


class Testing:
    """Participant minimal pour les tests"""
    def __init__(self, sport, name="P"):
        self.sport = sport
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


@pytest.fixture
def participants_valid(sport):
    return [Testing(sport, "PSG"), Testing(sport, "OM")]


@pytest.fixture
def scores_valid(participants_valid):
    return {participants_valid[0]: 3, participants_valid[1]: 1}


@pytest.fixture
def date_valid():
    return date(2024, 1, 1)


def test_match_ok(sport, participants_valid, scores_valid, date_valid):
    match = Match(sport, participants_valid, scores_valid, date_valid)

    assert match.sport == sport
    assert len(match.participants) == 2
    assert match.scores == scores_valid
    assert match.date_match == date_valid


@pytest.mark.parametrize(
    "sport_val, participants, scores, date_match, error",
    [
        ("football", [1, 2], {}, date(2024, 1, 1), TypeError),
        (Sport("Football", "Collectif", 11, "desc", True), "not list", {}, date(2024, 1, 1),
         TypeError),
        (Sport("Football", "Collectif", 11, "desc", True), [1, 2], "not dict", date(2024, 1, 1),
         TypeError),
        (Sport("Football", "Collectif", 11, "desc", True), [1, 2], {}, "2024-01-01", TypeError),
        (Sport("Football", "Collectif", 11, "desc", True), [], {}, date(2024, 1, 1), ValueError),
        (Sport("Football", "Collectif", 11, "desc", True), [Testing(None), Testing(None)], {},
         date(2024, 1, 1), ValueError),
    ],
)
def test_match_errors(sport_val, participants, scores, date_match, error):
    with pytest.raises(error):
        Match(sport_val, participants, scores, date_match)


def test_match_missing_score(sport):
    p1 = Testing(sport)
    p2 = Testing(sport)

    with pytest.raises(ValueError):
        Match(sport, [p1, p2], {p1: 0}, date(2024, 1, 1))


def test_match_future_date(sport):
    p1 = Testing(sport)
    p2 = Testing(sport)

    with pytest.raises(ValueError):
        Match(sport, [p1, p2], {p1: 1, p2: 2}, date(2100, 1, 1))


def test_match_str(sport, participants_valid, scores_valid, date_valid):
    match = Match(sport, participants_valid, scores_valid, date_valid)
    text = str(match)

    assert "Match" in text
    assert "Résultats" in text
    assert "PSG" in text


def test_match_repr(sport, participants_valid, scores_valid, date_valid):
    match = Match(sport, participants_valid, scores_valid, date_valid)
    text = repr(match)

    assert "Match(" in text
    assert "sport=" in text
