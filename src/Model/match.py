from datetime import date
from .sport import Sport
from .participant import Participant


class Match:
    def __init__(
        self,
        sport: Sport,
        participant_1: Participant,
        participant_2: Participant,
        score_participant_1: int,
        score_participant_2: int,
        date_match: date,
    ):
        if not isinstance(sport, Sport):
            raise TypeError("sport doit être une instance de Sport")
        if not isinstance(participant_1, Participant):
            raise TypeError("participant_1 doit être une instance de Participant (Team ou Player)")
        if not isinstance(participant_2, Participant):
            raise TypeError("participant_2 doit être une instance de Participant (Team ou Player)")
        if not isinstance(date_match, date):
            raise TypeError("date_match doit être une instance de date")
        if participant_1 is participant_2:
            raise ValueError("participant_1 et participant_2 doivent être différents")
        if score_participant_1 < 0 or score_participant_2 < 0:
            raise ValueError("Les scores ne peuvent pas être négatifs")
        if date_match > date.today():
            raise ValueError("La date du match ne peut pas être dans le futur")

        self.sport = sport
        self.participant_1 = participant_1
        self.participant_2 = participant_2
        self.score: dict = {
            participant_1: score_participant_1,
            participant_2: score_participant_2,
        }
        self.date_match = date_match

    def get_winner(self) -> Participant | None:
        """Return the winning Participant, or None if it's a draw.

        Returns:
            Participant | None: The participant with the higher score, or None.
        """
        score_1 = self.score[self.participant_1]
        score_2 = self.score[self.participant_2]
        if score_1 > score_2:
            return self.participant_1
        if score_2 > score_1:
            return self.participant_2
        return None

    def __str__(self) -> str:
        s1 = self.score[self.participant_1]
        s2 = self.score[self.participant_2]
        return (
            f"{self.date_match} | {self.participant_1.full_name} {s1}"
            f" - {s2} {self.participant_2.full_name}"
            f" [{self.sport.nom}]"
        )
