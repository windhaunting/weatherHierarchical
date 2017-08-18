#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:57:31 2017

@author: fubao
"""

#read us city and state file


import pandas as pd
from ghcndextractor import ghcndextractor
from commons import writeListRowToFileWriterTsv

#read usa city and state from a file
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
    
#get all usa's station id, and output to a file                ;
def getUSACodeId(stateCityMap, outFile):
      #(stationIDCodesToNameMap[stationMonth.stationID] in stateCityMap) and
        stationNameToIDCodesMap = ghcndextractor.readStationsFile()

         
        print ("stationNameToIDCodesMap: ", len(stationNameToIDCodesMap), len(stateCityMap))
        #debug
       # while(stationNameToIDCodesMap:
        USAStationLst = []
        #stationNametoCodeId
        for k in stateCityMap.keys():
            for stName, stcodeId in stationNameToIDCodesMap.items():
                #print ("k: ", k, stName)
                if k in stName:
                    USAStationLst.append([stcodeId, k])
        
        #print ("USAStationLst: ", len(USAStationLst))
        
        #write into file for later read, because it takes too much time for reading every time
        fd = open(outFile,'a')
        for ele in USAStationLst:
            writeListRowToFileWriterTsv(fd, ele, '\t')
        
#main entry
def readcitySatesExecute():
    
    ghcndextractor.ghcnFolder = "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/weatherData/" 
    
    inputXlsFile = "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/weatherData/List-of-Cities-States-and-Counties.xlsx"
    stateCityMap, stateToCountyMap, countyToCityMap = readcityStateExl(inputXlsFile)

    return stateCityMap, stateToCountyMap, countyToCityMap

#get all usa stationID and write into file
def getUSAStationExecute():
    stateCityMap, stateToCountyMap, countyToCityMap = readcitySatesExecute()
    outfileUSAStationId = "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/weatherData/weatherParser/output/outfileUSAStationId"
    
    getUSACodeId(stateCityMap, outfileUSAStationId)


#get USA state's stationId code
def getOneStateStationCodeId(inputUSAStationFile, state):
    df = pd.read_csv(inputUSAStationFile)
    print ("df: ",df)

def main():
    #readcitySatesExecute()

    #test
    outfileUSAStationId = "../output/outfileUSAStationId"
    getOneStateStationCodeId(outfileUSAStationId, 'ma')
    
    
if __name__== "__main__":
  main()