from typing import List

import pandas as pd

from src.Model.team import Team
from src.Model.sports_catalogue import CS2
from src.Parsers.Adapters.base_adapter import BaseTeamLoader


class CS2TeamLoader(BaseTeamLoader):
    """Loads teams from data/counter_strike_2/team.csv.

    CSV columns:
        team              : str  - full name, e.g. "FURIA"
        team_abbreviation : str  - e.g. "FURIA"
        location          : str  - e.g. "Brazil"
        region            : str  - e.g. "South America"
    """

    def load_all_teams(self) -> List[Team]:
        """Load all CS2 teams from the CSV file.

        Returns:
            List[Team]: One Team object per row.
        """
        raise NotImplementedError

    def load_teams_as_dict(self) -> dict:
        """Load teams indexed by full name for fast lookup.

        Returns:
            dict: {team_name (str): Team}
        """
        return {team.full_name: team for team in self.load_all_teams()}
