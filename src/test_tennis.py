from Parsers.Loaders.genericloaders import (
    GenericTeamLoader,
    GenericPlayerLoader,
    GenericMatchLoader
)
from Parsers.Adapters.Tennis.TennisTeamAdapter import TennisTeamAdapter
from Parsers.Adapters.Tennis.TennisPlayerAdapter import TennisPlayerAdapter
from Parsers.Adapters.Tennis.TennisMatchAdapter import TennisMatchAdapter


def test_tennis():
    print("=== TEST TENNIS (ATP 2024) ===\n")

    try:
        # 1. TEAMS (une Team solo par joueur)
        team_loader = GenericTeamLoader(
            "../data/tennis/atp_players_2024.csv",
            TennisTeamAdapter()
        )
        teams = team_loader.load()
        print(f"OK {len(teams)} teams chargees")
        print("Exemple:", teams[0].__dict__)

        # 2. PLAYERS
        player_loader = GenericPlayerLoader(
            "../data/tennis/atp_players_2024.csv",
            TennisPlayerAdapter()
        )
        players = player_loader.load()
        print(f"OK {len(players)} players charges")

        # 3. MATCHES
        teams_dict = team_loader.load_as_dict("id")

        match_loader = GenericMatchLoader(
            "../data/tennis/atp_matches_2024.csv",
            TennisMatchAdapter(equipes=teams_dict)
        )
        matches = match_loader.load()
        print(f"OK {len(matches)} matchs charges")

        print("\nTEST REUSSI")

    except Exception as e:
        print("\nERREUR :", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_tennis()
