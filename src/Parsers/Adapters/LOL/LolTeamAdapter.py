import pandas as pd
from src.Model.sport import Sport

LOL = Sport("LeagueOfLegends", "esport", 5, "Jeu de strategie en equipe 5v5", True)


class LolTeamAdapter:
    """
    Convertit une ligne de league_of_legends/team.csv en dict Team.

    Colonnes CSV : team, team_abbreviation, location, region

    L'equipe est indexee par abbreviation (ex: "TH", "RGE")
    pour etre retrouvee depuis les colonnes team_blue / team_red du CSV de matchs.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        abbrev = str(row["team_abbreviation"]).strip() if pd.notna(row.get("team_abbreviation")) else str(row["team"])[:10]
        return {
            "id":           abs(hash(str(row["team"]))) % (10 ** 7),
            "sport":        LOL,
            "players":      [],
            "full_name":    str(row["team"]),
            "abbreviation": abbrev,
            "country":      str(row["location"]) if pd.notna(row.get("location")) else None,
            "region":       str(row["region"]) if pd.notna(row.get("region")) else None,
        }
