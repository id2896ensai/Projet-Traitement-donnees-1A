import pytest
from datetime import date
from Model.team import Team
from Model.sport import Sport
from Model.player import Player


@pytest.fixture
def sport_defaut():
    return Sport(
        nom="Sport A",
        categorie="Categorie A",
        nb_joueurs=5,
        description="Description du sport A.",
        sport_en_equipe=True,
    )


def type_player(id, nom, prenom):
    return Player(
        id=id,
        pseudo=None,
        nom=nom,
        prenom=prenom,
        date_de_naissance=date(2000, 10, 10),
        pays_de_naissance=None,
        sexe="M",
        poids=70,
        taille=175,
        role=None,
        team=None,
    )


@pytest.fixture
def players_defaut():
    return [type_player(1, "Nom A", "Prenom A"), type_player(2, "Nom B", "Prenom B")]


@pytest.mark.parametrize(
    "params, error, message",
    [
        (
            {"id": "1", "sport": Sport("F", "C", 1, "d", True), "players": [], "full_name": "Team"},
            TypeError,
            "id doit être un int",
        ),
        (
            {"id": 1, "sport": "football", "players": [], "full_name": "Team"},
            TypeError,
            "sport doit être une instance de Sport",
        ),
        (
            {"id": 1, "sport": Sport("F", "C", 1, "d", True), "players": "not list",
             "full_name": "Team"},
            TypeError,
            "players doit être une liste",
        ),
        (
            {"id": 1, "sport": Sport("F", "C", 1, "d", True), "players": [object()],
             "full_name": "Team"},
            TypeError,
            "Chaque élément de players doit être un Player",
        ),
        (
            {"id": 1, "sport": Sport("F", "C", 1, "d", True), "players": [], "team_api_id": "x",
             "full_name": "Team"},
            TypeError,
            "team_api_id doit être un int ou None",
        ),
        (
            {"id": 1, "sport": Sport("F", "C", 1, "d", True), "players": [], "full_name": 123},
            TypeError,
            "full_name doit être une str ou None",
        ),
        (
            {"id": 1, "sport": Sport("F", "C", 1, "d", True), "players": [], "full_name": "   "},
            ValueError,
            "full_name ne peut pas être vide",
        ),
        (
            {"id": 1, "sport": Sport("F", "C", 1, "d", True), "players": [], "abbreviation": 123},
            TypeError,
            "abbreviation doit être une str ou None",
        ),
        (
            {"id": 1, "sport": Sport("F", "C", 1, "d", True), "players": [], "nickname": 123},
            TypeError,
            "nickname doit être une str ou None",
        ),
        (
            {"id": 1, "sport": Sport("F", "C", 1, "d", True), "players": [], "city": 123},
            TypeError,
            "city doit être une str ou None",
        ),
        (
            {"id": 1, "sport": Sport("F", "C", 1, "d", True), "players": [], "state": 123},
            TypeError,
            "state doit être une str ou None",
        ),
        (
            {"id": 1, "sport": Sport("F", "C", 1, "d", True), "players": [], "country": 123},
            TypeError,
            "country doit être une str ou None",
        ),
        (
            {"id": 1, "sport": Sport("F", "C", 1, "d", True), "players": [], "region": 123},
            TypeError,
            "region doit être une str ou None",
        ),
    ],
)
def test_team_isinstance_errors(params, error, message):
    with pytest.raises(error, match=message):
        Team(**params)


@pytest.mark.parametrize(
    "params, attribut, valeur_attendue",
    [
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"},
            "id",
            1,
        ),
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"},
            "full_name",
            "Equipe A",
        ),
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"},
            "abbreviation",
            "EQA",
        ),
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"},
            "team_api_id",
            None,
        ),
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"},
            "nickname",
            None,
        ),
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"},
            "city",
            None,
        ),
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"},
            "state",
            None,
        ),
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"},
            "country",
            None,
        ),
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"},
            "region",
            None,
        ),
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA", "team_api_id": 99},
            "team_api_id",
            99,
        ),
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA", "city": "Ville A"},
            "city",
            "Ville A",
        ),
        (
            {"id": 1, "full_name": "Equipe A", "abbreviation": "EQA", "nickname": "Surnom A"},
            "nickname",
            "Surnom A",
        ),
    ],
)
def test_team_attributs(params, attribut, valeur_attendue, sport_defaut):
    team = Team(sport=sport_defaut, players=[], **params)
    assert getattr(team, attribut) == valeur_attendue


@pytest.mark.parametrize(
    "nb_joueurs_attendu, players",
    [
        (0, []),
        (1, [type_player(1, "Nom A", "Prenom A")]),
        (2, [type_player(1, "Nom A", "Prenom A"), type_player(2, "Nom B", "Prenom B")]),
    ],
)
def test_team_nb_players(nb_joueurs_attendu, players, sport_defaut):
    team = Team(id=1, sport=sport_defaut, players=players,
                full_name="Equipe A", abbreviation="EQA")
    assert team.nb_players == nb_joueurs_attendu


@pytest.mark.parametrize(
    "params, contenu_attendu",
    [
        ({"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"}, "1"),
        ({"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"}, "Equipe A"),
        ({"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"}, "EQA"),
        ({"id": 1, "full_name": "Equipe A", "abbreviation": "EQA", "city": "Ville A"}, "Ville A"),
        ({"id": 1, "full_name": "Equipe A", "abbreviation": "EQA", "country": "Pays A"}, "Pays A"),
    ],
)
def test_team_str_contenu(params, contenu_attendu, sport_defaut):
    team = Team(sport=sport_defaut, players=[], **params)
    assert contenu_attendu in str(team)


@pytest.mark.parametrize(
    "params, contenu_attendu",
    [
        ({"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"}, "Team("),
        ({"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"}, "Equipe A"),
        ({"id": 1, "full_name": "Equipe A", "abbreviation": "EQA"}, "EQA"),
        ({"id": 42, "full_name": "Equipe A", "abbreviation": "EQA"}, "42"),
    ],
)
def test_team_repr_contenu(params, contenu_attendu, sport_defaut):
    team = Team(sport=sport_defaut, players=[], **params)
    assert contenu_attendu in repr(team)
