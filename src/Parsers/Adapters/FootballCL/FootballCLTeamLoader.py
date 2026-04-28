from typing import List

import pandas as pd

from src.Model.team import Team
from src.Model.sports_catalogue import FOOTBALL_CL
from src.Parsers.Adapters.base_adapter import BaseTeamLoader


class FootballCLTeamLoader(BaseTeamLoader):
    """Loads teams from data/football_champions_league/team.csv.

    CSV columns:
        full_name     : str  - e.g. "Manchester City Football Club"
        short_name    : str  - e.g. "Manchester City"
        year_founded  : int
        country       : str  - e.g. "England"
        league        : str  - e.g. "Premier League"
        city          : str
    """

    def load_all_teams(self) -> List[Team]:
        """Load all Champions League teams from the CSV file.

        Returns:
            List[Team]: One Team object per row.

        Example mapping:
            Team(
                full_name=row["short_name"],   # shorter name for display
                sport=FOOTBALL_CL,
                country=row["country"],
                city=row["city"],
            )
        """
        raise NotImplementedError

    def load_teams_as_dict(self) -> dict:
        """Load teams indexed by short_name for fast lookup.

        Returns:
            dict: {short_name (str): Team}
        """
        return {team.full_name: team for team in self.load_all_teams()}
