#Copyright 2012-2013 SAP Ltd
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# This is part of the COCOMA framework
#
# COCOMA is a framework for COntrolled COntentious and MAlicious patterns
#

import math
import Pyro4, time, psutil
#import sqlite3 as sqlite
#import datetime as dt
#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'

#lists for return
stressValues = []
runStartTimeList=[]
runDurations = []

RESTYPE = "null"
MALLOC_LIMIT = 4095

import sys
import Library
from Library import getHomepath
sys.path.insert(0, getHomepath() + '/distributions/')
from abstract_dist import *

class dist_real_trace1(abstract_dist):
    pass

def functionCount(emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,resType,HOMEPATH):
    
    #startLoad = int(distributionArg["startload"])
    #stopLoad = int(distributionArg["stopload"])
    trace = distributionArg["trace"]
    groupingRange = int(distributionArg["groupingrange"])
    global RESTYPE
    RESTYPE = resType
    global stressValues
    global runStartTimeList
    global runDurations
    
#    memReading=psutil.phymem_usage()
#    allMemoryPc =(memReading.total/1048576.00)/100.00
    
    try:
    
        f = open(trace, 'r')
        #print f
        line = f.readline()
        HEAD, NCPUS = line.strip().split("\t")
        line = f.readline()
        HEAD, MEMTOTAL = line.strip().split("\t")
        line = f.readline()
        HEAD, TIMESTAMP = line.strip().split("\t")
        line = f.readline()
        HEAD, POLLFR = line.strip().split("\t")
        FR = int(POLLFR)
        # skip the header
        prevline = f.readline()

        memArray = []
        cpuArray = []
        for line in f:
            cpuValue, memValue = line.split()
            memArray.append(memValue)
            cpuArray.append(cpuValue)
    
        if RESTYPE == "mem":
            if ("MEMUSED%" in prevline):
                memArray = Library.memToInt(memArray) #Convert memory stressValues from % to real values
            else:
                memArray = map(lambda stressVal: int(stressVal)  // (1024**2), memArray)
#                for memVal in memArray: memVal = memVal / (1024**2) #Convert from Bytes into MegaBytes
            groupingRange = (Library.getTotalMem() // 100) * groupingRange #Convert from % to real value
            (stressValues, runStartTimeList, runDurations) = Library.realTraceSmoothing(memArray, startTimesec, FR, groupingRange)
            splitMemMalloc()
            
        if RESTYPE == "cpu":
            (stressValues, runStartTimeList, runDurations) = Library.realTraceSmoothing(cpuArray, startTimesec, FR, groupingRange)

            
    except Exception, e:
        return "Unable to create distribution:\n" + str(e)

    triggerType = "time"
    return stressValues, runStartTimeList, runDurations, triggerType


#Checks if mem stressvalue is higher than MALLOC_LIMIT, splits jobs if so
def splitMemMalloc():
    global stressValues
    global runStartTimeList
    global runDurations
    mallocReached = True
    
    while (mallocReached):
        mallocReached = False
        tempJobs = [] #Holds details of split jobs, to be merged with main arrays/lists
        for i, stressValue in enumerate(stressValues): 
            if stressValue > MALLOC_LIMIT:
                stressValues[i] = MALLOC_LIMIT
                tempJob = [i, stressValue-MALLOC_LIMIT, runStartTimeList[i], runDurations[i]]
                tempJobs.append(tempJob)
                mallocReached = True
        
        for tempJob in reversed(tempJobs): #Add the values into the lists at position tempJob[0]
            stressValues.insert(tempJob[0]+1,tempJob[1])
            runStartTimeList.insert(tempJob[0]+1,tempJob[2])
            runDurations.insert(tempJob[0]+1,tempJob[3])
    
    print "stressValues out ", stressValues #REMOVE

def distHelp():
    '''
    Help method that gives description of trapezoidal distribution usage
    '''
    
    print "Trapezoidal distribution takes in start and stop load (plus malloclimit for MEM) parameters and gradually increasing resource workload by spawning jobs in parallel. Can be used with MEM,IO,NET resource types."
        
    return "Trapezoidal distribution takes in start and stop load (plus malloclimit for MEM) parameters and gradually increasing resource workload by spawning jobs in parallel. Can be used with MEM,IO,NET resource types."
    

def argNames(Rtype=None):
    '''
    We specify how many arguments distribution instance require to run properly
    Rtype = <MEM, IO, NET>
    IMPORTANT: All argument variable names must be in lower case
    '''

    #discovery of supported resources
    if Rtype == None:
        argNames = ["mem","cpu"]
        
        return argNames
   
    if Rtype.lower() == "cpu":
        
        argNames={"trace":{"upperBound":999999,"lowerBound":0, "argHelp":"Path to trace file (must be lower-case).\nSee documentation for additional help"}, "groupingRange":{"upperBound":99,"lowerBound":1, "argHelp":"Range to group jobs together by.\nSee documentation for additional help"}, "minJobTime":{"upperBound":10000000,"lowerBound":2, "argHelp":"Minimum time a single job's duration can be (any jobs under will be deleted).\nUnits: seconds"}}
        return argNames
   
    #get free amount of memory and set it to upper bound
    if Rtype.lower() == "mem":
        
        memReading=psutil.phymem_usage()
        allMemory =memReading.total/1048576

        argNames={"trace":{"upperBound":999999,"lowerBound":0, "argHelp":"Path to trace file (must be lower-case).\nSee documentation for additional help"}, "groupingRange":{"upperBound":99,"lowerBound":1, "argHelp":"Range to group jobs together by.\nSee documentation for additional help"}, "minJobTime":{"upperBound":10000000,"lowerBound":2, "argHelp":"Minimum time a single job's duration can be (any jobs under will be deleted).\nUnits: seconds"}}
        return argNames

if __name__=="__main__":
        pass