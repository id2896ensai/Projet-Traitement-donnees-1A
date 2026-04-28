from typing import List

import pandas as pd

from src.Model.team import Team
from src.Parsers.Adapters.base_adapter import BaseTeamLoader


class FootballTeamLoader(BaseTeamLoader):
    """Loads teams from data/football_european_leagues/team.csv.

    CSV columns:
        id             : int
        team_api_id    : int  - unique identifier (used in match.csv as home/away team)
        team_long_name : str  - e.g. "KRC Genk"
        team_short_name: str  - e.g. "GEN"
    """

    def load_all_teams(self) -> List[Team]:
        """Load all football teams from the CSV file.

        Returns:
            List[Team]: One Team object per row.

        Example mapping:
            Team(
                id=row["team_api_id"],
                full_name=row["team_long_name"],
                abreviation=row["team_short_name"],
                ...
            )
        """
        raise NotImplementedError

    def load_teams_as_dict(self) -> dict:
        """Load teams indexed by team_api_id for fast lookup in FootballMatchLoader.

        Returns:
            dict: {team_api_id (int): Team}
        """
        return {team.id: team for team in self.load_all_teams()}
