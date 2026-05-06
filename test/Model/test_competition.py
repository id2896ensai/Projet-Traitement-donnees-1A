import re
import pytest
from datetime import date

from src.Model.competition import Competition


@pytest.fixture
def valid_competition():
    return Competition(
        id=1,
        nom="Coupe du Monde",
        date_de_debut=date(2022, 11, 20),
        date_de_fin=date(2022, 12, 18),
        lieu="Qatar",
        type="Championnat",
        sports=["Football"]
    )


def test_competition_creation(valid_competition):
    assert valid_competition.id == 1
    assert valid_competition.nom == "Coupe du Monde"
    assert valid_competition.lieu == "Qatar"
    assert valid_competition.type == "Championnat"
    assert "Football" in valid_competition.sports


@pytest.mark.parametrize(
    "params, erreur, message",
    [
        (
            {"id": "1", "nom": "Coupe du Monde", "date_de_debut": date(2024, 1, 1),
             "date_de_fin": date(2024, 1, 2), "lieu": "Qatar", "type": "Championnat",
             "sports": ["Football"],
             },
            TypeError,
            "le id doit etre en entier",
        ),
        (
            {"id": 1, "nom": 123, "date_de_debut": date(2024, 1, 1),
             "date_de_fin": date(2024, 1, 2), "lieu": "Qatar", "type": "Championnat",
             "sports": ["Football"],
             },
            TypeError,
            "le nom doit etre en str",
        ),
        (
            {"id": 1, "nom": "Coupe du Monde", "date_de_debut": date(2024, 1, 1),
             "date_de_fin": date(2024, 1, 2), "lieu": 35, "type": "Championnat",
             "sports": ["Football"],
             },
            TypeError,
            "Le lieu doit etre en str",
        ),
        (
            {"id": 1, "nom": "Coupe du Monde", "date_de_debut": "2024-01-01",
             "date_de_fin": date(2024, 1, 2), "lieu": "Qatar", "type": "Championnat",
             "sports": ["Football"],
             },
            TypeError,
            "La date de début doit être une date",
        ),
        (
            {"id": 1, "nom": "Coupe du Monde", "date_de_debut": date(2024, 1, 1),
             "date_de_fin": "2024-01-02", "lieu": "Qatar", "type": "Championnat",
             "sports": ["Football"],
             },
            TypeError,
            "La date de fin doit être une date",
        ),
        (
            {"id": 1, "nom": "Coupe du Monde", "date_de_debut": date(2024, 1, 5),
             "date_de_fin": date(2024, 1, 2), "lieu": "Qatar", "type": "Championnat",
             "sports": ["Football"],
             },
            ValueError,
            "La date de fin doit être après la date de début",
        ),
        (
            {"id": 1, "nom": "Coupe du Monde", "date_de_debut": date(2024, 1, 1),
             "date_de_fin": date(2024, 1, 2), "lieu": "Qatar", "type": "Championnat",
             "sports": "Football",
             },
            TypeError,
            "Les sports doievent etre en liste",
        ),
        (
            {"id": 1, "nom": "Coupe du Monde", "date_de_debut": date(2024, 1, 1),
             "date_de_fin": date(2024, 1, 2), "lieu": "Qatar", "type": "Championnat",
             "sports": [2],
             },
            TypeError,
            "Le sport doit etre en str",
        ),
    ],
)
def test_competition_invalid(params, erreur, message):
    with pytest.raises(erreur, match=re.escape(message)):
        Competition(**params)


def test_competition_str(valid_competition):
    result = str(valid_competition)

    assert "Competition" in result
    assert "Coupe du Monde" in result
    assert "Qatar" in result
    assert "Football" in result


def test_competition_repr(valid_competition):
    result = repr(valid_competition)

    assert "Competition(" in result
    assert "nom:" in result
    assert "Qatar" in result
