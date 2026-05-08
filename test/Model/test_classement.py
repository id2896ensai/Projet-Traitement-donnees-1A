import re
import pytest
from datetime import date
from Model.classement import Classement
from Model.competition import Competition
from Model.team import Team
from Model.sport import Sport


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


@pytest.fixture
def sport_defaut():
    return Sport(
        nom="Sport A",
        categorie="Categorie A",
        nb_joueurs=5,
        description="Description A.",
        sport_en_equipe=True,
    )


def make_team(id, nom, sport):
    return Team(
        id=id,
        sport=sport,
        players=[],
        full_name=nom,
        abbreviation=nom[:3].upper(),
    )


@pytest.fixture
def classement_defaut(competition_defaut):
    return Classement(competition=competition_defaut)


@pytest.mark.parametrize(
    "competition, erreur, message_erreur",
    [
        (
            "pas une competition",
            TypeError,
            "competition doit être une instance de Competition",
        ),
        (
            123,
            TypeError,
            "competition doit être une instance de Competition",
        ),
        (
            None,
            TypeError,
            "competition doit être une instance de Competition",
        ),
    ],
)
def test_classement_init_type_error(competition, erreur, message_erreur):
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Classement(competition=competition)


def test_classement_init(classement_defaut, competition_defaut):
    assert classement_defaut.competition == competition_defaut
    assert classement_defaut.entree == {}


@pytest.mark.parametrize(
    "entrees, ordre_attendu",
    [
        (
            {"Equipe A": 10.0, "Equipe B": 20.0, "Equipe C": 15.0},
            ["Equipe B", "Equipe C", "Equipe A"],
        ),
        (
            {"Equipe A": 5.0, "Equipe B": 5.0},
            ["Equipe A", "Equipe B"],
        ),
        (
            {},
            [],
        ),
    ],
)
def test_classement_tri(entrees, ordre_attendu, competition_defaut, sport_defaut):
    classement = Classement(competition=competition_defaut)
    teams = {
        nom: make_team(i, nom, sport_defaut)
        for i, nom in enumerate(entrees.keys(), 1)
    }
    for nom, points in entrees.items():
        classement.entree[teams[nom]] = points

    resultat = classement.trier()
    noms_resultat = [equipe.full_name for equipe, _ in resultat]
    assert noms_resultat == ordre_attendu


@pytest.mark.parametrize(
    "contenu_attendu",
    [
        "Classement",
        "Competition A",
    ],
)
def test_classement_str(contenu_attendu, classement_defaut):
    assert contenu_attendu in str(classement_defaut)


@pytest.mark.parametrize(
    "contenu_attendu",
    [
        "Classement(",
        "competition:",
        "entree:",
    ],
)
def test_classement_repr(contenu_attendu, classement_defaut):
    assert contenu_attendu in repr(classement_defaut)
