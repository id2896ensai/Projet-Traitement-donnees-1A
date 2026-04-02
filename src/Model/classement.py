from .competition import Competition
from .team import Team


class Classement:
    def __init__(self, competition: Competition):
        self.competition = competition
        self.entree: dict[Team, float] = {}

    def trier(self):
        return sorted(self.entree.items(), key=lambda x: x[1], reverse=True)

    def __str__(self) -> str:
        lignes = [f"Classement de la competition de {self.competition}"]
        classement_trie = self.trier()
        for i, (equipe, points) in enumerate(classement_trie, start=1):
            lignes.append(f"{i}. {equipe} — {points} pts")
        return "\n".join(lignes)
