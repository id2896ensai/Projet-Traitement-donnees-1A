import datetime
import pandas as pd
from Model.sport import Sport

FOOTBALL = Sport("Football", "ballon", 22, "Sport collectif avec but", True)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class FootballPlayerAdapter:
    """
    Convertit une ligne de football_european_leagues/player.csv en dict Player.

    Colonnes CSV : player_api_id, player_name, birthday, weight (kg), height (cm)

    Le nom complet est séparé sur le premier espace : "Aaron Cresswell"
    -> prenom="Aaron", nom="Cresswell".
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        nom_complet = str(row["player_name"]).strip()
        parties = nom_complet.split(" ", 1)
        prenom = parties[0]
        nom = parties[1] if len(parties) == 2 else "Inconnu"

        try:
            dob = datetime.date.fromisoformat(str(row["birthday"]))
        except (ValueError, TypeError):
            dob = _DATE_INCONNUE

        return {
            "id":                int(row["player_api_id"]),
            "nom":               nom,
            "prenom":            prenom,
            "date_de_naissance": dob,
            "pseudo":            None,
            "pays_de_naissance": None,
            "sexe":              None,
            "poids":             float(row["weight (kg)"]) if pd.notna(row.get("weight (kg)")) else 0.0,
            "taille":            float(row["height (cm)"]) if pd.notna(row.get("height (cm)")) else 0.0,
            "role":              None,
            "team":              None,
            "sport":             FOOTBALL,
        }
