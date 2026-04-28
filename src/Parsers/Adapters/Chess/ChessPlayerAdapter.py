import datetime

import pandas as pd

from src.Model.sports_catalogue import CHESS


class ChessPlayerAdapter:
    """Maps a chess/player.csv row to a Player dict.

    CSV columns:
        fide_id        -> id
        name           -> nom + prenom  (format "Lastname, Firstname" or single token)
        birth_year     -> date_de_naissance  (only year available, set to Jan 1)
        gender         -> sexe
        federation     -> pays_de_naissance
        fide_title     -> role

    The raw name is stored as pseudo so full_name returns the exact string
    used in match.csv for cross-referencing.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raw_name = str(row["name"]).strip()
        parts = raw_name.split(", ", 1)
        nom = parts[0]
        prenom = parts[1] if len(parts) == 2 else ""

        birth_year = row.get("birth_year")
        dob = (
            datetime.date(int(birth_year), 1, 1)
            if pd.notna(birth_year)
            else None
        )

        fide_id = row.get("fide_id")
        return {
            "id":                int(fide_id) if pd.notna(fide_id) else None,
            "nom":               nom,
            "prenom":            prenom,
            "pseudo":            raw_name,
            "date_de_naissance": dob,
            "sexe":              str(row["gender"]) if pd.notna(row.get("gender")) else None,
            "pays_de_naissance": str(row["federation"]) if pd.notna(row.get("federation")) else None,
            "role":              str(row["fide_title"]) if pd.notna(row.get("fide_title")) else None,
            "sport":             CHESS,
        }
