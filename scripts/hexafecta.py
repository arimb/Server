from functions import get_tba_data
from numpy import count_nonzero
import json
import traceback

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
        events = get_tba_data("events/"+str(year)+"/simple")
        events = list(filter(lambda event : event["event_type"] in [0,1,2,3,4,5,7], events))
        dates = list(map(lambda event : event["end_date"] if event["end_date"] is not None else event["start_date"] if event["start_date"] is not None else str(year)+"-00-00", events))
        dates, events = zip(*[(date, event) for date,event in sorted(zip(dates,events), key = lambda pair : pair[0])])
        for event, date in zip(events, dates):
            print(event["key"])
            try:
                awards = get_tba_data("event/"+event["key"]+"/awards")
                awards = filter(lambda award : award["award_type"] in lookup, awards)
                for award in awards:
                    team = award["recipient_list"][0]["team_key"]
                    if team not in data:
                        data[team] = [0,0,0,0,0,0]
                    data[team][lookup[award["award_type"]]] += 1
                    if count_nonzero(data[team]) == 6 and team not in hexafecta_teams:
                        hexafecta_teams[team] = date
            except Exception:
                print(traceback.format_exc())

    hexafecta = list(map(lambda team : [team[0][3:]]+data[team[0]]+[team[1]], reversed(list(hexafecta_teams.items()))))
    
    data = dict(sorted(data.items(), key = lambda team : (sum(team[1]), int(team[0][3:]))))
    quinfecta = list(map(lambda team : [team[3:]]+data[team]+[names[data[team].index(0)]], filter(lambda team : count_nonzero(data[team]) == 5, data)))
    all_teams = [[team[3:]]+value+[sum(value)] for (team,value) in sorted(data.items(), key = lambda team : (-sum(team[1]), int(team[0][3:])))]


    return {"hexafecta": hexafecta,
           "quinfecta": quinfecta,
           "all_teams": all_teams}


def run(year):
    with open("hexafecta.json", "w+") as file:
        json.dump(get_hexafecta(year), file)
