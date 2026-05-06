import datetime
import pandas as pd
from src.Model.sport import Sport

VOLLEYBALL = Sport("Volleyball", "ballon", 6, "Sport collectif avec filet", True)


class VolleyballMatchAdapter:
    """
    Convertit une ligne de volleyball/match_men.csv en dict Match.

    Colonnes CSV : date, stage, country_code_1, country_code_2, set_country_1, set_country_2

    Requiert un dict d'equipes pre-charge {abbreviation (str): Team}.
    Score = nombre de sets gagnes.
    """

    def __init__(self, teams: dict) -> None:
        self.teams = teams

    def adapt(self, row: pd.Series) -> dict:
        code_1 = str(row["country_code_1"]).strip()
        code_2 = str(row["country_code_2"]).strip()

        team_1 = self.teams.get(code_1)
        team_2 = self.teams.get(code_2)

        if team_1 is None or team_2 is None:
            raise KeyError(f"Equipe introuvable : '{code_1}' ou '{code_2}'")

        return {
            "sport":               VOLLEYBALL,
            "participant_1":       team_1,
            "participant_2":       team_2,
            "score_participant_1": int(row["set_country_1"]),
            "score_participant_2": int(row["set_country_2"]),
            "date_match":          datetime.date.fromisoformat(str(row["date"])),
        }
