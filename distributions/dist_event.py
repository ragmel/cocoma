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

import math,psutil,Library

import sys
from Library import getHomepath
sys.path.insert(0, getHomepath() + '/distributions/')
from abstract_dist import *

class dist_event(abstract_dist):
    pass

def functionCount(emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,resType,HOMEPATH):
    '''
    The actual distribution function which counts start time, duration and stress value for each run of distribution.  
    '''
    
    try:
        nextevent = distributionArg["nextevent"]
    except:
        nextevent="none"
    
    
    duration = float(duration)
    
    #lists for return
    stressValues = []
    
    runStartTimeList=[]
    runDurations = [0]
    
    
    stressValues.append(nextevent)
    runStartTimeList.append(startTimesec)
    
    triggerType="event"
    return stressValues,runStartTimeList,runDurations, triggerType
    
    
def distHelp():
    '''
    Help method that gives description of linear distribution usage
    '''
    
    print "Event driven distribution.Can be only used with emulators that eventually will terminate by themselves with static parameters. Distributions within payload XML are processed sequentially,order matters."
    return "Event driven distribution.Can be only used with emulators that eventually will terminate by themselves with static parameters. Distributions within payload XML are processed sequentially,order matters."
    
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
        
        argNames={"nextevent":{"upperBound":1000000,"lowerBound":0}}
        return argNames
   
    #get free amount of memory and set it to upper bound
    if Rtype.lower() == "mem":
        
        argNames={"nextevent":{"upperBound":1000000,"lowerBound":0}}
        return argNames
        
    if Rtype.lower() == "io":
        argNames={"nextevent":{"upperBound":1000000,"lowerBound":0}}
        return argNames
    
    if Rtype.lower() == "net":
        argNames={"nextevent":{"upperBound":1000000,"lowerBound":0}}
        return argNames
    


if __name__=="__main__":
        distHelp()
        pass