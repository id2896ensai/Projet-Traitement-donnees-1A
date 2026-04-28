from typing import List

from src.Model.team import Team
from src.Parsers.generic_loaders import GenericTeamLoader
from src.Parsers.Adapters.Basketball.BasketballTeamAdapter import BasketballTeamAdapter
from src.Parsers.Adapters.Football.FootballTeamAdapter import FootballTeamAdapter
from src.Parsers.Adapters.FootballCL.FootballCLTeamAdapter import FootballCLTeamAdapter
from src.Parsers.Adapters.Lol.LolTeamAdapter import LolTeamAdapter
from src.Parsers.Adapters.Volleyball.VolleyballTeamAdapter import VolleyballTeamAdapter
from src.Parsers.Adapters.CS2.CS2TeamAdapter import CS2TeamAdapter

# Sports individuels (chess, tennis, badminton, starcraft2) n'ont pas d'equipes.
_team_loaders_by_sport = {
    "basketball":       GenericTeamLoader("./data/basketball/team.csv", BasketballTeamAdapter()),
    "football":         GenericTeamLoader("./data/football_european_leagues/team.csv", FootballTeamAdapter()),
    "football_cl":      GenericTeamLoader("./data/football_champions_league/team.csv", FootballCLTeamAdapter()),
    "lol":              GenericTeamLoader("./data/league_of_legends/team.csv", LolTeamAdapter()),
    "cs2":              GenericTeamLoader("./data/counter_strike_2/team.csv", CS2TeamAdapter()),
    "volleyball_men":   GenericTeamLoader("./data/volleyball/country.csv", VolleyballTeamAdapter()),
    "volleyball_women": GenericTeamLoader("./data/volleyball/country.csv", VolleyballTeamAdapter()),
}

SUPPORTED_SPORTS = list(_team_loaders_by_sport.keys())


class TeamLoader:
    """Generic team loader — dispatches to the right sport-specific adapter."""

    def load_all_teams(self, sport_name: str) -> List[Team]:
        try:
            return _team_loaders_by_sport[sport_name].load()
        except KeyError:
            raise ValueError(
                f"Sport sans equipes ou non supporte : '{sport_name}'. "
                f"Disponibles : {SUPPORTED_SPORTS}"
            )
