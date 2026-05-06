import datetime
import pandas as pd
from src.Model.sport import Sport

VOLLEYBALL = Sport("Volleyball", "ballon", 6, "Sport collectif avec filet", True)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class VolleyballPlayerAdapter:
    """
    Convertit une ligne de volleyball/player_men.csv en dict Player.

    Colonnes CSV : name, country_code, height, birth_date, birth_place, nickname

    Le nom complet est stocke dans pseudo car les matchs referencent
    les joueurs par leur nom d'affichage.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        pseudo = str(row["name"]).strip()
        parties = pseudo.split(" ", 1)
        prenom = parties[0]
        nom = parties[1] if len(parties) == 2 else "Inconnu"

        try:
            dob = datetime.date.fromisoformat(str(row["birth_date"]))
        except (ValueError, TypeError):
            dob = _DATE_INCONNUE

        return {
            "id":                abs(hash(pseudo)) % (10 ** 7),
            "nom":               nom,
            "prenom":            prenom,
            "date_de_naissance": dob,
            "pseudo":            pseudo,
            "pays_de_naissance": str(row["country_code"]) if pd.notna(row.get("country_code")) else None,
            "sexe":              None,
            "poids":             0.0,
            "taille":            float(row["height"]) if pd.notna(row.get("height")) else 0.0,
            "role":              None,
            "team":              None,
            "sport":             VOLLEYBALL,
        }
