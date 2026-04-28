from typing import List

import pandas as pd

from src.Model.team import Team
from src.Model.sports_catalogue import BASKETBALL
from src.Parsers.Adapters.base_adapter import BaseTeamLoader


class BasketballTeamLoader(BaseTeamLoader):
    """Loads teams from data/basketball/team.csv.

    CSV columns:
        id           : int  - unique team identifier (used in game.csv)
        full_name    : str  - e.g. "Atlanta Hawks"
        abbreviation : str  - e.g. "ATL"
        nickname     : str  - e.g. "Hawks"
        city         : str  - e.g. "Atlanta"
        state        : str  - e.g. "Atlanta"
    """

    def load_all_teams(self) -> List[Team]:
        """Load all NBA teams from the CSV file.

        Returns:
            List[Team]: 30 Team objects.
        """
        df = pd.read_csv(self.file_path)
        teams = []
        for _, row in df.iterrows():
            team = Team(
                full_name=str(row["full_name"]),
                sport=BASKETBALL,
                id=int(row["id"]),
                abbreviation=str(row["abbreviation"]),
                nickname=str(row["nickname"]),
                city=str(row["city"]),
                state=str(row["state"]),
            )
            teams.append(team)
        return teams

    def load_teams_as_dict(self) -> dict:
        """Load teams indexed by id for fast lookup in BasketballMatchLoader.

        Returns:
            dict: {team_id (int): Team}
        """
        return {team.id: team for team in self.load_all_teams()}
