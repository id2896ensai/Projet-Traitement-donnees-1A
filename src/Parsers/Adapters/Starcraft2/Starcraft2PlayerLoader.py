from typing import List

import pandas as pd

from src.Model.player import Player
from src.Model.sports_catalogue import STARCRAFT2
from src.Parsers.Adapters.base_adapter import BasePlayerLoader


class Starcraft2PlayerLoader(BasePlayerLoader):
    """Loads players from data/starcraft_2/player.csv.

    Starcraft 2 is an INDIVIDUAL esport.

    CSV columns:
        pseudo      : str  - in-game name, e.g. "Zest"
        name        : str  - real full name, e.g. "Joo Sung-wook"
        nationality : str  - e.g. "South Korea"
        birthdate   : str  - format YYYY-MM-DD
        race        : str  - "Protoss", "Terran", or "Zerg"
        team        : str  - team name (optional affiliation)
    """

    def load_all_players(self) -> List[Player]:
        """Load all Starcraft 2 players from the CSV file.

        Returns:
            List[Player]: One Player object per row.

        Example mapping:
            parts = row["name"].split(" ", 1)
            Player(
                id=row["pseudo"],
                pseudo=row["pseudo"],
                prenom=parts[0],
                nom=parts[1] if len(parts) > 1 else "",
                pays_de_naissance=row["nationality"],
                date_de_naissance=...,  # parse "YYYY-MM-DD"
                role=row["race"],
                sport=STARCRAFT2,
            )
        """
        raise NotImplementedError
