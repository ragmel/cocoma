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
MALLOC_LIMIT = 1000000

import sys
from Library import getHomepath
sys.path.insert(0, getHomepath() + '/distributions/')
from abstract_dist import *

class dist_real_trace1(abstract_dist):
    pass

def functionCount(emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,resType,HOMEPATH):
    
    #startLoad = int(distributionArg["startload"])
    #stopLoad = int(distributionArg["stopload"])
    trace = distributionArg["trace"]
    global MALLOC_LIMIT
    global RESTYPE
    RESTYPE = resType
    
    runStartTime = startTimesec
    # we check that the resource type is mem, if not we give malloc limit a value 1000000, because is not used for the other resource types
    
    if RESTYPE == "mem":
        MALLOC_LIMIT = int(distributionArg["malloclimit"])
    
    memReading=psutil.phymem_usage()
    allMemoryPc =(memReading.total/1048576.00)/100.00
    
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
    # load the first line
    prevline = f.readline()
    count = 1
    Tcount = count
    
    for line in f:
        CPUprev, MEMUSEDprev = prevline.split()
        CPU, MEMUSED = line.split()
        if RESTYPE == "mem":
            if MEMUSED == MEMUSEDprev:
                count = count+1
                Tcount = Tcount+1
                MEMUSEDprev = MEMUSED
                #prevline = line
            else:
                runDuration = count * FR
                count = 1
                # converting MEM in % to actual value in current machine
                MU=int(MEMUSEDprev)*allMemoryPc
                load = int(MU)
                insertLoad(load, runStartTime, runDuration)
                runStartTime = runStartTime + runDuration
                MEMUSEDprev = MEMUSED
                prevline = line
                
        if RESTYPE == "cpu":
            if CPU == CPUprev:
                count = count+1
                Tcount = Tcount+1
                CPUprev = CPU
                #prevline = line
            else:
                runDuration = count * FR
                count = 1
                load = int(CPUprev)
                insertLoad(load, runStartTime, runDuration)
                runStartTime = runStartTime + runDuration
                CPUprev = CPU
                prevline = line
    
    # if the total count is greater than 1 we still have last insert to do
    if Tcount > 1:
        # last run to insert        
        runDuration = count * FR
        CPU, MEMUSED = prevline.split()
        # converting MEM in % to actual value in current machine
        if RESTYPE == "mem":
                MU=int(MEMUSED)*allMemoryPc
                load = int(MU)
        if RESTYPE == "cpu":
                load = int(CPU)   
        
        insertLoad(load, runStartTime, runDuration)

    triggerType = "time"
    return stressValues, runStartTimeList, runDurations, triggerType

def insertRun(stressValue, startTime, runDuration):
    stressValues.append(stressValue)
    runStartTimeList.append(startTime)
    runDurations.append(runDuration)

# this function checks if the load is higher than the malloc limit. In that case creates smaller runs
def insertLoad(load, startTime, duration):
    # if not a resource tyme MEM we just insert it
    if load > MALLOC_LIMIT and RESTYPE == "mem":
        div = int(load // MALLOC_LIMIT)
        rest = load - (div * MALLOC_LIMIT)
        for _ in range(0,div):
            insertRun(MALLOC_LIMIT, startTime, duration)
        if rest > 0:
            insertRun(rest, startTime, duration)
    else:
        insertRun(load, startTime, duration)

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
        
        argNames={"trace":{"upperBound":999999,"lowerBound":0}}
        return argNames
   
    #get free amount of memory and set it to upper bound
    if Rtype.lower() == "mem":
        
        memReading=psutil.phymem_usage()
        allMemory =memReading.total/1048576

        #argNames={"startload":{"upperBound":allMemory,"lowerBound":50,},"stopload":{"upperBound":allMemory,"lowerBound":50}, "malloclimit":{"upperBound":4095,"lowerBound":50}, "trace":""}
        argNames={"malloclimit":{"upperBound":4095,"lowerBound":50},"trace":{"upperBound":999999,"lowerBound":0}}
#        print "Use Arg's: ",argNames," with mem"
        return argNames

if __name__=="__main__":
        
        pass
