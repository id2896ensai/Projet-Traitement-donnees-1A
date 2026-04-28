from src.Model.sport import Sport

# One instance per sport — adapters import from here so that
# participant.sport == match.sport comparisons work by identity.

BASKETBALL = Sport("basketball", "ballon", 5, "NBA", sport_en_equipe=True)
FOOTBALL = Sport("football", "ballon", 11, "Football européen", sport_en_equipe=True)
FOOTBALL_CL = Sport("football_cl", "ballon", 11, "UEFA Champions League", sport_en_equipe=True)
LOL = Sport("lol", "esport", 5, "League of Legends", sport_en_equipe=True)
CS2 = Sport("cs2", "esport", 5, "Counter-Strike 2", sport_en_equipe=True)
VOLLEYBALL = Sport("volleyball", "ballon", 6, "Volleyball", sport_en_equipe=True)
TENNIS = Sport("tennis", "raquette", 1, "Tennis", sport_en_equipe=False)
CHESS = Sport("chess", "stratégie", 1, "Échecs", sport_en_equipe=False)
BADMINTON = Sport("badminton", "raquette", 1, "Badminton", sport_en_equipe=False)
STARCRAFT2 = Sport("starcraft2", "esport", 1, "Starcraft 2", sport_en_equipe=False)
