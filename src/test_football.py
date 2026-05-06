from Parsers.Loaders.genericloaders import GenericTeamLoader, GenericPlayerLoader, GenericMatchLoader
from Parsers.Adapters.Football.FootballTeamAdapter import FootballTeamAdapter
from Parsers.Adapters.Football.FootballPlayerAdapter import FootballPlayerAdapter
from Parsers.Adapters.Football.FootballMatchAdapter import FootballMatchAdapter


def test_football():
    print("=== TEST FOOTBALL ===\n")
    try:
        team_loader = GenericTeamLoader(
            "../data/football_european_leagues/team.csv",
            FootballTeamAdapter()
        )
        teams = team_loader.load()
        print(f"OK {len(teams)} teams chargees")

        player_loader = GenericPlayerLoader(
            "../data/football_european_leagues/player.csv",
            FootballPlayerAdapter()
        )
        players = player_loader.load()
        print(f"OK {len(players)} players charges")

        teams_dict = team_loader.load_as_dict("id")
        match_loader = GenericMatchLoader(
            "../data/football_european_leagues/match.csv",
            FootballMatchAdapter(equipes=teams_dict)
        )
        matches = match_loader.load()
        print(f"OK {len(matches)} matchs charges")
        print("\nTEST REUSSI")

    except Exception as e:
        print("\nERREUR :", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_football()
