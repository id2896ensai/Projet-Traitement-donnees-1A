import datetime
import pandas as pd
from Model.sport import Sport

CS2 = Sport("Counter-Strike 2", "esport", 10, "FPS tactique 5v5", True)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class CS2PlayerAdapter:
    """
    Convertit une ligne de counter_strike_2/player.csv en dict Player.

    Colonnes CSV : pseudo, name, birthdate, nationality, role
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        nom_complet = str(row["name"]).strip()
        parties = nom_complet.split(" ", 1)
        prenom = parties[0]
        nom = parties[1] if len(parties) == 2 else "Inconnu"

        try:
            dob = datetime.date.fromisoformat(str(row["birthdate"]))
        except (ValueError, TypeError):
            dob = _DATE_INCONNUE

        return {
            "id":                abs(hash(str(row["pseudo"]))) % (10**7),
            "nom":               nom,
            "prenom":            prenom,
            "date_de_naissance": dob,
            "pseudo":            str(row["pseudo"]),
            "pays_de_naissance": str(row["nationality"]) if pd.notna(row.get("nationality")) else None,
            "sexe":              None,
            "poids":             0.0,
            "taille":            0.0,
            "role":              str(row["role"]) if pd.notna(row.get("role")) else None,
            "team":              None,
            "sport":             CS2,
        }
