import datetime
import pandas as pd
from src.Model.sport import Sport
from src.Model.team import Team
from src.Model.player import Player

CHESS = Sport("Chess", "strategie", 2, "Jeu d'echecs", False)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


class ChessTeamAdapter:
    """
    Cree une Team d'un seul joueur depuis chess/player.csv (sport individuel).

    Colonnes CSV : name, fide_id, birth_year, gender, federation, fide_title

    Le pseudo (nom brut) est utilise comme full_name pour retrouver
    l'equipe dans le dictionnaire lors du chargement des matchs.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raw_name = str(row["name"]).strip()
        parts = raw_name.split(", ", 1)
        nom = parts[0]
        prenom = parts[1] if len(parts) == 2 else "Inconnu"

        birth_year = row.get("birth_year")
        try:
            dob = datetime.date(int(birth_year), 1, 1)
        except (ValueError, TypeError):
            dob = _DATE_INCONNUE

        fide_id = row.get("fide_id")
        player_id = int(fide_id) if pd.notna(fide_id) else abs(hash(raw_name)) % (10 ** 7)

        joueur = Player(
            id=player_id,
            nom=nom,
            prenom=prenom,
            date_de_naissance=dob,
            pseudo=raw_name,
            pays_de_naissance=str(row["federation"]) if pd.notna(row.get("federation")) else None,
            sexe=str(row["gender"]) if pd.notna(row.get("gender")) else None,
            poids=0.0,
            taille=0.0,
            role=str(row["fide_title"]) if pd.notna(row.get("fide_title")) else None,
            team=None,
            sport=CHESS,
        )

        return {
            "id":           player_id,
            "sport":        CHESS,
            "players":      [joueur],
            "full_name":    raw_name,
            "abbreviation": raw_name[:10],
        }
