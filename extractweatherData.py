#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 10:06:05 2017

@author: fubao
"""

# year 1945 to 2010 ?
import os
import codecs
import csv

from commons import writeListRowToFileWriterTsv

from ghcndextractor import ghcndextractor
from readCityState import readcitySatesExecute

#set global filters (we will not filter by year)
stationIDCodesUSALst = []

#read all the station code Id of USA
def readUSAStation(inputFile):
    stationIDCodesUSALst = []
    with codecs.open(inputFile, 'rU') as csvfile:
         tsvin = csv.reader(csvfile, delimiter='\t')
         for row in tsvin:
             #print ("stationCodeId: ", stationCodeId)
             stationCodeId = row[0].strip()
             stationIDCodesUSALst.append(stationCodeId)
    

#get the daily data of days in months, years
def getDailyWeather(inputFile, years, months, days, outFile):
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
        
    stateCityMap, stateToCountyMap, countyToCityMap = readcitySatesExecute()

    #dayDictList= ghcndextractor.getDailyUSDataYears(["2001"], ["12"], ["25"], ["USW00014780"])
    #dayDictList= ghcndextractor.getDailyUSDataYears(["1988"], ["12"], ["25"], ["USW00014780"])
    
    dayDictList= ghcndextractor.getDailyUSDataYears(years, months, days, stationIDCodesUSALst)

    #print ("dayDictList: ", type(dayDictList), dayDictList)
    fd = open(outFile,'a')
    for ele in dayDictList:
        writeListRowToFileWriterTsv(fd, [ele], '\t')



def main():
    
    #read USA stationCodeId
    outfileUSAStationId = "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/weatherData/weatherParser/output/outfileUSAStationId"
    readUSAStation(outfileUSAStationId)
    
    #get daily weather of usa
    #generate years
    years = []
    for i in range(2010, 2011):
        years.append(str(i))
    
    #generate month:
    months = []
    for i in range(1, 13):
        months.append(str(i))
    
    days = []
    for i in range(1, 32):
        days.append(str(i))
        
    inputFile = "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/weatherData"   
    outFile =  "/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/weatherData/weatherParser/output/outFile01"
    os.remove(outFile) if os.path.exists(outFile) else None
    getDailyWeather(inputFile, years, months, days, outFile)
    

if __name__== "__main__":
  main()