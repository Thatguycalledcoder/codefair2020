#!/usr/bin/env python
# coding: utf-8

import sys
if len(sys.argv) != 3:
    print("parameter usage: <interpreter> <programme> <covid_data> <population_data>")
    sys.exit(0)

covid_data = sys.argv[1]
population_data = sys.argv[2]

import os
os.chdir('E:\Projects and stuff\Career Fair')

import pandas as pd
data = pd.read_csv(covid_data)

data_pp = pd.read_csv(population_data)

countrypop = []
for i in range(len(data_pp['Country'])):
    countrypop.append(data_pp['Country'][i])

populationpop = []
for i in range(len(data_pp['Population'])):
    populationpop.append(data_pp['Population'][i])

dateRep = []
for i in range(len(data['CountryExp'])):
    dateRep.append(data['DateRep'][i])

countryexp = []
for i in range(len(data['CountryExp'])):
    countryexp.append(data['CountryExp'][i])

newConfCases = []
for i in range(len(data['CountryExp'])):
    newConfCases.append(data['NewConfCases'][i])

newDeaths = []
for i in range(len(data['CountryExp'])):
    newDeaths.append(data['NewDeaths'][i])

covcountcase = {}
accum = 0
for i in range(len(data['CountryExp'])-1):
    if data['CountryExp'][i] == data['CountryExp'][i+1]:
        accum += data['NewConfCases'][i]
        pass
    else:
        covcountcase[data['CountryExp'][i]] = accum
        accum = 0
x = list(covcountcase.keys())[-1]
covcountcase[x] = covcountcase[x] + data['NewConfCases'][len(data['NewConfCases'])-1]

diecountcase = {}
accum = 0
for i in range(len(data['CountryExp'])-1):
    if data['CountryExp'][i] == data['CountryExp'][i+1]:
        accum += data['NewDeaths'][i]
        pass
    else:
        diecountcase[data['CountryExp'][i]] = accum
        accum = 0
die_count = list(diecountcase.keys())
x = list(diecountcase.keys())[-1]
diecountcase[x] = diecountcase[x] + data['NewDeaths'][len(data['NewDeaths'])-1]

popcountcase = {}
accum = 0
for i in range(len(countrypop)):
    popcountcase[countrypop[i]] = populationpop[i]
ke = list(covcountcase.keys())

covidpop = {}
for i in range(len(covcountcase)): 
    for key,value in popcountcase.items():
        if ke[i] == key:
            covidpop[ke[i]] = value
cpkeys = list(covidpop.keys())
covidvalues = {}
for i in range(len(covidpop)): 
    for key,value in covcountcase.items():
        if cpkeys[i] == key:
            covidvalues[cpkeys[i]] = value

#question 1
most = 0
keylist = list(covcountcase.keys())
for i in range(len(covcountcase)):
    if covcountcase[keylist[i]] > most:
        most = covcountcase[keylist[i]]
        pos = keylist[i]
print(pos, "has the highest number of infected people, cases recorded:",most)

kk = list(covidvalues.keys())
kkk = list(covcountcase.values())
kkk.sort()
sechigh = kkk[-2]
def get_key(val):
    for key,value in covcountcase.items():
        if val == value:
            return key
            
b = get_key(sechigh)
print(b, "has the second highest number of infected people, cases recorded:",sechigh)

populationvalues = list(covidpop.values())
acovidvalues = list(covidvalues.values())

infrat = []
for i in range(len(covidpop)):
    infrat.append(acovidvalues[i] / populationvalues[i])
maxval = max(infrat)
maxvalpos = infrat.index(maxval)

#question 3
print(kk[maxvalpos], "had the highest infection rate, infection rate:", maxval)

#question 4
covcase = list(covcountcase.values())
diecase = list(diecountcase.values())
print("The overall death ratio is", sum(diecase)/sum(covcase))

#question 5
deathratio = []
for i in range(len(covcase)):
    try:
        deathratio.append(diecase[i] / covcase[i])
    except ZeroDivisionError:
        deathratio.append(0)
maxdthval = max(deathratio)
maxdthvalpos = deathratio.index(maxdthval)
print(die_count[maxdthvalpos], "had the highest death ratio, death ratio:", maxdthval)

infslope = []
for i in range(len(keylist)):
    c = countryexp.index(keylist[i]) #searches for index of the country in countryexp from keylist and strores to a variable
    infslope.append(newConfCases[c:c+7]) #uses the value stored to append a list of the first seven items to infslope

def get_slope(masa):
    dna = []
    for i in masa:
        baa = i
        zuludu = (baa[5] / 2) - (baa[6] / 1)
        for j in range(len(i)-3,-1,-1):
            zuludu = (baa[j] / 7 - j) - zuludu
        dna.append(zuludu)
    return dna
slopes = get_slope(infslope)

pos_slope = []
neg_slope = []
for i in slopes:
    if i > 0:
        pos_slope.append(i)
    elif i < 0:
        neg_slope.append(i)

pos_slope.sort()
in_pos = []
for i in pos_slope:
    in_pos.append(slopes.index(i))
neg_slope.sort()
in_neg = []
for i in neg_slope:
    in_neg.append(slopes.index(i))

h_rate = in_pos[-1]
l_rate = in_neg[0]

#question 6
pos_slope_country = ""
for i in in_pos:
    pos_slope_country += keylist[i] + ", "
print(pos_slope_country[:-2], "are the countries with the number of infections per day on the rise.(estimation over one week of data)")

#question 7
print(keylist[h_rate], "has the steepest increase in infection rate.(estimation over one week of data)")

#question 8
neg_slope_country = []
for i in in_neg:
    if keylist[i] in neg_slope_country:
        pass
    else:
        neg_slope_country.append(keylist[i])
neg_slope_country_j = ', '.join(neg_slope_country)
print(neg_slope_country_j, "are the countries with the number of infections per day decreasing.(estimation over one week of data)")

#question 9
print(keylist[l_rate], "has the steepest decrease in infection rate.(estimation over one week of data)")

#question 10
neg_neg = []
try:
    for i in range(len(in_neg)):
        if in_neg[i] == in_neg[i+1]:
            pass
        else:
            neg_neg.append(in_neg[i])
except IndexError:
    neg_neg.append(in_neg[-1])

neg_country_peak = []
for i in neg_neg:
    annex = keylist[i]
    annex_value = max(infslope[i])
    annex_value_pos = infslope[i].index(annex_value)
    neg_country_peak.append(annex + ", " + str(annex_value) + ", " + str(annex_value_pos))

neg_country_peak_value = [] #keeps the peak value
neg_country_peak_day = [] #keeps the peak day
for i in neg_neg:
    annex_value = max(infslope[i])
    annex_value_pos = infslope[i].index(annex_value)
    neg_country_peak_value.append(annex_value)
    neg_country_peak_day.append(annex_value_pos)

earlyday = max(neg_country_peak_day) #takes the max,earliest day
#stores all peak values of countries with the same earliest day in a list
earlyday_pos = []
for i in neg_country_peak_day:
    if i == earlyday:
        earlyday_pos.append(neg_country_peak_day.index(i)) 

earlycoun = ""
for i in earlyday_pos:
    earlycoun += neg_country_peak[i][:-6] + ", "
print(earlycoun[:-2], "was the earliest to peak. It did so on day", 7 - earlyday, "of the week.(estimation over one week of recent data)")
