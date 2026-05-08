# Vérifie que le diagramme de classes est respecté :
# toutes les classes et méthodes attendues existent.
import datetime
import pytest

from Model.sport import Sport
from Model.person import Person
from Model.player import Player
from Model.team import Team
from Model.match import Match
from Model.classement import Classement
from Model.competition import Competition


# Helpers

def _sport() -> Sport:
    return Sport("Football", "ballon", 11, "Sport collectif", True)


def _player(id: int = 1) -> Player:
    return Player(
        id=id, pseudo=None, nom="Dupont", prenom="Antoine",
        date_de_naissance=datetime.date(1991, 7, 11),
        pays_de_naissance="France", sexe="M",
        poids=80.0, taille=183.0, role="Attaquant", team=None,
    )


def _team(id: int = 1) -> Team:
    s = _sport()
    return Team(id=id, sport=s, players=[], full_name="PSG", abbreviation="PSG")


# Sport
def test_sport_exists() -> None:
    s = _sport()
    assert s.nom == "Football"
    assert s.sport_en_equipe is True


def test_sport_eq_hash() -> None:
    s1 = Sport("Tennis", "raquette", 1, "Sport individuel", False)
    s2 = Sport("Tennis", "raquette", 1, "Sport individuel", False)
    assert s1 == s2
    assert hash(s1) == hash(s2)


def test_sport_str_repr() -> None:
    s = _sport()
    assert "Football" in str(s)
    assert "Sport(" in repr(s)


# Person

def test_person_exists() -> None:
    p = Person("Dupont", "Antoine", datetime.date(1991, 7, 11))
    assert p.nom == "Dupont"


def test_person_invalid_date() -> None:
    with pytest.raises(TypeError, match="date_de_naissance doit être une date"):
        Person("Dupont", "Antoine", "1991-07-11")  # type: ignore[arg-type]


# Player

def test_player_exists() -> None:
    p = _player()
    assert p.id == 1
    assert p.nom == "Dupont"


def test_player_filtres() -> None:
    p = _player(id=42)
    assert p.filtre_id(42) is True
    assert p.filtre_id(99) is False
    assert p.filtre_nom("Dupont") is True
    assert p.filtre_prenom("Antoine") is True
    assert p.filtre_sexe("M") is True


def test_player_str_repr() -> None:
    p = _player()
    assert "Athlete" in str(p)
    assert "Player(" in repr(p)


# Team

def test_team_exists() -> None:
    t = _team()
    assert t.full_name == "PSG"
    assert t.nb_players == 0


def test_team_with_players() -> None:
    s = _sport()
    p = _player()
    t = Team(id=1, sport=s, players=[p], full_name="Equipe A", abbreviation="EQA")
    assert t.nb_players == 1


def test_team_str_repr() -> None:
    t = _team()
    assert "PSG" in str(t)
    assert "Team(" in repr(t)


# Match

def test_match_exists() -> None:
    s = _sport()
    t1, t2 = _team(1), _team(2)
    m = Match(
        sport=s, participants=[t1, t2],
        scores={t1: 2, t2: 1},
        date_match=datetime.date(2024, 1, 1),
    )
    assert m.sport == s
    assert len(m.participants) == 2


def test_match_future_date_raises() -> None:
    s = _sport()
    t1, t2 = _team(1), _team(2)
    with pytest.raises(ValueError):
        Match(sport=s, participants=[t1, t2],
              scores={t1: 1, t2: 0},
              date_match=datetime.date(2100, 1, 1))


def test_match_str_repr() -> None:
    s = _sport()
    t1, t2 = _team(1), _team(2)
    m = Match(sport=s, participants=[t1, t2],
              scores={t1: 2, t2: 1},
              date_match=datetime.date(2024, 1, 1))
    assert "Match" in str(m)
    assert "Match(" in repr(m)


# Competition

def test_competition_exists() -> None:
    c = Competition(
        id=1, nom="Coupe du Monde",
        date_de_debut=datetime.date(2024, 6, 1),
        date_de_fin=datetime.date(2024, 7, 15),
        lieu="Allemagne", type="Championnat",
        sports=["Football"],
    )
    assert c.nom == "Coupe du Monde"


# Classement

def test_classement_exists() -> None:
    c = Competition(
        id=1, nom="Test",
        date_de_debut=datetime.date(2024, 1, 1),
        date_de_fin=datetime.date(2024, 1, 2),
        lieu="Paris", type="Coupe", sports=["Football"],
    )
    cl = Classement(c)
    t = _team()
    cl.entree[t] = 10
    assert cl.trier()[0][1] == 10


# Vérification structure (méthodes publiques)

def test_sport_has_required_methods() -> None:
    assert hasattr(Sport, "__eq__")
    assert hasattr(Sport, "__hash__")
    assert hasattr(Sport, "__str__")
    assert hasattr(Sport, "__repr__")


def test_player_has_filter_methods() -> None:
    for methode in ("filtre_id", "filtre_nom", "filtre_prenom",
                    "filtre_date_de_naissance", "filtre_sexe"):
        assert hasattr(Player, methode), f"Player.{methode} manquant"


def test_team_has_required_attributes() -> None:
    t = _team()
    for attr in ("id", "sport", "players", "full_name", "abbreviation",
                 "nb_players", "country", "region"):
        assert hasattr(t, attr), f"Team.{attr} manquant"


def test_match_has_required_attributes() -> None:
    s = _sport()
    t1, t2 = _team(1), _team(2)
    m = Match(sport=s, participants=[t1, t2],
              scores={t1: 1, t2: 0},
              date_match=datetime.date(2024, 1, 1))
    for attr in ("sport", "participants", "scores", "date_match"):
        assert hasattr(m, attr), f"Match.{attr} manquant"
