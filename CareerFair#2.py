#!usr/bin/env python

import sys
if len(sys.argv) != 3:
    print("Parameter error: <interpreter> <filename> <covid data> <partial time series data")
    sys.exit(0)

covid_data = sys.argv[1]
partial_series = sys.argv[2]

import pandas as pd
data = pd.read_csv(covid_data)
data_pts = pd.read_csv(partial_series)

daterep = []
for i in range(len(data['DateRep'])):
    daterep.append(data['DateRep'][i])

countryrep = []
for i in range(len(data['CountryRep'])):
    countryrep.append(data['CountryRep'][i])

newconfcases = []
for i in range(len(data['NewConfCases'])):
    newconfcases.append(data['NewConfCases'][i])

pts_values = []
for i in data_pts:
    pts_values.append(i)

for i in range(len(pts_values)):
    for j in range(len(newconfcases)):
        if pts_values[i] == newconfcases[j] and pts_values[i+1] == newconfcases[j+1] and pts_values[i+2] == newconfcases[j+2]:
            print("It is at index", j)
            print("It is exactly there.")
            break
    break
