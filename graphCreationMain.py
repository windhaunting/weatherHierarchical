#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 12:49:10 2017

@author: fubao
"""

#main function for creation graph data
from readCityState import readcityStateExl

class graphCreation:
    startNodeId = 1            #graph node Id starting from 1

    graphNodeNameToIdMap  = {}            #store node name -> ID map
    def __init__(self):
      self.x = 1
      
      
    def createNodeIdPlaces():
        stateCityMap, stateToCountyMap, countyToCityMap = readcityStateExl()
        for state, city in stateCityMap.items():
            if state not in graphNodeNameToIdMap:
                graphNodeNameToIdMap[state] = self.startNodeId
                startNodeId += 1
            if city not in raphNodeNameToIdMap:
                graphNodeNameToIdMap[city] = startNodeId
                startNodeId += 1
            #get edge list
            
     
    #read the output of extrated daily weather (getDailyWeather) into edge list
    def readstationWeatherOutput():
        x = 1


def main():
    x = 1
    
if __name__== "__main__":
  main()