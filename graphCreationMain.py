#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 12:49:10 2017

@author: fubao
"""

#main function for creation graph data
from readCityState import readcitySatesExecute
from blist import blist

class nodeType:
    placeType = 1
    timeType = 2             #time type, year, month or day time
    tempType = 3             #temperature range
    prcpType = 4             #precipation
    snowType = 5             #snow depth
    
class graphCreationClass:
    startNodeId = 1            #graph node Id starting from 1
    graphNodeNameToIdMap  = {}            #store node name -> ID map
    gNodeIdToNameMap  = {}               #store node id -> name  map
    
    graNodeTypeMap = {}                 #node id to type
    edgeList = blist()                       #graph edge list
    def __init__(self):
      pass
      
      
    def createNodeIdPlaces(self):
        stateCityMap, stateToCountyMap, countyToCityMap = readcitySatesExecute()
        #get state and county edge list
        for state, county in stateToCountyMap.items():
            #store state and id mapping
            if state not in graphCreationClass.graphNodeNameToIdMap:
                graphCreationClass.graphNodeNameToIdMap[state] = graphCreationClass.startNodeId
                graphCreationClass.gNodeIdToNameMap[graphCreationClass.startNodeId] = state
                #node type map
                if graphCreationClass.startNodeId not in graphCreationClass.graNodeTypeMap:
                    graphCreationClass.graNodeTypeMap[graphCreationClass.startNodeId] = nodeType.placeType

                
                graphCreationClass.startNodeId += 1
                
            #store county and id mapping
            if county not in graphCreationClass.graphNodeNameToIdMap:
                graphCreationClass.graphNodeNameToIdMap[county] = graphCreationClass.startNodeId
                #node type map
                if graphCreationClass.startNodeId not in graphCreationClass.graNodeTypeMap:
                    graphCreationClass.graNodeTypeMap[graphCreationClass.startNodeId] = nodeType.placeType

                graphCreationClass.startNodeId += 1
            #get edge list for each pair
            edgeProp = 'lower'                          #lower hierarchical relation
            graphCreationClass.edgeList.append([state, county, edgeProp])
            
            
        #get county and city edge list
        for county, city in countyToCityMap.items():
            #store state and id mapping
            if county not in graphCreationClass.graphNodeNameToIdMap:
                graphCreationClass.graphNodeNameToIdMap[county] = graphCreationClass.startNodeId
                graphCreationClass.gNodeIdToNameMap[graphCreationClass.startNodeId] = county
                
                graphCreationClass.startNodeId += 1
            #store city and id mapping
            if city not in graphCreationClass.graphNodeNameToIdMap:
                graphCreationClass.graphNodeNameToIdMap[city] = graphCreationClass.startNodeId
                graphCreationClass.startNodeId += 1
            #get edge list for each pair
            edgeProp = 'lower'             #lower hierarchical relation
            graphCreationClass.edgeList.append([state, city, edgeProp])
    
    
    #read the output of extrated daily weather (getDailyWeather) into edge list
    def readstationWeatherOutput(self):
        x = 1


def main():
    
    gcObj = graphCreationClass()
    gcObj.createNodeIdPlaces()    
    print ('len graphCreationClass edgelist: ', len(graphCreationClass.edgeList))
    
if __name__== "__main__":
  main()