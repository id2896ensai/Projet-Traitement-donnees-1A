from Parsers.Loaders.genericloaders import GenericTeamLoader, GenericMatchLoader
from Parsers.Adapters.FootballCL.FootballCLTeamAdapter import FootballCLTeamAdapter
from Parsers.Adapters.FootballCL.FootballCLMatchAdapter import FootballCLMatchAdapter


def test_footballcl():
    print("=== TEST FOOTBALL CHAMPIONS LEAGUE ===\n")
    try:
        team_loader = GenericTeamLoader(
            "../data/football_champions_league/team.csv",
            FootballCLTeamAdapter()
        )
        teams = team_loader.load()
        print(f"OK {len(teams)} teams chargees")

        teams_dict = team_loader.load_as_dict("full_name")
        match_loader = GenericMatchLoader(
            "../data/football_champions_league/match.csv",
            FootballCLMatchAdapter(equipes=teams_dict)
        )
        matches = match_loader.load()
        print(f"OK {len(matches)} matchs charges")
        print("\nTEST REUSSI")

    except Exception as e:
        print("\nERREUR :", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_footballcl()
