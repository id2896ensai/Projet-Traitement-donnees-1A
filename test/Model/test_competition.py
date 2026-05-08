import re
import pytest
from datetime import date
from Model.competition import Competition


@pytest.fixture
def competition_defaut():
    return Competition(
        id=1,
        nom="Competition A",
        date_de_debut=date(2024, 1, 1),
        date_de_fin=date(2024, 12, 31),
        lieu="Lieu A",
        type="Tournoi",
        sports=["Sport A"],
    )


@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {"id": "1", "nom": "Competition A", "date_de_debut": date(2024, 1, 1),
             "date_de_fin": date(2024, 12, 31), "lieu": "Lieu A",
             "type": "Tournoi", "sports": ["Sport A"]},
            TypeError,
            "le id doit etre en entier",
        ),
        (
            {"id": 1, "nom": 123, "date_de_debut": date(2024, 1, 1),
             "date_de_fin": date(2024, 12, 31), "lieu": "Lieu A",
             "type": "Tournoi", "sports": ["Sport A"]},
            TypeError,
            "le nom doit etre en str",
        ),
        (
            {"id": 1, "nom": "Competition A", "date_de_debut": date(2024, 1, 1),
             "date_de_fin": date(2024, 12, 31), "lieu": 123,
             "type": "Tournoi", "sports": ["Sport A"]},
            TypeError,
            "Le lieu doit etre en str",
        ),
        (
            {"id": 1, "nom": "Competition A", "date_de_debut": "2024-01-01",
             "date_de_fin": date(2024, 12, 31), "lieu": "Lieu A",
             "type": "Tournoi", "sports": ["Sport A"]},
            TypeError,
            "La date de début doit être une date",
        ),
        (
            {"id": 1, "nom": "Competition A", "date_de_debut": date(2024, 1, 1),
             "date_de_fin": "2024-12-31", "lieu": "Lieu A",
             "type": "Tournoi", "sports": ["Sport A"]},
            TypeError,
            "La date de fin doit être une date",
        ),
        (
            {"id": 1, "nom": "Competition A", "date_de_debut": date(2024, 6, 1),
             "date_de_fin": date(2024, 1, 1), "lieu": "Lieu A",
             "type": "Tournoi", "sports": ["Sport A"]},
            ValueError,
            "La date de fin doit être après la date de début",
        ),
        (
            {"id": 1, "nom": "Competition A", "date_de_debut": date(2024, 1, 1),
             "date_de_fin": date(2024, 12, 31), "lieu": "Lieu A",
             "type": "Tournoi", "sports": "Sport A"},
            TypeError,
            "Les sports doievent etre en liste",
        ),
        (
            {"id": 1, "nom": "Competition A", "date_de_debut": date(2024, 1, 1),
             "date_de_fin": date(2024, 12, 31), "lieu": "Lieu A",
             "type": "Tournoi", "sports": [123]},
            TypeError,
            "Le sport doit etre en str",
        ),
    ],
)
def test_competition_invalid(params, erreur, message_erreur):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Competition(**params)


@pytest.mark.parametrize(
    "attribut, valeur_attendue",
    [
        ("id", 1),
        ("nom", "Competition A"),
        ("date_de_debut", date(2024, 1, 1)),
        ("date_de_fin", date(2024, 12, 31)),
        ("lieu", "Lieu A"),
        ("type", "Tournoi"),
        ("sports", ["Sport A"]),
    ],
)
def test_competition_creation(attribut, valeur_attendue, competition_defaut):
    assert getattr(competition_defaut, attribut) == valeur_attendue


@pytest.mark.parametrize(
    "contenu_attendu",
    [
        "Competition A",
        "Lieu A",
        "Tournoi",
        "2024-01-01",
        "2024-12-31",
    ],
)
def test_competition_str(contenu_attendu, competition_defaut):
    assert contenu_attendu in str(competition_defaut)


@pytest.mark.parametrize(
    "contenu_attendu",
    [
        "Competition(",
        "Competition A",
        "Lieu A",
        "Tournoi",
        "2024-01-01",
        "2024-12-31",
    ],
)
def test_competition_repr(contenu_attendu, competition_defaut):
    assert contenu_attendu in repr(competition_defaut)
