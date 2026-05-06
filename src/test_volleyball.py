from Parsers.Loaders.genericloaders import (
    GenericTeamLoader,
    GenericPlayerLoader,
    GenericMatchLoader
)
from Parsers.Adapters.Volleyball.VolleyballTeamAdapter import VolleyballTeamAdapter
from Parsers.Adapters.Volleyball.VolleyballPlayerAdapter import VolleyballPlayerAdapter
from Parsers.Adapters.Volleyball.VolleyballMatchAdapter import VolleyballMatchAdapter


def test_volleyball():
    print("=== TEST VOLLEYBALL (hommes) ===\n")

    try:
        # 1. TEAMS (equipes nationales)
        team_loader = GenericTeamLoader(
            "../data/volleyball/country.csv",
            VolleyballTeamAdapter()
        )
        teams = team_loader.load()
        print(f"OK {len(teams)} teams chargees")
        print("Exemple:", teams[0].__dict__)

        # 2. PLAYERS
        player_loader = GenericPlayerLoader(
            "../data/volleyball/player_men.csv",
            VolleyballPlayerAdapter()
        )
        players = player_loader.load()
        print(f"OK {len(players)} players charges")

        # 3. MATCHES
        teams_dict = team_loader.load_as_dict("abbreviation")

        match_loader = GenericMatchLoader(
            "../data/volleyball/match_men.csv",
            VolleyballMatchAdapter(equipes=teams_dict)
        )
        matches = match_loader.load()
        print(f"OK {len(matches)} matchs charges")

        print("\nTEST REUSSI")

    except Exception as e:
        print("\nERREUR :", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_volleyball()
