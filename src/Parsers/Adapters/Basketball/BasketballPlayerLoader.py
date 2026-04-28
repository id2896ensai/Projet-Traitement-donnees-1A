from typing import List

import pandas as pd

from src.Model.player import Player
from src.Parsers.Adapters.base_adapter import BasePlayerLoader


class BasketballPlayerLoader(BasePlayerLoader):
    """Loads players from data/basketball/player.csv.

    CSV columns:
        person_id   : int   - unique player identifier
        first_name  : str
        last_name   : str
        birthdate   : str   - format YYYY-MM-DD (e.g. "1999-09-19")
        height      : str   - format feet-inches (e.g. "6-8")
        weight      : int   - in pounds
        jersey      : int
        position    : str   - e.g. "Forward", "Center", "Guard"
        team_id     : int   - references basketball/team.csv
    """

    def load_all_players(self) -> List[Player]:
        """Load all NBA players from the CSV file.

        Returns:
            List[Player]: One Player object per row.

        Example mapping:
            Player(
                id=row["person_id"],
                nom=row["last_name"],
                prenom=row["first_name"],
                date_de_naissance=...,   # parse "YYYY-MM-DD"
                poids=row["weight"],
                taille=row["height"],
                ...
            )
        """
        raise NotImplementedError
