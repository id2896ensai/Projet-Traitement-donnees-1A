from .competition import Competition
from .team import Team


class Classement:
    """
    Classe modélisant le classement des équipes pour une compétition donnée.

    Attributes
    ----------
    competition : Competition
        La compétition à laquelle ce classement est associé.
    entree : dict[Team, float]
        Dictionnaire associant chaque équipe à son nombre de points.
        Initialisé vide, à remplir au fur et à mesure de la compétition.
    """
    def __init__(self, competition: Competition):
        if not isinstance(competition, Competition):
            raise TypeError("competition doit être une instance de Competition")
        self.competition = competition
        self.entree: dict[Team, float] = {}

    def trier(self) -> list[tuple[Team, float]]:
        """Retourne les entrées du classement triées par points décroissants.

        Returns
        -------
        list[tuple[Team, float]]
            Liste de tuples (équipe, points) triée du plus grand
            au plus petit nombre de points.
        """
        return sorted(self.entree.items(), key=lambda x: x[1], reverse=True)

    def __str__(self) -> str:
        lignes = [f"Classement de la competition de {self.competition}"]
        classement_trie = self.trier()
        for i, (equipe, points) in enumerate(classement_trie, start=1):
            lignes.append(f"{i}. {equipe} — {points} pts")
        return "\n".join(lignes)

    def __repr__(self) -> str:
        entree_triee = self.trier()
        entree_str = "{" + ", ".join(
            repr(equipe) + ": " + str(points)
            for equipe, points in entree_triee
        ) + "}"
        return (
            "Classement("
            + "competition: " + repr(self.competition)
            + ", entree: " + entree_str
            + ")"
        )
