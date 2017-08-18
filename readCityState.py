#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 23:57:31 2017

@author: fubao
"""

#read us city and state file

import os
import pandas as pd
from ghcndextractor import ghcndextractor
from commons import writeListRowToFileWriterTsv
from shutil import copy2


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
        ele = str(state)                 # + "," + str(city)).lower()
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
        ghcndextractor.ghcnFolder = "../../ghcnd_all/" 
        stationNameToIDCodesMap = ghcndextractor.readStationsFile()

         
        print ("stationNameToIDCodesMap: ", len(stationNameToIDCodesMap), len(stateCityMap))
        #debug
       # while(stationNameToIDCodesMap:
        USAStationLst = []
        #stationNametoCodeId
        for k in stateCityMap.keys():
            for stName, stcodeId in stationNameToIDCodesMap.items():
                #print ("k: ", k, stName)
                if k in stName.split(",")[0]:
                    USAStationLst.append([stcodeId, k])
        
        #print ("USAStationLst: ", len(USAStationLst))
        
        #write into file for later read, because it takes too much time for reading every time
        fd = open(outFile,'a')
        for ele in USAStationLst:
            writeListRowToFileWriterTsv(fd, ele, '\t')
        
#main entry
def readcitySatesExecute():
    
    inputXlsFile = "../../List-of-Cities-States-and-Counties.xlsx"
    stateCityMap, stateToCountyMap, countyToCityMap = readcityStateExl(inputXlsFile)

    return stateCityMap, stateToCountyMap, countyToCityMap

#get usa state name
def getStateNames():
    stateCityMap, stateToCountyMap, countyToCityMap = readcitySatesExecute()
    states = []
    for st in stateCityMap.keys():
        states.append(st.split(",")[0])
    return states

#get all usa stationID and write into file
def getUSAStationExecute():
    stateCityMap, stateToCountyMap, countyToCityMap = readcitySatesExecute()
    outfileUSAStationId = "../output/outfileUSAStationId"
    os.remove(outfileUSAStationId) if os.path.exists(outfileUSAStationId) else None
    getUSACodeId(stateCityMap, outfileUSAStationId)


#get USA state's stationId code
def getOneStateStationCodeId(inputUSAStationFile, state):
    df = pd.read_csv(inputUSAStationFile,  names = ["stationId", "stateName"], delimiter = '\t')
    
    #df.apply(numpy.sum, axis=1) # equiv to df.sum(1)
    df['state'] = df['stateName'].apply(lambda x: x.split(',')[0].strip() == state)
    stateStationCodeIdSeries = df[df['state'] == True]['stationId']                 #series type
    print ("df: ",len(df), len(stateStationCodeIdSeries), type(stateStationCodeIdSeries))
    return stateStationCodeIdSeries


def getUSAStationDlyFiles(outfileUSAStationIdFile, allgncFolder):
    df = pd.read_csv(outfileUSAStationIdFile,  names = ["stationId", "stateName"], delimiter = '\t')

    usadir = "../../USAdlyFileDir/"
    fileList = os.listdir(allgncFolder)       #get
    print("getUSAStationDlyFiles enter: " , len(fileList))
    for fileName in fileList:
        if fileName[0:11] in df["stationId"].unqiue():
            filePath = os.path.join(allgncFolder, fileName)
            copy2(filePath, usadir)

    
def main():
    #getUSAStationExecute()

    #test
    outfileUSAStationIdFile = "../output/outfileUSAStationId"
    #getOneStateStationCodeId(outfileUSAStationId, 'ma')
    allgncFolder = "../../ghcnd_all/"
    getUSAStationDlyFiles(outfileUSAStationIdFile, allgncFolder)
    
if __name__== "__main__":
  main()