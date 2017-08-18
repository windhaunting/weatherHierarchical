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
import time

from commons import writeListRowToFileWriterTsv

from ghcndextractor import ghcndextractor
from readCityState import getOneStateStationCodeId

#set global filters (we will not filter by year)
#stationIDCodesUSALst = []

#read all the station code Id of USA
def readUSAStation(inputFile):
    stationIDCodesUSALst = []
    with codecs.open(inputFile, 'rU') as csvfile:
         tsvin = csv.reader(csvfile, delimiter='\t')
         for row in tsvin:
             #print ("stationCodeId: ", stationCodeId)
             stationCodeId = row[0].strip()
             stationIDCodesUSALst.append(stationCodeId)
    
    return stationIDCodesUSALst

#get the daily data of days in months, years
def getDailyWeather(inputFile, years, months, days, stationIDCodesLst, outFile):
    #ghcndextractor.countries = ["US"]
    #ghcndextractor.states = ["NJ"]     
    
    ghcndextractor.ghcnFolder = inputFile  #"/home/fubao/workDir/ResearchProjects/GraphQuerySearchRelatedPractice/Data/weatherData"   
    
    #ghcndextractor.readStationsFile()
    #print ("stations: ", ghcndextractor.stationIDCodesMap)
    #ghcndextractor.readDailyFiles()
    #dayCSV = ghcndextractor.getDailyDataCSV(["12"], ["25"], ["USW00014780"])
    #print ("dayCSV: ", type(dayCSV))
    #dayDictList01= ghcndextractor.getDailyData(["12"], ["25"], ["USW00014780"])
    #print ("dayDictList1: ", dayDictList01)
    
    ghcndextractor.readStationsFileSelectStation(stationIDCodesLst)
    ghcndextractor.readDailyFilesSelectStation(stationIDCodesLst)
    #ddayDictList= ghcndextractor.getDailyUSDataYears(["2001"], ["12"], ["25"], ["USW00014780"])
    #dayDictList= ghcndextractor.getDailyUSDataYears(["1988"], ["12"], ["25"], ["USW00014780"])
    
    dayDictList= ghcndextractor.getDailyUSDataYears(years, months, days, stationIDCodesLst)

    #print ("dayDictList: ", type(dayDictList), dayDictList)
    fd = open(outFile,'a')
    for ele in dayDictList:
        writeListRowToFileWriterTsv(fd, [ele], '\t')


def main():
    
    #read USA stationCodeId
    outfileUSAStationId = "../output/outfileUSAStationId"
    stationIDCodesUSALst = readUSAStation(outfileUSAStationId)
    #print (" len stationIDCodesUSALst: ", len(stationIDCodesUSALst), stationIDCodesUSALst[0], stationIDCodesUSALst[1])
    #get daily weather of usa
    #generate years
    years = []
    for i in range(2000, 2011):
        years.append(str(i))
    
    #generate month:
    months = []
    for i in range(1, 13):
        months.append(str(i))
    
    days = []
    for i in range(1, 32):
        days.append(str(i))
        
    inputFile = "../../USAdlyFileDir"   
    outFile =  "../output/outFile01"
    os.remove(outFile) if os.path.exists(outFile) else None
    #state = 'ma'
    #stationIDCodesSeries = getOneStateStationCodeId(outfileUSAStationId, state)
    
    start = time.time()
    #getDailyWeather(inputFile, years, months, days, stationIDCodesSeries.tolist(), outFile)
    getDailyWeather(inputFile, years, months, days, stationIDCodesUSALst, outFile)
    end = time.time()
    print("time elpased for getDailyWeather: ", end - start)

if __name__== "__main__":
  main()