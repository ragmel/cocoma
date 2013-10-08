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
from Library import getHomepath
sys.path.insert(0, getHomepath() + '/distributions/')
from abstract_dist import *

import math, psutil

class dist_linear(abstract_dist):
    pass

def distHelp():
    '''
    Help method that gives description of fuzz distribution usage
    '''

    print "Fuzz distribution takes in startload and duration and supplies these values to the Backfuzz emulator (along with several emulator parameters). This is only for use with the backfuzz emulator to simulate malicious network activity"
    return "Fuzz distribution takes in startload and duration and supplies these values to the Backfuzz emulator (along with several emulator parameters). This is only for use with the backfuzz emulator to simulate malicious network activity"
    

def functionCount(emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,resType,HOMEPATH):
    
    startLoad = int(distributionArg["startload"])

    duration = float(duration)

    #lists for return
    stressValues = [startLoad]
    runStartTimeList = [startTimesec]
    runDurations = [duration]

    triggerType = "time"
    return stressValues, runStartTimeList, runDurations, triggerType

def argNames(Rtype=None):

        '''
        We specify how many arguments distribution instance require to run properly
        Rtype = <NET>
        IMPORTANT: All argument variable names must be in lower case
        '''

        #discovery of supported resources
        if Rtype == None:
            argNames = ["net"]

            return argNames

        if Rtype.lower() == "net":
            argNames = {"startload":{"upperBound":1000000,"lowerBound":0}}
            return argNames



if __name__ == "__main__": #For testing
    try:
#        functionCount()
#        obj.insertRun()
#        obj.insertLoad()
        distHelp()
        argNames()
    except NotImplementedError:
        print "Some methods not implemented"