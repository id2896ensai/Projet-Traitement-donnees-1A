class Sport:
    """Classe modélisant un sport"""

    def __init__(self, nom: str, categorie: str, nb_joueurs: int, description: str, sport_en_equipe: bool):
        self.nom = nom
        self.categorie = categorie
        self.nb_joueurs = nb_joueurs
        self.description = description
        self.sport_en_equipe = sport_en_equipe

    def __str__(self):
        return "Sport : " + self.nom
        + ", catégorie : " + str(self.categorie)
        + ", nombre de joueurs neccessaire : " + self.nb_joueurs
        + ", des : " + str(self.poids)
        + "taille : " + str(self.taille)