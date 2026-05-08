import re
import pytest
from datetime import date
from Model.coach import Coach


# ══════════════════════════════════════════════════════════════════
# Fixture
# ══════════════════════════════════════════════════════════════════

@pytest.fixture
def coach_defaut():
    return Coach(
        nom="Nom A",
        prenom="Prenom A",
        date_de_naissance=date(1970, 1, 1),
    )


# ══════════════════════════════════════════════════════════════════
# Tests des erreurs à l'instanciation (héritées de Person)
# ══════════════════════════════════════════════════════════════════

@pytest.mark.parametrize(
    "params, erreur, message_erreur",
    [
        (
            {"nom": 123, "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            TypeError,
            "nom doit être une str",
        ),
        (
            {"nom": "   ", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            ValueError,
            "nom ne peut pas être vide",
        ),
        (
            {"nom": "Nom A", "prenom": 123, "date_de_naissance": date(1970, 1, 1)},
            TypeError,
            "prenom doit être une str",
        ),
        (
            {"nom": "Nom A", "prenom": "   ", "date_de_naissance": date(1970, 1, 1)},
            ValueError,
            "prenom ne peut pas être vide",
        ),
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": "1970-01-01"},
            TypeError,
            "date_de_naissance doit être une date",
        ),
    ],
)
def test_coach_erreurs_instanciation(params, erreur, message_erreur):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Coach(**params)


# ══════════════════════════════════════════════════════════════════
# Tests des attributs après instanciation
# ══════════════════════════════════════════════════════════════════

@pytest.mark.parametrize(
    "params, attribut, valeur_attendue",
    [
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            "nom",
            "Nom A",
        ),
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            "prenom",
            "Prenom A",
        ),
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            "date_de_naissance",
            date(1970, 1, 1),
        ),
    ],
)
def test_coach_attributs(params, attribut, valeur_attendue):
    coach = Coach(**params)
    assert getattr(coach, attribut) == valeur_attendue


# ══════════════════════════════════════════════════════════════════
# Tests du contenu de __str__
# ══════════════════════════════════════════════════════════════════

@pytest.mark.parametrize(
    "params, contenu_attendu",
    [
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            "Coach",
        ),
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            "Nom A",
        ),
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            "Prenom A",
        ),
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            "1970-01-01",
        ),
    ],
)
def test_coach_str_contenu(params, contenu_attendu):
    coach = Coach(**params)
    assert contenu_attendu in str(coach)


# ══════════════════════════════════════════════════════════════════
# Tests du contenu de __repr__
# ══════════════════════════════════════════════════════════════════

@pytest.mark.parametrize(
    "params, contenu_attendu",
    [
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            "Coach(",
        ),
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            "Nom A",
        ),
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            "Prenom A",
        ),
        (
            {"nom": "Nom A", "prenom": "Prenom A", "date_de_naissance": date(1970, 1, 1)},
            "1970-01-01",
        ),
    ],
)
def test_coach_repr_contenu(params, contenu_attendu):
    coach = Coach(**params)
    assert contenu_attendu in repr(coach)
