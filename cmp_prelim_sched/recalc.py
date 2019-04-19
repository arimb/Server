#!/usr/bin/python3

"""
Copyright 2018 Wes Jordan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import pandas
import json

from sys import argv

events = {
        "2019arc": "Archimedes.csv",
        "2019cars": "Carson.csv",
        "2019cur": "Curie.csv",
        "2019dal": "Daly.csv",
        "2019dar": "Darwin.csv",
        "2019tes": "Tesla.csv"
        }

for event_key, filename in events.items():
    df = pandas.read_csv(filename, dtype=str)

    output = []
    print(filename)
    for index, row in df.iterrows():
      redsurrogates = [ 'frc' + team[:team.index("*")] for team in row[['Red 1', 'Red 2', 'Red 3']] if isinstance(team, str) and '*' in team ]
      blusurrogates = [ 'frc' + team[:team.index("*")] for team in row[['Blue 1', 'Blue 2', 'Blue 3']] if isinstance(team, str) and '*' in team ]

      outputrow = {
        "actual_time": None,
        "alliances": {
          "blue": {
            "dq_team_keys": [],
            "score": -1,
            "surrogate_team_keys": blusurrogates,
            "team_keys": [
              'frc' + row['Blue 1'][:row['Blue 1'].index(" ")].replace('*',''),
              'frc' + row['Blue 2'][:row['Blue 2'].index(" ")].replace('*',''),
              'frc' + row['Blue 3'][:row['Blue 3'].index(" ")].replace('*',''),
            ]
          },
          "red": {
            "dq_team_keys": [],
            "score": -1,
            "surrogate_team_keys": redsurrogates,
            "team_keys": [
              'frc' + row['Red 1'][:row['Red 1'].index(" ")].replace('*',''),
              'frc' + row['Red 2'][:row['Red 2'].index(" ")].replace('*',''),
              'frc' + row['Red 3'][:row['Red 3'].index(" ")].replace('*',''),
            ]
          }
        },
        "comp_level": "qm",
        "event_key": event_key,
        "key": event_key + "_qm" + str(index+1),
        "predicted_time": 0,
        "match_number": index+1,
        "set_number": 1,
        "time": 0,
        "winning_alliance": ""
      }

      output.append(outputrow)

    outfilename = event_key + '.json'

    with open(event_key + '.json', 'w+') as outputfile:
      json.dump(output, outputfile, indent=4)
      print(outfilename)