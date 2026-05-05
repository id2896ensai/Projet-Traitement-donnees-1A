from src.Parsers.generic_loaders import GenericMatchLoader, GenericTeamLoader
from src.Parsers.Adapters.Volleyball.VolleyballTeamAdapter import VolleyballTeamAdapter
from src.Parsers.Adapters.Volleyball.VolleyballMatchAdapter import VolleyballMatchAdapter


class VolleyballMatchLoader(GenericMatchLoader):
    """Wires team loading and match mapping for Volleyball."""

    def __init__(self, match_filepath: str, country_filepath: str) -> None:
        # Les matchs referencent les pays par leur code (ex: "USA", "ARG")
        teams = GenericTeamLoader(country_filepath, VolleyballTeamAdapter()).load_as_dict("abbreviation")
        adapter = VolleyballMatchAdapter(teams)
        super().__init__(match_filepath, adapter)
