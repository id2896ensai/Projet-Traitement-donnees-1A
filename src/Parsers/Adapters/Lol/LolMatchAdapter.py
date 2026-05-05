import datetime

import pandas as pd

from src.Model.sports_catalogue import LOL


class LolMatchAdapter:
    """Convertit une ligne de league_of_legends/match.csv en dict Match.

    Requiert un dictionnaire d'equipes pre-charge {abbreviation (str): Team}.
    Score : 1 pour le vainqueur, 0 pour le perdant.
    """

    def __init__(self, equipes: dict) -> None:
        self.equipes = equipes

    def adapt(self, row: pd.Series) -> dict:
        abrv_bleu = str(row["team_blue"]).strip()
        abrv_rouge = str(row["team_red"]).strip()

        equipe_bleu = self.equipes.get(abrv_bleu)
        equipe_rouge = self.equipes.get(abrv_rouge)

        if equipe_bleu is None or equipe_rouge is None:
            raise KeyError("Equipe introuvable dans le dictionnaire")

        # La colonne winner contient l'abreviation de l'equipe gagnante
        vainqueur = str(row["winner"]).strip()
        score_bleu = 1 if vainqueur == abrv_bleu else 0
        score_rouge = 1 if vainqueur == abrv_rouge else 0

        return {
            "sport":               LOL,
            "participant_1":       equipe_bleu,
            "participant_2":       equipe_rouge,
            "score_participant_1": score_bleu,
            "score_participant_2": score_rouge,
            "date_match":          datetime.date.fromisoformat(str(row["date"])),
        }
