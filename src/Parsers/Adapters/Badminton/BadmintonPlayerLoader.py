from typing import List

import pandas as pd

from src.Model.player import Player
from src.Model.sports_catalogue import BADMINTON
from src.Parsers.Adapters.base_adapter import BasePlayerLoader


class BadmintonPlayerLoader(BasePlayerLoader):
    """Loads players from data/badminton/player.csv.

    Badminton is an INDIVIDUAL sport.

    CSV columns:
        name      : str  - full name, e.g. "Akane Yamaguchi"
        country   : str  - e.g. "Japan"
        continent : str  - e.g. "Asia"
    """

    def load_all_players(self) -> List[Player]:
        """Load all badminton players from the CSV file.

        Returns:
            List[Player]: One Player object per row.

        Example mapping:
            parts = row["name"].split(" ", 1)
            Player(
                prenom=parts[0],
                nom=parts[1] if len(parts) > 1 else "",
                pays_de_naissance=row["country"],
                sport=BADMINTON,
            )
        """
        raise NotImplementedError
