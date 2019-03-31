import requests
import time
import csv

class Team:
    def __init__(self, key):
        self.key = key
        self.qual = 0
        self.alliance = 0
        self.playoff = 0
        self.awards = 0
        self.bestQual = 0
        self.bestPlayoff = 0
        self.bestAlliance = 0
        self.num_events = 0
    def add_event(self, event, DP):
        factor = [1, 1, 0.37, 1.2, 0, 0.37][event["event_type"]]
        self.qual += DP["qual_points"]*factor
        self.alliance += DP["alliance_points"]*factor
        self.playoff += DP["elim_points"]*factor
        self.awards += DP["award_points"]*factor
        self.bestQual = max(self.bestQual, DP["qual_points"])
        self.bestPlayoff = max(self.bestPlayoff, DP["elim_points"])
        self.bestAlliance = max(self.bestAlliance, DP["alliance_points"])
        self.num_events += 1
    def total(self):
        return self.qual + self.alliance + self.playoff
    def total_award(self):
        return self.qual + self.alliance + self.playoff + self.awards
    def adj(self):
        return self.total() / (self.num_events ** 0.7)
    def adjawards(self):
        return self.total_award() / (self.num_events ** 0.7)
    def valadj(self, value):
        return value * (self.num_events ** -0.7)

def get_tba_data(url):
    return requests.get("https://www.thebluealliance.com/api/v3/" + url,
                        {"accept": "application%2Fjson",
                         "X-TBA-Auth-Key": "gl4GXuoqG8anLUrLo356LIeeQZk15cfSoXF72YT3mYkI38cCoAmReoCSSF4XWccQ"}).json()

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
    data = get_district_points(year)
    with open(str(year) + ".csv", "w+") as file:
        file.write("Team,AdjDP,AwardsAdj,TotalDP,AwardsTotal,Playoff,BestPlayoff,Alliance,BestAlliance,Qual,BestQual,AdjPlayoff,AdjAlliance,AdjQual,Awards,AdjAwards,NumEvents\n")
        for team, DP in data.items():
            file.write(team[3:] + ',' +
                       str(DP.adj()) + ',' +
                       str(DP.adjawards()) +',' +
                       str(DP.total()) + ',' +
                       str(DP.total_award()) + ',' +
                       str(DP.playoff) + ',' +
                       str(DP.bestPlayoff) + ',' +
                       str(DP.alliance) + ',' +
                       str(DP.bestAlliance) + ',' +
                       str(DP.qual) + ',' +
                       str(DP.bestQual) + ',' +
                       str(DP.valadj(DP.alliance)) + ',' +
                       str(DP.valadj(DP.playoff)) + ',' +
                       str(DP.valadj(DP.qual)) + ',' +
                       str(DP.awards) + ',' +
                       str(DP.valadj(DP.awards)) + ',' +
                       str(DP.num_events) + '\n')

    times = {}
    # with open("times.csv", "w+") as file:
    #     reader = csv.DictReader(file)
    #     for row in reader:
    #         times[row["Year"]] = row["Time"]
    #     print(times)
    #     times[str(year)] = str(time.time())
    #     file.write("Year,Time\n")
    #     for y, t in times.items():
    #         file.write(y + ',' + t + '\n')

    return data