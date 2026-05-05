import datetime

import pandas as pd

from src.Model.sports_catalogue import VOLLEYBALL


class VolleyballPlayerAdapter:
    """Convertit une ligne volleyball player CSV en dict Player.

    Fonctionne pour player_men.csv et player_women.csv.
    Le nom est au format "NOM Prenom" (nom en majuscules).
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        # On stocke le nom complet dans pseudo pour conserver l'affichage exact
        nom_complet = str(row["name"]).strip()

        naissance = row.get("birth_date")
        dob = datetime.date.fromisoformat(str(naissance)) if pd.notna(naissance) else None

        return {
            "pseudo":            nom_complet,
            "pays_de_naissance": str(row["country_code"]) if pd.notna(row.get("country_code")) else None,
            "taille":            str(int(float(row["height"]))) if pd.notna(row.get("height")) else None,
            "date_de_naissance": dob,
            "sport":             VOLLEYBALL,
        }
