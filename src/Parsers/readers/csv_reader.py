import pandas as pd

from src.Common.utils import print_timings


@print_timings
def read_csv(filepath: str, sep: str = ",") -> pd.DataFrame:
    """Read a CSV file and return a DataFrame.

    Args:
        filepath: Path to the CSV file.
        sep:      Column separator (default ",").

    Returns:
        pd.DataFrame: The loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    try:
        return pd.read_csv(filepath, sep=sep)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable : {filepath}")
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la lecture du CSV : {e}")
