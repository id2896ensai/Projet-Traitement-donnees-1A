from typing import List

import pandas as pd

from src.Model.player import Player
from src.Model.sports_catalogue import CS2
from src.Parsers.Adapters.base_adapter import BasePlayerLoader


class CS2PlayerLoader(BasePlayerLoader):
    """Loads players from data/counter_strike_2/player.csv.

    CSV columns:
        pseudo       : str  - in-game name, e.g. "yuurih"
        name         : str  - real full name
        nationality  : str  - e.g. "Brazil"
        birthdate    : str  - format YYYY-MM-DD
        role         : str  - "rifler", "lurker", "AWPer", "IGL", etc.
        team         : str  - team name (references team.csv)
    """

    def load_all_players(self) -> List[Player]:
        """Load all CS2 players from the CSV file.

        Returns:
            List[Player]: One Player object per row.
        """
        raise NotImplementedError
