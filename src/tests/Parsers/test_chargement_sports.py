# Tests d'intégration : vérifie que chaque sport se charge correctement
# via le registre SPORTS_REGISTRY (équipes, joueurs, matchs).
import pytest
from typing import Any

from Parsers.sport_registry import SPORTS_REGISTRY
from Parsers.Loaders.genericloaders import (
    GenericTeamLoader,
    GenericMatchLoader,
    GenericPlayerLoader,
)
from Model.match import Match
from Model.team import Team


def _charger(sport_nom: str) -> tuple[list[Team], list[Any], list[Match]]:
    """Charge équipes, joueurs et matchs pour le sport donné via le registre."""
    cfg = SPORTS_REGISTRY[sport_nom]

    team_loader = GenericTeamLoader(cfg["team_csv"], cfg["TeamAdapter"]())
    teams: list[Team] = team_loader.load()

    players: list[Any] = []
    if cfg.get("player_csv") and cfg.get("PlayerAdapter"):
        player_loader = GenericPlayerLoader(cfg["player_csv"], cfg["PlayerAdapter"]())
        players = player_loader.load()

    teams_dict = team_loader.load_as_dict(cfg["team_key"])
    kwarg: str = cfg["match_kwarg"]
    match_adapter = cfg["MatchAdapter"](**{kwarg: teams_dict})
    matches: list[Match] = GenericMatchLoader(cfg["match_csv"], match_adapter).load()

    return teams, players, matches


# ---- Basketball ----

def test_basketball_teams_charges() -> None:
    teams, _, _ = _charger("Basketball")
    assert len(teams) > 0, "Aucune equipe chargee"


def test_basketball_matchs_charges() -> None:
    _, _, matches = _charger("Basketball")
    assert len(matches) > 0, "Aucun match charge"


def test_basketball_match_structure() -> None:
    _, _, matches = _charger("Basketball")
    m = matches[0]
    assert len(m.participants) == 2
    assert isinstance(m.scores, dict)
    assert m.date_match is not None


# ---- Badminton ----

def test_badminton_teams_charges() -> None:
    teams, _, _ = _charger("Badminton")
    assert len(teams) > 0


def test_badminton_matchs_charges() -> None:
    _, _, matches = _charger("Badminton")
    assert len(matches) > 0


# ---- Echecs ----

def test_echecs_teams_charges() -> None:
    teams, _, _ = _charger("Echecs")
    assert len(teams) > 0


def test_echecs_matchs_charges() -> None:
    _, _, matches = _charger("Echecs")
    assert len(matches) > 0


# ---- Tennis ----

def test_tennis_teams_charges() -> None:
    teams, _, _ = _charger("Tennis")
    assert len(teams) > 0


def test_tennis_matchs_charges() -> None:
    _, _, matches = _charger("Tennis")
    assert len(matches) > 0


# ---- Volleyball ----

def test_volleyball_teams_charges() -> None:
    teams, _, _ = _charger("Volleyball")
    assert len(teams) > 0


def test_volleyball_matchs_charges() -> None:
    _, _, matches = _charger("Volleyball")
    assert len(matches) > 0


# ---- Starcraft 2 ----

def test_starcraft2_teams_charges() -> None:
    teams, _, _ = _charger("Starcraft 2")
    assert len(teams) > 0


def test_starcraft2_matchs_charges() -> None:
    _, _, matches = _charger("Starcraft 2")
    assert len(matches) > 0


# ---- League of Legends ----

def test_lol_teams_charges() -> None:
    teams, _, _ = _charger("League of Legends")
    assert len(teams) > 0


def test_lol_matchs_charges() -> None:
    _, _, matches = _charger("League of Legends")
    assert len(matches) > 0


# ---- Football (Ligues europeennes) ----

def test_football_eu_teams_charges() -> None:
    teams, _, _ = _charger("Football (Ligues europeennes)")
    assert len(teams) > 0


def test_football_eu_matchs_charges() -> None:
    _, _, matches = _charger("Football (Ligues europeennes)")
    assert len(matches) > 0


# ---- Football (Champions League) ----

def test_football_cl_teams_charges() -> None:
    teams, _, _ = _charger("Football (Champions League)")
    assert len(teams) > 0


def test_football_cl_matchs_charges() -> None:
    _, _, matches = _charger("Football (Champions League)")
    assert len(matches) > 0


# ---- CS2 ----

def test_cs2_teams_charges() -> None:
    teams, _, _ = _charger("CS2")
    assert len(teams) > 0


def test_cs2_matchs_charges() -> None:
    _, _, matches = _charger("CS2")
    assert len(matches) > 0


# ---- Tests de statistiques ----

def test_stats_podium_basketball() -> None:
    from Analysis.stats import podium
    _, _, matches = _charger("Basketball")
    top3 = podium(matches, n=3)
    assert len(top3) == 3
    # vérifie tri décroissant
    assert top3[0][1] >= top3[1][1] >= top3[2][1]


def test_stats_victoires_equipe_football_cl() -> None:
    from Analysis.stats import victoires_equipe
    _, _, matches = _charger("Football (Champions League)")
    nb = victoires_equipe(matches, "Real Madrid")
    assert nb > 0


def test_stats_matchs_joueur_badminton() -> None:
    from Analysis.stats import matchs_joueur
    _, _, matches = _charger("Badminton")
    # Yamaguchi Akane est dans le dataset
    trouves = matchs_joueur(matches, "Yamaguchi", "Akane")
    assert len(trouves) > 0


def test_stats_descriptives_football_cl() -> None:
    from Analysis.stats import stats_descriptives
    _, _, matches = _charger("Football (Champions League)")
    stats = stats_descriptives(matches, "Real Madrid")
    assert "erreur" not in stats
    assert stats["nb_matchs"] > 0
    assert stats["nb_victoires"] + stats["nb_defaites"] + stats["nb_nuls"] == stats["nb_matchs"]
    assert 0.0 <= stats["pct_victoires"] <= 100.0
