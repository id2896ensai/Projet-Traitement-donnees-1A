import datetime
import pandas as pd
from src.Model.sport import Sport

BASKETBALL = Sport("Basketball", "ballon", 10, "Sport collectif avec panier", True)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


def _parse_date(val: str) -> datetime.date:
    """
    Parse une date potentiellement tronquée (ex: '2022-10-2' → '2022-10-02').
    Utilise dateutil pour être robuste aux formats incomplets du CSV.
    """
    try:
        # Tentative ISO standard d'abord
        return datetime.date.fromisoformat(val)
    except ValueError:
        pass
    try:
        # Fallback : parsing flexible via dateutil
        from dateutil import parser as du
        return du.parse(val).date()
    except Exception:
        return _DATE_INCONNUE


class BasketballMatchAdapter:
    """
    Convertit une ligne de basketball/game.csv en dict prêt pour GenericMatchLoader.

    Colonnes CSV : game_date, team_id_home, team_id_away, pts_home, pts_away

    Requiert un dict d'équipes pré-chargé {id (int): Team}.
    Produit les clés plates participant_1/2 et score_participant_1/2
    que GenericMatchLoader.create_object assemble en participants[] et scores{}.
    """

    def __init__(self, teams: dict) -> None:
        self.teams = teams

    def adapt(self, row: pd.Series) -> dict:
        return {
            "sport":               BASKETBALL,
            "participant_1":       self.teams[int(row["team_id_home"])],
            "participant_2":       self.teams[int(row["team_id_away"])],
            "score_participant_1": int(row["pts_home"]),
            "score_participant_2": int(row["pts_away"]),
            "date_match":          _parse_date(str(row["game_date"])),
        }
