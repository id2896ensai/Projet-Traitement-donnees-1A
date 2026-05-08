# Projet Traitement de Données 1A — Application de Statistiques Sportives

Application en ligne de commande (CLI) permettant de consulter les résultats
et statistiques de compétitions sportives variées, avec un système de gestion
des données réservé aux administrateurs.

---

## Table des matières

1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Lancement de l'application](#lancement-de-lapplication)
4. [Tests](#tests)
5. [Linter et formateur](#linter-et-formateur)
6. [Style de documentation](#style-de-documentation)
7. [Structure du projet](#structure-du-projet)
8. [Sports disponibles](#sports-disponibles)
9. [Fonctionnalités](#fonctionnalités)
10. [Ajout d'un sport personnalisé](#ajout-dun-sport-personnalisé)
11. [Notes techniques](#notes-techniques)

---

## Prérequis

- Python **3.13** (ou supérieur)
- `pip`

---

## Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/id2896ensai/Projet-Traitement-donnees-1A.git
cd Projet-Traitement-donnees-1A

# 2. Créer l'environnement virtuel
python -m venv venv

# 3. Activer l'environnement virtuel
#    Windows (PowerShell / cmd)
venv\Scripts\activate
#    macOS / Linux
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt
```

---

## Lancement de l'application

```bash
python __main__.py
```

Au démarrage, l'application affiche un écran d'accueil. Vous pouvez :

- **Appuyer sur Entrée** pour continuer en tant qu'utilisateur (consultation
  libre, lecture seule).
- **Saisir un login + mot de passe** pour vous connecter en tant
  qu'administrateur et accéder aux fonctions de gestion des données.

---

## Tests

La suite de tests utilise **pytest** avec mesure de couverture.

```bash
# Lancer tous les tests
pytest --cov

# Variantes selon l'environnement
python -m pytest --cov
conda run pytest --cov
```

Les tests se trouvent dans le dossier `test/`. Ils couvrent :

- les classes du modèle (`test/Model/`)
- les parseurs et chargeurs (`test/Parsers/`)
- les fonctions utilitaires (`test/Common/`)
- un test de cohérence globale (`test/test_sanity_check.py`)

---

## Linter et formateur

### Linter — Ruff

Ce projet utilise **Ruff** comme linter.

```bash
ruff check .
```

### Formateur — Black

Ce projet utilise **Black** comme formateur de code.

```bash
black .
```

Les deux outils sont inclus dans `requirements.txt` et s'installent
automatiquement avec `pip install -r requirements.txt`.

---

## Style de documentation

Les docstrings suivent le style **NumPy**.

Exemple :

```python
def podium(matches: list, n: int = 3) -> list:
    """
    Classement des n premières équipes par nombre de victoires.

    Parameters
    ----------
    matches : list
        Liste d'objets Match.
    n : int, optional
        Nombre de places à retourner (défaut : 3).

    Returns
    -------
    list
        Liste de tuples (Team, nb_victoires) triée par ordre décroissant.
    """
```

---

## Structure du projet

```
Projet-Traitement-donnees-1A/
│
├── __main__.py                  # Point d'entrée — interface CLI complète
├── requirements.txt
├── pytest.ini
│
├── data/                        # Données brutes par sport (CSV)
│   ├── basketball/
│   ├── chess/
│   ├── football_european_leagues/
│   ├── football_champions_league/
│   ├── tennis/
│   ├── volleyball/
│   ├── badminton/
│   ├── starcraft_2/
│   ├── counter_strike_2/
│   └── league_of_legends/
│
├── src/
│   ├── Model/                   # Classes métier (Match, Team, Player, Sport…)
│   ├── Parsers/
│   │   ├── Adapters/            # Un sous-dossier par sport + generique.py
│   │   ├── Loaders/             # Chargeurs génériques (CSV → objets)
│   │   ├── sport_registry.py    # Registre central de tous les sports
│   │   └── baseloader.py
│   └── Analysis/
│       ├── stats.py             # Statistiques maison (podium, victoires…)
│       ├── visualisation.py     # Graphiques matplotlib
│       └── basket_avance.py     # Statistiques avancées basketball (pandas)
│
└── test/                        # Suite de tests pytest
    ├── Model/
    ├── Parsers/
    ├── Common/
    └── test_sanity_check.py
```

---

## Sports disponibles

| Sport | Données disponibles |
|---|---|
| Basketball (NBA) | Équipes, joueurs, matchs, stats avancées |
| Football — Ligues européennes | Équipes, joueurs, matchs |
| Football — Ligue des Champions | Équipes, joueurs, matchs |
| Tennis (ATP & WTA 2024) | Joueurs, matchs |
| Volleyball (hommes & femmes) | Équipes, joueurs, matchs |
| Échecs (FIDE) | Joueurs, matchs |
| Badminton | Joueurs, matchs |
| League of Legends (e-sport) | Équipes, joueurs, matchs |
| Counter-Strike 2 (e-sport) | Équipes, joueurs, matchs |
| StarCraft 2 (e-sport) | Joueurs, matchs |

---

## Fonctionnalités

### Pour tous les utilisateurs

- **Classement (podium)** : top N des équipes/joueurs par nombre de victoires.
- **Matchs d'une équipe** : liste de tous les matchs d'une équipe donnée.
- **Matchs d'un joueur** : recherche flexible par nom, prénom, pseudo ou
  partie du nom (insensible à la casse).
- **Statistiques descriptives** : nb de matchs, victoires, défaites, nuls,
  % victoires, moyenne de points marqués/encaissés, score max/min.
- **Statistiques avancées basketball** : eFG%, TS%, OffRtg, DefRtg, NetRtg,
  Pace, Four Factors — avec tableau de bord matplotlib (4 graphiques).
- **Visualisations** : podium en barres horizontales, bilan en camembert,
  timeline des victoires par saison, tableau stylisé.
- **Informations joueur** : fiche détaillée (nom, prénom, pseudo, pays, rôle…).

### Pour les administrateurs

- **Ajouter un sport personnalisé** : assistant guidé — fournir les CSV
  équipes, joueurs et matchs, mapper les colonnes, le sport est ensuite
  disponible immédiatement dans l'application.
- **Gérer les données existantes** : afficher, rechercher, ajouter, modifier
  ou supprimer des lignes dans n'importe quel fichier CSV d'un sport.

---

## Ajout d'un sport personnalisé

L'administrateur peut ajouter un nouveau sport via le menu **Administration →
Ajouter un sport**. L'assistant demande :

1. Le nom du sport.
2. Les fichiers CSV pour les équipes, les joueurs et les matchs.
3. Pour chaque fichier, la correspondance entre les colonnes du CSV et les
   champs attendus (nom de l'équipe, scores, date du match, etc.).

Les fichiers sont automatiquement copiés dans `data/<sport>/` pour garantir
la portabilité du projet. La configuration est sauvegardée dans
`sports_custom.json` et rechargée à chaque démarrage.

> **Limite connue** : le système modélise des matchs à **deux participants**.
> Les sports avec plus de deux compétiteurs simultanés (Formule 1, natation,
> etc.) ne sont pas supportés en l'état et nécessiteraient un nouveau modèle
> de données.

---

## Notes techniques

### Architecture

- Le `__main__.py` est le seul point de couplage entre les couches : il
  importe les parseurs, appelle les fonctions d'analyse et gère l'interface.
  Les sous-packages (`Model`, `Parsers`, `Analysis`) ne s'importent pas entre
  eux.
- Chaque sport dispose de trois adaptateurs (`TeamAdapter`, `PlayerAdapter`,
  `MatchAdapter`) qui transforment une ligne CSV en objet métier.
- `sport_registry.py` est le registre central : il associe chaque nom de
  sport à ses adaptateurs et chemins de données.

### Modèle de données

Les classes principales sont `Sport`, `Team`, `Player`, `Match`.
Certains attributs définis dans le modèle UML initial ne sont pas exploités
dans l'interface actuelle (voir rapport) :

- `Player.poids` — toujours 0.0, aucun CSV ne le fournit.
- `Player.sexe` — renseigné pour les Échecs, non utilisé dans les filtres.
- `Player.team` — lien inverse Player → Team, laissé à `None` par tous les
  adaptateurs (le sens inverse `team.players` est utilisé).
- `Team.team_api_id` — identifiant API externe du football européen, non
  utilisé dans les statistiques.
- Méthodes `Player.filtre_*()` — conçues pour le chaînage, non appelées
  (l'interface filtre directement dans les listes).

Ces éléments reflètent un modèle UML conçu pour être extensible : brancher
`Competition` ou les méthodes de filtrage ne nécessiterait pas de réécrire
le modèle, seulement d'ajouter des adaptateurs et des menus.
