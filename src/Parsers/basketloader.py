from baseloader import BaseLoader
from ..Model.team import Team
from ..Model.sport import Sport
import pandas as pd


class BasketLoader(BaseLoader):
    pass

    def __init__(self, filepath):
        super().__init__(filepath)

        self.files = {"players": "player.csv", "games": "game.csv", "teams": "team.csv"}

    def load_data(self):
        for name, file in self.files.items():
            path = self.filepath + "/" + file
            self.data[name] = pd.read_csv(path)
        return self.data

    def teamloader(self):
        data = self.data["teams"]
        data["team_api_id"] = None
        data["country"] = "USA"
        data["region"] = None
        data["nb_players"] = 0
        data["players"] = None
        data["sport"] = Sport("basketball", "ballon", 10, "blabla", True)

        """teams = [
            Team(
                data['id'],
                data['team_api_id'],
                data['full_name'],
                data['abbreviation'],
                data['nickname'],
                data['city'],
                data['state'],
                data['country'],
                data['region'],
                data['nb_players'],
                data['players'],
                data['sport']  
            )
            for _, row in data.iterrows()
        ]"""

        return data[
            [
                "id",
                "team_api_id",
                "full_name",
                "abbreviation",
                "nickname",
                "city",
                "state",
                "country",
                "region",
            ]
        ]
