import pytest
from datetime import date

from Model.player import Player
from Model.sport import Sport


SPORT = Sport("Basketball", "Collectif", 5, "Jeu de ballon panier", True)
DOB = date(1995, 6, 17)


@pytest.fixture
def joueur_complet():
    return Player(
        id=1,
        pseudo="LeBron",
        nom="James",
        prenom="LeBron",
        date_de_naissance=DOB,
        pays_de_naissance="USA",
        sexe="M",
        poids=113.0,
        taille=206.0,
        role="Forward",
        team=None,
        sport=SPORT,
    )


@pytest.fixture
def joueur_minimal():
    return Player(
        id=2,
        pseudo=None,
        nom="Doe",
        prenom="John",
        date_de_naissance=DOB,
        pays_de_naissance=None,
        sexe=None,
        poids=0.0,
        taille=0.0,
        role=None,
        team=None,
        sport=None,
    )


# ── Création valide ───────────────────────────────────────────


def test_player_creation_complete(joueur_complet):
    assert joueur_complet.id == 1
    assert joueur_complet.pseudo == "LeBron"
    assert joueur_complet.nom == "James"
    assert joueur_complet.prenom == "LeBron"
    assert joueur_complet.date_de_naissance == DOB
    assert joueur_complet.pays_de_naissance == "USA"
    assert joueur_complet.sexe == "M"
    assert joueur_complet.poids == 113.0
    assert joueur_complet.taille == 206.0
    assert joueur_complet.role == "Forward"
    assert joueur_complet.team is None
    assert joueur_complet.sport == SPORT


def test_player_creation_minimal(joueur_minimal):
    assert joueur_minimal.pseudo is None
    assert joueur_minimal.pays_de_naissance is None
    assert joueur_minimal.sexe is None
    assert joueur_minimal.role is None
    assert joueur_minimal.sport is None


# ── Validation des types ──────────────────────────────────────


@pytest.mark.parametrize(
    "params, erreur, message",
    [
        (
            {"id": "1", "pseudo": None, "nom": "James", "prenom": "LeBron",
             "date_de_naissance": DOB, "pays_de_naissance": None, "sexe": None,
             "poids": 0.0, "taille": 0.0, "role": None, "team": None},
            TypeError,
            "id doit être un int",
        ),
        (
            {"id": 1, "pseudo": 42, "nom": "James", "prenom": "LeBron",
             "date_de_naissance": DOB, "pays_de_naissance": None, "sexe": None,
             "poids": 0.0, "taille": 0.0, "role": None, "team": None},
            TypeError,
            "pseudo doit être une str ou None",
        ),
        (
            {"id": 1, "pseudo": None, "nom": 123, "prenom": "LeBron",
             "date_de_naissance": DOB, "pays_de_naissance": None, "sexe": None,
             "poids": 0.0, "taille": 0.0, "role": None, "team": None},
            TypeError,
            "nom doit être une str",
        ),
        (
            {"id": 1, "pseudo": None, "nom": "", "prenom": "LeBron",
             "date_de_naissance": DOB, "pays_de_naissance": None, "sexe": None,
             "poids": 0.0, "taille": 0.0, "role": None, "team": None},
            ValueError,
            "nom ne peut pas être vide",
        ),
        (
            {"id": 1, "pseudo": None, "nom": "James", "prenom": 42,
             "date_de_naissance": DOB, "pays_de_naissance": None, "sexe": None,
             "poids": 0.0, "taille": 0.0, "role": None, "team": None},
            TypeError,
            "prenom doit être une str",
        ),
        (
            {"id": 1, "pseudo": None, "nom": "James", "prenom": "",
             "date_de_naissance": DOB, "pays_de_naissance": None, "sexe": None,
             "poids": 0.0, "taille": 0.0, "role": None, "team": None},
            ValueError,
            "prenom ne peut pas être vide",
        ),
        (
            {"id": 1, "pseudo": None, "nom": "James", "prenom": "LeBron",
             "date_de_naissance": DOB, "pays_de_naissance": 99, "sexe": None,
             "poids": 0.0, "taille": 0.0, "role": None, "team": None},
            TypeError,
            "pays_de_naissance doit être une str ou None",
        ),
        (
            {"id": 1, "pseudo": None, "nom": "James", "prenom": "LeBron",
             "date_de_naissance": DOB, "pays_de_naissance": None, "sexe": 1,
             "poids": 0.0, "taille": 0.0, "role": None, "team": None},
            TypeError,
            "sexe doit être une str ou None",
        ),
        (
            {"id": 1, "pseudo": None, "nom": "James", "prenom": "LeBron",
             "date_de_naissance": DOB, "pays_de_naissance": None, "sexe": None,
             "poids": "lourd", "taille": 0.0, "role": None, "team": None},
            TypeError,
            "poids doit être un int ou float",
        ),
        (
            {"id": 1, "pseudo": None, "nom": "James", "prenom": "LeBron",
             "date_de_naissance": DOB, "pays_de_naissance": None, "sexe": None,
             "poids": 0.0, "taille": "grand", "role": None, "team": None},
            TypeError,
            "taille doit être un int ou float",
        ),
        (
            {"id": 1, "pseudo": None, "nom": "James", "prenom": "LeBron",
             "date_de_naissance": DOB, "pays_de_naissance": None, "sexe": None,
             "poids": 0.0, "taille": 0.0, "role": 42, "team": None},
            TypeError,
            "role doit être une str ou None",
        ),
        (
            {"id": 1, "pseudo": None, "nom": "James", "prenom": "LeBron",
             "date_de_naissance": DOB, "pays_de_naissance": None, "sexe": None,
             "poids": 0.0, "taille": 0.0, "role": None, "team": None,
             "sport": "Basketball"},
            TypeError,
            "sport doit être une instance de Sport ou None",
        ),
    ],
)
def test_player_invalid(params, erreur, message):
    with pytest.raises(erreur, match=message):
        Player(**params)


# ── __str__ et __repr__ ───────────────────────────────────────


def test_player_str(joueur_complet):
    result = str(joueur_complet)
    assert "James" in result
    assert "LeBron" in result


def test_player_repr(joueur_complet):
    result = repr(joueur_complet)
    assert "Player(" in result
    assert "nom:" in result
    assert "James" in result
    assert "LeBron" in result


# ── Méthodes filtre_* ─────────────────────────────────────────


def test_filtre_id(joueur_complet):
    assert joueur_complet.filtre_id(1) is True
    assert joueur_complet.filtre_id(99) is False


def test_filtre_nom(joueur_complet):
    assert joueur_complet.filtre_nom("James") is True
    assert joueur_complet.filtre_nom("Durant") is False


def test_filtre_prenom(joueur_complet):
    assert joueur_complet.filtre_prenom("LeBron") is True
    assert joueur_complet.filtre_prenom("Kevin") is False


def test_filtre_date_de_naissance(joueur_complet):
    assert joueur_complet.filtre_date_de_naissance(DOB) is True
    assert joueur_complet.filtre_date_de_naissance(date(2000, 1, 1)) is False


def test_filtre_sexe(joueur_complet):
    assert joueur_complet.filtre_sexe("M") is True
    assert joueur_complet.filtre_sexe("F") is False


def test_filtre_sexe_none(joueur_minimal):
    assert joueur_minimal.filtre_sexe(None) is True
    assert joueur_minimal.filtre_sexe("M") is False
