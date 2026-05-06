# Interface en ligne de commande pour l'application de statistiques sportives.
import datetime

from Parsers.Loaders.genericloaders import (
    GenericTeamLoader,
    GenericPlayerLoader,
    GenericMatchLoader,
)
from Parsers.sport_registry import SPORTS_REGISTRY
from Analysis.stats import (
    podium,
    victoires_equipe,
    matchs_equipe,
    matchs_joueur,
    stats_descriptives,
)

SEP = "-" * 52


def charger_donnees(sport_nom: str):
    """Charge et retourne (teams, players, matches) pour le sport sélectionné."""
    cfg = SPORTS_REGISTRY[sport_nom]

    print(f"  Chargement des equipes...")
    team_loader = GenericTeamLoader(cfg["team_csv"], cfg["TeamAdapter"]())
    teams = team_loader.load()

    players = []
    if cfg.get("player_csv") and cfg.get("PlayerAdapter"):
        print("  Chargement des joueurs...")
        player_loader = GenericPlayerLoader(cfg["player_csv"], cfg["PlayerAdapter"]())
        players = player_loader.load()

    print("  Chargement des matchs...")
    teams_dict = team_loader.load_as_dict(cfg["team_key"])
    kwarg = cfg["match_kwarg"]
    match_adapter = cfg["MatchAdapter"](**{kwarg: teams_dict})
    match_loader = GenericMatchLoader(cfg["match_csv"], match_adapter)
    matches = match_loader.load()

    return teams, players, matches


# ---------- sous-menus ----------

def menu_matchs(matches: list):
    """Affiche les matchs avec filtre optionnel par période."""
    print(SEP)
    print("Filtre par date (appuyer Entree pour ignorer)")
    date_debut_str = input("  Date debut (AAAA-MM-JJ) : ").strip()
    date_fin_str   = input("  Date fin   (AAAA-MM-JJ) : ").strip()

    filtres = list(matches)
    try:
        if date_debut_str:
            d = datetime.date.fromisoformat(date_debut_str)
            filtres = [m for m in filtres if m.date_match >= d]
        if date_fin_str:
            d = datetime.date.fromisoformat(date_fin_str)
            filtres = [m for m in filtres if m.date_match <= d]
    except ValueError:
        print("Format invalide, aucun filtre applique.")

    filtres.sort(key=lambda m: m.date_match)

    if not filtres:
        print("Aucun match trouve pour cette periode.")
        return

    # Limite l'affichage à 50 lignes pour rester lisible
    affichage = filtres[:50]
    print(f"\n{len(filtres)} match(s) - affichage des {len(affichage)} premiers :\n")
    for i, m in enumerate(affichage, 1):
        p1, p2 = m.participants[0], m.participants[1]
        s1, s2 = m.scores[p1], m.scores[p2]
        print(f"  {i:3}. [{m.date_match}]  {p1.full_name}  {s1} - {s2}  {p2.full_name}")

    if len(filtres) > 50:
        print(f"\n  ... et {len(filtres) - 50} autres matchs non affiches.")


def menu_podium(matches: list, sport_nom: str):
    """Affiche le podium (top 3) par nombre de victoires."""
    print(SEP)
    print(f"PODIUM - {sport_nom}\n")

    classement = podium(matches, n=3)

    if not classement:
        print("Pas assez de donnees pour etablir un podium.")
        return

    medailles = ["1er", "2eme", "3eme"]
    for i, (equipe, nb) in enumerate(classement):
        print(f"  {medailles[i]} : {equipe.full_name}  ({nb} victoire(s))")


def menu_matchs_joueur(matches: list):
    """Recherche des matchs pour un joueur donné (nom + prénom)."""
    print(SEP)
    nom    = input("  Nom du joueur    : ").strip()
    prenom = input("  Prenom du joueur : ").strip()

    if not nom or not prenom:
        print("Nom et prenom requis.")
        return

    trouves = matchs_joueur(matches, nom, prenom)

    if not trouves:
        print(f"\nAucun match trouve pour {prenom} {nom}.")
        return

    trouves.sort(key=lambda m: m.date_match)
    print(f"\n{len(trouves)} match(s) pour {prenom} {nom} :\n")
    for m in trouves:
        p1, p2 = m.participants[0], m.participants[1]
        s1, s2 = m.scores[p1], m.scores[p2]
        print(f"  [{m.date_match}]  {p1.full_name}  {s1} - {s2}  {p2.full_name}")


def menu_victoires_equipe(matches: list):
    """Affiche le nombre de victoires d'une équipe saisie par l'utilisateur."""
    print(SEP)
    nom = input("  Nom de l'equipe : ").strip()
    if not nom:
        print("Nom requis.")
        return

    nb_v = victoires_equipe(matches, nom)
    # Compte le total de matchs joués par cette équipe
    nb_total = len(matchs_equipe(matches, nom))

    if nb_total == 0:
        print(f"\nEquipe '{nom}' introuvable dans les matchs.")
    else:
        nb_d = nb_total - nb_v
        # Calcul des nuls : matchs où l'équipe ne gagne pas mais ce n'est pas une défaite nette
        print(f"\n  {nom}")
        print(f"    Matchs joues : {nb_total}")
        print(f"    Victoires    : {nb_v}")
        print(f"    Autres       : {nb_total - nb_v}")


def menu_stats_descriptives(matches: list):
    """Statistiques descriptives (buts/pts marqués et encaissés) pour une équipe."""
    print(SEP)
    nom = input("  Nom de l'equipe : ").strip()
    if not nom:
        print("Nom requis.")
        return

    stats = stats_descriptives(matches, nom)

    if "erreur" in stats:
        print("\n" + stats["erreur"])
        return

    print(f"\n  Stats pour '{nom}' :\n")
    print(f"    Matchs joues         : {stats['nb_matchs']}")
    print(f"    Victoires            : {stats['nb_victoires']}")
    print(f"    Defaites             : {stats['nb_defaites']}")
    print(f"    Nuls                 : {stats['nb_nuls']}")
    print(f"    Taux de victoire     : {stats['pct_victoires']} %")
    print(f"    Moy. pts marques     : {stats['moy_pts_marques']}")
    print(f"    Moy. pts encaisses   : {stats['moy_pts_encaisses']}")
    print(f"    Meilleur score       : {stats['max_score']}")
    print(f"    Pire score           : {stats['min_score']}")


# ---------- menu principal d'un sport ----------

def menu_sport(sport_nom: str):
    """Menu fonctionnalités après chargement des données d'un sport."""
    cfg = SPORTS_REGISTRY[sport_nom]
    collectif = cfg["sport_en_equipe"]

    print(f"\nChargement de {sport_nom}...")
    teams, players, matches = charger_donnees(sport_nom)
    print(f"\n  {len(teams)} equipes  |  {len(players)} joueurs  |  {len(matches)} matchs charges")

    while True:
        print("\n" + SEP)
        print(f"MENU  {sport_nom}\n")
        print("  1. Afficher les matchs (avec filtre date)")
        print("  2. Podium (top 3 par victoires)")
        print("  3. Matchs d'un joueur (nom + prenom)")
        print("  4. Nombre de victoires d'une equipe")
        if collectif:
            print("  5. Stats descriptives d'une equipe")
        print("  0. Retour au menu principal")

        choix = input("\n> ").strip()

        if choix == "1":
            menu_matchs(matches)
        elif choix == "2":
            menu_podium(matches, sport_nom)
        elif choix == "3":
            menu_matchs_joueur(matches)
        elif choix == "4":
            menu_victoires_equipe(matches)
        elif choix == "5" and collectif:
            menu_stats_descriptives(matches)
        elif choix == "0":
            break
        else:
            print("Choix invalide.")


# ---------- point d'entrée ----------

def main():
    """Point d'entrée principal : sélection du sport."""
    sports = list(SPORTS_REGISTRY.keys())

    while True:
        print("\n" + "=" * 52)
        print("  APPLICATION DE STATISTIQUES SPORTIVES")
        print("=" * 52)
        print("\nChoisissez un sport :\n")
        for i, nom in enumerate(sports, 1):
            print(f"  {i:2}. {nom}")
        print("\n   0. Quitter")

        choix = input("\n> ").strip()

        if choix == "0":
            print("Au revoir !")
            break

        try:
            idx = int(choix) - 1
            if 0 <= idx < len(sports):
                menu_sport(sports[idx])
            else:
                print("Choix invalide.")
        except ValueError:
            print("Entrez un nombre.")


if __name__ == "__main__":
    main()
