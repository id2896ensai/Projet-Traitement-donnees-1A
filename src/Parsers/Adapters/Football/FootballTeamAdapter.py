import pandas as pd

from src.Model.sports_catalogue import FOOTBALL


class FootballTeamAdapter:
    """Convertit une ligne de football_european_leagues/team.csv en dict Team."""

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        return {
            # team_api_id est l'identifiant utilise dans le CSV des matchs
            "id":           int(row["team_api_id"]),
            "full_name":    str(row["team_long_name"]),
            "abbreviation": str(row["team_short_name"]),
            "sport":        FOOTBALL,
        }
