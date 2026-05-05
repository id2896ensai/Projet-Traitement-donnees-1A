import datetime

import pandas as pd

from src.Model.sports_catalogue import TENNIS


class TennisPlayerAdapter:
    """Convertit une ligne ATP ou WTA player CSV en dict Player.

    Fonctionne pour atp_players_2024.csv et wta_players_2024.csv.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        # La date de naissance est un flottant au format AAAAMMJJ (ex: 19970420.0)
        dob = None
        dob_val = row.get("dob")
        if pd.notna(dob_val):
            dob_str = str(int(float(dob_val)))
            if len(dob_str) == 8:
                dob = datetime.date(int(dob_str[:4]), int(dob_str[4:6]), int(dob_str[6:8]))

        return {
            "id":                int(row["player_id"]),
            "nom":               str(row["name_last"]),
            "prenom":            str(row["name_first"]),
            "date_de_naissance": dob,
            "pays_de_naissance": str(row["ioc"]) if pd.notna(row.get("ioc")) else None,
            "taille":            str(int(float(row["height"]))) if pd.notna(row.get("height")) else None,
            "sport":             TENNIS,
        }
