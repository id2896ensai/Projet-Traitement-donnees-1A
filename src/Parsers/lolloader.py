from baseloader import BaseLoader
from ..Model.sport import Sport
from ..Model.team import Team
import pandas as pd


class LolLoader(BaseLoader):
    pass

    def __init__(self, filepath):
        super().__init__(filepath)

        self.files = {
            "coachs": "coach.csv",
            "matchs": "match.csv",
            "players": "player.csv",
            "teams": "team.csv"
        }

    def load_data(self):
        for name,  file in self.files.items():
            path = self.filepath + "/" + file
            self.data[name] = pd.read_csv(path)
        return self.data

    def load_team(self):
        data = self.data["teams"]
        data['id'] = None
        data['team_api_id'] = None
        data['nickname'] = None
        data['city'] = None
        data['state'] = None
        data['nb_players'] = 0
        data['players'] = None
        data['sport'] = Sport("LeagueOfLegends", "e-sport", 8, "blablabla", True)

        """team = [
            Team(
                data['id'],
                data['team_api_id'],
                data['team'],
                data['team_abbreviation'],
                data['nickname'],
                data['city'],
                data['state'],
                data['location'],
                data['region'],
                data['nb_players'],
                data['players'],
                data['sport']
            )
        ]
        for _, row in data.iterrows()
        ]"""

        return data[[
            "id",
            "team_api_id",
            "full_name",
            "abbreviation",
            "nickname",
            "city",
            "state",
            "country",
            "region",
        ]]
