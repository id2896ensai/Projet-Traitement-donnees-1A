from typing import List

import pandas as pd

from src.Model.player import Player
from src.Model.sports_catalogue import CHESS
from src.Parsers.Adapters.base_adapter import BasePlayerLoader


class ChessPlayerLoader(BasePlayerLoader):
    """Loads players from data/chess/player.csv.

    CSV columns:
        name           : str   - full name, format "Lastname, Firstname"
        fide_id        : int   - unique FIDE identifier
        birth_year     : int
        gender         : str   - "Male" / "Female"
        federation     : str   - country name, e.g. "France"
        fide_title     : str   - "Grandmaster", "International Master", etc.
        rating_standard: int
        rating_rapid   : int
        rating_blitz   : int
    """

    def load_all_players(self) -> List[Player]:
        """Load all chess players from the CSV file.

        Returns:
            List[Player]: One Player object per row.

        Tip:
            Names are "Lastname, Firstname" — split on ", ".

        Example mapping:
            parts = row["name"].split(", ", 1)
            Player(
                id=row["fide_id"],
                nom=parts[0],
                prenom=parts[1] if len(parts) > 1 else "",
                pays_de_naissance=row["federation"],
                sexe=row["gender"],
                sport=CHESS,
            )
        """
        raise NotImplementedError
