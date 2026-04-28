from src.Parsers.generic_loaders import GenericMatchLoader, GenericPlayerLoader
from src.Parsers.Adapters.Badminton.BadmintonPlayerAdapter import BadmintonPlayerAdapter
from src.Parsers.Adapters.Badminton.BadmintonMatchAdapter import BadmintonMatchAdapter


class BadmintonMatchLoader(GenericMatchLoader):
    """Wires player loading and match mapping for Badminton."""

    def __init__(self, match_filepath: str, player_filepath: str) -> None:
        players = GenericPlayerLoader(player_filepath, BadmintonPlayerAdapter()).load_as_dict("full_name")
        adapter = BadmintonMatchAdapter(players)
        super().__init__(match_filepath, adapter)
