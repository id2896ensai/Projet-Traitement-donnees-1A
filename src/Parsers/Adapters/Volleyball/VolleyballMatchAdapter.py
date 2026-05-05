import datetime

import pandas as pd

from src.Model.sports_catalogue import VOLLEYBALL


class VolleyballMatchAdapter:
    """Convertit une ligne volleyball match CSV en dict Match.

    Requiert un dictionnaire d'equipes pre-charge {code_pays (str): Team}.
    Le score correspond au nombre de sets gagnes.
    """

    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row: pd.Series) -> dict:
        equipe_1 = self.equipes.get(str(row["country_code_1"]).strip())
        equipe_2 = self.equipes.get(str(row["country_code_2"]).strip())

        if equipe_1 is None or equipe_2 is None:
            raise KeyError("Equipe introuvable dans le dictionnaire")

        return {
            "sport":               VOLLEYBALL,
            "participant_1":       equipe_1,
            "participant_2":       equipe_2,
            # sets gagnes par chaque equipe
            "score_participant_1": int(row["set_country_1"]),
            "score_participant_2": int(row["set_country_2"]),
            "date_match":          datetime.date.fromisoformat(str(row["date"])),
        }
