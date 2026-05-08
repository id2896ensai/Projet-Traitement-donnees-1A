from __future__ import annotations
import datetime
import pandas as pd
from typing import Any
from Model.match import Match
from Model.team import Team

# Matchs


def filtrer_matchs(
    matches: list[Match],
    date_debut: str | None = None,
    date_fin:   str | None = None,
    equipe:     str | None = None,
    score_min:  int | None = None,
) -> list[Match]:
    """
    Filtre une liste de matchs selon les critères fournis.
    Tous les critères sont optionnels et cumulables.

    Parameters
    ----------
    matches    : liste complète des matchs chargés
    date_debut : date ISO 'YYYY-MM-DD' (incluse)
    date_fin   : date ISO 'YYYY-MM-DD' (incluse)
    equipe     : filtre sur le full_name d'un participant (nom d'équipe/nom joueur)
    score_min  : garde les matchs où AU MOINS UN score >= score_min

    Returns
    -------
    list[Match] filtrée
    """
    result = matches

    if date_debut:
        d = datetime.date.fromisoformat(date_debut)
        result = [m for m in result if m.date_match >= d]

    if date_fin:
        d = datetime.date.fromisoformat(date_fin)
        result = [m for m in result if m.date_match <= d]

    if equipe:
        q = equipe.strip().lower()
        result = [
            m for m in result
            if any(q in (p.full_name or "").lower() for p in m.participants)
        ]

    if score_min is not None:
        def _max_score(m: Match) -> int:
            try:
                return max(int(s) for s in m.scores.values() if str(s).lstrip("-").isdigit())
            except (ValueError, TypeError):
                return 0
        result = [m for m in result if _max_score(m) >= score_min]

    return result


def matchs_vers_dataframe(matches: list[Match]) -> pd.DataFrame:
    """
    Convertit une liste de Match en DataFrame exportable.
    Gère le cas générique : participants est une liste de taille variable.
    Pour l'affichage, on nomme les colonnes participant_1, participant_2, ...
    """
    rows = []
    for m in matches:
        row = {
            "date":  m.date_match,
            "sport": m.sport.nom,
        }
        # participants et scores sont alignés via la liste
        for i, p in enumerate(m.participants, start=1):
            row[f"participant_{i}"] = p.full_name if hasattr(p, "full_name") else str(p)
            row[f"score_{i}"] = m.scores.get(p, "")

        rows.append(row)

    return pd.DataFrame(rows)


# Equipes

def filtrer_equipes(
    teams: list[Team],
    nom:     str | None = None,
    pays:    str | None = None,
    region:  str | None = None,
) -> list[Team]:
    """
    Filtre une liste d'équipes.

    Parameters
    ----------
    teams  : liste complète des équipes
    nom    : sous-chaîne sur full_name ou abbreviation
    pays   : sous-chaîne sur country
    region : sous-chaîne sur region
    """
    result = teams

    if nom:
        q = nom.strip().lower()
        result = [
            t for t in result
            if q in (t.full_name or "").lower()
            or q in (getattr(t, "abbreviation", None) or "").lower()
        ]

    if pays:
        q = pays.strip().lower()
        result = [
            t for t in result
            if q in (getattr(t, "country", None) or "").lower()
        ]

    if region:
        q = region.strip().lower()
        result = [
            t for t in result
            if q in (getattr(t, "region", None) or "").lower()
        ]

    return result


def equipes_vers_dataframe(teams: list[Team]) -> pd.DataFrame:
    rows = []
    for t in teams:
        rows.append({
            "full_name":    t.full_name,
            "abbreviation": getattr(t, "abbreviation", None),
            "city":         getattr(t, "city", None),
            "country":      getattr(t, "country", None),
            "region":       getattr(t, "region", None),
            "nb_players":   t.nb_players,
        })
    return pd.DataFrame(rows)


# Joueurs

def filtrer_joueurs(
    players: list[Any],
    nom:  str | None = None,
    pays: str | None = None,
    role: str | None = None,
    sexe: str | None = None,
) -> list[Any]:
    """
    Filtre une liste de joueurs.

    Parameters
    ----------
    players : liste complète des joueurs
    nom     : sous-chaîne sur pseudo, nom ou prenom
    pays    : sous-chaîne sur pays_de_naissance
    role    : sous-chaîne sur role
    sexe    : valeur exacte sur sexe ('M' ou 'F')
    """
    result = players

    if nom:
        q = nom.strip().lower()
        result = [
            p for p in result
            if q in (getattr(p, "pseudo", None) or "").lower()
            or q in (getattr(p, "nom", None) or "").lower()
            or q in (getattr(p, "prenom", None) or "").lower()
        ]

    if pays:
        q = pays.strip().lower()
        result = [
            p for p in result
            if q in (getattr(p, "pays_de_naissance", None) or "").lower()
        ]

    if role:
        q = role.strip().lower()
        result = [
            p for p in result
            if q in (getattr(p, "role", None) or "").lower()
        ]

    if sexe:
        result = [
            p for p in result
            if (getattr(p, "sexe", None) or "").upper() == sexe.upper()
        ]

    return result


def joueurs_vers_dataframe(players: list[Any]) -> pd.DataFrame:
    rows = []
    for p in players:
        rows.append({
            "pseudo":             getattr(p, "pseudo", None),
            "nom":                getattr(p, "nom", None),
            "prenom":             getattr(p, "prenom", None),
            "pays_de_naissance":  getattr(p, "pays_de_naissance", None),
            "sexe":               getattr(p, "sexe", None),
            "role":               getattr(p, "role", None),
            "date_de_naissance":  getattr(p, "date_de_naissance", None),
        })
    return pd.DataFrame(rows)
