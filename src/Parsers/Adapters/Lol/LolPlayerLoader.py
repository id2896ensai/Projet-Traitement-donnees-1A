from typing import List

import pandas as pd

from src.Model.player import Player
from src.Parsers.Adapters.base_adapter import BasePlayerLoader


class LolPlayerLoader(BasePlayerLoader):
    """Loads players from data/league_of_legends/player.csv.

    CSV columns:
        pseudo           : str  - in-game name, e.g. "Carlsen"
        name             : str  - real full name, e.g. "Carl Ulsted Carlsen"
        country_of_birth : str  - e.g. "Denmark"
        birthdate        : str  - format YYYY-MM-DD
        role             : str  - "top", "jungle", "mid", "bot", "sup"
        team             : str  - team name (references team.csv)
    """

    def load_all_players(self) -> List[Player]:
        """Load all LoL pro players from the CSV file.

        Returns:
            List[Player]: One Player object per row.

        Example mapping:
            Player(
                id=row["pseudo"],          # pseudo as unique id
                pseudo=row["pseudo"],
                nom=...,                   # split row["name"]
                prenom=...,                # split row["name"]
                pays_de_naissance=row["country_of_birth"],
                date_de_naissance=...,     # parse "YYYY-MM-DD"
                role=row["role"],
            )
        """
        raise NotImplementedError
