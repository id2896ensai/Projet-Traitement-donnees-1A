# Point d'entrée principal : python -m main  (depuis la racine du projet)
import sys
from pathlib import Path

# Ajoute src/ au chemin Python pour résoudre les imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from App.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
