import pandas as pd
from src.Model.sport import Sport

LOL = Sport("League of Legends", "esport", 10, "MOBA 5v5", True)


class LolTeamAdapter:
    """
    Convertit une ligne de league_of_legends/team.csv en dict Team.

    Colonnes CSV : team, team_abbreviation, location, region

    Pourquoi id généré par enumerate ?
    -----------------------------------
    Le CSV LoL n'a pas de colonne id numérique. On génère un id séquentiel
    via le loader (voir LolTeamLoader ou load_as_dict("abbreviation")).
    Ici on met id=0 comme placeholder ; en pratique on indexe par abbreviation.
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
            "abbreviation": str(row["team_abbreviation"]),
            "city":         str(row["location"]) if pd.notna(row.get("location")) else None,
            "region":       str(row["region"]) if pd.notna(row.get("region")) else None,
        }
