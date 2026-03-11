from src.Parsers.parse_csv import parse_players_csv


def test_parse_players_csv_returns_an_ordered_list_of_players():
    players = parse_players_csv("/home/onyxia/work/Projet-Traitement-donnees-1A/test/Parsers/players.csv")
    assert len(players) == 2
    assert players[0] == "Ousmane Dembélé"
    assert players[1] == "Stéphane Guivarc'h"
