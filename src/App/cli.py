import datetime
from typing import List

from src.Analysis.podium import compute_podium
from src.Parsers.matchloader import MatchLoader

# ── Catalogue des sports ──────────────────────────────────────────────────────

TEAM_SPORTS: dict[str, str] = {
    "basketball":       "Basketball (NBA 2022-2023)",
    "football":         "Football europeen (2008-2016)",
    "football_cl":      "Football Champions League (2021-2022)",
    "lol":              "League of Legends (2025)",
    "cs2":              "Counter-Strike 2",
    "volleyball_men":   "Volleyball Hommes (JO 2024)",
    "volleyball_women": "Volleyball Femmes (JO 2024)",
}

INDIVIDUAL_SPORTS: dict[str, str] = {
    "tennis_atp":  "Tennis ATP 2024",
    "tennis_wta":  "Tennis WTA 2024",
    "chess":       "Echecs (FIDE)",
    "badminton":   "Badminton",
    "starcraft2":  "Starcraft 2",
}

# ── Helpers d'affichage ───────────────────────────────────────────────────────

_MEDALS = ["1er", "2eme", "3eme"]
_SEP = "-" * 52


def _header(title: str) -> None:
    print(f"\n{_SEP}")
    print(f"  {title}")
    print(_SEP)


def _menu(options: dict[str, str], zero_label: str = "Retour") -> str | None:
    """Display a numbered menu and return the chosen key, or None for 0."""
    keys = list(options.keys())
    for i, key in enumerate(keys, start=1):
        print(f"  {i}. {options[key]}")
    print(f"  0. {zero_label}")
    while True:
        raw = input("> ").strip()
        if raw == "0":
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(keys):
            return keys[int(raw) - 1]
        print("  Choix invalide, reessayez.")


# ── Requetes ─────────────────────────────────────────────────────────────────

def _show_podium(sport_key: str, sport_label: str) -> None:
    print(f"\n  Chargement des matchs de {sport_label}...")
    loader = MatchLoader()
    matches = loader.load_all_matches(sport_key)
    podium = compute_podium(matches, top_n=3)

    _header(f"Podium - {sport_label}")
    if not podium:
        print("  Aucun vainqueur trouve (tous les matchs sont des nuls ?).")
        return
    for rank, (participant, wins) in enumerate(podium):
        medal = _MEDALS[rank] if rank < len(_MEDALS) else f"{rank + 1}."
        print(f"  {medal:<6} {participant.full_name:<30} {wins} victoire(s)")


def _show_matches_by_date(sport_key: str, sport_label: str) -> None:
    raw = input("  Date recherchee (JJ/MM/AAAA) : ").strip()
    try:
        date = datetime.datetime.strptime(raw, "%d/%m/%Y").date()
    except ValueError:
        print("  Format invalide. Attendu : JJ/MM/AAAA")
        return

    loader = MatchLoader()
    matches = loader.load_matches_by_date(sport_key, date)

    _header(f"Matchs du {raw} - {sport_label}")
    if not matches:
        print("  Aucun match trouve a cette date.")
        return
    for m in matches:
        winner = m.get_winner()
        winner_str = f"  -> Gagnant : {winner.full_name}" if winner else "  -> Match nul"
        print(f"  {m}")
        print(winner_str)


def _show_all_matches(sport_key: str, sport_label: str) -> None:
    loader = MatchLoader()
    matches = loader.load_all_matches(sport_key)

    _header(f"Matchs - {sport_label}  (10 premiers sur {len(matches)})")
    for m in matches[:10]:
        print(f"  {m}")


# ── Navigation ────────────────────────────────────────────────────────────────

_QUERIES: dict[str, str] = {
    "podium":           "Podium - Top 3 par victoires",
    "matches_by_date":  "Matchs a une date donnee",
    "all_matches":      "Tous les matchs (10 premiers)",
}

_QUERY_HANDLERS = {
    "podium":          _show_podium,
    "matches_by_date": _show_matches_by_date,
    "all_matches":     _show_all_matches,
}


def _sport_menu(sports: dict[str, str], category_label: str) -> None:
    while True:
        _header(category_label)
        sport_key = _menu(sports)
        if sport_key is None:
            return

        sport_label = sports[sport_key]
        while True:
            _header(f"{sport_label} - Que souhaitez-vous afficher ?")
            query_key = _menu(_QUERIES)
            if query_key is None:
                break

            try:
                _QUERY_HANDLERS[query_key](sport_key, sport_label)
            except NotImplementedError:
                print(f"\n  Ce sport n'est pas encore implemente.")
                print(f"  A faire : adapter src/Parsers/Adapters/.../{sport_key}")
            except Exception as e:
                print(f"\n  Erreur inattendue : {e}")

            input("\n  [Appuyez sur Entree pour continuer]")


_CATEGORIES: dict[str, str] = {
    "team":       "Sports en equipe  (Basketball, Football, LoL...)",
    "individual": "Sports individuels (Tennis, Echecs, Badminton...)",
}


def main() -> None:
    """Entry point for the interactive CLI."""
    print("\n" + "=" * 52)
    print("   Application de resultats sportifs")
    print("=" * 52)

    while True:
        _header("Choisissez une categorie")
        choice = _menu(_CATEGORIES, zero_label="Quitter")

        if choice is None:
            print("\n  Au revoir !\n")
            break
        elif choice == "team":
            _sport_menu(TEAM_SPORTS, "Sports en equipe")
        elif choice == "individual":
            _sport_menu(INDIVIDUAL_SPORTS, "Sports individuels")
