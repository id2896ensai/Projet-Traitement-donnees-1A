from typing import List

import pandas as pd

from src.Model.team import Team
from src.Parsers.Adapters.base_adapter import BaseTeamLoader


class LolTeamLoader(BaseTeamLoader):
    """Loads teams from data/league_of_legends/team.csv.

    CSV columns:
        team              : str  - full team name, e.g. "Team Heretics"
        team_abbreviation : str  - e.g. "TH"
        location          : str  - e.g. "Spain"
        region            : str  - e.g. "EMEA"
    """

    def load_all_teams(self) -> List[Team]:
        """Load all LoL esport teams from the CSV file.

        Returns:
            List[Team]: One Team object per row.

        Example mapping:
            Team(
                full_name=row["team"],
                abreviation=row["team_abbreviation"],
                ...
            )
        """
        raise NotImplementedError

    def load_teams_as_dict(self) -> dict:
        """Load teams indexed by full name for fast lookup in LolMatchLoader.

        Returns:
            dict: {team_name (str): Team}
        """
        return {team.full_name: team for team in self.load_all_teams()}
