import datetime

import pandas as pd

from src.Model.sports_catalogue import LOL


class LolPlayerAdapter:
    """Convertit une ligne de league_of_legends/player.csv en dict Player."""

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        # Separation du vrai nom sur le premier espace
        nom_complet = str(row["name"]).strip()
        parties = nom_complet.split(" ", 1)
        prenom = parties[0]
        nom = parties[1] if len(parties) == 2 else ""

        naissance = row.get("birthdate")
        dob = datetime.date.fromisoformat(str(naissance)) if pd.notna(naissance) else None

        return {
            "pseudo":            str(row["pseudo"]),
            "nom":               nom,
            "prenom":            prenom,
            "date_de_naissance": dob,
            "pays_de_naissance": str(row["country_of_birth"]) if pd.notna(row.get("country_of_birth")) else None,
            "role":              str(row["role"]) if pd.notna(row.get("role")) else None,
            "sport":             LOL,
        }
