import pandas as pd
from Model.sport import Sport

LOL = Sport("League of Legends", "esport", 10, "MOBA 5v5", True)


class LolTeamAdapter:
    """
    Convertit une ligne de league_of_legends/team.csv en dict Team.

    Colonnes CSV : team, team_abbreviation, location, region

    L'equipe est indexee par abbreviation (ex: "TH", "RGE")
    pour etre retrouvee depuis les colonnes team_blue / team_red du CSV de matchs.
    """

    _counter = 0

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        LolTeamAdapter._counter += 1
        return {
            "id":           LolTeamAdapter._counter,
            "sport":        LOL,
            "players":      [],
            "full_name":    str(row["team"]),
            "abbreviation": str(row["team_abbreviation"]) if pd.notna(row.get("team_abbreviation")) else str(row["team"])[:10],
            "city":         str(row["location"]) if pd.notna(row.get("location")) else None,
            "region":       str(row["region"]) if pd.notna(row.get("region")) else None,
        }
