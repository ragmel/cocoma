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
import random
#import sqlite3 as sqlite
#import datetime as dt
#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'

#lists for return
stressValues = []        
runStartTimeList= []         
runDurations = []
MALLOC_LIMIT = 4095

import sys
from Library import getHomepath
sys.path.insert(0, getHomepath() + '/distributions/')
from abstract_dist import *

class dist_exp(abstract_dist):
    pass

def functionCount(emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,resType,HOMEPATH):
    
    startLoad = int(distributionArg["startload"])
    stopLoad = int(distributionArg["stopload"])

    random.seed(100)
    
    duration = float(duration)
    timescale = duration/distributionGranularity

    mylambda = 1/float(timescale)
    runStartTime = startTimesec

    for x in xrange(1,distributionGranularity+1):
            timeON = timescale*x/distributionGranularity
            if timeON == timescale:
                timeOFF = 1
                timeON = timescale -1
            else:
                timeOFF = (timescale - timeON)
                
            durationLambda = 1/float(timeON)
            durationExp = random.expovariate(durationLambda)
            waitLambda = 1/float(timeOFF)
            waitExp = random.expovariate(waitLambda)
            insertLoad(startLoad,runStartTime, durationExp)
            runStartTime=runStartTime+durationExp+waitExp

    triggerType = "time"            
    return stressValues, runStartTimeList, runDurations, triggerType

def insertRun(stressValue, startTime, runRuration):
    stressValues.append(stressValue)
    runStartTimeList.append(startTime)
    runDurations.append(runRuration)
#    print "Inserted RUN: ", stressValue, time.strftime("%Y-%m-%d %H:%M:%S.%f", time.gmtime(startTime)), runRuration

# this function checks if the load is higher than the malloc limit. In that case creates smaller runs
def insertLoad(load, startTime, duration):
    # if not a resource type MEM we just insert it
    if load > MALLOC_LIMIT and resType == "mem":
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
        argNames = ["mem","io","net","cpu"]
        
        return argNames
    
    if Rtype.lower() == "cpu":
        
        argNames={"startload":{"upperBound":100,"lowerBound":0},"stopload":{"upperBound":100,"lowerBound":0}, "granularity":{"upperBound":100000,"lowerBound":0, "argHelp":"Number of runs to create"}, "duration":{"upperBound":100000,"lowerBound":0, "argHelp":"Time Distribution lasts for.\nUnits: seconds"}, "minJobTime":{"upperBound":10000000,"lowerBound":2, "argHelp":"Minimum time a single job's duration can be (any jobs under will be deleted).\nUnits: seconds"}}
        return argNames
       
    #get free amount of memory and set it to upper bound
    if Rtype.lower() == "mem":
        
        memReading=psutil.phymem_usage()
        allMemory =memReading.total/1048576

        argNames={"startload":{"upperBound":allMemory,"lowerBound":50, "argHelp":"Value for distribution to begin at.\nUnits: MB or %"},"stopload":{"upperBound":allMemory,"lowerBound":50, "argHelp":"Value for distribution to stop at.\nUnits: MB or %"}, "granularity":{"upperBound":100000,"lowerBound":0, "argHelp":"Number of runs to create"}, "duration":{"upperBound":100000,"lowerBound":0, "argHelp":"Time Distribution lasts for.\nUnits: seconds"}, "minJobTime":{"upperBound":10000000,"lowerBound":2, "argHelp":"Minimum time a single job's duration can be (any jobs under will be deleted).\nUnits: seconds"}}
        RESTYPE = "MEM"
#        print "Use Arg's: ",argNames," with mem"
        return argNames
        
    if Rtype.lower() == "io":
        argNames={"startload":{"upperBound":999999,"lowerBound":0, "argHelp":"Value for distribution to begin at.\nUnits: MB/s throughput"},"stopload":{"upperBound":999999,"lowerBound":0, "argHelp":"Value for distribution to stop at.\nUnits: MB/s throughput"}, "granularity":{"upperBound":100000,"lowerBound":0, "argHelp":"Number of runs to create"}, "duration":{"upperBound":100000,"lowerBound":0, "argHelp":"Time Distribution lasts for.\nUnits: seconds"}, "minJobTime":{"upperBound":10000000,"lowerBound":2, "argHelp":"Minimum time a single job's duration can be (any jobs under will be deleted).\nUnits: seconds"}}
        RESTYPE = "IO"
#        print "Use Arg's: ",argNames," with io"
        return argNames
    
    if Rtype.lower() == "net":
        argNames={"startload":{"upperBound":1000000,"lowerBound":0, "argHelp":"Value for distribution to begin at.\nUnits: MB/s throughput"},"stopload":{"upperBound":1000000,"lowerBound":0, "argHelp":"Value for distribution to stop at.\nUnits: MB/s throughput"}, "granularity":{"upperBound":100000,"lowerBound":0, "argHelp":"Number of runs to create"}, "duration":{"upperBound":100000,"lowerBound":0, "argHelp":"Time Distribution lasts for.\nUnits: seconds"}, "minJobTime":{"upperBound":10000000,"lowerBound":2, "argHelp":"Minimum time a single job's duration can be (any jobs under will be deleted).\nUnits: seconds"}}
        RESTYPE = "NET"
#        print "Use Arg's: ",argNames," with net"
        return argNames
    

if __name__=="__main__":
        pass