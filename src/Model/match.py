from datetime import date
from .sport import Sport
from .team import Team


class Match:
    def __init__(
        self,
        sport,
        equipe_1,
        equipe_2,
        score_equipe_1: int,
        score_equipe_2: int,
        date_match: date,
    ):
        if not isinstance(sport, Sport):
            raise TypeError("sport doit être une instance de Sport")
        if not isinstance(equipe_1, Team):
            raise TypeError("equipe_1 doit être une instance de Equipe")
        if not isinstance(equipe_2, Team):
            raise TypeError("equipe_2 doit être une instance de Equipe")
        if not isinstance(date_match, date):
            raise TypeError("date_match doit être une instance de date")
        if equipe_1 == equipe_2:
            raise ValueError("equipe_1 et equipe_2 doivent être différentes")
        if equipe_1.sport != sport or equipe_2.sport != sport:
            raise ValueError("Les deux équipes doivent pratiquer le sport du match")
        if score_equipe_1 < 0 or score_equipe_2 < 0:
            raise ValueError("Les scores ne peuvent pas être négatifs")
        if date_match > date.today():
            raise ValueError("La date du match ne peut pas être dans le futur")

        self.sport = sport
        self.equipe_1 = equipe_1
        self.equipe_2 = equipe_2
        self.score: dict = {equipe_1: score_equipe_1, equipe_2: score_equipe_2}
        self.date_match = date_match

    def __str__(self) -> str:
        return (
            f"Match [{self.sport}] — {self.equipe_1.full_name} {self.score[self.equipe_1]} "
            f"vs {self.score[self.equipe_2]} {self.equipe_2.full_name} "
            f"(le {self.date_match})"
        )
