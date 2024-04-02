from functions import get_tba_data
from numpy import count_nonzero
import json
import pickle as pkl

lookup = {
    16: 0,
    17: 1,
    20: 2,
    21: 3,
    26: 3,
    29: 4,
    38: 4,
    71: 5
}
names = ["IndDsn","Qual","Creativ","EngEx","Cntrl","Auton"]

def get_hexafecta(year):
    data = {}
    hexafecta_teams = {}

    for year in range(1992,year+1):
        print(year)
        events = get_tba_data("events/"+str(year))
        events = filter(lambda event : event["event_type"] in [0,1,2,3,4,5,7], events)
        events = sorted(events, key=lambda event : event["week"] if event["week"] is not None else 9999)
        for event in events:
            print(event["key"])
            awards = get_tba_data("event/"+event["key"]+"/awards")
            awards = filter(lambda award : award["award_type"] in lookup, awards)
            for award in awards:
                team = award["recipient_list"][0]["team_key"]
                if team not in data:
                    data[team] = [0,0,0,0,0,0]
                data[team][lookup[award["award_type"]]] += 1
                if count_nonzero(data[team]) == 6 and team not in hexafecta_teams:
                    hexafecta_teams[team] = year

    with open("pkl.pkl, b") as file:
        pkl.dump([data, hexafecta_teams], file)

    hexafecta = list(map(lambda team : [team[0][3:]]+data[team[0]]+[team[1]], reversed(hexafecta_teams.items())))
    
    data = dict(sorted(data.items(), key = lambda team : (sum(team[1]), int(team[0][3:]))))
    quinfecta = list(map(lambda team : [team]+data[team]+[names[data[team].index(0)]], filter(lambda team : count_nonzero(data[team]) == 5, data)))
    all_teams = [[team[3:]]+value+[sum(value)] for (team,value) in data.items()]


    return {"hexafecta": hexafecta,
           "quinfecta": quinfecta,
           "all_teams": all_teams}


def run(year):
    with open("hexafecta.json", "w+") as file:
        json.dump(get_hexafecta(year), file)


run(2024)