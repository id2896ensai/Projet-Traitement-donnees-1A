import datetime
import pandas as pd
from src.Model.sport import Sport

STARCRAFT2 = Sport("Starcraft2", "strategie", 1, "Jeu de strategie en temps reel individuel", False)


class Starcraft2MatchAdapter:
    """
    Convertit une ligne de starcraft_2/match.csv en dict Match.

    Colonnes CSV : date, round, group, best_of, player_1, player_2, score_player_1, score_player_2

    Requiert un dict d'equipes pre-charge {full_name/pseudo (str): Team}.
    Score = nombre de maps gagnees.
    """

    def __init__(self, teams: dict) -> None:
        self.teams = teams

    def adapt(self, row: pd.Series) -> dict:
        p1_pseudo = str(row["player_1"]).strip()
        p2_pseudo = str(row["player_2"]).strip()

        team_1 = self.teams.get(p1_pseudo)
        team_2 = self.teams.get(p2_pseudo)

        if team_1 is None or team_2 is None:
            raise KeyError(f"Joueur introuvable : '{p1_pseudo}' ou '{p2_pseudo}'")

        return {
            "sport":               STARCRAFT2,
            "participant_1":       team_1,
            "participant_2":       team_2,
            "score_participant_1": int(row["score_player_1"]),
            "score_participant_2": int(row["score_player_2"]),
            "date_match":          datetime.date.fromisoformat(str(row["date"])),
        }
