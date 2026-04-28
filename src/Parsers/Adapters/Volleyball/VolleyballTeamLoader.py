from typing import List

import pandas as pd

from src.Model.team import Team
from src.Parsers.Adapters.base_adapter import BaseTeamLoader


class VolleyballTeamLoader(BaseTeamLoader):
    """Loads national teams from data/volleyball/country.csv.

    In volleyball (JO 2024), teams are countries.

    CSV columns:
        code         : str  - IOC country code, e.g. "GER" (used in match CSV)
        country      : str  - short name, e.g. "Germany"
        country_long : str  - full name, e.g. "Germany"
    """

    def load_all_teams(self) -> List[Team]:
        """Load all volleyball national teams from the country CSV.

        Returns:
            List[Team]: One Team object per country row.

        Example mapping:
            Team(
                id=row["code"],
                full_name=row["country_long"],
                abreviation=row["code"],
                ...
            )
        """
        raise NotImplementedError

    def load_teams_as_dict(self) -> dict:
        """Load teams indexed by country code for fast lookup in VolleyballMatchLoader.

        Returns:
            dict: {country_code (str): Team}
        """
        return {team.id: team for team in self.load_all_teams()}
