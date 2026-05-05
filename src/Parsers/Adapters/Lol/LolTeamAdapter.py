import pandas as pd

from src.Model.sports_catalogue import LOL


class LolTeamAdapter:
    """Convertit une ligne de league_of_legends/team.csv en dict Team."""

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        return {
            "full_name":    str(row["team"]),
            "abbreviation": str(row["team_abbreviation"]),
            "city":         str(row["location"]) if pd.notna(row.get("location")) else None,
            "region":       str(row["region"]) if pd.notna(row.get("region")) else None,
            "sport":        LOL,
        }
