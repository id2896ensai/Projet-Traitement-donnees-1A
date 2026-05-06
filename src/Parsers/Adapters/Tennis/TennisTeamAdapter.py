import datetime
import pandas as pd
from src.Model.sport import Sport
from src.Model.player import Player

TENNIS = Sport("Tennis", "raquette", 1, "Sport de raquette individuel", False)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


def _parse_dob(val) -> datetime.date:
    """Parse une date au format YYYYMMDD (entier ou float)."""
    try:
        s = str(int(float(val)))
        return datetime.date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    except (ValueError, TypeError):
        return _DATE_INCONNUE


class TennisTeamAdapter:
    """
    Cree une Team d'un seul joueur depuis tennis/atp_players_2024.csv (sport individuel).

    Colonnes CSV : player_id, name_first, name_last, hand, dob, ioc, height

    L'equipe est indexee par player_id pour etre retrouvee
    depuis les colonnes winner_id / loser_id du CSV de matchs.
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        player_id = int(row["player_id"])
        nom = str(row["name_last"])
        prenom = str(row["name_first"])
        dob = _parse_dob(row.get("dob"))

        joueur = Player(
            id=player_id,
            nom=nom,
            prenom=prenom,
            date_de_naissance=dob,
            pseudo=None,
            pays_de_naissance=str(row["ioc"]) if pd.notna(row.get("ioc")) else None,
            sexe=None,
            poids=0.0,
            taille=float(row["height"]) if pd.notna(row.get("height")) else 0.0,
            role=None,
            team=None,
            sport=TENNIS,
        )

        return {
            "id":           player_id,
            "sport":        TENNIS,
            "players":      [joueur],
            "full_name":    f"{prenom} {nom}",
            "abbreviation": f"{prenom[0]}.{nom}"[:10],
        }
