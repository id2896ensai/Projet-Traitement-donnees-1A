from typing import List

from src.Model.player import Player
from src.Parsers.generic_loaders import GenericPlayerLoader
from src.Parsers.Adapters.Basketball.BasketballPlayerAdapter import BasketballPlayerAdapter
from src.Parsers.Adapters.Football.FootballPlayerAdapter import FootballPlayerAdapter
from src.Parsers.Adapters.Lol.LolPlayerAdapter import LolPlayerAdapter
from src.Parsers.Adapters.Tennis.TennisPlayerAdapter import TennisPlayerAdapter
from src.Parsers.Adapters.Volleyball.VolleyballPlayerAdapter import VolleyballPlayerAdapter
from src.Parsers.Adapters.Chess.ChessPlayerAdapter import ChessPlayerAdapter
from src.Parsers.Adapters.Badminton.BadmintonPlayerAdapter import BadmintonPlayerAdapter
from src.Parsers.Adapters.Starcraft2.Starcraft2PlayerAdapter import Starcraft2PlayerAdapter
from src.Parsers.Adapters.CS2.CS2PlayerAdapter import CS2PlayerAdapter

_player_loaders_by_sport = {
    "basketball":       GenericPlayerLoader("./data/basketball/player.csv", BasketballPlayerAdapter()),
    "football":         GenericPlayerLoader("./data/football_european_leagues/player.csv", FootballPlayerAdapter()),
    "lol":              GenericPlayerLoader("./data/league_of_legends/player.csv", LolPlayerAdapter()),
    "tennis_atp":       GenericPlayerLoader("./data/tennis/atp_players_2024.csv", TennisPlayerAdapter()),
    "tennis_wta":       GenericPlayerLoader("./data/tennis/wta_players_2024.csv", TennisPlayerAdapter()),
    "volleyball_men":   GenericPlayerLoader("./data/volleyball/player_men.csv", VolleyballPlayerAdapter()),
    "volleyball_women": GenericPlayerLoader("./data/volleyball/player_women.csv", VolleyballPlayerAdapter()),
    "chess":            GenericPlayerLoader("./data/chess/player.csv", ChessPlayerAdapter()),
    "badminton":        GenericPlayerLoader("./data/badminton/player.csv", BadmintonPlayerAdapter()),
    "starcraft2":       GenericPlayerLoader("./data/starcraft_2/player.csv", Starcraft2PlayerAdapter()),
    "cs2":              GenericPlayerLoader("./data/counter_strike_2/player.csv", CS2PlayerAdapter()),
}

SUPPORTED_SPORTS = list(_player_loaders_by_sport.keys())


class PlayerLoader:
    """Generic player loader — dispatches to the right sport-specific adapter."""

    def load_all_players(self, sport_name: str) -> List[Player]:
        try:
            return _player_loaders_by_sport[sport_name].load()
        except KeyError:
            raise ValueError(
                f"Sport non supporte : '{sport_name}'. "
                f"Disponibles : {SUPPORTED_SPORTS}"
            )
