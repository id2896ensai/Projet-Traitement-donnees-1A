class Sport:
    """Classe modélisant un sport"""

    def __init__(self, nom: str, categorie: str, nb_joueurs: int, description: str, sport_en_equipe: bool):
        self.nom = nom
        self.categorie = categorie
        self.nb_joueurs = nb_joueurs
        self.description = description
        self.sport_en_equipe = sport_en_equipe

    def __str__(self):
        if self.sport_en_equipe:
            texte = "collectif."
        elif not self.sport_en_equipe:
            texte = "individuel."
        return "Sport : " + self.nom
        + ", catégorie : " + str(self.categorie)
        + ", nombre de joueurs neccessaire : " + self.nb_joueurs
        + ", description : " + str(self.description)
        + ", Sport individuel ou collectif : " + texte
    
    def __repr__(self):
        return "Sport(" + self.nom
        + ", categorie: " + str(self.categorie)
        + ", nb_joueurs: " + self.nb_joueurs
        + ", description: " + str(self.description)
        + ", sport_en_equipe: " + self.sport_en_equipe
        + ")"