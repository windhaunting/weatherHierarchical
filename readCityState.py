#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:57:31 2017

@author: fubao
"""

#read us city and state file


import pandas as pd
from ghcndextractor import ghcndextractor


def readcityStateExl(inputXlsFile):
    

    xls = pd.ExcelFile(inputXlsFile)

    sheets = xls.sheet_names[0]
    sheetX = xls.parse(sheets)      #2 is the sheet number


    stateLst = sheetX['State']

    print( len(stateLst), stateLst[1])

    cityLst = sheetX['City']
    print( len(cityLst), cityLst[1])


    countyLst = sheetX['County']

    print( len(countyLst), countyLst[1])

    stateCityMap = {}          #state + " " + city map
    stateToCountyMap = {}
    countyToCityMap = {}
    
    
    for i, state in enumerate(stateLst):
        city = str(cityLst[i])
        ele = (str(state) + "," + str(city)).lower()
        if ele not in stateCityMap:
            stateCityMap[ele] = 1
        
        county = str(countyLst[i])
        if state.lower() not in stateToCountyMap:
            stateToCountyMap[state.lower()] = [county]
        else:
            stateToCountyMap[state.lower()].append(county)
        
        if county.lower() not in countyToCityMap:
            countyToCityMap[county.lower()] = [city]
        else:
            countyToCityMap[county.lower()].append(city)
    
    return stateCityMap, stateToCountyMap, countyToCityMap
    
#get all usa's station id                  ;
def getUSACodeId(stateCityMap):
      #(stationIDCodesToNameMap[stationMonth.stationID] in stateCityMap) and
        ghcndextractor.readStationsFile()

        stationNameToIDCodesMap =  ghcndextractor.stationNameToIDCodesMap

        USAStationLst = []
        #stationNametoCodeId
        for k in stateCityMap.keys():
            for stName in stationNameToIDCodesMap:
                if k in stName:
                    USAStationLst.append(stationNameToIDCodesMap[stName])
        
        print ("USAStationLst: ", len(USAStationLst))
        
def readcitySatesExecute():
    
    inputXlsFile = "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/weatherData/List-of-Cities-States-and-Counties.xlsx"
    stateCityMap, stateToCountyMap, countyToCityMap = readcityStateExl(inputXlsFile)

    getUSACodeId(stateCityMap)
    return stateCityMap, stateToCountyMap, countyToCityMap

readcitySatesExecute()