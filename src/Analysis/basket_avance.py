"""
Stats avancées Basketball calculées à partir de game.csv.

Formules :
  eFG%   = (FGM + 0.5 * FG3M) / FGA
  TS%    = PTS / (2 * (FGA + 0.44 * FTA))
  AST/TO = AST / TOV  (TOV=0 → inf)
  OREB%  = OREB / (OREB + opp_DREB)
  DREB%  = DREB / (DREB + opp_OREB)
  Poss   = FGA - OREB + TOV + 0.44 * FTA
  OffRtg = 100 * PTS / Poss
  DefRtg = 100 * opp_PTS / opp_Poss
  NetRtg = OffRtg - DefRtg
  Pace   = 48 * (Poss + opp_Poss) / (2 * MIN)   (MIN = minutes jouées)
  TOV%   = TOV / (FGA + 0.44 * FTA + TOV)
  FTR    = FTA / FGA
"""

from __future__ import annotations

import pandas as pd
import numpy as np


_STATS = ["fgm", "fga", "fg3m", "fg3a", "ftm", "fta",
          "oreb", "dreb", "reb", "ast", "stl", "blk", "tov", "pts"]


def _reshape(df: pd.DataFrame) -> pd.DataFrame:
    """Transforme une ligne par match en deux lignes (home + away)."""
    home_cols = {s: f"{s}_home" for s in _STATS}
    away_cols = {s: f"{s}_away" for s in _STATS}

    home = df[["team_id_home", "team_id_away", "game_date"] +
               list(home_cols.values())].copy()
    home.columns = ["team_id", "opp_id", "game_date"] + _STATS  # type: ignore[assignment]

    away = df[["team_id_away", "team_id_home", "game_date"] +
               list(away_cols.values())].copy()
    away.columns = ["team_id", "opp_id", "game_date"] + _STATS  # type: ignore[assignment]

    return pd.concat([home, away], ignore_index=True)


def calculer_stats_basket(game_csv: str, team_csv: str) -> pd.DataFrame:
    """
    Calcule les stats traditionnelles et avancées par équipe.

    Retourne un DataFrame une ligne par équipe avec colonnes :
      full_name, abbreviation, city, state, nb_matchs,
      pts_pg, reb_pg, ast_pg, stl_pg, blk_pg, tov_pg,
      efg_pct, ts_pct, ast_tov, oreb_pct, dreb_pct,
      off_rtg, def_rtg, net_rtg, pace,
      efg_f, tov_pct, oreb_f, ftr     (Four Factors)
    Trié par net_rtg décroissant.
    """
    games = pd.read_csv(game_csv)
    teams_df = pd.read_csv(team_csv)

    long = _reshape(games)
    long = long.reset_index(drop=True)

    # Agrégats par équipe (sommes)
    agg = long.groupby("team_id")[_STATS].sum()

    # Agrégats adversaire (pour les stats défensives)
    opp_agg = long.groupby("opp_id")[_STATS].sum()
    opp_agg.index.name = "team_id"

    nb = long.groupby("team_id").size().rename("nb_matchs")

    df = agg.join(opp_agg, rsuffix="_opp").join(nb)
    df = df.reset_index()

    n = df["nb_matchs"]

    # Traditionnelles par match
    for col in ["pts", "reb", "ast", "stl", "blk", "tov"]:
        df[f"{col}_pg"] = df[col] / n

    # eFG%
    df["efg_pct"] = (df["fgm"] + 0.5 * df["fg3m"]) / df["fga"].replace(0, np.nan)

    # TS%
    denom_ts = 2 * (df["fga"] + 0.44 * df["fta"])
    df["ts_pct"] = df["pts"] / denom_ts.replace(0, np.nan)

    # AST/TOV
    df["ast_tov"] = df["ast"] / df["tov"].replace(0, np.nan)

    # Possessions (propres et adversaire)
    df["poss"]     = df["fga"] - df["oreb"] + df["tov"] + 0.44 * df["fta"]
    df["poss_opp"] = (df["fga_opp"] - df["oreb_opp"]
                      + df["tov_opp"] + 0.44 * df["fta_opp"])

    # OREB% et DREB%
    df["oreb_pct"] = df["oreb"] / (df["oreb"] + df["dreb_opp"]).replace(0, np.nan)
    df["dreb_pct"] = df["dreb"] / (df["dreb"] + df["oreb_opp"]).replace(0, np.nan)

    # Ratings
    df["off_rtg"] = 100 * df["pts"] / df["poss"].replace(0, np.nan)
    df["def_rtg"] = 100 * df["pts_opp"] / df["poss_opp"].replace(0, np.nan)
    df["net_rtg"] = df["off_rtg"] - df["def_rtg"]

    # Pace (possessions par 48 min ; on suppose ~240 min par match NBA = 5 x 48)
    total_poss = df["poss"] + df["poss_opp"]
    df["pace"] = 48 * total_poss / (2 * n * 240).replace(0, np.nan)

    # Four Factors
    df["efg_f"]   = df["efg_pct"]
    df["tov_pct"] = df["tov"] / (df["fga"] + 0.44 * df["fta"] + df["tov"]).replace(0, np.nan)
    df["oreb_f"]  = df["oreb_pct"]
    df["ftr"]     = df["fta"] / df["fga"].replace(0, np.nan)

    # Jointure noms d'équipes
    teams_df["id"] = teams_df["id"].astype(df["team_id"].dtype)
    df = df.merge(
        teams_df[["id", "full_name", "abbreviation", "city", "state"]],
        left_on="team_id", right_on="id", how="left"
    )

    cols_out = [
        "full_name", "abbreviation", "city", "state", "nb_matchs",
        "pts_pg", "reb_pg", "ast_pg", "stl_pg", "blk_pg", "tov_pg",
        "efg_pct", "ts_pct", "ast_tov", "oreb_pct", "dreb_pct",
        "off_rtg", "def_rtg", "net_rtg", "pace",
        "efg_f", "tov_pct", "oreb_f", "ftr",
    ]
    return df[cols_out].sort_values("net_rtg", ascending=False).reset_index(drop=True)
