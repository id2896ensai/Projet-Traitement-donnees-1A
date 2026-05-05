import pandas as pd

from src.Model.sports_catalogue import BADMINTON


class BadmintonPlayerAdapter:
    """Convertit une ligne de badminton/player.csv en dict Player."""

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        # On stocke le nom complet dans pseudo pour que full_name retourne le nom exact
        return {
            "pseudo":            str(row["name"]).strip(),
            "pays_de_naissance": str(row["country"]) if pd.notna(row.get("country")) else None,
            "sport":             BADMINTON,
        }
