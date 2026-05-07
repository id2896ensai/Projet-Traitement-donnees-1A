import pytest
from datetime import date

from Model.person import Person


def test_person_creation():
    p = Person("Ronaldo", "Cristiano", date(1985, 2, 5))

    assert p.nom == "Ronaldo"
    assert p.prenom == "Cristiano"
    assert p.date_de_naissance == date(1985, 2, 5)


@pytest.mark.parametrize(
    "nom, prenom, date_naissance, erreur, message",
    [
        (123, "Cristiano", date(1985, 2, 5), TypeError, "nom doit être une str"),
        ("", "Cristiano", date(1985, 2, 5), ValueError, "nom ne peut pas être vide"),

        ("Ronaldo", 123, date(1985, 2, 5), TypeError, "prenom doit être une str"),
        ("Ronaldo", "", date(1985, 2, 5), ValueError, "prenom ne peut pas être vide"),

        ("Ronaldo", "Cristiano", "1985-02-05", TypeError, "date_de_naissance doit être une date"),
    ],
)
def test_person_invalid(nom, prenom, date_naissance, erreur, message):
    with pytest.raises(erreur, match=message):
        Person(nom, prenom, date_naissance)


def test_person_str():
    p = Person("Ronaldo", "Cristiano", date(1985, 2, 5))

    result = str(p)

    assert "Personne" in result
    assert "Ronaldo" in result
    assert "Cristiano" in result
    assert "1985" in result


def test_person_repr():
    p = Person("Ronaldo", "Cristiano", date(1985, 2, 5))

    result = repr(p)

    assert "Person(" in result
    assert "nom:" in result
    assert "prenom:" in result
    assert "1985" in result
