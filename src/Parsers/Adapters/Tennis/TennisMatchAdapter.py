import datetime
import pandas as pd
from Model.sport import Sport

TENNIS = Sport("Tennis", "raquette", 1, "Sport de raquette individuel", False)

_DATE_INCONNUE = datetime.date(1900, 1, 1)


def _parse_date(val) -> datetime.date:
    """Parse une date au format YYYYMMDD (entier)."""
    try:
        s = str(int(float(val)))
        return datetime.date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    except (ValueError, TypeError):
        return _DATE_INCONNUE


class TennisMatchAdapter:
    """
    Convertit une ligne de tennis/atp_matches_2024.csv en dict Match.

    Colonnes CSV : tourney_date, winner_id, loser_id

    Requiert un dict d'equipes pre-charge {player_id (int): Team}.
    Score : gagnant = 1, perdant = 0.
    """

    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row: pd.Series) -> dict:
        team_1 = self.equipes.get(int(row["winner_id"]))
        team_2 = self.equipes.get(int(row["loser_id"]))

        if team_1 is None or team_2 is None:
            raise KeyError(f"Joueur introuvable : winner_id={row['winner_id']} ou loser_id={row['loser_id']}")

        return {
            "sport":        TENNIS,
            "participants": [team_1, team_2],
            "scores":       {team_1: 1, team_2: 0},
            "date_match":   _parse_date(row.get("tourney_date")),
        }
