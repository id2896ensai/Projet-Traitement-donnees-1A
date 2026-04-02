from .competition import Competition
from .equipe import Equipe

class Classement:
    """
    Attributs :
        competition : Competition  — la compétition associée
        entree : dict[Equipe, list[float]]  — points par équipe (interprété du diagramme)
    """

    def __init__(self, competition: Competition):
        """
        Initialise le classement pour une compétition donnée.
        L'entrée est un dictionnaire {Equipe: [points]} construit à partir des matchs.
        """
        self.competition = competition
        self.equipe: dict{Equipe} = {}  # {Equipe: points_total}

    def __str__(self) -> str:
        lignes = [f"Classement - {self.competition}"]
        classement_trie = self.trier()
        for i, (equipe, points) in enumerate(classement_trie, start=1):
            lignes.append(f"{i}. {equipe} — {points} pts")
        return "\n".join(lignes)

    def mettre_a_jour(self, points: list[float], equipe) -> list:
        """
        Met à jour les points d'une équipe dans le classement.
        Retourne la liste mise à jour [str, Equipe].
        """
        if equipe not in self.entree:
            self.entree[equipe] = 0
        for p in points:
            self.entree[equipe] += p
        return [str(equipe), equipe]

    def avoir_rang(self, equipe) -> int:
        """
        Retourne le rang (position) d'une équipe dans le classement.
        """
        classement_trie = self.trier()
        equipes_triees = [eq for eq, _ in classement_trie]
        if equipe in equipes_triees:
            return equipes_triees.index(equipe) + 1
        raise ValueError(f"L'équipe {equipe} n'est pas dans le classement.")

    def avoir_podium(self) -> str:
        """
        Retourne une représentation textuelle du podium (top 3).
        """
        classement_trie = self.trier()
        podium = classement_trie[:3]
        lignes = ["🏆 Podium :"]
        medailles = ["🥇", "🥈", "🥉"]
        for i, (equipe, points) in enumerate(podium):
            lignes.append(f"{medailles[i]} {equipe} — {points} pts")
        return "\n".join(lignes)

    def trier(self) -> list[tuple]:
        """
        Trie les équipes par points décroissants.
        Retourne une liste de tuples (Equipe, points) triée.
        """
        return sorted(self.entree.items(), key=lambda x: x[1], reverse=True)