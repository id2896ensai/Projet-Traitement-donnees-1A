"""
Adaptateurs génériques configurables par mapping de colonnes.

Utilisés par l'administrateur pour ajouter un nouveau sport sans écrire
de code Python : il suffit de décrire les colonnes du CSV.

Config attendue (dict) :
  Pour les équipes :
    sport_obj         : instance Sport
    col_full_name     : colonne nom complet (obligatoire)
    col_abbreviation  : colonne abréviation (optionnel)
    col_country       : colonne pays (optionnel)
    col_region        : colonne région (optionnel)
    col_city          : colonne ville (optionnel)

  Pour les joueurs :
    sport_obj            : instance Sport
    col_nom              : colonne nom de famille OU nom complet (obligatoire)
    col_prenom           : colonne prénom (optionnel — si absent, découpe col_nom sur espace)
    col_pays             : colonne pays/nationalité (optionnel)
    col_role             : colonne rôle/poste (optionnel)
    col_date_naissance   : colonne date de naissance (optionnel)
    col_taille           : colonne taille en cm (optionnel)
    col_pseudo           : colonne pseudo/identifiant (optionnel)

  Pour les matchs :
    sport_obj     : instance Sport
    col_team1     : colonne équipe 1 dans le CSV de matchs
    col_team2     : colonne équipe 2
    col_score1    : colonne score équipe 1
    col_score2    : colonne score équipe 2
    col_date      : colonne date du match (format ISO AAAA-MM-JJ)
"""

import datetime
import pandas as pd

_DATE_INCONNUE = datetime.date(1900, 1, 1)


# ─── Adaptateur Équipe ───────────────────────────────────────

class GenericTeamAdapter:
    """Adaptateur d'équipe piloté par une config de colonnes."""

    _counter = 0

    def __init__(self, config: dict) -> None:
        self.cfg = config

    def adapt(self, row: pd.Series) -> dict:
        col = self.cfg

        # ID : depuis une colonne CSV si col_id est fourni, sinon compteur auto
        col_id = col.get("col_id", "")
        if col_id and col_id in row.index and pd.notna(row.get(col_id)):
            raw = row[col_id]
            try:
                id_val: int | str = int(raw)
            except (ValueError, TypeError):
                id_val = str(raw).strip()
        else:
            GenericTeamAdapter._counter += 1
            id_val = GenericTeamAdapter._counter

        data: dict = {
            "id":        id_val,
            "sport":     col["sport_obj"],
            "players":   [],
            "full_name": str(row[col["col_full_name"]]).strip(),
        }
        for attr, cle in [
            ("abbreviation", "col_abbreviation"),
            ("country",      "col_country"),
            ("region",       "col_region"),
            ("city",         "col_city"),
            ("state",        "col_state"),
            ("nickname",     "col_nickname"),
        ]:
            c = col.get(cle)
            if c and c in row.index and pd.notna(row.get(c)):
                data[attr] = str(row[c]).strip()
        return data


# ─── Adaptateur Joueur ────────────────────────────────────────

class GenericPlayerAdapter:
    """Adaptateur de joueur piloté par une config de colonnes."""

    def __init__(self, config: dict) -> None:
        self.cfg = config

    def adapt(self, row: pd.Series) -> dict:
        col = self.cfg

        # Décomposition nom/prénom
        col_nom    = col.get("col_nom", "")
        col_prenom = col.get("col_prenom", "")
        col_pseudo = col.get("col_pseudo", "")

        pseudo: str | None = None
        if col_pseudo and col_pseudo in row.index and pd.notna(row.get(col_pseudo)):
            pseudo = str(row[col_pseudo]).strip()

        if col_prenom and col_prenom in row.index and pd.notna(row.get(col_prenom)):
            prenom = str(row[col_prenom]).strip() or "?"
            nom_val = str(row.get(col_nom, "")).strip() or "Inconnu"
        elif col_nom and col_nom in row.index and pd.notna(row.get(col_nom)):
            parties = str(row[col_nom]).strip().split(" ", 1)
            prenom  = parties[0] or "?"
            nom_val = parties[1] if len(parties) == 2 else "Inconnu"
        else:
            prenom  = pseudo or "?"
            nom_val = "Inconnu"

        # Date de naissance
        dob = _DATE_INCONNUE
        col_dob = col.get("col_date_naissance", "")
        if col_dob and col_dob in row.index and pd.notna(row.get(col_dob)):
            try:
                dob = datetime.date.fromisoformat(str(row[col_dob])[:10])
            except ValueError:
                pass

        # Taille
        taille = 0.0
        col_taille = col.get("col_taille", "")
        if col_taille and col_taille in row.index and pd.notna(row.get(col_taille)):
            try:
                taille = float(row[col_taille])
            except ValueError:
                pass

        # Pays / rôle
        pays: str | None = None
        col_pays = col.get("col_pays", "")
        if col_pays and col_pays in row.index and pd.notna(row.get(col_pays)):
            pays = str(row[col_pays]).strip()

        role: str | None = None
        col_role = col.get("col_role", "")
        if col_role and col_role in row.index and pd.notna(row.get(col_role)):
            role = str(row[col_role]).strip()

        return {
            "id":                abs(hash(prenom + nom_val + (pseudo or ""))) % (10 ** 7),
            "nom":               nom_val,
            "prenom":            prenom,
            "date_de_naissance": dob,
            "pseudo":            pseudo,
            "pays_de_naissance": pays,
            "sexe":              None,
            "poids":             0.0,
            "taille":            taille,
            "role":              role,
            "team":              None,
            "sport":             col["sport_obj"],
        }


# ─── Adaptateur Match ─────────────────────────────────────────

class GenericMatchAdapter:
    """Adaptateur de match piloté par une config de colonnes."""

    def __init__(self, equipes: dict, config: dict) -> None:
        self.equipes = equipes
        self.cfg     = config

    def adapt(self, row: pd.Series) -> dict | None:
        col = self.cfg

        # Équipes — cherche par string, puis par int si non trouvé (IDs numériques)
        def _lookup(raw_key: str):
            t = self.equipes.get(raw_key)
            if t is None:
                try:
                    t = self.equipes.get(int(raw_key))
                except (ValueError, TypeError):
                    pass
            return t

        key1 = str(row.get(col["col_team1"], "")).strip()
        key2 = str(row.get(col["col_team2"], "")).strip()
        team1 = _lookup(key1)
        team2 = _lookup(key2)
        if team1 is None or team2 is None:
            return None  # paire non trouvée → ligne ignorée

        # Scores
        try:
            s1 = float(row[col["col_score1"]])
            s2 = float(row[col["col_score2"]])
        except (ValueError, TypeError, KeyError):
            return None

        # Date
        try:
            date_str = str(row.get(col["col_date"], ""))[:10]
            date = datetime.date.fromisoformat(date_str)
        except ValueError:
            return None

        return {
            "sport":        col["sport_obj"],
            "participants": [team1, team2],
            "scores":       {team1: s1, team2: s2},
            "date_match":   date,
        }
