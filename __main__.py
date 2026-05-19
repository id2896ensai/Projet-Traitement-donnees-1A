import os
import sys
import json
import shutil
import datetime
import pandas as pd
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent / "src"))

from Analysis.visualisation import (
    plot_podium,
    plot_bilan_equipe,
    plot_summary_tableau,
)
from Analysis.filtrage import (
    filtrer_matchs,
    matchs_vers_dataframe,
    filtrer_equipes,
    equipes_vers_dataframe,
    filtrer_joueurs,
    joueurs_vers_dataframe,
)
from Parsers.Loaders.genericloaders import (  # noqa: E402
    GenericTeamLoader,
    GenericPlayerLoader,
    GenericMatchLoader,
)
from Parsers.sport_registry import SPORTS_REGISTRY  # noqa: E402
from Analysis.stats import (  # noqa: E402
    podium,
    victoires_equipe,
    matchs_equipe,
    matchs_joueur,
    stats_descriptives,
)
from Analysis.basket_avance import calculer_stats_basket  # noqa: E402
from Model.match import Match  # noqa: E402
from Model.team import Team  # noqa: E402




SEP = "-" * 56
_PROJECT_ROOT = Path(__file__).parent


def _resolve_csv_path(p: str) -> str:
    """Résout un chemin relatif depuis la racine projet."""
    path = Path(p)
    return str(path if path.is_absolute() else _PROJECT_ROOT / path)


# ─── Authentification ─────────────────────────────────────────
# Identifiants stockés en mémoire : {login: mot_de_passe}
_UTILISATEURS: dict[str, str] = {
    "admin": "admin2024",
}
# Logins disposant des droits administrateur
_ADMINS: set[str] = {"admin"}

# Fichier JSON de persistance des sports personnalisés
_CUSTOM_SPORTS_FILE = Path(__file__).parent / "sports_custom.json"


def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _pause() -> None:
    input("\nAppuyer sur Entree pour continuer...")


# ─── Chargement ───────────────────────────────────────────────


def charger_donnees(sport_nom: str) -> tuple[list[Team], list[Any], list[Match]]:
    """Charge et retourne (teams, players, matches) pour le sport sélectionné."""
    cfg = SPORTS_REGISTRY[sport_nom]

    print("  Chargement des equipes...")
    team_loader = GenericTeamLoader(cfg["team_csv"], cfg["TeamAdapter"]())
    # Un seul chargement : teams_dict et teams partagent les mêmes objets Team,
    # qui seront ensuite référencés dans les participants des Match.
    teams_dict = team_loader.load_as_dict(cfg["team_key"])
    teams: list[Team] = list(teams_dict.values())

    players: list[Any] = []
    if cfg.get("player_csv") and cfg.get("PlayerAdapter"):
        print("  Chargement des joueurs...")
        player_loader = GenericPlayerLoader(cfg["player_csv"], cfg["PlayerAdapter"]())
        players = player_loader.load()

    print("  Chargement des matchs...")
    kwarg: str = cfg["match_kwarg"]
    match_adapter = cfg["MatchAdapter"](**{kwarg: teams_dict})
    match_loader = GenericMatchLoader(cfg["match_csv"], match_adapter)
    matches: list[Match] = match_loader.load()

    # Rattache les joueurs à leurs équipes pour les sports collectifs.
    # Nécessaire pour que matchs_joueur() puisse chercher dans team.players.
    ptc = cfg.get("player_team_col")
    pta = cfg.get("player_team_attr")
    if ptc and pta and players and cfg.get("player_csv"):
        try:
            df_p = pd.read_csv(cfg["player_csv"])
            teams_by_attr: dict[str, Any] = {str(getattr(t, pta, "")): t for t in teams}
            for player, (_, row) in zip(players, df_p.iterrows()):
                team_val = str(row.get(ptc, ""))
                team = teams_by_attr.get(team_val)
                if team is not None:
                    team.players.append(player)
        except Exception:
            pass

    return teams, players, matches


# ─── Helpers généraux ─────────────────────────────────────────


def _resoudre_equipe(matches: list[Match], query: str) -> str:
    """Résout full_name / abréviation / surnom vers le full_name canonique."""
    q = query.strip().lower()
    for m in matches:
        for t in m.participants:
            if t.full_name and t.full_name.lower() == q:
                return t.full_name
    for m in matches:
        for t in m.participants:
            abrev = getattr(t, "abbreviation", None)
            if abrev and abrev.lower() == q:
                return t.full_name or query
    for m in matches:
        for t in m.participants:
            nick = getattr(t, "nickname", None)
            if nick and nick.lower() == q:
                return t.full_name or query
    return query


def _afficher_details_joueur(player: Any, sport_nom: str) -> None:
    """Affiche les informations d'un joueur, adaptées au sport."""
    pseudo = getattr(player, "pseudo", None)
    nom = getattr(player, "nom", None)
    prenom = getattr(player, "prenom", None)

    titre = pseudo or f"{prenom or ''} {nom or ''}".strip() or "Inconnu"
    print(f"\n  [ {titre} ]")

    if pseudo and (nom or prenom):
        print(f"    {'Nom réel':<17}: {(prenom or '')} {(nom or '')}".rstrip())

    pays = getattr(player, "pays_de_naissance", None)
    if pays:
        labels_pays = {
            "Echecs": "Fédération",
            "CS2": "Nationalité",
            "League of Legends": "Pays de naissance",
            "Starcraft 2": "Nationalité",
            "Tennis": "Code IOC",
            "Volleyball": "Code pays",
        }
        print(f"    {labels_pays.get(sport_nom, 'Pays'):<17}: {pays}")

    role = getattr(player, "role", None)
    if role:
        labels_role = {
            "Echecs": "Titre FIDE",
            "Starcraft 2": "Race",
            "League of Legends": "Lane",
            "CS2": "Rôle",
            "Basketball": "Poste",
        }
        print(f"    {labels_role.get(sport_nom, 'Rôle'):<17}: {role}")

    dob = getattr(player, "date_de_naissance", None)
    if dob and dob.year != 1900:
        if sport_nom == "Echecs":
            print(f"    {'Année naiss.':<17}: {dob.year}")
        else:
            print(f"    {'Naissance':<17}: {dob}")

    taille = getattr(player, "taille", None)
    if taille and taille > 0:
        print(f"    {'Taille':<17}: {int(taille)} cm")

    poids = getattr(player, "poids", None)
    if poids and poids > 0:
        print(f"    {'Poids':<17}: {int(poids)} kg")


# ─── Infos joueur ─────────────────────────────────────────────


def menu_info_joueur(sport_nom: str, players: list[Any]) -> None:
    """Recherche et affichage des informations d'un joueur."""
    print(SEP)
    if not players:
        print("  Pas de donnees joueurs disponibles pour ce sport.")
        _pause()
        return

    recherche = input("  Recherche (pseudo, nom ou prenom) : ").strip().lower()
    if not recherche:
        _pause()
        return

    trouves = []
    for p in players:
        identite = " ".join(
            filter(
                None,
                [
                    (getattr(p, "pseudo", None) or ""),
                    (getattr(p, "nom", None) or ""),
                    (getattr(p, "prenom", None) or ""),
                ],
            )
        ).lower()
        if recherche in identite:
            trouves.append(p)

    if not trouves:
        print(f"\n  Aucun joueur trouve pour '{recherche}'.")
        _pause()
        return

    nb = len(trouves)
    affichage = trouves[:10]
    print(
        f"\n  {nb} joueur(s) trouve(s)"
        + (" — 10 premiers affiches" if nb > 10 else "")
        + " :"
    )
    for p in affichage:
        _afficher_details_joueur(p, sport_nom)

    _pause()


# ─── Infos équipe ─────────────────────────────────────────────


def menu_info_equipe(sport_nom: str, teams: list[Team]) -> None:
    """Recherche et affichage des informations d'une équipe."""
    print(SEP)
    query = input("  Nom, abreviation ou surnom : ").strip().lower()
    if not query:
        _pause()
        return

    trouves = []
    for t in teams:
        candidats = [
            (t.full_name or "").lower(),
            (getattr(t, "abbreviation", None) or "").lower(),
            (getattr(t, "nickname", None) or "").lower(),
        ]
        if any(query in c for c in candidats if c):
            trouves.append(t)

    if not trouves:
        print(f"\n  Aucune equipe trouvee pour '{query}'.")
        _pause()
        return

    affichage = trouves[:8]
    print(
        f"\n  {len(trouves)} equipe(s)"
        + (", 8 premieres affichees" if len(trouves) > 8 else "")
        + " :\n"
    )

    for t in affichage:
        print(f"  --- {t.full_name} ---")
        abrev = getattr(t, "abbreviation", None)
        if abrev:
            print(f"    Abreviation : {abrev}")
        nick = getattr(t, "nickname", None)
        if nick:
            print(f"    Surnom      : {nick}")
        city = getattr(t, "city", None)
        if city:
            print(f"    Ville       : {city}")
        state = getattr(t, "state", None)
        if state:
            print(f"    Etat/Region : {state}")
        country = getattr(t, "country", None)
        if country:
            print(f"    Pays        : {country}")
        region = getattr(t, "region", None)
        if region:
            print(f"    Region      : {region}")
        print()

    _pause()


# ─── Coaches ──────────────────────────────────────────────────


def menu_info_coach(sport_nom: str, cfg: dict) -> None:
    """Affichage des informations sur les coaches (CS2, LoL, Volleyball)."""
    coach_csv = cfg.get("coach_csv")
    if not coach_csv:
        print("\n  Pas de donnees coaches disponibles.")
        _pause()
        return

    print(SEP)
    recherche = (
        input("  Recherche coach (pseudo ou nom, Entree = tous) : ").strip().lower()
    )

    try:
        df = pd.read_csv(coach_csv)
    except Exception as e:
        print(f"  Erreur lecture fichier coaches : {e}")
        _pause()
        return

    resultats = []
    for _, row in df.iterrows():
        identite = " ".join(str(v) for v in row.values if pd.notna(v)).lower()
        if not recherche or recherche in identite:
            resultats.append(row)

    if not resultats:
        print(f"\n  Aucun coach trouve pour '{recherche}'.")
        _pause()
        return

    affichage = resultats[:20]
    print(
        f"\n  {len(resultats)} coach(es)"
        + (", 20 premiers affiches" if len(resultats) > 20 else "")
        + " :\n"
    )

    for row in affichage:
        pseudo = str(row["pseudo"]).strip() if pd.notna(row.get("pseudo")) else None
        nom = str(row["name"]).strip() if pd.notna(row.get("name")) else None
        equipe = str(row["team"]).strip() if pd.notna(row.get("team")) else None
        dob = (
            str(row.get("birthdate", "")).strip()
            if pd.notna(row.get("birthdate"))
            else None
        )
        nat = (
            str(row["nationality"]).strip()
            if pd.notna(row.get("nationality"))
            else str(row["country_of_birth"]).strip()
            if pd.notna(row.get("country_of_birth"))
            else str(row["country_code"]).strip()
            if pd.notna(row.get("country_code"))
            else None
        )
        role = str(row["role"]).strip() if pd.notna(row.get("role")) else None

        titre = pseudo or nom or "Inconnu"
        print(f"  [{titre}]" + (f"  {nom}" if pseudo and nom else ""))
        if equipe:
            print(f"    Equipe      : {equipe}")
        if role:
            print(f"    Role        : {role}")
        if nat:
            print(f"    Nationalite : {nat}")
        if dob:
            print(f"    Naissance   : {dob}")
        print()

    _pause()


# ─── Affichage enrichi des matchs ─────────────────────────────


def menu_matchs_badminton(cfg: dict) -> None:
    """Matchs de badminton avec infos tournoi, lieu et manche."""
    print(SEP)
    print("Filtres (Entree pour ignorer)")
    date_debut_str = input("  Date debut   (AAAA-MM-JJ) : ").strip()
    date_fin_str = input("  Date fin     (AAAA-MM-JJ) : ").strip()
    filtre_tournoi = input("  Filtre tournoi             : ").strip().lower()

    try:
        df = pd.read_csv(cfg["match_csv"])
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        if date_debut_str:
            df = df[df["date"] >= pd.Timestamp(date_debut_str)]
        if date_fin_str:
            df = df[df["date"] <= pd.Timestamp(date_fin_str)]
        if filtre_tournoi:
            df = df[df["tournament"].str.lower().str.contains(filtre_tournoi, na=False)]

        df = df.sort_values("date")

        if df.empty:
            print("\n  Aucun match trouve.")
            _pause()
            return

        affichage = df.head(30)
        print(f"\n  {len(df)} match(s) — affichage des {len(affichage)} premiers :\n")

        for _, row in affichage.iterrows():
            date = (
                row["date"].strftime("%Y-%m-%d") if pd.notna(row.get("date")) else "?"
            )
            tournoi = str(row.get("tournament", "?"))
            ville = str(row.get("city", "")) if pd.notna(row.get("city")) else ""
            pays = str(row.get("country", "")) if pd.notna(row.get("country")) else ""
            lieu = f"{ville}, {pays}" if ville and pays else (ville or pays)
            tour = str(row.get("round", "")) if pd.notna(row.get("round")) else ""
            p1 = str(row.get("player_1", "?"))
            p2 = str(row.get("player_2", "?"))
            winner = str(row.get("winner", "?"))
            scores = [
                str(row.get(f"game_{i}_score", ""))
                for i in (1, 2, 3)
                if pd.notna(row.get(f"game_{i}_score"))
                and str(row.get(f"game_{i}_score", "")).strip()
            ]
            score_str = "  |  ".join(scores)

            print(f"  [{date}]  {p1}  vs  {p2}")
            print(
                f"    Vainqueur : {winner}" + (f"   ({score_str})" if score_str else "")
            )
            print(f"    {tournoi}  |  {lieu}  |  {tour}")
            print()

        if len(df) > 30:
            print(f"  ... et {len(df) - 30} autres matchs.")

    except Exception as e:
        print(f"  Erreur : {e}")

    _pause()


def menu_matchs_footballcl(cfg: dict) -> None:
    """Matchs de Football (Champions League) avec phase et groupe."""
    print(SEP)
    print("Filtres (Entree pour ignorer)")
    date_debut_str = input("  Date debut   (AAAA-MM-JJ) : ").strip()
    date_fin_str = input("  Date fin     (AAAA-MM-JJ) : ").strip()
    filtre_phase = input("  Filtre phase (group/round) : ").strip().lower()

    try:
        df = pd.read_csv(cfg["match_csv"])
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        if date_debut_str:
            df = df[df["date"] >= pd.Timestamp(date_debut_str)]
        if date_fin_str:
            df = df[df["date"] <= pd.Timestamp(date_fin_str)]
        if filtre_phase:
            phase_col = df.get("phase", df.get("round", None))
            if phase_col is not None:
                df = df[phase_col.str.lower().str.contains(filtre_phase, na=False)]

        df = df.sort_values("date")

        if df.empty:
            print("\n  Aucun match trouve.")
            _pause()
            return

        affichage = df.head(40)
        print(f"\n  {len(df)} match(s) — affichage des {len(affichage)} premiers :\n")

        for _, row in affichage.iterrows():
            date = (
                row["date"].strftime("%Y-%m-%d") if pd.notna(row.get("date")) else "?"
            )
            phase = (
                str(row.get("phase", "")).strip() if pd.notna(row.get("phase")) else ""
            )
            groupe = (
                str(row.get("group", "")).strip() if pd.notna(row.get("group")) else ""
            )
            rnd = (
                str(row.get("round", "")).strip() if pd.notna(row.get("round")) else ""
            )
            eq1 = str(row.get("team_home", "?"))
            eq2 = str(row.get("team_away", "?"))
            s1 = str(row.get("score_team_home", "?"))
            s2 = str(row.get("score_team_away", "?"))
            contexte = "  |  ".join(
                filter(None, [phase, rnd, f"Groupe {groupe}" if groupe else ""])
            )
            print(f"  [{date}]  {eq1}  {s1} - {s2}  {eq2}")
            if contexte:
                print(f"    {contexte}")

        if len(df) > 40:
            print(f"\n  ... et {len(df) - 40} autres matchs.")

    except Exception as e:
        print(f"  Erreur : {e}")

    _pause()


def menu_tournois_tennis(cfg: dict, teams: list[Team]) -> None:
    """Vue par tournoi pour le tennis : liste les tournois avec surface et stats."""
    print(SEP)
    filtre = input("  Filtre nom de tournoi (Entree = tous) : ").strip().lower()

    try:
        df = pd.read_csv(cfg["match_csv"])

        if filtre:
            df = df[df["tourney_name"].str.lower().str.contains(filtre, na=False)]

        if df.empty:
            print("\n  Aucun tournoi trouve.")
            _pause()
            return

        # Résumé par tournoi
        tournois = (
            df.groupby(["tourney_name", "surface"])
            .agg(nb_matchs=("winner_id", "count"))
            .reset_index()
            .sort_values("tourney_name")
        )

        print(f"\n  {len(tournois)} tournoi(s) :\n")
        for _, t in tournois.iterrows():
            print(
                f"  {t['tourney_name']:<40}  {t['surface']:<10}  {t['nb_matchs']} matchs"
            )

        # Optionnel : détail d'un tournoi
        print()
        detail = input(
            "  Entrer un nom de tournoi pour le detail (Entree pour ignorer) : "
        ).strip()
        if detail:
            sub = df[
                df["tourney_name"].str.lower().str.contains(detail.lower(), na=False)
            ]
            # Construire lookup id → nom depuis teams
            id_to_nom = {t.id: t.full_name for t in teams if t.id is not None}
            print(f"\n  Matchs pour '{detail}' :\n")
            for _, row in sub.head(30).iterrows():
                winner = id_to_nom.get(
                    int(row.get("winner_id", 0)), str(row.get("winner_id", "?"))
                )
                loser = id_to_nom.get(
                    int(row.get("loser_id", 0)), str(row.get("loser_id", "?"))
                )
                score = str(row.get("score", "?"))
                rnd = str(row.get("round", "?"))
                print(f"    {rnd:<12} {winner} def. {loser}  {score}")

    except Exception as e:
        print(f"  Erreur : {e}")

    _pause()


# ─── Menus génériques ─────────────────────────────────────────


def menu_matchs(matches: list[Match]) -> None:
    """Affiche les matchs avec filtre optionnel par période."""
    print(SEP)
    print("Filtre par date (Entree pour ignorer)")
    date_debut_str = input("  Date debut (AAAA-MM-JJ) : ").strip()
    date_fin_str = input("  Date fin   (AAAA-MM-JJ) : ").strip()

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
        _pause()
        return

    affichage = filtres[:50]
    print(f"\n{len(filtres)} match(s) - affichage des {len(affichage)} premiers :\n")
    for i, m in enumerate(affichage, 1):
        p1, p2 = m.participants[0], m.participants[1]
        s1, s2 = m.scores[p1], m.scores[p2]
        print(f"  {i:3}. [{m.date_match}]  {p1.full_name}  {s1} - {s2}  {p2.full_name}")

    if len(filtres) > 50:
        print(f"\n  ... et {len(filtres) - 50} autres matchs non affiches.")

    _pause()


def menu_podium(matches: list[Match], sport_nom: str) -> None:
    """Affiche le podium (top 3) par nombre de victoires."""
    print(SEP)
    print(f"PODIUM - {sport_nom}\n")

    classement = podium(matches, n=3)

    if not classement:
        print("Pas assez de donnees pour etablir un podium.")
        _pause()
        return

    medailles = ["1er", "2eme", "3eme"]
    for i, (equipe, nb) in enumerate(classement):
        print(f"  {medailles[i]} : {equipe.full_name}  ({nb} victoire(s))")

    plot_podium(matches, sport_nom, n=10)
    _pause()


def menu_matchs_joueur(matches: list[Match]) -> None:
    """Recherche des matchs pour un joueur (nom complet ou partie du nom)."""
    print(SEP)
    query = input("  Nom du joueur (ou partie du nom) : ").strip()

    if not query:
        print("  Recherche vide.")
        _pause()
        return

    trouves = matchs_joueur(matches, query)

    if not trouves:
        print(f"\n  Aucun match trouve pour '{query}'.")
        _pause()
        return

    trouves.sort(key=lambda m: m.date_match)
    print(f"\n  {len(trouves)} match(s) pour '{query}' :\n")
    for m in trouves:
        p1, p2 = m.participants[0], m.participants[1]
        s1, s2 = m.scores[p1], m.scores[p2]
        print(f"  [{m.date_match}]  {p1.full_name}  {s1} - {s2}  {p2.full_name}")

    _pause()


def menu_victoires_equipe(matches: list[Match]) -> None:
    """Affiche le nombre de victoires d'une équipe (full_name, abrév. ou surnom)."""
    print(SEP)
    nom = input("  Nom / abreviation de l'equipe : ").strip()
    if not nom:
        print("Nom requis.")
        _pause()
        return

    nom_resolu = _resoudre_equipe(matches, nom)
    if nom_resolu != nom:
        print(f"  (Equipe identifiee : {nom_resolu})")

    nb_v = victoires_equipe(matches, nom_resolu)
    nb_total = len(matchs_equipe(matches, nom_resolu))

    if nb_total == 0:
        print(f"\n  Equipe '{nom}' introuvable dans les matchs.")
    else:
        print(f"\n  {nom_resolu}")
        print(f"    Matchs joues : {nb_total}")
        print(f"    Victoires    : {nb_v}")
        print(f"    Autres       : {nb_total - nb_v}")
    plot_bilan_equipe(matches, nom_resolu)

    _pause()


def menu_stats_descriptives(matches: list[Match]) -> None:
    """Statistiques descriptives (pts marqués/encaissés) pour une équipe."""
    print(SEP)
    nom = input("  Nom / abreviation de l'equipe : ").strip()
    if not nom:
        print("Nom requis.")
        _pause()
        return

    nom_resolu = _resoudre_equipe(matches, nom)
    if nom_resolu != nom:
        print(f"  (Equipe identifiee : {nom_resolu})")

    stats = stats_descriptives(matches, nom_resolu)

    if "erreur" in stats:
        print("\n" + stats["erreur"])
        _pause()
        return

    print(f"\n  Stats pour '{nom_resolu}' :\n")
    print(f"    Matchs joues         : {stats['nb_matchs']}")
    print(f"    Victoires            : {stats['nb_victoires']}")
    print(f"    Defaites             : {stats['nb_defaites']}")
    print(f"    Nuls                 : {stats['nb_nuls']}")
    print(f"    Taux de victoire     : {stats['pct_victoires']} %")
    print(f"    Moy. pts marques     : {stats['moy_pts_marques']}")
    print(f"    Moy. pts encaisses   : {stats['moy_pts_encaisses']}")
    print(f"    Meilleur score       : {stats['max_score']}")
    print(f"    Pire score           : {stats['min_score']}")

    _pause()


# ─── Connexion ────────────────────────────────────────────────


def connexion() -> tuple[str | None, bool]:
    """Demande login/mdp. Retourne (login, is_admin) ou (None, False) si invité."""
    _clear()
    print("=" * 60)
    print("   Bienvenue dans l'application de statistiques sportives !")
    print("=" * 60)
    print()
    print("  Consultez les résultats et statistiques de vos sports")
    print("  favoris : basketball, football, tennis, échecs et plus.")
    print()
    print("  Connectez-vous en tant qu'administrateur avec votre")
    print("  login et mot de passe, ou appuyez sur Entrée pour")
    print("  continuer en tant qu'utilisateur (consultation libre).")
    print()
    print("-" * 60)
    login = input("  Login (Entrée pour continuer) : ").strip()
    if not login:
        print("  Connexion en tant qu'utilisateur (lecture seule).")
        return None, False
    mdp = input("  Mot de passe                  : ").strip()
    if _UTILISATEURS.get(login) == mdp:
        is_admin = login in _ADMINS
        role = "ADMINISTRATEUR" if is_admin else "utilisateur"
        print(f"  Bienvenue {login} ({role}).")
        return login, is_admin
    print("  Identifiants incorrects. Connexion en tant qu'utilisateur.")
    return None, False


# ─── Persistance sports personnalisés ─────────────────────────


def _charger_sports_custom() -> dict:
    """Charge les sports personnalisés depuis le fichier JSON."""
    if _CUSTOM_SPORTS_FILE.exists():
        try:
            return json.loads(_CUSTOM_SPORTS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _sauver_sports_custom(data: dict) -> None:
    """Sauvegarde les sports personnalisés dans le fichier JSON."""
    _CUSTOM_SPORTS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _creer_entree_registre(cfg_json: dict) -> dict:
    """
    Construit une entrée compatible avec SPORTS_REGISTRY depuis une config JSON.
    Utilise les adaptateurs génériques configurables.
    """
    from Model.sport import Sport
    from Parsers.Adapters.generique import (
        GenericTeamAdapter,
        GenericPlayerAdapter,
        GenericMatchAdapter,
    )

    sport_obj = Sport(
        cfg_json["nom_sport"],
        cfg_json.get("categorie", "Sport"),
        cfg_json.get("nb_joueurs", 2),
        cfg_json.get("description", "Sport personnalise"),
        cfg_json.get("sport_en_equipe", True),
    )

    # Config partagée avec le sport instancié
    team_cfg = {**cfg_json, "sport_obj": sport_obj}
    player_cfg = {**cfg_json, "sport_obj": sport_obj}
    match_cfg = {**cfg_json, "sport_obj": sport_obj}

    # Factories sans argument (signature attendue par charger_donnees)
    def TeamAdapterFactory() -> GenericTeamAdapter:
        return GenericTeamAdapter(team_cfg)

    def PlayerAdapterFactory() -> GenericPlayerAdapter:
        return GenericPlayerAdapter(player_cfg)

    # Classe partielle pour le MatchAdapter (reçoit equipes= en kwarg)
    class MatchAdapterFactory:
        def __init__(self, equipes: dict) -> None:
            self._inner = GenericMatchAdapter(equipes, match_cfg)

        def adapt(self, row: Any) -> dict | None:
            return self._inner.adapt(row)

    entree: dict = {
        "team_csv": _resolve_csv_path(cfg_json["team_csv"]),
        "match_csv": _resolve_csv_path(cfg_json["match_csv"]),
        "TeamAdapter": TeamAdapterFactory,
        "MatchAdapter": MatchAdapterFactory,
        "match_kwarg": "equipes",
        "team_key": cfg_json.get("team_key", "full_name"),
        "sport_en_equipe": cfg_json.get("sport_en_equipe", True),
    }
    if cfg_json.get("player_csv"):
        entree["player_csv"] = _resolve_csv_path(cfg_json["player_csv"])
        entree["PlayerAdapter"] = PlayerAdapterFactory
    return entree


# ─── Helpers CSV ──────────────────────────────────────────────


def _lire_colonnes(csv_path: str) -> list[str]:
    """Retourne les colonnes d'un CSV sans le charger entièrement."""
    try:
        df = pd.read_csv(csv_path, nrows=0, sep=None, engine="python")
        return list(df.columns)
    except Exception as e:
        print(f"  Impossible de lire '{csv_path}' : {e}")
        return []


def _demander_col(
    colonnes: list[str], label: str, obligatoire: bool = True
) -> str | None:
    """Demande une colonne parmi la liste (colonnes affichées une seule fois avant)."""
    while True:
        val = input(f"    {label}: ").strip()
        if not val:
            if not obligatoire:
                return None
            print("    (champ obligatoire)")
        elif val in colonnes:
            return val
        else:
            print(f"    '{val}' inconnu. Options: {', '.join(colonnes)}")


def _copier_csv(src: str, sport_slug: str, dest_name: str) -> str:
    """Copie un CSV dans data/<sport_slug>/ et retourne le chemin relatif."""
    dest_dir = _PROJECT_ROOT / "data" / sport_slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / dest_name
    shutil.copy2(src, dest)
    return str(Path("data") / sport_slug / dest_name)


# ─── Wizard admin : ajouter un sport ──────────────────────────


def admin_ajouter_sport(sports_custom: dict) -> None:
    """Wizard simplifié : CSV copiés dans data/, chemins relatifs sauvegardés."""
    print("\n" + SEP)
    print("AJOUT D'UN NOUVEAU SPORT\n")

    nom = input("  Nom du sport : ").strip()
    if not nom:
        return
    if nom in SPORTS_REGISTRY or nom in sports_custom:
        print(f"  '{nom}' existe deja.")
        return

    slug = nom.lower().replace(" ", "_").replace("(", "").replace(")", "")
    cfg: dict = {
        "nom_sport": nom,
        "sport_en_equipe": input("  Sport collectif ? (o/n) : ").strip().lower() == "o",
    }

    # ── CSV Équipes ───────────────────────────────────────────
    print("\n  -- Fichier equipes --")
    while True:
        team_src = input(
            "  Chemin complet du fichier CSV equipes (ou joueurs si sport individuel): "
            ).strip()
        if not team_src:
            print("  Abandon.")
            return
        cols = _lire_colonnes(team_src)
        if cols:
            break
        print(
            "  Fichier introuvable ou illisible. Retapez le chemin (Entree=annuler) :"
        )
    print(f"  Colonnes detectees : {', '.join(cols)}")
    cfg["col_full_name"] = _demander_col(cols, "Colonne NOM d'equipe (obligatoire)")
    cfg["col_abbreviation"] = _demander_col(
        cols, "Colonne abreviation      (Entree=ignorer)", False
    )
    cfg["col_country"] = _demander_col(
        cols, "Colonne pays             (Entree=ignorer)", False
    )
    cfg["col_city"] = _demander_col(
        cols, "Colonne ville            (Entree=ignorer)", False
    )
    cfg["col_region"] = _demander_col(
        cols, "Colonne region           (Entree=ignorer)", False
    )

    print("\n  Comment match.csv identifie les equipes ?")
    print(
        "  Si match.csv utilise un ID numerique (ex: team_id), indiquez la colonne ID de team.csv."
    )
    print("  Si match.csv utilise les noms ou abreviations, laissez vide.")
    col_id = _demander_col(
        cols, "Colonne ID equipe dans team.csv (Entree=ignorer)", False
    )
    if col_id:
        cfg["col_id"] = col_id
        cfg["team_key"] = "id"
    else:
        default_key = cfg.get("col_abbreviation") or cfg["col_full_name"]
        rep = input(f"  Colonne cle pour les noms [{default_key}] : ").strip()
        cfg["team_key"] = rep if rep in cols else default_key

    cfg["team_csv"] = _copier_csv(team_src, slug, "team.csv")

    # ── CSV Joueurs (optionnel) ───────────────────────────────
    print("\n  -- Fichier joueurs (optionnel) --")
    while True:
        player_src = input("  Chemin complet (Entree=ignorer) : ").strip()
        if not player_src:
            break
        pcols = _lire_colonnes(player_src)
        if pcols:
            print(f"  Colonnes detectees : {', '.join(pcols)}")
            cfg["col_nom"] = _demander_col(pcols, "Colonne NOM (obligatoire)")
            cfg["col_prenom"] = _demander_col(
                pcols, "Colonne prenom           (Entree=ignorer)", False
            )
            cfg["col_pseudo"] = _demander_col(
                pcols, "Colonne pseudo           (Entree=ignorer)", False
            )
            cfg["col_pays"] = _demander_col(
                pcols, "Colonne pays             (Entree=ignorer)", False
            )
            cfg["col_role"] = _demander_col(
                pcols, "Colonne role/poste       (Entree=ignorer)", False
            )
            cfg["col_date_naissance"] = _demander_col(
                pcols, "Colonne date naissance   (Entree=ignorer)", False
            )
            cfg["col_taille"] = _demander_col(
                pcols, "Colonne taille cm        (Entree=ignorer)", False
            )
            cfg["player_csv"] = _copier_csv(player_src, slug, "player.csv")
            break
        print(
            "  Fichier introuvable ou illisible. Retapez le chemin (Entree=ignorer) :"
        )

    # ── CSV Matchs ────────────────────────────────────────────
    print("\n  -- Fichier matchs --")
    while True:
        match_src = input("  Chemin complet du fichier CSV matchs : ").strip()
        if not match_src:
            print("  Abandon.")
            return
        mcols = _lire_colonnes(match_src)
        if mcols:
            break
        print(
            "  Fichier introuvable ou illisible. Retapez le chemin (Entree=annuler) :"
        )
    print(f"  Colonnes detectees : {', '.join(mcols)}")
    cfg["col_team1"] = _demander_col(mcols, "Colonne equipe/joueur 1  (obligatoire)")
    cfg["col_team2"] = _demander_col(mcols, "Colonne equipe/joueur 2  (obligatoire)")
    cfg["col_score1"] = _demander_col(mcols, "Colonne score 1          (obligatoire)")
    cfg["col_score2"] = _demander_col(mcols, "Colonne score 2          (obligatoire)")
    cfg["col_date"] = _demander_col(mcols, "Colonne date AAAA-MM-JJ  (obligatoire)")
    cfg["match_csv"] = _copier_csv(match_src, slug, "match.csv")

    # ── Test de chargement ────────────────────────────────────
    print("\n  Test de chargement...")
    try:
        entree = _creer_entree_registre(cfg)
        tl = GenericTeamLoader(entree["team_csv"], entree["TeamAdapter"]())
        teams = tl.load()
        td = tl.load_as_dict(entree["team_key"])
        ml = GenericMatchLoader(entree["match_csv"], entree["MatchAdapter"](equipes=td))
        matchs = ml.load()
        print(f"  OK : {len(teams)} equipes, {len(matchs)} matchs charges.")
    except Exception as e:
        print(f"  Erreur : {e}")
        print(
            "  Verifiez les colonnes. Les fichiers ont quand meme ete copies dans data/{slug}/"
        )
        return

    sports_custom[nom] = cfg
    _sauver_sports_custom(sports_custom)
    print(f"\n  Sport '{nom}' ajoute ! Fichiers dans data/{slug}/")
    _pause()


# ─── Admin : gestion des données CSV ──────────────────────────


def _csvs_du_sport(sport_nom: str, sports_custom: dict) -> dict[str, str]:
    """Retourne {label: chemin_absolu} pour tous les CSV d'un sport."""
    cfg = SPORTS_REGISTRY.get(sport_nom) or sports_custom.get(sport_nom) or {}
    result: dict[str, str] = {}
    for key, label in [
        ("team_csv", "Equipes"),
        ("player_csv", "Joueurs"),
        ("match_csv", "Matchs"),
        ("coach_csv", "Coaches"),
    ]:
        val = cfg.get(key)
        if val:
            result[label] = _resolve_csv_path(str(val))
    return result


def _afficher_df_page(df: pd.DataFrame, titre: str, n: int = 25) -> None:
    """Affiche les n premières lignes avec numéros de ligne."""
    cols = list(df.columns)
    print(f"\n{SEP}\n{titre}  ({len(df)} lignes)\n")
    print(f"  Colonnes : {', '.join(cols)}\n")
    for i, row in df.head(n).iterrows():
        vals = "  |  ".join(f"{str(row[c])[:18]:<18}" for c in cols[:5])
        print(f"  [{i:>4}]  {vals}")
    if len(df) > n:
        print(f"\n  ... {len(df) - n} lignes non affichees (affichage limite a {n})")


def _chercher_lignes(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Recherche insensible à la casse dans toutes les colonnes."""
    mask = pd.Series(False, index=df.index)
    for col in df.columns:
        try:
            mask |= df[col].astype(str).str.contains(query, case=False, na=False)
        except Exception:
            pass
    return df[mask]


def _selectionner_ligne(df: pd.DataFrame) -> int | None:
    """Affiche le df, laisse l'utilisateur chercher puis choisir un index."""
    _afficher_df_page(df, "Donnees")
    query = input("\n  Recherche (mot-cle) ou numero de ligne directement : ").strip()
    if not query:
        return None
    if query.isdigit() and int(query) in df.index:
        return int(query)
    resultats = _chercher_lignes(df, query)
    if resultats.empty:
        print("  Aucun resultat.")
        return None
    _afficher_df_page(resultats, f"Resultats pour '{query}'")
    num = input("  Numero de ligne : ").strip()
    if num.isdigit() and int(num) in resultats.index:
        return int(num)
    print("  Numero invalide.")
    return None


def _admin_ajouter_ligne(path: str) -> None:
    df = pd.read_csv(path)
    print(f"\n  Colonnes : {', '.join(df.columns)}")
    print("  Entrez les valeurs (Entree = laisser vide) :\n")
    new_row = {col: input(f"    {col} : ").strip() for col in df.columns}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(path, index=False)
    print("  Ligne ajoutee.")


def _admin_modifier_ligne(path: str) -> None:
    df = pd.read_csv(path)
    idx = _selectionner_ligne(df)
    if idx is None:
        return
    print(f"\n  Modification ligne {idx} (Entree = garder la valeur actuelle) :\n")
    for col in df.columns:
        actuel = df.at[idx, col]
        val = input(f"    {col} [{actuel}] : ").strip()
        if val:
            df.at[idx, col] = val
    df.to_csv(path, index=False)
    print("  Modifications enregistrees.")


def _admin_supprimer_ligne(path: str) -> None:
    df = pd.read_csv(path)
    idx = _selectionner_ligne(df)
    if idx is None:
        return
    print("\n  Ligne a supprimer :")
    for col in df.columns:
        print(f"    {col} : {df.at[idx, col]}")
    if input("\n  Confirmer ? (o/n) : ").strip().lower() == "o":
        df = df.drop(index=idx).reset_index(drop=True)
        df.to_csv(path, index=False)
        print("  Ligne supprimee.")
    else:
        print("  Annule.")


def _admin_gerer_fichier(path: str, label: str) -> None:
    """Sous-menu : voir / ajouter / modifier / supprimer dans un CSV."""
    while True:
        print(f"\n{SEP}\nFICHIER  {label}\n")
        print("  1. Voir les donnees")
        print("  2. Ajouter une ligne")
        print("  3. Modifier une ligne")
        print("  4. Supprimer une ligne")
        print("  0. Retour")
        choix = input("\n> ").strip()
        try:
            if choix == "1":
                _afficher_df_page(pd.read_csv(path), label, n=30)
                _pause()
            elif choix == "2":
                _admin_ajouter_ligne(path)
                _pause()
            elif choix == "3":
                _admin_modifier_ligne(path)
                _pause()
            elif choix == "4":
                _admin_supprimer_ligne(path)
                _pause()
            elif choix == "0":
                break
            else:
                print("  Choix invalide.")
        except Exception as e:
            print(f"  Erreur : {e}")


def admin_gerer_donnees(sports_custom: dict) -> None:
    """Permet à l'admin de gérer les données CSV de n'importe quel sport."""
    tous = list(SPORTS_REGISTRY.keys()) + list(sports_custom.keys())
    print(f"\n{SEP}\nGESTION DES DONNEES — choisir un sport\n")
    for i, nom in enumerate(tous, 1):
        tag = "[custom] " if nom in sports_custom else "[integre]"
        print(f"  {i:2}. {tag} {nom}")
    print("   0. Retour")

    choix = input("\n> ").strip()
    if choix == "0" or not choix.isdigit():
        return
    idx = int(choix) - 1
    if not (0 <= idx < len(tous)):
        print("  Choix invalide.")
        return

    sport_nom = tous[idx]
    csvs = _csvs_du_sport(sport_nom, sports_custom)
    if not csvs:
        print("  Aucun fichier CSV trouve pour ce sport.")
        _pause()
        return

    while True:
        print(f"\n{SEP}\nFICHIERS  {sport_nom}\n")
        items = list(csvs.items())
        for i, (label, path) in enumerate(items, 1):
            print(f"  {i}. {label}  ({path})")
        print("  0. Retour")
        c = input("\n> ").strip()
        if c == "0":
            break
        if c.isdigit() and 1 <= int(c) <= len(items):
            label, path = items[int(c) - 1]
            _admin_gerer_fichier(path, f"{sport_nom} / {label}")
        else:
            print("  Choix invalide.")


def admin_supprimer_sport(sports_custom: dict) -> None:
    """Supprime un sport personnalisé (seuls les sports ajoutés peuvent être supprimés)."""
    print("\n" + SEP)
    if not sports_custom:
        print("  Aucun sport personnalise a supprimer.")
        _pause()
        return
    print("  Sports personnalises :")
    for nom in sports_custom:
        print(f"    - {nom}")
    nom = input("\n  Nom du sport a supprimer : ").strip()
    if nom in sports_custom:
        del sports_custom[nom]
        _sauver_sports_custom(sports_custom)
        print(f"  '{nom}' supprime.")
    else:
        print(f"  '{nom}' introuvable.")
    _pause()


def menu_stats_avancees_basket(cfg: dict, matches: list[Match]) -> None:
    """Stats avancées d'une équipe Basketball choisie par l'utilisateur."""
    print(SEP)
    nom = input("  Nom / abreviation de l'equipe : ").strip()
    if not nom:
        print("Nom requis.")
        _pause()
        return

    nom_resolu = _resoudre_equipe(matches, nom)
    if nom_resolu != nom:
        print(f"  (Equipe identifiee : {nom_resolu})")

    print("\nCalcul des stats avancees...")
    try:
        df = calculer_stats_basket(cfg["match_csv"], cfg["team_csv"])
    except Exception as exc:
        print(f"Erreur lors du calcul : {exc}")
        _pause()
        return

    # Recherche de l'équipe dans le DataFrame (full_name ou abbreviation)
    mask = (df["full_name"].str.lower() == nom_resolu.lower()) | (
        df["abbreviation"].str.lower() == nom_resolu.lower()
    )
    if not mask.any():
        # Deuxième tentative : correspondance partielle sur full_name
        mask = df["full_name"].str.lower().str.contains(nom_resolu.lower(), na=False)
    if not mask.any():
        print(f"  Equipe '{nom_resolu}' introuvable dans les statistiques.")
        _pause()
        return

    row = df[mask].iloc[0]
    rang = int(df[mask].index[0]) + 1  # rang dans le classement NetRtg

    # ── Affichage texte ────────────────────────────────────────
    print(f"\n{SEP}")
    print(f"STATS AVANCEES  —  {row['full_name']}  ({row['abbreviation']})")
    print(f"  {row['city']}, {row['state']}   |   {int(row['nb_matchs'])} matchs")
    print(f"  Rang NetRtg : {rang} / {len(df)}")
    print()
    print("  TRADITIONNELLES (moyennes par match)")
    print(
        f"    PTS : {row['pts_pg']:>6.1f}"
        f"   REB : {row['reb_pg']:>5.1f}"
        f"   AST : {row['ast_pg']:>5.1f}"
    )
    print(
        f"    STL : {row['stl_pg']:>6.1f}"
        f"   BLK : {row['blk_pg']:>5.1f}"
        f"   TOV : {row['tov_pg']:>5.1f}"
    )
    print()
    print("  AVANCEES")
    print(
        f"    eFG%   : {row['efg_pct'] * 100:>5.1f}%   (qualite des tirs avec bonus 3pts)"
    )
    print(f"    TS%    : {row['ts_pct'] * 100:>5.1f}%   (efficacite reelle tirs + LF)")
    print(f"    AST/TO : {row['ast_tov']:>5.2f}    (ratio passes decisives / pertes)")
    print(f"    OREB%  : {row['oreb_pct'] * 100:>5.1f}%   (% rebonds offensifs captes)")
    print(f"    DREB%  : {row['dreb_pct'] * 100:>5.1f}%   (% rebonds defensifs captes)")
    print()
    print("  RATINGS (pour 100 possessions)")
    print(
        f"    OffRtg : {row['off_rtg']:>6.1f}"
        f"   DefRtg : {row['def_rtg']:>6.1f}"
        f"   NetRtg : {row['net_rtg']:>+6.1f}"
    )
    print(f"    Pace   : {row['pace']:>6.1f}   (possessions par 48 min)")
    print()
    print("  FOUR FACTORS")
    print(
        f"    eFG%   : {row['efg_f'] * 100:>5.1f}%   TOV%   : {row['tov_pct'] * 100:>5.1f}%"
    )
    print(f"    OREB%  : {row['oreb_f'] * 100:>5.1f}%   FTR    : {row['ftr']:>5.3f}")

    # ── Dashboard matplotlib ───────────────────────────────────
    try:
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec
    except ImportError:
        print("\n[matplotlib non installe — graphique indisponible]")
        _pause()
        return

    ligue_med = df.median(numeric_only=True)

    fig = plt.figure(figsize=(14, 9))
    fig.suptitle(
        f"Dashboard  {row['full_name']}  —  rang NetRtg {rang}/{len(df)}",
        fontsize=13,
        fontweight="bold",
    )
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.5, wspace=0.4)

    # 1. Stats traditionnelles vs médiane ligue
    ax1 = fig.add_subplot(gs[0, 0])
    trad_labels = ["PTS", "REB", "AST", "STL", "BLK", "TOV"]
    trad_cols = ["pts_pg", "reb_pg", "ast_pg", "stl_pg", "blk_pg", "tov_pg"]
    team_vals = [float(row[c]) for c in trad_cols]
    ligue_vals = [float(ligue_med[c]) for c in trad_cols]
    x = range(len(trad_labels))
    w = 0.35
    ax1.bar(
        [xi - w / 2 for xi in x],
        team_vals,
        width=w,
        label=row["abbreviation"],
        color="#3498db",
        alpha=0.85,
    )
    ax1.bar(
        [xi + w / 2 for xi in x],
        ligue_vals,
        width=w,
        label="Médiane ligue",
        color="#bdc3c7",
        alpha=0.85,
    )
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(trad_labels, fontsize=8)
    ax1.set_title("Traditionnelles vs ligue")
    ax1.legend(fontsize=7)

    # 2. Ratings : OffRtg / DefRtg / NetRtg vs médiane
    ax2 = fig.add_subplot(gs[0, 1])
    rtg_labels = ["OffRtg", "DefRtg", "NetRtg"]
    rtg_cols = ["off_rtg", "def_rtg", "net_rtg"]
    t_vals = [float(row[c]) for c in rtg_cols]
    l_vals = [float(ligue_med[c]) for c in rtg_cols]
    x2 = range(len(rtg_labels))
    ax2.bar(
        [xi - w / 2 for xi in x2],
        t_vals,
        width=w,
        label=row["abbreviation"],
        color="#2ecc71",
        alpha=0.85,
    )
    ax2.bar(
        [xi + w / 2 for xi in x2],
        l_vals,
        width=w,
        label="Médiane ligue",
        color="#bdc3c7",
        alpha=0.85,
    )
    ax2.set_xticks(list(x2))
    ax2.set_xticklabels(rtg_labels, fontsize=8)
    ax2.set_title("Ratings vs ligue")
    ax2.legend(fontsize=7)

    # 3. Four Factors vs médiane ligue
    ax3 = fig.add_subplot(gs[1, 0])
    ff_labels = ["eFG%", "TOV%", "OREB%", "FTR"]
    ff_cols = ["efg_f", "tov_pct", "oreb_f", "ftr"]
    t_ff = [float(row[c]) * 100 for c in ff_cols]
    l_ff = [float(ligue_med[c]) * 100 for c in ff_cols]
    x3 = range(len(ff_labels))
    ax3.bar(
        [xi - w / 2 for xi in x3],
        t_ff,
        width=w,
        label=row["abbreviation"],
        color="#e67e22",
        alpha=0.85,
    )
    ax3.bar(
        [xi + w / 2 for xi in x3],
        l_ff,
        width=w,
        label="Médiane ligue",
        color="#bdc3c7",
        alpha=0.85,
    )
    ax3.set_xticks(list(x3))
    ax3.set_xticklabels(ff_labels, fontsize=8)
    ax3.set_title("Four Factors vs ligue (%)")
    ax3.legend(fontsize=7)

    # 4. Position dans le classement NetRtg (toutes équipes)
    ax4 = fig.add_subplot(gs[1, 1])
    colors_net = [
        "#e74c3c" if a != row["abbreviation"] else "#2ecc71" for a in df["abbreviation"]
    ]
    ax4.barh(
        list(range(len(df))),
        df["net_rtg"].tolist(),
        color=colors_net,
        edgecolor="white",
        linewidth=0.3,
    )
    ax4.set_yticks(list(range(len(df))))
    ax4.set_yticklabels(df["abbreviation"].tolist(), fontsize=6)
    ax4.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax4.set_xlabel("Net Rating")
    ax4.set_title(f"Classement ligue (surbrillance : {row['abbreviation']})")
    ax4.invert_yaxis()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    _pause()


def menu_admin(sports_custom: dict) -> None:
    """Menu réservé à l'administrateur."""
    while True:
        _clear()
        print(SEP)
        print("MENU ADMINISTRATEUR\n")
        print("  1. Ajouter un nouveau sport")
        print("  2. Supprimer un sport personnalise")
        print("  3. Lister tous les sports actifs")
        print(
            "  4. Gerer les donnees d'un sport (voir / ajouter / modifier / supprimer)"
        )
        print("  0. Retour")

        choix = input("\n> ").strip()
        if choix == "1":
            admin_ajouter_sport(sports_custom)
        elif choix == "2":
            admin_supprimer_sport(sports_custom)
        elif choix == "3":
            print("\n  Sports integres :")
            for s in SPORTS_REGISTRY:
                print(f"    [integre]  {s}")
            if sports_custom:
                print("\n  Sports personnalises :")
                for s in sports_custom:
                    print(f"    [custom]   {s}")
            _pause()
        elif choix == "4":
            admin_gerer_donnees(sports_custom)
        elif choix == "0":
            break
        else:
            print("Choix invalide.")


# ─── Sous-menus par bloc ──────────────────────────────────────


def _submenu_joueurs(sport_nom: str, players: list[Any], matches: list[Match]) -> None:
    while True:
        _clear()
        print(SEP)
        print(f"  JOUEURS  ——  {sport_nom}\n")
        print("  1. Fiche d'un joueur")
        print("  2. Matchs d'un joueur")
        print("  0. Retour")
        c = input("\n> ").strip()
        if c == "1":
            menu_info_joueur(sport_nom, players)
        elif c == "2":
            menu_matchs_joueur(matches)
        elif c == "0":
            break
        else:
            print("  Choix invalide.")


def _submenu_matchs(
    sport_nom: str, cfg: dict, matches: list[Match], teams: list[Team]
) -> None:
    while True:
        _clear()
        print(SEP)
        print(f"  MATCHS  ——  {sport_nom}\n")
        print("  1. Tous les matchs")
        print("  2. Podium (top 3 par victoires)")
        print("  3. Tableau classement general")
        if sport_nom == "Tennis":
            print("  4. Tournois et surfaces")
        print("  0. Retour")
        c = input("\n> ").strip()
        if c == "1":
            if sport_nom == "Badminton":
                menu_matchs_badminton(cfg)
            elif sport_nom == "Football (Champions League)":
                menu_matchs_footballcl(cfg)
            else:
                menu_matchs(matches)
        elif c == "2":
            menu_podium(matches, sport_nom)
        elif c == "3":
            plot_summary_tableau(matches, sport_nom)
        elif c == "4" and sport_nom == "Tennis":
            menu_tournois_tennis(cfg, teams)
        elif c == "0":
            break
        else:
            print("  Choix invalide.")


def _submenu_equipes(
    sport_nom: str,
    cfg: dict,
    teams: list[Team],
    matches: list[Match],
    collectif: bool,
    a_coaches: bool,
) -> None:
    while True:
        _clear()
        print(SEP)
        print(f"  EQUIPES  ——  {sport_nom}\n")
        print("  1. Fiche d'une equipe")
        print("  2. Victoires d'une equipe")
        if collectif:
            print("  3. Stats descriptives")
        if sport_nom == "Basketball":
            print("  4. Stats avancees (eFG%, TS%, NetRtg, dashboard)")
        if a_coaches:
            print("  5. Coaches")
        print("  0. Retour")
        c = input("\n> ").strip()
        if c == "1":
            menu_info_equipe(sport_nom, teams)
        elif c == "2":
            menu_victoires_equipe(matches)
        elif c == "3" and collectif:
            menu_stats_descriptives(matches)
        elif c == "4" and sport_nom == "Basketball":
            menu_stats_avancees_basket(cfg, matches)
        elif c == "5" and a_coaches:
            menu_info_coach(sport_nom, cfg)
        elif c == "0":
            break
        else:
            print("  Choix invalide.")


# ─── Filtrage et extraction ───────────────────────────────────


def _saisir_int(label: str) -> int | None:
    val = input(label).strip()
    if not val:
        return None
    try:
        return int(val)
    except ValueError:
        print("  (valeur ignoree — pas un entier)")
        return None


def _collecter_filtres_matchs(matches: list[Match]) -> dict:
    print(SEP)
    print("  Filtres matchs (Entree pour ignorer)\n")
    ex_date = matches[0].date_match.isoformat() if matches else "2023-01-15"
    ex_equipe = matches[0].participants[0].full_name if matches else "Lakers"
    ex_score = max(
        (
            int(s)
            for m in matches[:20]
            for s in m.scores.values()
            if str(s).lstrip("-").isdigit()
        ),
        default=100,
    )
    return {
        "date_debut": input(f"  Date debut   (ex: {ex_date})        : ").strip()
        or None,
        "date_fin": input(f"  Date fin     (ex: {ex_date})        : ").strip() or None,
        "equipe": input(f"  Equipe       (ex: {ex_equipe[:20]}) : ").strip() or None,
        "score_min": _saisir_int(f"  Score min    (ex: {ex_score})       : "),
    }


def _collecter_filtres_equipes(teams: list[Team]) -> dict:
    print(SEP)
    print("  Filtres equipes (Entree pour ignorer)\n")
    ex_nom = teams[0].full_name if teams else "Lakers"
    ex_pays = next(
        (getattr(t, "country", None) for t in teams if getattr(t, "country", None)),
        "USA",
    )
    ex_region = next(
        (getattr(t, "region", None) for t in teams if getattr(t, "region", None)),
        "Europe",
    )
    return {
        "nom": input(f"  Nom / abrev  (ex: {ex_nom[:20]}) : ").strip() or None,
        "pays": input(f"  Pays         (ex: {ex_pays})     : ").strip() or None,
        "region": input(f"  Region       (ex: {ex_region})   : ").strip() or None,
    }


def _collecter_filtres_joueurs(players: list[Any]) -> dict:
    print(SEP)
    print("  Filtres joueurs (Entree pour ignorer)\n")
    ex_nom = next(
        (getattr(p, "nom", None) for p in players if getattr(p, "nom", None)), "Federer"
    )
    ex_pays = next(
        (
            getattr(p, "pays_de_naissance", None)
            for p in players
            if getattr(p, "pays_de_naissance", None)
        ),
        "FRA",
    )
    ex_role = next(
        (getattr(p, "role", None) for p in players if getattr(p, "role", None)),
        "Forward",
    )
    return {
        "nom": input(f"  Nom / pseudo (ex: {ex_nom[:20]})  : ").strip() or None,
        "pays": input(f"  Pays         (ex: {ex_pays})      : ").strip() or None,
        "role": input(f"  Role / poste (ex: {ex_role[:20]}) : ").strip() or None,
        "sexe": input("  Sexe         (ex: M ou F)         : ").strip() or None,
    }


def _filtrer_et_afficher(
    donnees, type_donnee, fn_filtre, fn_appliquer, fn_vers_df
) -> None:
    criteres = fn_filtre()
    criteres_actifs = {k: v for k, v in criteres.items() if v is not None}
    resultat = fn_appliquer(donnees, **criteres_actifs)
    print(f"\n  {len(resultat)} {type_donnee} trouve(s) sur {len(donnees)} total.\n")
    if not resultat:
        _pause()
        return
    df = fn_vers_df(resultat)
    print(df.head(20).to_string(index=False))
    if len(resultat) > 20:
        print(
            f"\n  ... {len(resultat) - 20} ligne(s) supplementaire(s) non affichee(s)."
        )
    print()
    if input("  Exporter en CSV ? (o/n) : ").strip().lower() == "o":
        file = input("  Nom du fichier (ex: export.csv) : ").strip()
        chemin = input(
            r"  Chemin complet du fichier à sauvegarder (ex: C:\Users\Moi\Documents) : "
            ).strip()
        if not file.endswith(".csv"):
            file += ".csv"
        chemin_complet = os.path.join(chemin, file)
        try:
            df.to_csv(chemin_complet, index=False, encoding="utf-8-sig")
            print(f"  Fichier sauvegarde : {chemin_complet}")
        except Exception as e:
            print(f"  Erreur export : {e}")
    _pause()


def _submenu_filtrage(sport_nom, matches, teams, players) -> None:
    while True:
        _clear()
        print(SEP)
        print(f"  FILTRER ET EXTRAIRE  ——  {sport_nom}\n")
        print("  1. Filtrer les matchs")
        print("  2. Filtrer les equipes")
        print("  3. Filtrer les joueurs")
        print("  0. Retour")
        c = input("\n> ").strip()
        if c == "1":
            _filtrer_et_afficher(
                donnees=matches,
                type_donnee="matchs",
                fn_filtre=lambda: _collecter_filtres_matchs(matches),
                fn_appliquer=filtrer_matchs,
                fn_vers_df=matchs_vers_dataframe,
            )
        elif c == "2":
            _filtrer_et_afficher(
                donnees=teams,
                type_donnee="equipes",
                fn_filtre=lambda: _collecter_filtres_equipes(teams),
                fn_appliquer=filtrer_equipes,
                fn_vers_df=equipes_vers_dataframe,
            )
        elif c == "3":
            if not players:
                print("\n  Pas de joueurs disponibles pour ce sport.")
                _pause()
            else:
                _filtrer_et_afficher(
                    donnees=players,
                    type_donnee="joueurs",
                    fn_filtre=lambda: _collecter_filtres_joueurs(players),
                    fn_appliquer=filtrer_joueurs,
                    fn_vers_df=joueurs_vers_dataframe,
                )
        elif c == "0":
            break
        else:
            print("  Choix invalide.")


# ─── Menu principal d'un sport ────────────────────────────────


def menu_sport(sport_nom: str) -> None:

    cfg = SPORTS_REGISTRY[sport_nom]
    collectif: bool = cfg["sport_en_equipe"]
    a_coaches: bool = bool(cfg.get("coach_csv"))

    print(f"\nChargement de {sport_nom}...")
    teams, players, matches = charger_donnees(sport_nom)

    while True:
        _clear()
        print(SEP)
        print(f"  {sport_nom}")
        print(
            f"  {len(teams)} equipes  |  {len(players)} joueurs  |  {len(matches)} matchs\n"
        )
        print("---- Sur quelle catégorie souhaitez-vous travailler ? ---- \n")
        print("  1. Joueurs")
        print("  2. Matchs")
        print("  3. Equipes")
        print("  4. Filtrer et extraire des données")
        print("  0. Retour")

        choix = input("\n> ").strip()
        if choix == "1":
            _submenu_joueurs(sport_nom, players, matches)
        elif choix == "2":
            _submenu_matchs(sport_nom, cfg, matches, teams)
        elif choix == "3":
            _submenu_equipes(sport_nom, cfg, teams, matches, collectif, a_coaches)
        elif choix == "4":  # ← ajouter
            _submenu_filtrage(sport_nom, matches, teams, players)
        elif choix == "0":
            break
        else:
            print("  Choix invalide.")


# ─── Menu principal ───────────────────────────────────────────


def main() -> None:
    """Point d'entrée principal : connexion puis sélection du sport."""
    # Connexion (invité ou compte enregistré)
    login, is_admin = connexion()

    # Chargement des sports personnalisés persistés
    sports_custom = _charger_sports_custom()

    # Registre actif = sports intégrés + sports personnalisés
    registre_custom: dict = {}
    for nom, cfg_json in sports_custom.items():
        try:
            registre_custom[nom] = _creer_entree_registre(cfg_json)
        except Exception:
            pass  # sport mal configuré : ignoré silencieusement

    def _liste_sports() -> list[str]:
        return list(SPORTS_REGISTRY.keys()) + list(registre_custom.keys())

    while True:
        _clear()
        sports = _liste_sports()
        role_str = ("ADMIN" if is_admin else login) if login else "utilisateur"
        print("=" * 56)
        print(f"  APPLICATION SPORTIVE  [{role_str}]")
        print("=" * 56)
        print("\nChoisissez un sport :\n")
        for i, nom in enumerate(sports, 1):
            tag = "  [custom]" if nom in registre_custom else ""
            print(f"  {i:2}. {nom}{tag}")
        print()
        if is_admin:
            print("   A. Menu administrateur")
        print("   0. Quitter")

        choix = input("\n> ").strip()

        if choix == "0":
            print("Au revoir !")
            break

        if choix.upper() == "A" and is_admin:
            menu_admin(sports_custom)
            # Recharger le registre après ajout/suppression éventuel
            registre_custom.clear()
            for nom, cfg_json in sports_custom.items():
                try:
                    registre_custom[nom] = _creer_entree_registre(cfg_json)
                except Exception:
                    pass
            continue

        try:
            idx = int(choix) - 1
            if 0 <= idx < len(sports):
                sport_choisi = sports[idx]
                if sport_choisi in registre_custom:
                    # Sport personnalisé : charger via registre_custom
                    _charger_et_afficher_sport_custom(
                        sport_choisi, registre_custom[sport_choisi]
                    )
                else:
                    menu_sport(sport_choisi)
            else:
                print("Choix invalide.")
        except ValueError:
            print("Entrez un nombre.")


def _charger_et_afficher_sport_custom(sport_nom: str, entree: dict) -> None:
    """Charge et affiche le menu pour un sport personnalisé."""
    print(f"\nChargement de {sport_nom}...")
    try:
        tl = GenericTeamLoader(entree["team_csv"], entree["TeamAdapter"]())
        teams: list[Team] = tl.load()

        players: list[Any] = []
        if entree.get("player_csv") and entree.get("PlayerAdapter"):
            players = GenericPlayerLoader(
                entree["player_csv"], entree["PlayerAdapter"]()
            ).load()

        td = tl.load_as_dict(entree["team_key"])
        matches: list[Match] = GenericMatchLoader(
            entree["match_csv"], entree["MatchAdapter"](equipes=td)
        ).load()

        collectif: bool = bool(entree.get("sport_en_equipe", False))

        while True:
            _clear()
            print(SEP)
            print(f"  {sport_nom}")
            print(
                f"  {len(teams)} equipes  |  {len(players)} joueurs  |  {len(matches)} matchs\n"
            )
            print("  1. Joueurs")
            print("  2. Matchs")
            print("  3. Equipes")
            print("  0. Retour")

            c = input("\n> ").strip()
            if c == "1":
                _submenu_joueurs(sport_nom, players, matches)
            elif c == "2":
                _submenu_matchs(sport_nom, entree, matches, teams)
            elif c == "3":
                _submenu_equipes(sport_nom, entree, teams, matches, collectif, False)
            elif c == "0":
                break
            else:
                print("  Choix invalide.")
    except Exception as e:
        print(f"  Erreur : {e}")
        _pause()


if __name__ == "__main__":
    main()
