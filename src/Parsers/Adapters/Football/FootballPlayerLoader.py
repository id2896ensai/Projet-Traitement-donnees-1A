from typing import List

import pandas as pd

from src.Model.player import Player
from src.Parsers.Adapters.base_adapter import BasePlayerLoader


class FootballPlayerLoader(BasePlayerLoader):
    """Loads players from data/football_european_leagues/player.csv.

    CSV columns:
        id             : int
        player_api_id  : int  - unique identifier (used in match.csv lineups)
        player_name    : str  - full name, e.g. "Aaron Cresswell"
        birthday       : str  - format YYYY-MM-DD
        weight (kg)    : float
        height (cm)    : float
    """

    def load_all_players(self) -> List[Player]:
        """Load all football players from the CSV file.

        Returns:
            List[Player]: One Player object per row.

        Example mapping:
            Player(
                id=row["player_api_id"],
                nom=...,          # split row["player_name"]
                prenom=...,       # split row["player_name"]
                date_de_naissance=...,  # parse "YYYY-MM-DD"
                poids=row["weight (kg)"],
                taille=row["height (cm)"],
            )
        """
        raise NotImplementedError
