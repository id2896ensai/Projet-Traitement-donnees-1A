import datetime
import pandas as pd
from src.Model.sport import Sport

CS2 = Sport("Counter-Strike 2", "esport", 10, "FPS tactique 5v5", True)


class CS2MatchAdapter:
    """
    Convertit une ligne de counter_strike_2/match.csv en dict Match.

    Colonnes CSV : date, team_1, team_2, score_team_1, score_team_2

    Requiert un dict d'équipes pré-chargé {full_name (str): Team}.
    Score = nombre de maps gagnées.
    """

    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row: pd.Series) -> dict:
        equipe_1 = self.equipes.get(str(row["team_1"]).strip())
        equipe_2 = self.equipes.get(str(row["team_2"]).strip())

        if equipe_1 is None or equipe_2 is None:
            raise KeyError("Equipe introuvable dans le dictionnaire")

        return {
            "sport":               CS2,
            "participant_1":       equipe_1,
            "participant_2":       equipe_2,
            "score_participant_1": int(row["score_team_1"]),
            "score_participant_2": int(row["score_team_2"]),
            "date_match":          datetime.date.fromisoformat(str(row["date"])),
        }
