from typing import List

import pandas as pd

from src.Model.player import Player
from src.Parsers.Adapters.base_adapter import BasePlayerLoader


class TennisPlayerLoader(BasePlayerLoader):
    """Loads players from ATP or WTA CSV files.

    Works for both:
    - data/tennis/atp_players_2024.csv
    - data/tennis/wta_players_2024.csv

    CSV columns:
        player_id  : int   - unique identifier (used in match CSV as winner_id / loser_id)
        name_first : str   - e.g. "Alexander"
        name_last  : str   - e.g. "Zverev"
        hand       : str   - "R" (right), "L" (left), "U" (unknown)
        dob        : float - date of birth as YYYYMMDD float (e.g. 19970420.0), can be NaN
        ioc        : str   - country code (IOC), e.g. "GER"
        height     : float - in cm, can be NaN
    """

    def load_all_players(self) -> List[Player]:
        """Load all tennis players from the CSV file.

        Returns:
            List[Player]: One Player object per row.

        Tip:
            dob can be NaN — use pandas isna() to handle missing values.
            Parse dob with: datetime.datetime.strptime(f"{row['dob']:.0f}", "%Y%m%d").date()

        Example mapping:
            Player(
                id=row["player_id"],
                nom=row["name_last"],
                prenom=row["name_first"],
                pays_de_naissance=row["ioc"],
                date_de_naissance=...,  # handle NaN
                taille=int(row["height"]) if not isnan else None,
            )
        """
        raise NotImplementedError

    def load_players_as_dict(self) -> dict:
        """Load players indexed by player_id for fast lookup in TennisMatchLoader.

        Returns:
            dict: {player_id (int): Player}
        """
        return {player.id: player for player in self.load_all_players()}
