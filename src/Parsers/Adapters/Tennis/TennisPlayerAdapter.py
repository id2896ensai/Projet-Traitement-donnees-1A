import pandas as pd

from src.Model.sports_catalogue import TENNIS


class TennisPlayerAdapter:
    """Maps an ATP or WTA player CSV row to a Player dict.

    Works for both atp_players_2024.csv and wta_players_2024.csv.

    CSV columns:
        player_id  -> id
        name_first -> prenom
        name_last  -> nom
        hand       -> (ignored or stored in role)
        dob        -> date_de_naissance  (float YYYYMMDD, can be NaN)
        ioc        -> pays_de_naissance
        height     -> taille  (in cm, can be NaN)

    Tip:
        import numpy as np
        date = datetime.datetime.strptime(f"{row['dob']:.0f}", "%Y%m%d").date()
              if not np.isnan(row["dob"]) else None
    """

    @staticmethod
    def adapt(row: pd.Series) -> dict:
        raise NotImplementedError
