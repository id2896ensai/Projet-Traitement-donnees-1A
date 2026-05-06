from .person import Person


class Coach(Person):
    """Classe modélisant un coach, héritant de Person.

    Attributes
    ----------
    nom : str
        Nom de famille du coach (hérité de Person).
    prenom : str
        Prénom du coach (hérité de Person).
    date_de_naissance : date
        Date de naissance du coach (hérité de Person).
    """

    def __str__(self) -> str:
        return (
            "Coach : " + self.nom + " " + self.prenom
            + ", date de naissance : " + str(self.date_de_naissance)
        )

    def __repr__(self) -> str:
        return (
            "Coach("
            + "nom: " + self.nom
            + ", prenom: " + self.prenom
            + ", date_de_naissance: " + str(self.date_de_naissance)
            + ")"
        )
