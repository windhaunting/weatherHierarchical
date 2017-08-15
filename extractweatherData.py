#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 10:06:05 2017

@author: fubao
"""

# year 1945 to 2010 ?
import os

from commons import writeListRowToFileWriterTsv
from ghcndextractor import ghcndextractor
from readCityState import readcitySatesExecute

#set global filters (we will not filter by year)
def getDailyWeather(inputFile, outFile):
    #ghcndextractor.countries = ["US"]
    #ghcndextractor.states = ["NJ"]     
    
    ghcndextractor.ghcnFolder = inputFile  #"/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/weatherData"   
    
    ghcndextractor.readStationsFile()
    #print ("stations: ", ghcndextractor.stationIDCodesMap)
    ghcndextractor.readDailyFiles()
    #dayCSV = ghcndextractor.getDailyDataCSV(["12"], ["25"], ["USW00014780"])
    #print ("dayCSV: ", type(dayCSV))
    #dayDictList01= ghcndextractor.getDailyData(["12"], ["25"], ["USW00014780"])
    #print ("dayDictList1: ", dayDictList01)
    #generate month:
    months = []
    
    for i in range(1, 13):
        months.append(str(i))
    
    days = []
    for i in range(1, 32):
        days.append(str(i))
     
    #stationIDCodesLst = ghcndextractor.stationIDCodes
    
    stateCityMap, stateToCountyMap, countyToCityMap = readcitySatesExecute()

    dayDictList= ghcndextractor.getDailyUSDataYears(["2001"], ["12"], ["25"], ["USW00014780"])
    #dayDictList= ghcndextractor.getDailyUSDataYears(["1988"], ["12"], ["25"], ["USW00014780"])
    
    print ("dayDictList: ", type(dayDictList), dayDictList)
    fd = open(outFile,'a')
    for ele in dayDictList:
        writeListRowToFileWriterTsv(fd, [ele], '\t')


#get daily weather of usa
inputFile = "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/weatherData"   
outFile =  "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/weatherData/weatherParser/output/outFile01"
os.remove(outFile) if os.path.exists(outFile) else None
getDailyWeather(inputFile, outFile)