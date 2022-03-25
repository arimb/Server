from functions import get_tba_data
import json
from scipy.special import erfinv
from math import ceil

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
    def add_event(self, event, status):
        factor = [1, 1, 0.37, 1.2, 0, 0.37][event["event_type"]]
        try:
            q = ceil(7.676*erfinv((status['qual']['num_teams']-2*status['qual']['ranking']['rank']+2)/(1.07*status['qual']['num_teams']))+12)*factor
        except TypeError: q=0
        if status['alliance'] is not None:
            a = (17-status['alliance']['number'] if status['alliance']['pick']<2 else status['alliance']['number'] if status['alliance']['pick']==2 else 0)*factor
        else: a=0
        if status['playoff'] is not None:
            p = ({'ef':0, 'qf':0, 'sf':10, 'f':20}[status['playoff']['level']]+(10 if status['playoff']['status']=='won' else 0))*factor
        else: p=0
        self.qual += q
        self.alliance += a
        self.playoff += p
        self.bestQual = max(self.bestQual, q)
        self.bestPlayoff = max(self.bestPlayoff, p)
        self.bestAlliance = max(self.bestAlliance, a)
        self.num_events += 1 if q+a+p>0 else 0
    def add_award(self, event, award):
        factor = [1, 1, 0.37, 1.2, 0, 0.37][event["event_type"]]
        try:
            self.awards += {0:10, 9:8, 10:8, 11:5, 12:5, 13:5, 15:5, 16:5, 17:5, 18:5, 19:5, 20:5, 21:5, 22:5, 23:5, 26:5, 27:5, 28:5, 29:5, 30:5, 31:5, 32:5, 69:8}[award['award_type']]*factor
        except KeyError: pass

    def adj(self):
        if self.num_events==0: return 0
        return (self.qual + self.alliance + self.playoff) / (self.num_events ** 0.7)
    def adjawards(self):
        if self.num_events==0: return 0
        return (self.qual + self.alliance + self.playoff + self.awards) / (self.num_events ** 0.7)
    def valadj(self, value):
        if self.num_events==0: return 0
        return value * (self.num_events ** -0.7)
    def make_dict(self):
        return [self.adj(),
                self.valadj(self.qual),
                self.valadj(self.alliance),
                self.valadj(self.playoff),
                self.num_events]
    def make_dict_awards(self):
        return [self.adjawards(),
                self.valadj(self.qual),
                self.valadj(self.alliance),
                self.valadj(self.playoff),
                self.num_events]

def get_district_points(year):
    teams = {}

    events = get_tba_data("events/"+str(year))
    for event in events:
        if event["event_type"]>5 or (event['event_type']==5 and len(event["division_keys"])>0): continue
        if event['event_type']==4:
            matches = get_tba_data('event/'+event['key']+'/matches/simple')
            if matches is None: continue
            for match in matches:
                if not match['winning_alliance']: continue
                for team in match['alliances'][match['winning_alliance']]['team_keys']:
                    if team not in teams:
                        teams[team] = Team(team)
                    teams[team].playoff += 2*1.2
        else:
            statuses = get_tba_data("event/"+event["key"]+"/teams/statuses")
            if statuses is None or len(statuses)==0: continue
            print(event["key"])
            for team, status in statuses.items():
                if status is None: continue
                if team not in teams:
                    teams[team] = Team(team)
                teams[team].add_event(event, status)
        awards = get_tba_data('event/'+event['key']+'/awards')
        if awards is None: continue
        for award in awards:
            for recipient in award['recipient_list']:
                if recipient['team_key'] is None: continue
                if recipient['team_key'] not in teams:
                    teams[recipient['team_key']] = Team(recipient['team_key'])
                teams[recipient['team_key']].add_award(event, award)
    return teams

def recalc(year):
    gdp = get_district_points(year)
    tmp = [(team[3:], (i, Team.make_dict(x))) for (i, (team, x)) in enumerate(sorted(gdp.items(),
                                                                            key=lambda y: (
                                                                                y[1].adj(),
                                                                                y[1].valadj(y[1].playoff),
                                                                                y[1].bestPlayoff,
                                                                                y[1].valadj(y[1].alliance),
                                                                                y[1].valadj(y[1].alliance),
                                                                                y[1].bestAlliance,
                                                                                y[1].valadj(y[1].qual)),
                                                                            reverse=True), start=1)]
    tmp_awards = [(team[3:], (i, Team.make_dict_awards(x))) for (i, (team, x)) in enumerate(sorted(gdp.items(),
                                                                                            key=lambda y: (
                                                                                                y[1].adjawards(),
                                                                                                y[1].valadj(y[1].playoff),
                                                                                                y[1].bestPlayoff,
                                                                                                y[1].valadj(y[1].alliance),
                                                                                                y[1].valadj(y[1].alliance),
                                                                                                y[1].bestAlliance,
                                                                                                y[1].valadj(y[1].qual)),
                                                                                            reverse=True), start=1)]
    with open("district_points/" + str(year) + ".json", "w+") as file:
        json.dump(tmp, file)
    with open("district_points/" + str(year) + "_awards.json", "w+") as file:
        json.dump(tmp_awards, file)
