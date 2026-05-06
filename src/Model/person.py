from datetime import date


class Person:
    """Classe modélisant une personne : joueur ou coach.

    Attributes
    ----------
    nom : str
        Nom de famille de la personne.
    prenom : str
        Prénom de la personne.
    date_de_naissance : date
        Date de naissance de la personne.
    """

    def __init__(self, nom: str, prenom: str, date_de_naissance) -> None:
        """
        Initialise une instance de Person.

        Parameters
        ----------
        nom : str
            Nom de famille de la personne.
        prenom : str
            Prénom de la personne.
        date_de_naissance : date
            Date de naissance de la personne.
        """
        if not isinstance(nom, str):
            raise TypeError("nom doit être une str")
        if not nom.strip():
            raise ValueError("nom ne peut pas être vide")

        if not isinstance(prenom, str):
            raise TypeError("prenom doit être une str")
        if not prenom.strip():
            raise ValueError("prenom ne peut pas être vide")

        if not isinstance(date_de_naissance, date):
            raise TypeError("date_de_naissance doit être une date")

        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance

    def __str__(self) -> str:
        """
        Retourne une représentation lisible de la personne, destinée à l'affichage utilisateur.

        Returns
        -------
        str
            Chaîne de caractères décrivant les attributs de la personne
            de manière claire et lisible.
        """
        return (
            "Personne : " + self.nom + " " + self.prenom
            + ", date de naissance : " + str(self.date_de_naissance)
        )

    def __repr__(self) -> str:
        """
        Retourne une représentation technique de la personne, destinée au débogage.

        Returns
        -------
        str
            Chaîne de caractères contenant le nom de la classe et l'ensemble
            des attributs de l'instance.
        """
        return (
            "Person("
            + "nom: " + self.nom
            + ", prenom: " + self.prenom
            + ", date_de_naissance: " + str(self.date_de_naissance)
            + ")"
        )
