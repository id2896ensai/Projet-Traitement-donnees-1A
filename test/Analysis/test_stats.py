"""
Tests unitaires pour src/Analysis/stats.py.

Toutes les données sont construites en mémoire (aucun CSV lu).
Les classes Fake sont hashables pour pouvoir servir de clés dans scores.
"""
import pytest
from datetime import date

from Analysis.stats import (
    podium,
    victoires_equipe,
    matchs_equipe,
    matchs_joueur,
    stats_descriptives,
)


# ── Helpers ───────────────────────────────────────────────────


class FakeTeam:
    """Équipe minimale hashable (nécessaire pour être clé du dict scores)."""
    def __init__(self, name: str, players=None):
        self.full_name = name
        self.players = players or []


class FakePlayer:
    def __init__(self, nom: str, prenom: str, pseudo: str | None = None):
        self.nom = nom
        self.prenom = prenom
        self.pseudo = pseudo


class FakeMatch:
    def __init__(self, t1: FakeTeam, s1: float, t2: FakeTeam, s2: float):
        self.participants = [t1, t2]
        self.scores = {t1: s1, t2: s2}
        self.date_match = date(2024, 1, 1)


def _team(name: str, players=None):
    return FakeTeam(name, players)


def _player(nom: str, prenom: str, pseudo: str | None = None):
    return FakePlayer(nom, prenom, pseudo)


def _match(t1, s1: float, t2, s2: float):
    return FakeMatch(t1, s1, t2, s2)


# ── Fixtures ──────────────────────────────────────────────────


@pytest.fixture
def psg():
    return _team("PSG")


@pytest.fixture
def om():
    return _team("OM")


@pytest.fixture
def lyon():
    return _team("Lyon")


@pytest.fixture
def trois_matchs(psg, om, lyon):
    """PSG gagne 2x, OM gagne 1x, Lyon perd tout."""
    return [
        _match(psg, 3, om, 1),
        _match(psg, 2, lyon, 0),
        _match(om, 1, lyon, 0),
    ]


# ── podium ────────────────────────────────────────────────────


def test_podium_ordre_decroissant(trois_matchs, psg, om):
    result = podium(trois_matchs, n=3)
    assert result[0][0] == psg
    assert result[0][1] == 2
    assert result[1][0] == om
    assert result[1][1] == 1


def test_podium_limite_n(trois_matchs):
    result = podium(trois_matchs, n=1)
    assert len(result) == 1


def test_podium_egalite_non_comptee():
    t1, t2 = _team("A"), _team("B")
    result = podium([_match(t1, 1, t2, 1)], n=3)
    assert result == []


def test_podium_liste_vide():
    assert podium([]) == []


# ── victoires_equipe ──────────────────────────────────────────


def test_victoires_equipe_compte_correct(trois_matchs):
    assert victoires_equipe(trois_matchs, "PSG") == 2
    assert victoires_equipe(trois_matchs, "OM") == 1
    assert victoires_equipe(trois_matchs, "Lyon") == 0


def test_victoires_equipe_insensible_casse(trois_matchs):
    assert victoires_equipe(trois_matchs, "psg") == 2
    assert victoires_equipe(trois_matchs, "PSG") == 2


def test_victoires_equipe_inconnu(trois_matchs):
    assert victoires_equipe(trois_matchs, "Monaco") == 0


def test_victoires_equipe_avec_nul():
    t1, t2 = _team("PSG"), _team("OM")
    matchs = [_match(t1, 1, t2, 1), _match(t1, 2, t2, 0)]
    assert victoires_equipe(matchs, "PSG") == 1
    assert victoires_equipe(matchs, "OM") == 0


# ── matchs_equipe ─────────────────────────────────────────────


def test_matchs_equipe_retourne_bons_matchs(trois_matchs):
    result = matchs_equipe(trois_matchs, "PSG")
    assert len(result) == 2


def test_matchs_equipe_insensible_casse(trois_matchs):
    assert len(matchs_equipe(trois_matchs, "psg")) == 2


def test_matchs_equipe_equipe_absente(trois_matchs):
    assert matchs_equipe(trois_matchs, "Monaco") == []


def test_matchs_equipe_liste_vide():
    assert matchs_equipe([], "PSG") == []


# ── matchs_joueur ─────────────────────────────────────────────


@pytest.fixture
def equipe_avec_joueurs():
    mbappe = _player("Mbappé", "Kylian", pseudo="KM7")
    neymar = _player("Neymar", "Junior")
    return _team("PSG", players=[mbappe, neymar])


@pytest.fixture
def equipe_adverse():
    return _team("Real Madrid", players=[_player("Benzema", "Karim")])


@pytest.fixture
def un_match(equipe_avec_joueurs, equipe_adverse):
    return [_match(equipe_avec_joueurs, 2, equipe_adverse, 1)]


def test_matchs_joueur_par_nom(un_match):
    assert len(matchs_joueur(un_match, "Mbappé")) == 1


def test_matchs_joueur_par_prenom(un_match):
    assert len(matchs_joueur(un_match, "Kylian")) == 1


def test_matchs_joueur_par_pseudo(un_match):
    assert len(matchs_joueur(un_match, "KM7")) == 1


def test_matchs_joueur_recherche_partielle(un_match):
    assert len(matchs_joueur(un_match, "mbap")) == 1


def test_matchs_joueur_insensible_casse(un_match):
    assert len(matchs_joueur(un_match, "kylian")) == 1
    assert len(matchs_joueur(un_match, "NEYMAR")) == 1


def test_matchs_joueur_nom_complet(un_match):
    assert len(matchs_joueur(un_match, "Kylian Mbappé")) == 1


def test_matchs_joueur_inconnu(un_match):
    assert matchs_joueur(un_match, "Ronaldo") == []


def test_matchs_joueur_par_nom_equipe(un_match):
    assert len(matchs_joueur(un_match, "PSG")) == 1


# ── stats_descriptives ────────────────────────────────────────


def test_stats_descriptives_equipe_inconnue(trois_matchs):
    result = stats_descriptives(trois_matchs, "Monaco")
    assert "erreur" in result


def test_stats_descriptives_valeurs():
    psg = _team("PSG")
    om = _team("OM")
    lyon = _team("Lyon")
    matchs = [
        _match(psg, 3, om, 1),    # victoire PSG
        _match(psg, 0, lyon, 2),  # défaite PSG
        _match(psg, 1, om, 1),    # nul PSG
    ]
    stats = stats_descriptives(matchs, "PSG")

    assert stats["nb_matchs"] == 3
    assert stats["nb_victoires"] == 1
    assert stats["nb_defaites"] == 1
    assert stats["nb_nuls"] == 1
    assert stats["pct_victoires"] == round(100 / 3, 1)
    assert stats["moy_pts_marques"] == round((3 + 0 + 1) / 3, 2)
    assert stats["moy_pts_encaisses"] == round((1 + 2 + 1) / 3, 2)
    assert stats["max_score"] == 3
    assert stats["min_score"] == 0


def test_stats_descriptives_coherence_total():
    psg = _team("PSG")
    om = _team("OM")
    lyon = _team("Lyon")
    matchs = [
        _match(psg, 2, om, 0),
        _match(psg, 1, lyon, 3),
        _match(psg, 2, om, 2),
    ]
    stats = stats_descriptives(matchs, "PSG")
    assert stats["nb_victoires"] + stats["nb_defaites"] + stats["nb_nuls"] == stats["nb_matchs"]
    assert 0.0 <= stats["pct_victoires"] <= 100.0
