# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 11:52:41 2016

@author: fubao
"""

import csv
import numpy as np

#read file
def mycsv_reader(csv_reader):         #
  while True: 
    try: 
      yield next(csv_reader) 
    except csv.Error: 
      # error handling what you want.
      pass
    continue 
  return


#write list
def writeListRowToFileWriterTsv(fd, listRow, delimiter):
 #   with open(outFile, "a") as fd:
    writer = csv.writer(fd, delimiter = delimiter, lineterminator='\n')
    writer.writerows([listRow])

#write string
def appendStringRowToFileWriterTsv(fd, stringRow):
 #   with open(outFile, "a") as fd:
    #fd = open(outFile,'a')
    fd.write(stringRow)
    #fd.close()
    
#transfer object/string to float
def get_series_ids(x):
    '''Function returns a pandas series consisting of ids, 
       corresponding to objects in input pandas series x
       Example: 
       get_series_ids(pd.Series(['a','a','b','b','c'])) 
       returns Series([0,0,1,1,2], dtype=int)'''

    values = np.unique(x)
    values2nums = dict(zip(values,range(len(values))))
    return x.replace(values2nums)