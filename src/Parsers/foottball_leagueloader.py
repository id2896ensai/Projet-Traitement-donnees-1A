from baseloader import BaseLoader
from ..Model.sport import Sport
from ..Model.team import Team
import pandas as pd


class FootballLoader(BaseLoader):

    def __init__(self, filepath: str):
        super().__init__(filepath)

        self.files = {
            "country": "country.csv",
            "league": "league.csv",
            "matches": "match.csv",
            "players": "player.csv",
            "teams": "team.csv",
        }

    def load_data(self):
        for name, file in self.files.items():
            path = self.filepath + "/" + file
            self.data[name] = pd.read_csv(path)
        return self.data

    def team_players(self, team_id: int) -> pd.DataFrame:
        """
        Retourne un DataFrame des joueurs associés à une équipe via les matchs.
        """
        matches_df = self.data.get("matches")
        players_df = self.data.get("players")

        if matches_df is None or players_df is None:
            raise ValueError(
                "Les données 'matches' et 'players' doivent être chargées."
            )

        # Colonnes des joueurs dans match.csv (home + away)
        player_columns = [
            col
            for col in matches_df.columns
            if "home_player" in col and col[-1].isdigit()
        ] + [
            col
            for col in matches_df.columns
            if "away_player" in col and col[-1].isdigit()
        ]

        # Filtrer les matchs où l'équipe apparaît (domicile ou extérieur)
        team_matches = matches_df[
            (matches_df["home_team_api_id"] == team_id)
            | (matches_df["away_team_api_id"] == team_id)
        ]

        # Récupérer tous les player_api_id uniques
        player_ids = set()
        for col in player_columns:
            ids = team_matches[col].dropna().astype(int).tolist()
            player_ids.update(ids)

        # Filtrer et renommer les colonnes selon les attributs de Player
        result_df = players_df[players_df["player_api_id"].isin(player_ids)].copy()

        result_df[["prenom", "nom"]] = result_df["player_name"].str.split(
            " ", n=1, expand=True
        )

        result_df = result_df.rename(
            columns={
                "birthday": "date_de_naissance",
                "weight (kg)": "poids",
                "height (cm)": "taille",
            }
        )

        result_df = result_df[
            ["id", "nom", "prenom", "date_de_naissance", "poids", "taille"]
        ]

        return result_df.reset_index(drop=True)
