from Parsers.Loaders.genericloaders import (
    GenericTeamLoader,
    GenericPlayerLoader,
    GenericMatchLoader
)
from Parsers.Adapters.LOL.LolTeamAdapter import LolTeamAdapter
from Parsers.Adapters.LOL.LolPlayerAdapter import LolPlayerAdapter
from Parsers.Adapters.LOL.LolMatchAdapter import LolMatchAdapter


def test_lol():
    print("=== TEST LEAGUE OF LEGENDS ===\n")

    try:
        # 1. TEAMS
        team_loader = GenericTeamLoader(
            "../data/league_of_legends/team.csv",
            LolTeamAdapter()
        )
        teams = team_loader.load()
        print(f"OK {len(teams)} teams chargees")
        print("Exemple:", teams[0].__dict__)

        # 2. PLAYERS
        player_loader = GenericPlayerLoader(
            "../data/league_of_legends/player.csv",
            LolPlayerAdapter()
        )
        players = player_loader.load()
        print(f"OK {len(players)} players charges")

        # 3. MATCHES
        teams_dict = team_loader.load_as_dict("abbreviation")

        match_loader = GenericMatchLoader(
            "../data/league_of_legends/match.csv",
            LolMatchAdapter(equipes=teams_dict)
        )
        matches = match_loader.load()
        print(f"OK {len(matches)} matchs charges")

        print("\nTEST REUSSI")

    except Exception as e:
        print("\nERREUR :", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_lol()
