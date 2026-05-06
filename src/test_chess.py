from Parsers.Loaders.genericloaders import (
    GenericTeamLoader,
    GenericPlayerLoader,
    GenericMatchLoader
)
from Parsers.Adapters.Chess.ChessTeamAdapter import ChessTeamAdapter
from Parsers.Adapters.Chess.ChessPlayerAdapter import ChessPlayerAdapter
from Parsers.Adapters.Chess.ChessMatchAdapter import ChessMatchAdapter


def test_chess():
    print("=== TEST CHESS ===\n")

    try:
        # 1. TEAMS (une Team solo par joueur)
        team_loader = GenericTeamLoader(
            "../data/chess/player.csv",
            ChessTeamAdapter()
        )
        teams = team_loader.load()
        print(f"OK {len(teams)} teams chargees")
        print("Exemple:", teams[0].__dict__)

        # 2. PLAYERS
        player_loader = GenericPlayerLoader(
            "../data/chess/player.csv",
            ChessPlayerAdapter()
        )
        players = player_loader.load()
        print(f"OK {len(players)} players charges")

        # 3. MATCHES
        teams_dict = team_loader.load_as_dict("full_name")

        match_loader = GenericMatchLoader(
            "../data/chess/match.csv",
            ChessMatchAdapter(equipes=teams_dict)
        )
        matches = match_loader.load()
        print(f"OK {len(matches)} matchs charges")

        print("\nTEST REUSSI")

    except Exception as e:
        print("\nERREUR :", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_chess()
