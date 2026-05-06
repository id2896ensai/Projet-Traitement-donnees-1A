from .person import Person


class Player(Person):

    def __init__(self, id, pseudo, nom, prenom, date_de_naissance, pays_de_naissance, sexe, poids,
                 taille, role, team):

        if not isinstance(id, int):
            raise TypeError("id doit être un int")

        if pseudo is not None and not isinstance(pseudo, str):
            raise TypeError("pseudo doit être une str ou None")

        if not isinstance(nom, str):
            raise TypeError("nom doit être une str")
        if not nom.strip():
            raise ValueError("nom ne peut pas être vide")

        if not isinstance(prenom, str):
            raise TypeError("prenom doit être une str")
        if not prenom.strip():
            raise ValueError("prenom ne peut pas être vide")

        if date_de_naissance is not None and not isinstance(date_de_naissance, (str, type(None))):
            raise TypeError("date_de_naissance doit être une str ou None")

        if pays_de_naissance is not None and not isinstance(pays_de_naissance, str):
            raise TypeError("pays_de_naissance doit être une str ou None")

        if sexe is not None and not isinstance(sexe, str):
            raise TypeError("sexe doit être une str ou None")

        if not isinstance(poids, (int, float)):
            raise TypeError("poids doit être un int ou float")

        if not isinstance(taille, (int, float)):
            raise TypeError("taille doit être un int ou float")

        if role is not None and not isinstance(role, str):
            raise TypeError("role doit être une str ou None")

        if team is not None and not isinstance(team, object):
            raise TypeError("team doit être une instance valide ou None")
        super().__init__(nom, prenom, date_de_naissance)
        self.id = id
        self.pseudo = pseudo
        self.pays_de_naissance = pays_de_naissance
        self.sexe = sexe
        self.poids = poids
        self.taille = taille
        self.role = role
        self.team = team

    def __str__(self):
        return (
            "Athlete : " + self.nom + " " + self.prenom
            + ", date de naissance : " + str(self.date_de_naissance)
            + ", sexe : " + self.sexe
            + ", poids : " + str(self.poids)
            + ", taille : " + str(self.taille)
        )

    def __repr__(self) -> str:
        """
        Retourne une représentation technique du joueur, destinée au débogage.

        Returns
        -------
        str
            Chaîne de caractères contenant le nom de la classe et l'ensemble
            des attributs de l'instance.
        """
        return (
            "Player(" + str(self.id)
            + ", pseudo: " + str(self.pseudo)
            + ", nom: " + self.nom
            + ", prenom: " + self.prenom
            + ", date_de_naissance: " + str(self.date_de_naissance)
            + ", pays_de_naissance: " + str(self.pays_de_naissance)
            + ", sexe: " + self.sexe
            + ", poids: " + str(self.poids)
            + ", taille: " + str(self.taille)
            + ", role: " + str(self.role)
            + ", team: " + repr(self.team)
            + ")"
        )

    def filtre_id(self, id_recherche: int) -> bool:
        """
        Vérifie si l'identifiant du joueur correspond à celui recherché.

        Parameters
        ----------
        id_recherche : int
            Identifiant à comparer avec celui du joueur.

        Returns
        -------
        bool
            True si les identifiants correspondent, False sinon.
        """
        return id_recherche == self.id

    def filtre_nom(self, nom_recherche: str) -> bool:
        """
        Vérifie si le nom du joueur correspond à celui recherché.

        Parameters
        ----------
        nom_recherche : str
            Nom à comparer avec celui du joueur.

        Returns
        -------
        bool
            True si les noms correspondent, False sinon.
        """
        return nom_recherche == self.nom

    def filtre_prenom(self, prenom_recherche: str) -> bool:
        """
        Vérifie si le prénom du joueur correspond à celui recherché.

        Parameters
        ----------
        prenom_recherche : str
            Prénom à comparer avec celui du joueur.

        Returns
        -------
        bool
            True si les prénoms correspondent, False sinon.
        """
        return prenom_recherche == self.prenom

    def filtre_date_de_naissance(self, date_de_naissance) -> bool:
        """
        Vérifie si la date de naissance du joueur correspond à celle recherchée.

        Parameters
        ----------
        date_de_naissance : date
            Date de naissance à comparer avec celle du joueur.

        Returns
        -------
        bool
            True si les dates correspondent, False sinon.
        """
        return date_de_naissance == self.date_de_naissance

    def filtre_sexe(self, sexe_recherche: str) -> bool:
        """
        Vérifie si le sexe du joueur correspond à celui recherché.

        Parameters
        ----------
        sexe_recherche : str
            Sexe à comparer avec celui du joueur.

        Returns
        -------
        bool
            True si les valeurs correspondent, False sinon.
        """
        return sexe_recherche == self.sexe
