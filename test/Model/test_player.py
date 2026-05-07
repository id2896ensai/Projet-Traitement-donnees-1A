import pytest
from datetime import date
from Model.player import Player


@pytest.fixture
def player():
    return Player(
        id=1,
        pseudo="CR7",
        nom="Ronaldo",
        prenom="Cristiano",
        date_de_naissance=date(1985, 2, 5),
        pays_de_naissance="Portugal",
        sexe="M",
        poids=85,
        taille=187,
        role="Attaquant",
        team="Al-Nassr"
    )


@pytest.mark.parametrize(
    "params, erreur, message",
    [
        (
            {"id": "1", "pseudo": "CR7", "nom": "Ronaldo", "prenom": "Cristiano",
             "date_de_naissance": "1985-02-05", "pays_de_naissance": "Portugal",
             "sexe": "M", "poids": 80, "taille": 187, "role": "Attaquant", "team": None,
             },
            TypeError,
            "id doit être un int",
        ),
        (
            {"id": 1, "pseudo": 123, "nom": "Ronaldo", "prenom": "Cristiano",
             "date_de_naissance": "1985-02-05", "pays_de_naissance": "Portugal",
             "sexe": "M", "poids": 80, "taille": 187, "role": "Attaquant", "team": None,
             },
            TypeError,
            "pseudo doit être une str ou None",
        ),
        (
            {"id": 1, "pseudo": "CR7", "nom": 123, "prenom": "Cristiano",
             "date_de_naissance": "1985-02-05", "pays_de_naissance": "Portugal",
             "sexe": "M", "poids": 80, "taille": 187, "role": "Attaquant", "team": None, },
            TypeError,
            "nom doit être une str",
        ),
        (
            {"id": 1, "pseudo": "CR7", "nom": "", "prenom": "Cristiano",
             "date_de_naissance": "1985-02-05", "pays_de_naissance": "Portugal",
             "sexe": "M", "poids": 80, "taille": 187, "role": "Attaquant", "team": None, },
            ValueError,
            "nom ne peut pas être vide",
        ),
        (
            {"id": 1, "pseudo": "CR7", "nom": "Ronaldo", "prenom": 123,
             "date_de_naissance": "1985-02-05", "pays_de_naissance": "Portugal",
             "sexe": "M", "poids": 80, "taille": 187, "role": "Attaquant", "team": None, },
            TypeError,
            "prenom doit être une str",
        ),
        (
            {"id": 1, "pseudo": "CR7", "nom": "Ronaldo", "prenom": "",
             "date_de_naissance": "1985-02-05", "pays_de_naissance": "Portugal",
             "sexe": "M", "poids": 80, "taille": 187, "role": "Attaquant", "team": None, },
            ValueError,
            "prenom ne peut pas être vide",
        ),
        (
            {"id": 1, "pseudo": "CR7", "nom": "Ronaldo", "prenom": "Cristiano",
             "date_de_naissance": "1985-02-05", "pays_de_naissance": "Portugal",
             "sexe": "M", "poids": "80", "taille": 187, "role": "Attaquant", "team": None, },
            TypeError,
            "poids doit être un int ou float",
        ),
        (
            {"id": 1, "pseudo": "CR7", "nom": "Ronaldo", "prenom": "Cristiano",
             "date_de_naissance": "1985-02-05", "pays_de_naissance": "Portugal",
             "sexe": "M", "poids": 80, "taille": "187", "role": "Attaquant", "team": None, },
            TypeError,
            "taille doit être un int ou float",
        ),
        (
            {"id": 1, "pseudo": "CR7", "nom": "Ronaldo", "prenom": "Cristiano",
             "date_de_naissance": "1985-02-05", "pays_de_naissance": "Portugal",
             "sexe": "M", "poids": 80, "taille": 187, "role": 3, "team": None, },
            TypeError,
            "role doit être une str ou None",
        ),
        (
            {"id": 1, "pseudo": "CR7", "nom": "Ronaldo", "prenom": "Cristiano",
             "date_de_naissance": "1985-02-05", "pays_de_naissance": 35,
             "sexe": "M", "poids": 80, "taille": 187, "role": "Attaquant", "team": None, },
            TypeError,
            "pays_de_naissance doit être une str ou None",
        ),
        (
            {"id": 1, "pseudo": "CR7", "nom": "Ronaldo", "prenom": "Cristiano",
             "date_de_naissance": "1985-02-05", "pays_de_naissance": "Portugal",
             "sexe": 1, "poids": 80, "taille": 187, "role": "Attaquant", "team": None, },
            TypeError,
            "sexe doit être une str ou None",
        ),
    ],
)
def test_player_isinstance_errors(params, erreur, message):
    with pytest.raises(erreur, match=message):
        Player(**params)


@pytest.mark.parametrize(
    "method, value, expected",
    [
        ("filtre_id", 1, True),
        ("filtre_id", 2, False),

        ("filtre_nom", "Ronaldo", True),
        ("filtre_nom", "Messi", False),

        ("filtre_prenom", "Cristiano", True),
        ("filtre_prenom", "Lionel", False),

        ("filtre_sexe", "M", True),
        ("filtre_sexe", "F", False),

        ("filtre_date_de_naissance", date(1985, 2, 5), True),
        ("filtre_date_de_naissance", date(2000, 1, 1), False),
    ],
)
def test_player_filtres(player, method, value, expected):
    assert getattr(player, method)(value) is expected


def test_player_repr(player):
    result = repr(player)
    assert "Player(" in result
    assert "Ronaldo" in result
    assert "Cristiano" in result
    assert "CR7" in result


def test_player_str(player):
    result = str(player)
    assert "Athlete" in result
    assert "Ronaldo" in result
    assert "Cristiano" in result
