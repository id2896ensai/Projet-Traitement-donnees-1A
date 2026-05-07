import datetime
import pandas as pd
from Model.sport import Sport

LOL = Sport("League of Legends", "esport", 10, "MOBA 5v5", True)


class LolMatchAdapter:
    """
    Convertit une ligne de league_of_legends/match.csv en dict Match.

    Colonnes CSV : date, team_blue, team_red, winner (abreviation de l'equipe gagnante)

    Requiert un dict d'equipes pre-charge {abbreviation (str): Team}.
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
            raise KeyError(f"Equipe introuvable : '{abrv_bleu}' ou '{abrv_rouge}'")

        vainqueur = str(row["winner"]).strip()
        score_bleu = 1 if vainqueur == abrv_bleu else 0
        score_rouge = 1 if vainqueur == abrv_rouge else 0

        return {
            "sport":        LOL,
            "participants": [equipe_bleu, equipe_rouge],
            "scores":       {equipe_bleu: score_bleu, equipe_rouge: score_rouge},
            "date_match":   datetime.date.fromisoformat(str(row["date"])),
        }
