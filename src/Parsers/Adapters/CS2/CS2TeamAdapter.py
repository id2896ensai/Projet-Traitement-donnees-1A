import pandas as pd

from src.Model.sports_catalogue import CS2


class CS2TeamAdapter:
    """Convertit une ligne de counter_strike_2/team.csv en dict Team."""

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        return {
            "full_name":    str(row["team"]),
            "abbreviation": str(row["team_abbreviation"]) if pd.notna(row.get("team_abbreviation")) else None,
            "country":      str(row["location"]) if pd.notna(row.get("location")) else None,
            "region":       str(row["region"]) if pd.notna(row.get("region")) else None,
            "sport":        CS2,
        }
