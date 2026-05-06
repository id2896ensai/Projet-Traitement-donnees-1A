from Parsers.Loaders.genericloaders import (
    GenericTeamLoader,
    GenericPlayerLoader,
    GenericMatchLoader
)

from Parsers.Adapters.Basketball.BasketballTeamAdapter import BasketballTeamAdapter
from Parsers.Adapters.Basketball.BasketballPlayerAdapter import BasketballPlayerAdapter
from Parsers.Adapters.Basketball.BasketballMatchAdapter import BasketballMatchAdapter


def test_basketball():
    print("=== TEST BASKETBALL ===\n")

    try:
        # -------------------------
        # 1. TEAMS
        # -------------------------
        team_loader = GenericTeamLoader(
            "data/basketball/team.csv",
            BasketballTeamAdapter()
        )
        teams = team_loader.load()
        print(f"✔ {len(teams)} teams chargées")
        print("Exemple:", teams[0].__dict__)

        # -------------------------
        # 2. PLAYERS
        # -------------------------
        player_loader = GenericPlayerLoader(
            "data/basketball/player.csv",
            BasketballPlayerAdapter()
        )
        players = player_loader.load()
        print(f"✔ {len(players)} players chargés")

        # -------------------------
        # 3. MATCHES
        # -------------------------
        teams_dict = team_loader.load_as_dict("id")

        match_loader = GenericMatchLoader(
            "data/basketball/game.csv",
            BasketballMatchAdapter(teams=teams_dict)
        )
        matches = match_loader.load()
        print(f"✔ {len(matches)} games chargés")

        # -------------------------
        print("\n✅ TEST RÉUSSI")

    except Exception as e:
        print("\n❌ ERREUR :", e)


if __name__ == "__main__":
    test_basketball()