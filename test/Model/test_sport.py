import re
import pytest
from src.Model.sport import Sport


@pytest.mark.parametrize(
    "params, erreur, message",
    [
        (
            {"nom": 123, "categorie": "Collectif", "nb_joueurs": 11, "description": "desc",
             "sport_en_equipe": True},
            TypeError,
            "Le nom doit être une str",
        ),
        (
            {"nom": "", "categorie": "Collectif", "nb_joueurs": 11, "description": "desc",
             "sport_en_equipe": True},
            ValueError,
            "Le nom ne peut pas être vide",
        ),
        (
            {"nom": "Foot", "categorie": 123, "nb_joueurs": 11, "description": "desc",
             "sport_en_equipe": True},
            TypeError,
            "La catégorie doit être une str",
        ),
        (
            {"nom": "Foot", "categorie": "Collectif", "nb_joueurs": "11", "description": "desc",
             "sport_en_equipe": True},
            TypeError,
            "Le nombre de joueurs doit être un int",
        ),
        (
            {"nom": "Foot", "categorie": "Collectif", "nb_joueurs": 0, "description": "desc",
             "sport_en_equipe": True},
            ValueError,
            "Le nombre de joueurs doit être >= 1",
        ),
        (
            {"nom": "Foot", "categorie": "Collectif", "nb_joueurs": 11, "description": 123,
             "sport_en_equipe": True},
            TypeError,
            "La description doit être une str",
        ),
        (
            {"nom": "Foot", "categorie": "Collectif", "nb_joueurs": 11, "description": "",
             "sport_en_equipe": True},
            ValueError,
            "La description ne peut pas être vide",
        ),
        (
            {"nom": "Foot", "categorie": "Collectif", "nb_joueurs": 11, "description": "desc",
             "sport_en_equipe": "oui"},
            TypeError,
            "sport_en_equipe doit être un bool",
        ),
    ],
)
def test_sport_parametres(params, erreur, message):
    with pytest.raises(erreur, match=re.escape(message)):
        Sport(**params)


@pytest.mark.parametrize(
    "params",
    [
        {"nom": "Football", "categorie": "Collectif", "nb_joueurs": 11, "description": "Ballon",
         "sport_en_equipe": True},
        {"nom": "Tennis", "categorie": "Individuel", "nb_joueurs": 1, "description": "Raquette",
         "sport_en_equipe": False},
    ],
)
def test_sport_creation_valide(params):
    sport = Sport(**params)
    assert sport.nom == params["nom"]
    assert sport.nb_joueurs == params["nb_joueurs"]


@pytest.mark.parametrize(
    "s1, s2, attendu",
    [
        (
            Sport("Tennis", "Individuel", 1, "desc", False),
            Sport("Tennis", "Autre", 2, "autre", True),
            True,
        ),
        (
            Sport("Tennis", "Individuel", 1, "desc", False),
            Sport("Football", "Collectif", 11, "desc", True),
            False,
        ),
    ],
)
def test_sport_equality(s1, s2, attendu):
    assert (s1 == s2) is attendu


def test_sport_eq_autre_type():
    sport = Sport("Tennis", "Individuel", 1, "desc", False)
    assert sport.__eq__(42) is NotImplemented


@pytest.mark.parametrize(
    "s1, s2",
    [
        (
            Sport("Tennis", "Individuel", 1, "desc", False),
            Sport("Tennis", "Collectif", 2, "desc", True),
        ),
    ],
)
def test_sport_hash(s1, s2):
    assert hash(s1) == hash(s2)


@pytest.mark.parametrize(
    "sport, attendu",
    [
        (Sport("Basket", "Collectif", 5, "Panier", True), "collectif"),
        (Sport("Tennis", "Individuel", 1, "Raquette", False), "individuel"),
    ],
)
def test_sport_str(sport, attendu):
    result = str(sport)
    assert sport.nom in result
    assert attendu in result


def test_sport_repr():
    sport = Sport("Tennis", "Individuel", 1, "desc", False)
    result = repr(sport)
    assert "Sport(" in result
    assert "Tennis" in result
