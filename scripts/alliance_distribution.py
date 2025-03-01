import tbapy
import matplotlib.pyplot as plt
import traceback

def level(alliance):
    if alliance is None:
        return []
    elif alliance['status'] == 'unknown':
        return []
    elif alliance['status']['status'] == 'won':
        return [1,2,3,4]
    elif alliance['status']['level'] == 'f':
        return [2,3,4]
    elif alliance['status']['level'] == 'sf':
        return [3,4]
    elif alliance['status']['level'] == 'qf':
        return [4]
    else:
        return []

def recalc(year):
    tba = tbapy.TBA('n7Dnypajo6tcZ5Io6nxG6PzsxfoRAMuBPiHIWnUb1n2KvWAaujDboTt0ZDrQVXlR')

    events = tba.events(year, simple=True)

    data = {1: {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0},
            2: {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0},
            3: {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0},
            4: {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0}}
    names = {1: "Winners", 2: "Finals", 3: "Semifinals", 4: "Quarterfinals"}

    for event in events:
        if event['event_type'] not in [0,1,2,3]:
            continue
        print(event['key'])
        try:
            alliances = tba.event_alliances(event['key'])
        except TypeError:
            continue
        except Exception:
            print(traceback.format_exc())
        for num, alliance in enumerate(alliances, start=1):
            for i in level(alliance):
                if 'name' in alliance:
                    seed = alliance['name'][-1]
                else:
                    seed = str(num)
                if seed in data[i].keys():
                    data[i][seed] += 1

    for i in data.keys():
        total = sum(data[i].values())
        if total == 0:
            continue
        fig, ax = plt.subplots()
        bars = plt.bar(data[i].keys(), [x/total for x in data[i].values()], align='center')
        ax.bar_label(bars, fmt='%.3f')
        plt.title(names[i])
        plt.xlabel('Alliance')
        plt.ylabel('Frequency')
        plt.savefig(f'alliance_distribution/{year}_{names[i]}.png')
        plt.close()