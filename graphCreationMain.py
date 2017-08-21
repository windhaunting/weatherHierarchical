#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 12:49:10 2017

@author: fubao
"""

#main function for creation graph data
import os
from readCityState import readcitySatesExecute
from extractweatherData import readUSAStationIdToNameMap
from blist import blist
import pandas as pd

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
    edgeList = blist()                       #graph edge list  "nodeId, nodeId, edge"
    def __init__(self):
      pass
      
      
    def createNodeIdPlaces(self):
        stateCityMap, stateToCountyMap, countyToCityMap = readcitySatesExecute()
        #get state and county edge list
        for state, counties in stateToCountyMap.items():
            nodeInfoState = state + "+" + str(nodeType.placeType)
            #store state and id mapping
            if nodeInfoState not in graphCreationClass.graphNodeNameToIdMap:
                graphCreationClass.graphNodeNameToIdMap[nodeInfoState] = graphCreationClass.startNodeId
                graphCreationClass.gNodeIdToNameMap[graphCreationClass.startNodeId] = nodeInfoState
                #node type map
                if graphCreationClass.startNodeId not in graphCreationClass.graNodeTypeMap:
                    graphCreationClass.graNodeTypeMap[graphCreationClass.startNodeId] = nodeType.placeType

                graphCreationClass.startNodeId += 1
                
            #store county and id mapping
            for county in set(counties):
                nodeInfoCounty = county + "+" + str(nodeType.placeType) 
                if county not in graphCreationClass.graphNodeNameToIdMap:
                    graphCreationClass.graphNodeNameToIdMap[nodeInfoCounty] = graphCreationClass.startNodeId
                    graphCreationClass.gNodeIdToNameMap[graphCreationClass.startNodeId] = nodeInfoCounty
                    #node type map
                    if graphCreationClass.startNodeId not in graphCreationClass.graNodeTypeMap:
                        graphCreationClass.graNodeTypeMap[graphCreationClass.startNodeId] = nodeType.placeType
    
                    graphCreationClass.startNodeId += 1
                #get edge list for each pair
                edgeProp = 'lower'                          #lower hierarchical relation
                graphCreationClass.edgeList.append([graphCreationClass.graphNodeNameToIdMap[nodeInfoState], graphCreationClass.graphNodeNameToIdMap[nodeInfoCounty], edgeProp])
                edgeProp = 'higher'
                graphCreationClass.edgeList.append([graphCreationClass.graphNodeNameToIdMap[nodeInfoCounty], graphCreationClass.graphNodeNameToIdMap[nodeInfoState], edgeProp])
            
        #get county and city edge list
        for county, cities in countyToCityMap.items():
            #store state and id mapping
            nodeInfoCounty = county + "+" + str(nodeType.placeType) 
            if county not in graphCreationClass.graphNodeNameToIdMap:
                graphCreationClass.graphNodeNameToIdMap[nodeInfoCounty] = graphCreationClass.startNodeId
                graphCreationClass.gNodeIdToNameMap[graphCreationClass.startNodeId] = nodeInfoCounty
                #node type map
                if graphCreationClass.startNodeId not in graphCreationClass.graNodeTypeMap:
                    graphCreationClass.graNodeTypeMap[graphCreationClass.startNodeId] = nodeType.placeType
                graphCreationClass.startNodeId += 1
                
            #store city and id mapping
            for city in set(cities):
                nodeInfoCity = city + "+" + str(nodeType.placeType) 
                if city not in graphCreationClass.graphNodeNameToIdMap:
                    graphCreationClass.graphNodeNameToIdMap[nodeInfoCounty] = graphCreationClass.startNodeId
                    graphCreationClass.gNodeIdToNameMap[graphCreationClass.startNodeId] = nodeInfoCounty
                    
                    #node type map
                    if graphCreationClass.startNodeId not in graphCreationClass.graNodeTypeMap:
                        graphCreationClass.graNodeTypeMap[graphCreationClass.startNodeId] = nodeType.placeType
                        
                    graphCreationClass.startNodeId += 1
                #get edge list for each pair
                edgeProp = 'lower'             #lower hierarchical relation
                graphCreationClass.edgeList.append([graphCreationClass.graphNodeNameToIdMap[nodeInfoCounty], graphCreationClass.graphNodeNameToIdMap[nodeInfoCity], edgeProp])
                edgeProp = 'higher'
                graphCreationClass.edgeList.append([graphCreationClass.graphNodeNameToIdMap[nodeInfoCity], graphCreationClass.graphNodeNameToIdMap[nodeInfoCounty], edgeProp])
    
                
    #read the output of extrated daily weather (getDailyWeather) into edge list
    #'stationID','year','month','day','tmax','tmin','snwd','acmm', 'acss','prcp','snow'])
    def readstationWeatherOutput(self, inUSAStationFile, inFileStationWeather):
        stationIDCodesUSAToNameMap = readUSAStationIdToNameMap(inUSAStationFile)

        df = pd.read_csv(inFileStationWeather, delimiter = "\t")
        #create edge list between city/town and weather
        df['stationTemp'] = list(zip(df["stationID"], df["tmax"], df["tmin"]))        #station temperature
        #print ("stationTemp: ", df['stationTemp'])
        #get temperature
        for tple in df['stationTemp'].unique():
            nodeInfoCity = stationIDCodesUSAToNameMap[tple[0]].split(',')[1].lower().strip() + "+" + str(nodeType.placeType) #state,city
            #print ("stationCity: ", stationCity, type(tple), type(tple[1]))
            
            if tple[1] is not None:
                nodeInfoTmperature = "[" + str(tple[2]) + "," + str(tple[1]) + "]" + "+" + str(nodeType.tempType)
                if nodeInfoTmperature not in graphCreationClass.graphNodeNameToIdMap:
                    graphCreationClass.graphNodeNameToIdMap[nodeInfoTmperature] = graphCreationClass.startNodeId
                    graphCreationClass.gNodeIdToNameMap[graphCreationClass.startNodeId] = nodeInfoTmperature
                    
                    if graphCreationClass.startNodeId not in graphCreationClass.graNodeTypeMap:
                        graphCreationClass.graNodeTypeMap[graphCreationClass.startNodeId] = nodeType.tempType
                    graphCreationClass.startNodeId += 1
                    
                 #edge for town/city to temperature
                 #cityNodeId = graphCreationClass.graphNodeNameToIdMap[stationCity]
                if nodeInfoCity in graphCreationClass.graphNodeNameToIdMap:
                    
                    edgeProp = 'same'             #lower hierarchical relation
                    graphCreationClass.edgeList.append([graphCreationClass.graphNodeNameToIdMap[nodeInfoCity], graphCreationClass.graphNodeNameToIdMap[nodeInfoTmperature], edgeProp])             
                    graphCreationClass.edgeList.append([graphCreationClass.graphNodeNameToIdMap[nodeInfoTmperature], graphCreationClass.graphNodeNameToIdMap[nodeInfoCity], edgeProp])             
         
        
        #get precipitation
        df['stationPrcp'] = list(zip(df["stationID"], df["prcp"]))        #station temperature
        for tple in df['stationPrcp']:
            stationCity = stationIDCodesUSAToNameMap[tple[0]].split(',')[1].lower().strip()     #state,city
            if tple[1] is not None:
                prcp = str(tple[1])
                if prcp not in graphCreationClass.graphNodeNameToIdMap:
                    graphCreationClass.graphNodeNameToIdMap[prcp] = graphCreationClass.startNodeId
                    graphCreationClass.gNodeIdToNameMap[graphCreationClass.startNodeId] = prcp
                    
                    if graphCreationClass.startNodeId not in graphCreationClass.graNodeTypeMap:
                        graphCreationClass.graNodeTypeMap[graphCreationClass.startNodeId] = nodeType.prcpType
                        #print("ddddddddddddddddddd: ", nodeType.prcpType)
                    graphCreationClass.startNodeId += 1
        
        #get snow type
        df['stationsnwd'] = list(zip(df["stationID"], df["snwd"]))        #station temperature
        print ("stationsnwd describe", df['stationsnwd'].describe())
        for tple in df['stationsnwd'].unique():
            stationCity = stationIDCodesUSAToNameMap[tple[0]].split(',')[1].lower().strip()     #state,city
            if tple[1] is not None:
                snwd = str(tple[1])
                print("previous eeeeeeeeeeeeeeeeee: ", nodeType.snowType, snwd)
                if snwd not in graphCreationClass.graphNodeNameToIdMap:
                    graphCreationClass.graphNodeNameToIdMap[snwd] = graphCreationClass.startNodeId
                    if graphCreationClass.startNodeId not in graphCreationClass.graNodeTypeMap:
                        graphCreationClass.graNodeTypeMap[graphCreationClass.startNodeId] = nodeType.snowType
                        print("eeeeeeeeeeeeeeeee: ", nodeType.snowType)

                    graphCreationClass.startNodeId += 1
                    
        #get time month/day/year
        df['tempTime'] = list(zip(df["tmax"], df["tmin"],df["month"], df["day"], df["year"]))        #station temperature

        for tple in df['tempTime'].unique():
            if tple[1] is not None and tple[3] is not None:         #temp tmin and time day is not None
                tmperature = str(tple[1]) + "--" + str(tple[0])
                time = str(tple[2]) + "/" + str(tple[3]) + "/" + str(tple[4])
                
                if tmperature not in graphCreationClass.graphNodeNameToIdMap:
                    graphCreationClass.graphNodeNameToIdMap[tmperature] = graphCreationClass.startNodeId
                    if graphCreationClass.startNodeId not in graphCreationClass.graNodeTypeMap:
                        graphCreationClass.graNodeTypeMap[graphCreationClass.startNodeId] = nodeType.tempType
                        print("fffffffffffffffffff: ", nodeType.tempType)

                    graphCreationClass.startNodeId += 1
                if time not in graphCreationClass.graphNodeNameToIdMap:
                    graphCreationClass.graphNodeNameToIdMap[tmperature] = graphCreationClass.startNodeId
                    
                    
    #write graphNodeNameToIdMap, graNodeTypeMap, and edgeList
    def writeIntoFile(self, outNodeTypeFile, outNodeNameToIdFile, outEdgeListFile):
        #write node type file
        df = pd.DataFrame.from_dict(graphCreationClass.graNodeTypeMap, orient='index')
        df.to_csv(outNodeTypeFile, sep='\t')
        
        
    
        #write edge list
    
    
    def testOnlyDictionaryWrite(self):
        dic = {5:0, 3:0, 4:1}
        df = pd.DataFrame.from_dict(dic, orient='index')
        df.to_csv("../testoutfile", sep='\t')
    
    
def main():
    
    gcObj = graphCreationClass()
    gcObj.createNodeIdPlaces()    
    print ('len graphCreationClass edgelist before: ', len(graphCreationClass.edgeList))
    
    inFileStationWeather = "../output/outFileStationWeather2000-2011MA.tsv"
    outfileUSAStationId = "../output/outfileUSAStationId"
    gcObj.readstationWeatherOutput(outfileUSAStationId, inFileStationWeather)
    
    
    #gcObj.testDictionaryWrite()
    
    outNodeTypeFile = "../output/outNodeTypeFile.csv"
    outNodeNameToIdFile = "../output/outNodeNameToIdFile.csv"
    outEdgeListFile = "../output/outEdgeListFile.csv"
    print ('len graphCreationClass edgelist after: ', len(graphCreationClass.edgeList), len(graphCreationClass.graNodeTypeMap))
    
    os.remove(outNodeTypeFile) if os.path.exists(outNodeTypeFile) else None

    gcObj.writeIntoFile(outNodeTypeFile, outNodeNameToIdFile, outEdgeListFile)
    
if __name__== "__main__":
  main()