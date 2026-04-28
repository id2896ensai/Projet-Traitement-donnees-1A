import datetime
from typing import List

from src.Model.match import Match
from src.Parsers.Adapters.Basketball.BasketballMatchLoader import BasketballMatchLoader
from src.Parsers.Adapters.Football.FootballMatchLoader import FootballMatchLoader
from src.Parsers.Adapters.FootballCL.FootballCLMatchLoader import FootballCLMatchLoader
from src.Parsers.Adapters.Lol.LolMatchLoader import LolMatchLoader
from src.Parsers.Adapters.Tennis.TennisMatchLoader import TennisMatchLoader
from src.Parsers.Adapters.Volleyball.VolleyballMatchLoader import VolleyballMatchLoader
from src.Parsers.Adapters.Chess.ChessMatchLoader import ChessMatchLoader
from src.Parsers.Adapters.Badminton.BadmintonMatchLoader import BadmintonMatchLoader
from src.Parsers.Adapters.Starcraft2.Starcraft2MatchLoader import Starcraft2MatchLoader
from src.Parsers.Adapters.CS2.CS2MatchLoader import CS2MatchLoader

# Factories — le loader n'est cree qu'au moment ou le sport est demande.
# Cela evite de lire tous les CSV au demarrage et permet de gerer les
# adaptateurs non encore implementes (NotImplementedError remonte proprement).
_match_loader_factories = {
    "basketball":      lambda: BasketballMatchLoader("./data/basketball/game.csv", "./data/basketball/team.csv"),
    "football":        lambda: FootballMatchLoader("./data/football_european_leagues/match.csv", "./data/football_european_leagues/team.csv"),
    "football_cl":     lambda: FootballCLMatchLoader("./data/football_champions_league/match.csv", "./data/football_champions_league/team.csv"),
    "lol":             lambda: LolMatchLoader("./data/league_of_legends/match.csv", "./data/league_of_legends/team.csv"),
    "tennis_atp":      lambda: TennisMatchLoader("./data/tennis/atp_matches_2024.csv", "./data/tennis/atp_players_2024.csv"),
    "tennis_wta":      lambda: TennisMatchLoader("./data/tennis/wta_matches_2024.csv", "./data/tennis/wta_players_2024.csv"),
    "volleyball_men":  lambda: VolleyballMatchLoader("./data/volleyball/match_men.csv", "./data/volleyball/country.csv"),
    "volleyball_women":lambda: VolleyballMatchLoader("./data/volleyball/match_women.csv", "./data/volleyball/country.csv"),
    "chess":           lambda: ChessMatchLoader("./data/chess/match.csv", "./data/chess/player.csv"),
    "badminton":       lambda: BadmintonMatchLoader("./data/badminton/match.csv", "./data/badminton/player.csv"),
    "starcraft2":      lambda: Starcraft2MatchLoader("./data/starcraft_2/match.csv", "./data/starcraft_2/player.csv"),
    "cs2":             lambda: CS2MatchLoader("./data/counter_strike_2/match.csv", "./data/counter_strike_2/team.csv"),
}

SUPPORTED_SPORTS = list(_match_loader_factories.keys())


class MatchLoader:
    """Generic match loader — dispatches to the right sport-specific adapter."""

    def load_all_matches(self, sport_name: str) -> List[Match]:
        try:
            return _match_loader_factories[sport_name]().load()
        except KeyError:
            raise ValueError(
                f"Sport non supporte : '{sport_name}'. "
                f"Disponibles : {SUPPORTED_SPORTS}"
            )

    def load_matches_by_date(self, sport_name: str, date: datetime.date) -> List[Match]:
        all_matches = self.load_all_matches(sport_name)
        return [m for m in all_matches if m.date_match == date]
