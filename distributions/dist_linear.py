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

import sys
from collections import OrderedDict
from Library import getHomepath
sys.path.insert(0, getHomepath() + '/distributions/')
from abstract_dist import *
from numpy import linspace

import math, psutil

MALLOC_LIMIT = 4095

class dist_linear(abstract_dist):
    pass

def distHelp():
    '''
    Help method that gives description of linear distribution usage
    '''
    
    print "Linear distribution takes in start and stop load parameters and gradually increasing resource workload. Can be used with CPU,MEM,IO,NET resource types."
    return "Linear distribution takes in start and stop load parameters and gradually increasing resource workload. Can be used with CPU,MEM,IO,NET resource types."
    

def functionCount(emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,resType,HOMEPATH):
    '''
    The actual distribution function which counts start time, duration and stress value for each run of distribution.  
    '''
    # we check that the resource type is mem, if not we give malloc limit a value 1000000, because is not used for the other resource types
    
    startLoad = int(distributionArg["startload"])
    stopLoad = int(distributionArg["stopload"])
    triggerType="time"
    
    upperBoundary= int(distributionGranularity)-1
    duration = float(duration)
    
    #lists for return
    stressValues = []        
    runStartTimeList=[]         
    runDurations = []
    runDuration = int(duration)/distributionGranularity
    runDuration = float(runDuration)
    
    if int(distributionGranularity)==1:
        stressValues.append(startLoad)
        runStartTimeList.append(startTimesec)
        runDurations.append(runDuration)
        return stressValues, runStartTimeList, runDurations, triggerType

    
    else:
        stressValues = map(int, linspace(startLoad, stopLoad, distributionGranularity))
        
        runStartTimeList = map (int, linspace(startTimesec, ((startTimesec + duration)-runDuration), distributionGranularity))
#        runStartTimeList = [sum(i) for i in enumerate(runStartTimeList)]
        
        runDurations = [runDuration]*distributionGranularity
        
        if resType.lower() == "mem":
            [mallocSplit(i, stressValues, runStartTimeList, runDurations) for i, load in enumerate(stressValues) if load > MALLOC_LIMIT]
        
        return stressValues, runStartTimeList, runDurations, triggerType

def mallocSplit (indexPostition, stressValues, runStartTimeList, runDurations):
    #Used to split MEM jobs that are larger than MALLOC_LIMIT
    remainingLoad = int(stressValues[indexPostition] - MALLOC_LIMIT)
    stressValues[indexPostition] = MALLOC_LIMIT
    stressValues.insert(indexPostition + 1, remainingLoad)
    runStartTimeList.insert(indexPostition + 1, runStartTimeList[indexPostition])
    runDurations.insert(indexPostition + 1, runDurations[indexPostition])


def argNames(Rtype=None):
        '''
        We specify how many arguments distribution instance require to run properly
        Rtype = <CPU,MEM,IO,NET>
        IMPORTANT: All argument variable names must be in lower case
        '''
        #discovery of supported resources
        if Rtype == None:
            argNames = ["cpu","mem","io","net"]
            
            return argNames
    
        if Rtype.lower() == "cpu":
            
            argNames=[("duration",{"upperBound":100000,"lowerBound":0, "argHelp":"Time Distribution lasts for.\nUnits: seconds"}),
                      ("granularity", {"upperBound":100000,"lowerBound":0, "argHelp":"Number of runs to create"}),
                      ("minJobTime",{"upperBound":10000000,"lowerBound":2, "argHelp":"Minimum time a single job's duration can be (any jobs under will be deleted).\nUnits: seconds (Min 2)"}),
                      ("startload",{"upperBound":100,"lowerBound":0, "argHelp":"Value for distribution to start at.\nUnits: %"}),
                      ("stopload", {"upperBound":100,"lowerBound":0, "argHelp":"Value for distribution to stop at.\nUnits: %"})]
            return OrderedDict(argNames)
       
        #get free amount of memory and set it to upper bound
        if Rtype.lower() == "mem":
            
            memReading=psutil.phymem_usage()
            allMemory =memReading.total/1048576

            argNames=[("duration", {"upperBound":100000,"lowerBound":0, "argHelp":"Time Distribution lasts for.\nUnits: seconds"}),
                      ("granularity", {"upperBound":100000,"lowerBound":0, "argHelp":"Number of runs to create"}),
                      ("minJobTime", {"upperBound":10000000,"lowerBound":2, "argHelp":"Minimum time a single job's duration can be (any jobs under will be deleted).\nUnits: seconds (Min 2)"}),
                      ("startload", {"upperBound":allMemory,"lowerBound":50, "argHelp":"Value for distribution to begin at.\nUnits: MB or %\ne.g. '10' (for 10MB) or '10%'"}),
                      ("stopload", {"upperBound":allMemory,"lowerBound":50, "argHelp":"Value for distribution to stop at.\nUnits: MB or %\ne.g. '10' (for 10MB) or '10%'"})]
            return OrderedDict(argNames)
            
        if Rtype.lower() == "io":
            argNames=[("duration", {"upperBound":100000,"lowerBound":0, "argHelp":"Time Distribution lasts for.\nUnits: seconds"}),
                      ("granularity", {"upperBound":100000,"lowerBound":0, "argHelp":"Number of runs to create"}),
                      ("minJobTime", {"upperBound":10000000,"lowerBound":2, "argHelp":"Minimum time a single job's duration can be (any jobs under will be deleted).\nUnits: seconds (Min 2)"}),
                      ("startload", {"upperBound":999999,"lowerBound":0, "argHelp":"Value for distribution to begin at.\nUnits: MB/s throughput"}),
                      ("stopload", {"upperBound":999999,"lowerBound":0, "argHelp":"Value for distribution to end at.\nUnits: MB/s throughput"})]
            return OrderedDict(argNames)
        
        if Rtype.lower() == "net":
            argNames=[("duration", {"upperBound":100000,"lowerBound":0, "argHelp":"Time Distribution lasts for.\nUnits: seconds"}),
                      ("granularity", {"upperBound":100000,"lowerBound":0, "argHelp":"Number of runs to create"}),
                      ("minJobTime", {"upperBound":10000000,"lowerBound":2, "argHelp":"Minimum time a single job's duration can be (any jobs under will be deleted).\nUnits: seconds (Min 2)"}),
                      ("startload", {"upperBound":999999,"lowerBound":0, "argHelp":"Value for distribution to begin at.\nUnits: MB/s throughput"}),
                      ("stopload", {"upperBound":999999,"lowerBound":0, "argHelp":"Value for distribution to end at.\nUnits: MB/s throughput"})]
            return OrderedDict(argNames)