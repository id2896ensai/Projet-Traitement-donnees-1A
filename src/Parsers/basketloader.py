from baseloader import BaseLoader
from ..Model.team import Team
from ..Model.sport import Sport
from ..Model.player import Player
import pandas as pd

class BasketLoader(BaseLoader):
    pass

    def __init__(self, filepath):
        super().__init__(filepath)

        self.files = {
            "players" : "player.csv",
            "games" : "game.csv",
            "teams" : "team.csv"
        }

    def load_data(self):
        for name,  file in self.files.items():
            path = self.filepath + "/" + file
            self.data[name] = pd.read_csv(path)
        return self.data

    def playerloader(self):
        data = self.data["players"]
        data['id'] = data['person_id']
        data['pseudo'] = data["jersey"]
        data['nom'] = data['first_name']
        data['prenom'] = data['last_name']
        data['date_de_naissance'] = data['birthdate']
        data['pays_de_naissance'] = None
        data['sexe'] = 'M'
        data['poids'] = data['weight']
        data['taille'] = data['height']
        data['role'] = data["position"]
        data['team'] = data['team_id']


    def teamloader(self):
        data = self.data["teams"]
        data['team_api_id'] = None
        data['country'] = "USA"
        data['region'] = None
        data['nb_players'] = 0
        data['players'] = [
            Player(
                data['id'],
                data['pseudo'],
                data['nom'],
                data['prenom'],
                data['date_de_naissance'],
                data['sexe'],
                data['poids'],
                data['taille'],
                data['role'],
                data['team']
            )
            for _, row in data.iterrows()
        ]
        data['sport'] = Sport('basketball', 'ballon', 10, 'blabla', True)

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
            "nb_players",
            "sport"
        ]]

    def matchloader(self):
        data = self.data['games']