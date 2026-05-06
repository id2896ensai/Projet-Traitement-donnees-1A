from Parsers.Loaders.genericloaders import GenericTeamLoader, GenericPlayerLoader, GenericMatchLoader
from Parsers.Adapters.CS2.CS2TeamAdapter import CS2TeamAdapter
from Parsers.Adapters.CS2.CS2PlayerAdapter import CS2PlayerAdapter
from Parsers.Adapters.CS2.CS2MatchAdapter import CS2MatchAdapter


def test_cs2():
    print("=== TEST CS2 ===\n")
    try:
        team_loader = GenericTeamLoader(
            "../data/counter_strike_2/team.csv",
            CS2TeamAdapter()
        )
        teams = team_loader.load()
        print(f"OK {len(teams)} teams chargees")

        player_loader = GenericPlayerLoader(
            "../data/counter_strike_2/player.csv",
            CS2PlayerAdapter()
        )
        players = player_loader.load()
        print(f"OK {len(players)} players charges")

        teams_dict = team_loader.load_as_dict("full_name")
        match_loader = GenericMatchLoader(
            "../data/counter_strike_2/match.csv",
            CS2MatchAdapter(equipes=teams_dict)
        )
        matches = match_loader.load()
        print(f"OK {len(matches)} matchs charges")
        print("\nTEST REUSSI")

    except Exception as e:
        print("\nERREUR :", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_cs2()
