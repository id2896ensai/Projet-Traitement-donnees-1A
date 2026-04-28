from src.Parsers.generic_loaders import GenericMatchLoader, GenericTeamLoader
from src.Parsers.Adapters.FootballCL.FootballCLTeamAdapter import FootballCLTeamAdapter
from src.Parsers.Adapters.FootballCL.FootballCLMatchAdapter import FootballCLMatchAdapter


class FootballCLMatchLoader(GenericMatchLoader):
    """Wires team loading and match mapping for Football Champions League."""

    def __init__(self, match_filepath: str, team_filepath: str) -> None:
        teams = GenericTeamLoader(team_filepath, FootballCLTeamAdapter()).load_as_dict("full_name")
        adapter = FootballCLMatchAdapter(teams)
        super().__init__(match_filepath, adapter)
