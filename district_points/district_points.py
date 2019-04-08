import requests
import json

class Team:
    def __init__(self, key):
        self.key = key
        self.qual = 0
        self.alliance = 0
        self.playoff = 0
        self.bestQual = 0
        self.bestPlayoff = 0
        self.bestAlliance = 0
        self.num_events = 0
        self.awards = 0
    def add_event(self, event, DP):
        factor = [1, 1, 0.37, 1.2, 0, 0.37][event["event_type"]]
        self.qual += DP["qual_points"]*factor
        self.alliance += DP["alliance_points"]*factor
        self.playoff += DP["elim_points"]*factor
        self.bestQual = max(self.bestQual, DP["qual_points"])
        self.bestPlayoff = max(self.bestPlayoff, DP["elim_points"])
        self.bestAlliance = max(self.bestAlliance, DP["alliance_points"])
        self.awards += DP["award_points"]*factor
        self.num_events += 1
    def adj(self):
        return (self.qual + self.alliance + self.playoff) / (self.num_events ** 0.7)
    def adjawards(self):
        return (self.qual + self.alliance + self.playoff + self.awards) / (self.num_events ** 0.7)
    def valadj(self, value):
        return value * (self.num_events ** -0.7)
    def make_dict(self):
        return {"adj": self.adj(),
                "adjawards": self.adjawards(),
                "adj_qual": self.valadj(self.qual),
                "adj_alliance": self.valadj(self.alliance),
                "adj_playoff": self.valadj(self.playoff),
                "num_events": self.num_events}

def get_tba_data(url):
    try:
        return requests.get("https://www.thebluealliance.com/api/v3/" + url,
                        {"accept": "application%2Fjson",
                         "X-TBA-Auth-Key": "gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ"}).json()
    except:
        print("oops " + url)
        return get_tba_data(url)

def get_district_points(year):
    teams = {}

    events = get_tba_data("events/"+str(year))
    for event in events:
        if event["event_type"] == 4 or event["event_type"] > 5 or len(event["division_keys"]) > 0: continue     #All Events
        #if event["event_type"] not in [0,1,2,5] or len(event["division_keys"]) > 0: continue     #Pre-Champs
        #if event["event_type"] > 1 or len(event["division_keys"]) > 0: continue     #Pre-DCMP
        DPs = get_tba_data("event/"+event["key"]+"/district_points")
        if DPs is None or len(DPs)==0: continue
        else: DPs = DPs["points"]
        print(event["key"])
        for teamKey in DPs:
            if teamKey not in teams:
                teams[teamKey] = Team(teamKey)
            teams[teamKey].add_event(event, DPs[teamKey])

    return teams
    # return sorted(teams.items(), key=lambda key:(teams[key].adjawards(),
    #                                      teams[key].adj(),
    #                                      teams[key].valadj(teams[key].playoff),
    #                                      teams[key].bestPlayoff,
    #                                      teams[key].valadj(teams[key].alliance),
    #                                      teams[key].valadj(teams[key].alliance),
    #                                      teams[key].bestAlliance,
    #                                      teams[key].valadj(teams[key].qual)), reverse=True)

def recalc(year):
    with open("/var/www/html/district_points/" + str(year) + ".json", "w+") as file:
        tmp = {team[3:]: Team.make_dict(x) for (team,x) in sorted(get_district_points(year).items(),
                                                                      key=lambda y: (
                                                                          y[1].adj(),
                                                                          y[1].valadj(y[1].playoff),
                                                                          y[1].bestPlayoff,
                                                                          y[1].valadj(y[1].alliance),
                                                                          y[1].valadj(y[1].alliance),
                                                                          y[1].bestAlliance,
                                                                          y[1].valadj(y[1].qual)),
                                                                      reverse=True)}
        json.dump(tmp, file)
