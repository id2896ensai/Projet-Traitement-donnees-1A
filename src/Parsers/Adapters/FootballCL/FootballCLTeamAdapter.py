import pandas as pd

from src.Model.sports_catalogue import FOOTBALL_CL


class FootballCLTeamAdapter:
    """Convertit une ligne de football_champions_league/team.csv en dict Team.

    Le short_name est utilise comme full_name car c'est ce nom qui apparait
    dans le CSV des matchs (ex: "Manchester City" et non "Manchester City Football Club").
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        return {
            "full_name": str(row["short_name"]),
            "nickname":  str(row["full_name"]),
            "country":   str(row["country"]) if pd.notna(row.get("country")) else None,
            "city":      str(row["city"]) if pd.notna(row.get("city")) else None,
            "sport":     FOOTBALL_CL,
        }
