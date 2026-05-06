from datetime import date


class Competition:
    """
    Classe modélisant une compétition sportive.

    Attributes
    ----------
    id : int
        Identifiant unique de la compétition.
    nom : str
        Nom de la compétition.
    date_de_debut : date
        Date de début de la compétition.
    date_de_fin : date
        Date de fin de la compétition.
    lieu : str
        Lieu où se déroule la compétition.
    type : str
        Type de la compétition (ex: "Championnat", "Coupe", "Tournoi").
    sports : list[str]
        Liste des sports pratiqués lors de la compétition.

    Raises
    ------
    TypeError
        Si id, nom, lieu, date_de_debut, date_de_fin ou sports
        ne sont pas des instances des types attendus.
    ValueError
        Si date_de_fin est antérieure à date_de_debut.
    """
    def __init__(self, id: int, nom: str, date_de_debut: date, date_de_fin: date, lieu: str,
                 type: str, sports: list[str]) -> None:
        if not isinstance(nom, str):
            raise TypeError("le nom doit etre en str")
        if not isinstance(id, int):
            raise TypeError("le id doit etre en entier")
        if not isinstance(lieu, str):
            raise TypeError("Le lieu doit etre en str ")
        if not isinstance(date_de_debut, date):
            raise TypeError("La date de début doit être une date")
        if not isinstance(date_de_fin, date):
            raise TypeError("La date de fin doit être une date")
        if date_de_fin < date_de_debut:
            raise ValueError("La date de fin doit être après la date de début")
        if not isinstance(sports, list):
            raise TypeError("Les sports doievent etre en liste")
        for s in sports:
            if not isinstance(s, str):
                raise TypeError("Le sport doit etre en str")
        self.id = id
        self.nom = nom
        self.date_de_debut = date_de_debut
        self.date_de_fin = date_de_fin
        self.lieu = lieu
        self.type = type
        self.sports = sports

    def __str__(self) -> str:
        return (
            f"Competition {self.id}, '{self.nom}',"
            f" du {self.date_de_debut} au {self.date_de_fin}, "
            f"lieu='{self.lieu}', type='{self.type}', sports={self.sports})"
        )

    def __repr__(self) -> str:
        return (
            "Competition("
            + "id: " + str(self.id)
            + ", nom: " + self.nom
            + ", date_de_debut: " + str(self.date_de_debut)
            + ", date_de_fin: " + str(self.date_de_fin)
            + ", lieu: " + self.lieu
            + ", type: " + self.type
            + ", sports: " + str(self.sports)
            + ")"
        )
