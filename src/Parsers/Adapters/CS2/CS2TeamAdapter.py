import pandas as pd
from Model.sport import Sport

CS2 = Sport("Counter-Strike 2", "esport", 10, "FPS tactique 5v5", True)


class CS2TeamAdapter:
    """
    Convertit une ligne de counter_strike_2/team.csv en dict Team.

    Colonnes CSV : team, team_abbreviation, location, region
    """

    _counter = 0

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        CS2TeamAdapter._counter += 1
        return {
            "id":           CS2TeamAdapter._counter,
            "sport":        CS2,
            "players":      [],
            "full_name":    str(row["team"]),
            "abbreviation": str(row["team_abbreviation"]) if pd.notna(row.get("team_abbreviation")) else None,
            "country":      str(row["location"]) if pd.notna(row.get("location")) else None,
            "region":       str(row["region"]) if pd.notna(row.get("region")) else None,
        }
