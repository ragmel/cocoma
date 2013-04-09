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

def functionCount(emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,HOMEPATH):
    
    startLoad = int(distributionArg["startload"])
    stopLoad = int(distributionArg["stopload"])
    
    # we check that the resource type is mem, if not we give malloc limit a value 1000000, because is not used for the other resource types
    MALLOC_LIMIT = 1000000
    if RESTYPE == "MEM":
        MALLOC_LIMIT = int(distributionArg["malloclimit"])
        
    
#    print "hello this is dist linear incr"
#    print "startLoad",startLoad
#    print "stopLoad",stopLoad
#    print "distributionGranularity",distributionGranularity
    
    duration = float(duration)
    runDuration = int(duration)/distributionGranularity
    runDuration = float(runDuration)
#    print "Duration is seconds:", runDuration
    
    runStartTime = startTimesec
    # check for the start load value if it's higher than malloc limit
    if startLoad < stopLoad:
        insertLoad(startLoad, runStartTime, duration, MALLOC_LIMIT)
    else:
        insertLoad(stopLoad, runStartTime, duration, MALLOC_LIMIT)

    if int(distributionGranularity)==1:
        return stressValues, runStartTimeList, runDurations
    
    else:
        runNo=int(1)
        
        #runStartTime=startTimesec+(duration*upperBoundary)
        # linearStep does not change, can be calculated just once
        linearStep=((int(stopLoad)-int(startLoad))/(int(distributionGranularity)-1))

        linearStep=math.fabs(linearStep)#making positive value
        linearStep=int(linearStep)

        upperBoundary= int(distributionGranularity)-1

        while(upperBoundary !=runNo):
#            print "Run No: ", runNo
#            print "self.startTimesec",startTimesec
            
            if startLoad < stopLoad:
                runStartTime=startTimesec+(runDuration*runNo)/2
                runDuration2 = duration - runDuration*runNo
            else:
                runDuration2 = (duration - runDuration*runNo)/2
                translatedStartTimesec = startTimesec + duration - runDuration2
                insertLoad(linearStep, translatedStartTimesec, runDuration2)

            insertLoad(linearStep,runStartTime, runDuration2, MALLOC_LIMIT)

            #increasing to next run            
            runNo=int(runNo)+1
        
#        print "Final Run"
        if startLoad < stopLoad:
            runStartTime = startTimesec+runDuration*upperBoundary/2
            insertLoad(linearStep, runStartTime, runDuration, MALLOC_LIMIT)
        else:
            runDuration2 = (duration - runDuration*upperBoundary)/2
            insertLoad(linearStep, runStartTime, runDuration2, MALLOC_LIMIT)
        
        
#        print "These are run stress Values:", stressValues
#        print "These are run start times:", runStartTimeList
#        print "These are run durations:", runDurations
            
        return stressValues, runStartTimeList, runDurations

def insertRun(stressValue, startTime, runRuration):
    stressValues.append(stressValue)
    runStartTimeList.append(startTime)
    runDurations.append(runRuration)
#    print "Inserted RUN: ", stressValue, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(startTime)), runRuration

# this function checks if the load is higher than the malloc limit. In that case creates smaller runs
def insertLoad(load, startTime, duration, mallocLimit):
    # if not a resource tyme MEM we just insert it
    if load > mallocLimit and RESTYPE == "MEM":
        div = int(load // mallocLimit)
        rest = load - (div * mallocLimit)
        for _ in range(0,div):
            insertRun(mallocLimit, startTime, duration)
        if rest > 0:
            insertRun(rest, startTime, duration)
    else:
        insertRun(load, startTime, duration)

def distHelp():
    
    print "Linear Distribution How-To:"
    print "Enter arg0 for first point and arg1 for 2nd point"
    
    print "Have fun"
    
    return "Linear Distribution How-To: Enter arg0 for first point and arg1 for 2nd point"
    
'''
here we specify how many arguments distribution instance require to run properly
'''

def argNames(Rtype):
    '''
    We specify how many arguments distribution instance require to run properly
    Rtype = <MEM, IO, NET>
    IMPORTANT: All argument variable names must be in lower case
    '''
   
    #get free amount of memory and set it to upper bound
    if Rtype.lower() == "mem":
        
        memReading=psutil.phymem_usage()
        allMemory =memReading.total/1048576

        argNames={"startload":{"upperBound":allMemory,"lowerBound":50,},"stopload":{"upperBound":allMemory,"lowerBound":50}, "malloclimit":{"upperBound":4095,"lowerBound":50}}
        RESTYPE = "MEM"
#        print "Use Arg's: ",argNames," with mem"
        return argNames
        
    if Rtype.lower() == "io":
        argNames={"startload":{"upperBound":999999,"lowerBound":0},"stopload":{"upperBound":999999,"lowerBound":0}}
        RESTYPE = "IO"
#        print "Use Arg's: ",argNames," with io"
        return argNames
    
    if Rtype.lower() == "net":
        argNames={"startload":{"upperBound":1000000,"lowerBound":0},"stopload":{"upperBound":1000000,"lowerBound":0}}
        RESTYPE = "NET"
#        print "Use Arg's: ",argNames," with net"
        return argNames
    


if __name__=="__main__":
        
        pass
