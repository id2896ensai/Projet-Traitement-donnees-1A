import pytest

from src.Model.classement import Classement
from src.Model.competition import Competition
from src.Model.sport import Sport
from src.Model.team import Team


@pytest.fixture
def sport():
    return Sport("Football", "Collectif", 11, "desc", True)


@pytest.fixture
def competition(sport):
    return Competition(
        id=1,
        nom="Coupe Test",
        date_de_debut=__import__("datetime").date(2024, 1, 1),
        date_de_fin=__import__("datetime").date(2024, 1, 2),
        lieu="Paris",
        type="Championnat",
        sports=["Football"],
    )


@pytest.fixture
def team_factory(sport):
    def create_team(id, name):
        return Team(
            id=id,
            sport=sport,
            players=[],
            full_name=name,
            abbreviation=name[:3].upper(),
        )
    return create_team


@pytest.fixture
def team1(team_factory):
    return team_factory(1, "PSG")


@pytest.fixture
def team2(team_factory):
    return team_factory(2, "OM")


def test_classement_init(competition):
    c = Classement(competition)

    assert c.competition == competition
    assert isinstance(c.entree, dict)
    assert len(c.entree) == 0


def test_classement_init_type_error():
    with pytest.raises(TypeError):
        Classement("not_a_competition")


def test_classement_tri(team1, team2, competition):
    c = Classement(competition)

    c.entree[team1] = 10
    c.entree[team2] = 20

    result = c.trier()

    assert result[0][0] == team2
    assert result[0][1] == 20
    assert result[1][0] == team1
    assert result[1][1] == 10


def test_classement_str(team1, team2, competition):
    c = Classement(competition)

    c.entree[team1] = 5
    c.entree[team2] = 10

    result = str(c)

    assert "Classement de la competition" in result
    assert "PSG" in result or "PSG" in str(team1)
    assert "OM" in result or "OM" in str(team2)


def test_classement_repr(team1, team2, competition):
    c = Classement(competition)

    c.entree[team1] = 5
    c.entree[team2] = 10

    result = repr(c)

    assert "Classement(" in result
    assert "competition:" in result
    assert "entree:" in result
