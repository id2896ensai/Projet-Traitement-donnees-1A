import pandas as pd
from ..Model.team import Team
from ..Model.team import Sport


class BasketballTeamLoader:
    def load_teams(self):
        teams = []
        df = pd.read_csv(
            "Projet_Traitement-donnees-1A/data/basketball/team.csv", sep=","
        )
        for index, row in df.iterrows():
            team = Team(
                id=df[index, "id"],
                team_api_id=None,
                full_name=df[index, "full_name"],
                abbreviation=df[index, "abreviation"],
                nickname=df[index, "nickname"],
                city=df[index, "city"],
                state=df[index, "state"],
                country=None,
                region=None,
                nb_players=10,
                players=list[None],
                sport=Sport("basketball", "ballon", 10, "blabla", True),
            )
            teams.append(team)
            return teams
