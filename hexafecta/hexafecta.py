import requests
from numpy import count_nonzero
import json

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

def get_tba_data(url):
    try:
        return requests.get("https://www.thebluealliance.com/api/v3/" + url,
                            {"accept": "application%2Fjson",
                             "X-TBA-Auth-Key": "gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ"}).json()
    except:
        print("oops " + url)
        return get_tba_data(url)

def get_hexafecta():
    hexafecta = {}
    quinfecta = {}
    all_teams = {}

    for year in range(1992,2020):
        print(year)
        events = get_tba_data("events/"+str(year)+"/simple")
        for event in events:
            if event["event_type"] > 5 : continue
            print(event["key"])
            awards = get_tba_data("event/"+event["key"]+"/awards")
            for award in awards:
                if award["award_type"] in lookup:
                    if award["recipient_list"][0]["team_key"] not in all_teams:
                        all_teams[award["recipient_list"][0]["team_key"]] = [0,0,0,0,0,0]
                    all_teams[award["recipient_list"][0]["team_key"]][lookup[award["award_type"]]] += 1

    for team in all_teams:
        if count_nonzero(all_teams[team]) == 6:
            hexafecta[team] = all_teams[team]
        elif count_nonzero(all_teams[team]) == 5:
            quinfecta[team] = all_teams[team] + [names[all_teams[team].index(0)]]
        all_teams[team] += [sum(all_teams[team])]

    hexafecta = {key[3:]:value for (key,value) in hexafecta.items()}
    quinfecta = {key[3:]:value for (key,value) in quinfecta.items()}
    all_teams = {key[3:]:value for (key,value) in all_teams.items()}

    # i = 0
    # while i==0:
    #     tmp = get_tba_data("teams/"+str(i)+"/keys")
    #     if len(tmp) == 0: break
    #     teams = teams + tmp
    #     print(i)
    #     i += 1
    #
    # for team in teams:
    #     print(team)
    #     awards = get_tba_data("team/"+team+"/awards")
    #     hex = [0, 0, 0, 0, 0, 0]
    #     for award in awards:
    #         try:
    #             hex[lookup.index(award["award_type"])] += 1
    #         except ValueError:
    #             if award["award_type"] == 26: hex[3] += 1
    #     if count_nonzero(hex) == 6:
    #         hexafecta[team] = hex
    #     elif count_nonzero(hex) == 5:
    #         quinfecta[team] = hex
    #     all_teams[team] = hex
    #
    return {"hexafecta": hexafecta,
           "quinfecta": quinfecta,
           "all_teams": all_teams}

def recalc():
    with open("hexafecta.json", "w+") as file:
        tmp = get_hexafecta()
        json.dump(tmp, file)