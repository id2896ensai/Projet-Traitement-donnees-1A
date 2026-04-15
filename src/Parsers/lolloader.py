from baseloader import BaseLoader
from ..Model.sport import Sport
from ..Model.player import Player
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
  
    def playerloader(self):
        data = self.data["players"]

        parts = data['name'].strip().split()
        prenom = " ".join(parts[:-1])
        nom = parts[-1]

        data['id'] = None
        data['nom'] = nom
        data['prenom'] = prenom
        data['date_de_naissance'] = data['birthdate']
        data['pays_de_naissance'] = data['country_of_birth']
        data['sexe'] = None
        data['poids'] = None
        data['taille'] = None
        data['team'] = None

        """player = [
            Player(
                data['id'],
                data['pseudo'],
                data['nom'],
                data['prenom'],
                data['date_de_naissance'],
                data['pays_de_naissance'],
                data['sexe'],
                data['poids'],
                data['taille'],
                data['role'],
                data['team'],
            )
        ]
        for _, row in data.iterrows()
        ]"""
        return data[[
            "id",
            "pseudo",
            "nom",
            "prenom",
            "date_de_naissance",
            "pays_de_naissance",
            "sexe",
            "poids",
            "taille",
            "role",
            "team"
        ]]

    def teamloader(self):
        data = self.data["teams"]
        data['id'] = None
        data['team_api_id'] = None
        data['full_name'] = data['team']
        data['abbreviation'] = data['team_abbreviation']
        data['nickname'] = None
        data['city'] = None
        data['state'] = None
        data['country'] = data['location']
        data['nb_players'] = 0
        data['players'] = None
        data['sport'] = Sport("LeagueOfLegends", "e-sport", 8, "blablabla", True)

        """team = [
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
