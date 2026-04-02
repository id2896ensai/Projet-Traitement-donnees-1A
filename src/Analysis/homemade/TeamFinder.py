from ...Model.team import Team

def TeamFinder(teams: list[Team], names: list[str]):
    teams_final = []
    for i in teams:
        if i.full_name in names:
            teams_final.append(i)

