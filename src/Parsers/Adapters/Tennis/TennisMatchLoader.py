from src.Parsers.generic_loaders import GenericMatchLoader, GenericPlayerLoader
from src.Parsers.Adapters.Tennis.TennisPlayerAdapter import TennisPlayerAdapter
from src.Parsers.Adapters.Tennis.TennisMatchAdapter import TennisMatchAdapter


class TennisMatchLoader(GenericMatchLoader):
    """Wires player loading and match mapping for Tennis (ATP or WTA).

    Works for both ATP and WTA — pass the right file paths.
    """

    def __init__(self, match_filepath: str, player_filepath: str) -> None:
        players = GenericPlayerLoader(player_filepath, TennisPlayerAdapter()).load_as_dict("id")
        adapter = TennisMatchAdapter(players)
        super().__init__(match_filepath, adapter)
