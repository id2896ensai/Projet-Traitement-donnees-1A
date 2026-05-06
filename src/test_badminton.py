from Parsers.Loaders.genericloaders import (
    GenericTeamLoader,
    GenericPlayerLoader,
    GenericMatchLoader
)
from Parsers.Adapters.Badminton.BadmintonTeamAdapter import BadmintonTeamAdapter
from Parsers.Adapters.Badminton.BadmintonPlayerAdapter import BadmintonPlayerAdapter
from Parsers.Adapters.Badminton.BadmintonMatchAdapter import BadmintonMatchAdapter


def test_badminton():
    print("=== TEST BADMINTON ===\n")

    try:
        # 1. TEAMS (une Team solo par joueur)
        team_loader = GenericTeamLoader(
            "data/badminton/player.csv",
            BadmintonTeamAdapter()
        )
        teams = team_loader.load()
        print(f"OK {len(teams)} teams chargees")
        print("Exemple:", teams[0].__dict__)

        # 2. PLAYERS
        player_loader = GenericPlayerLoader(
            "data/badminton/player.csv",
            BadmintonPlayerAdapter()
        )
        players = player_loader.load()
        print(f"OK {len(players)} players charges")

        # 3. MATCHES
        teams_dict = team_loader.load_as_dict("full_name")

        match_loader = GenericMatchLoader(
            "data/badminton/match.csv",
            BadmintonMatchAdapter(equipes=teams_dict)
        )
        matches = match_loader.load()
        print(f"OK {len(matches)} matchs charges")

        print("\nTEST REUSSI")

    except Exception as e:
        print("\nERREUR :", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_badminton()
