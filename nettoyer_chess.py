"""
Script de nettoyage des CSV Chess.
Transforme les noms au format  "Nom, Prenom"  en  "Nom Prenom"
dans data/chess/player.csv  (colonne 'name')
et   data/chess/match.csv   (colonnes 'player_1' et 'player_2').

Utilisation : python nettoyer_chess.py
"""
import pandas as pd
from pathlib import Path

DATA = Path(__file__).parent / "data" / "chess"


def nettoyer_colonne(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Remplace 'Nom, Prenom' par 'Nom Prenom' dans la colonne donnée."""
    df[col] = df[col].str.replace(r"^(.+?),\s+(.+)$", r"\1 \2", regex=True)
    return df


def main() -> None:
    # ---- player.csv ----
    player_path = DATA / "player.csv"
    df_players = pd.read_csv(player_path)
    avant = df_players["name"].str.contains(",", na=False).sum()
    df_players = nettoyer_colonne(df_players, "name")
    df_players.to_csv(player_path, index=False)
    print(f"player.csv : {avant} noms nettoyes")

    # ---- match.csv ----
    match_path = DATA / "match.csv"
    df_match = pd.read_csv(match_path)
    avant1 = df_match["player_1"].str.contains(",", na=False).sum()
    avant2 = df_match["player_2"].str.contains(",", na=False).sum()
    df_match = nettoyer_colonne(df_match, "player_1")
    df_match = nettoyer_colonne(df_match, "player_2")
    df_match.to_csv(match_path, index=False)
    print(f"match.csv  : {avant1 + avant2} noms nettoyes")

    print("\nFichiers mis a jour dans data/chess/")


if __name__ == "__main__":
    main()
