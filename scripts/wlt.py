from functions import get_tba_data
import json
import traceback

def get_winning_season(year):
    teams = {}
    events = get_tba_data("events/"+str(year)+"/simple")
    for event in events:
        if event["event_type"] > 5: continue
        print(event["key"])
        try:
            matches = get_tba_data("event/"+event["key"]+"/matches/simple")
            if matches is None or len(matches)==0: continue
            for match in matches:
                if None in [match["alliances"]["red"]["score"], match["alliances"]["blue"]["score"]] or \
                    -1 in [match["alliances"]["red"]["score"], match["alliances"]["blue"]["score"]]: continue
                for team in match["alliances"]["red"]["team_keys"]:
                    if team not in teams: teams[team] = [0, 0, 0]
                    if match["winning_alliance"] == "red": teams[team][0] += 1
                    elif match["winning_alliance"] == "blue": teams[team][1] += 1
                    else: teams[team][2] += 1
                for team in match["alliances"]["blue"]["team_keys"]:
                    if team not in teams: teams[team] = [0, 0, 0]
                    if match["winning_alliance"] == "blue": teams[team][0] += 1
                    elif match["winning_alliance"] == "red": teams[team][1] += 1
                    else: teams[team][2] += 1
        except Exception:
            print(traceback.format_exc())

    out = []
    for team, val in teams.items():
        out.append((team[3:], val[0], val[1], val[2]))
    out.sort(key=lambda x:x[1]+x[2]+x[3], reverse=True)
    out.sort(key=lambda x:x[3])
    out.sort(key=lambda x:x[1]/(max(x[1]+x[2],1)), reverse=True)
    return list(enumerate(out, start=1))

def recalc(year):
    with open("wlt/"+str(year)+".json", "w+") as file:
        json.dump(get_winning_season(year),file)