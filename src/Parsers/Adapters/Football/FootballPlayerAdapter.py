import datetime

import pandas as pd

from src.Model.sports_catalogue import FOOTBALL


class FootballPlayerAdapter:
    """Convertit une ligne de football_european_leagues/player.csv en dict Player."""

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        # Separation du nom complet sur le premier espace
        nom_complet = str(row["player_name"]).strip()
        parties = nom_complet.split(" ", 1)
        prenom = parties[0]
        nom = parties[1] if len(parties) == 2 else ""

        naissance = row.get("birthday")
        dob = datetime.date.fromisoformat(str(naissance)) if pd.notna(naissance) else None

        return {
            "id":                int(row["player_api_id"]),
            "nom":               nom,
            "prenom":            prenom,
            "date_de_naissance": dob,
            "taille":            str(row["height (cm)"]) if pd.notna(row.get("height (cm)")) else None,
            "poids":             float(row["weight (kg)"]) if pd.notna(row.get("weight (kg)")) else None,
            "sport":             FOOTBALL,
        }
