from typing import List

import pandas as pd

from src.Model.player import Player
from src.Parsers.Adapters.base_adapter import BasePlayerLoader


class VolleyballPlayerLoader(BasePlayerLoader):
    """Loads players from men's or women's volleyball player CSV.

    Works for both:
    - data/volleyball/player_men.csv
    - data/volleyball/player_women.csv

    CSV columns:
        name         : str  - full name in UPPERCASE, e.g. "FROMM Christian"
        country_code : str  - IOC country code, e.g. "GER" (references country.csv)
        height       : int  - in cm
        birth_date   : str  - format YYYY-MM-DD
        birth_place  : str  - city (can be empty)
        nickname     : str  - (can be empty)
    """

    def load_all_players(self) -> List[Player]:
        """Load all volleyball players from the CSV file.

        Returns:
            List[Player]: One Player object per row.

        Tip:
            Names are "LASTNAME Firstname" — split on first space.

        Example mapping:
            Player(
                nom=...,           # split row["name"]
                prenom=...,        # split row["name"]
                pays_de_naissance=row["country_code"],
                date_de_naissance=...,  # parse "YYYY-MM-DD"
                taille=row["height"],
            )
        """
        raise NotImplementedError
