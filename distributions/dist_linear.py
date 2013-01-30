#Copyright 2012 SAP Ltd
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
import Pyro4,imp,time,sys, psutil
import sqlite3 as sqlite
import datetime as dt
#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'


class distributionMod(object):
    
    
    def __init__(self,emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,HOMEPATH):
        
        self.startLoad = distributionArg["startLoad"]
        self.stopLoad = distributionArg["stopLoad"]
        
        distributionGranularity_count=distributionGranularity
        #startTimesec = startTimesec
        duration = float(duration)
        
        runNo=int(0)
        
        print "Hello this is dist_linear"
        print "emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,arg,HOMEPATH",emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,HOMEPATH
        

def functionCount(emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,HOMEPATH):
    
    startLoad = int(distributionArg["startLoad"])
    stopLoad = int(distributionArg["stopLoad"])
    
    print "hello this is dist linear"
    print "startLoad",startLoad
    print "stopLoad",stopLoad
    print "distributionGranularity",distributionGranularity
    
    distributionGranularity_count=distributionGranularity
    upperBoundary= int(distributionGranularity)-1
    #startTimesec = startTimesec
    duration = float(duration)
    
    #lists for return
    stressValues = []        
    runStartTimeList=[]         
    
    
    #run 1 at 0 time
    runStartTimeList.append(startTimesec)
    stressValues.append(startLoad)
    
    if int(distributionGranularity)==1:
        return stressValues, runStartTimeList
    
    else:
        runNo=int(1)
        
        #runStartTime=startTimesec+(duration*upperBoundary)
        
    
        linearStress=0
        while(upperBoundary !=runNo):
        
                print "Run No: "
                print runNo
                print "self.startTimesec",startTimesec
                runStartTime=startTimesec+(duration*runNo)
                
                #delay of one sec
                runStartTime =(runStartTime+(2*runNo))
                
                
                runStartTimeList.append(runStartTime)
                print "This run start time: "
                print runStartTime
                print "This is time passed to scheduler:"
                print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime))
            
                '''
                1. Distribution formula goes here
                '''
                 
                
                linearStep=((int(startLoad)-int(stopLoad))/(int(distributionGranularity)-1))
                print "linearSterp",linearStep
                linearStep=math.fabs((int(linearStep)))#making positive value
                print "LINEAR STEP SHOULD BE THE SAME"
                print linearStep
                
                if startLoad < stopLoad:
                    
                    linearStress= (linearStep*int(runNo))+int(startLoad)
                if startLoad > stopLoad:
    
                    linearStress= (linearStep*(upperBoundary-int(runNo)))+int(stopLoad)
                
                if startLoad == stopLoad:
                    linearStress=startLoad
                    
                #make sure we return integer
                linearStress=int(linearStress)
                print "LINEAR STRESS SHOULD CHANGE"
                print linearStress
                
                
                
                
                stressValues.append(linearStress)
                print "This run stress Value: "
                print stressValues
                
                print "runStartTimeList",runStartTimeList
                 
                #increasing to next run            
                runNo=int(runNo)+1
                
            
                
        #run last plus 2sec
        runStartTimeList.append((startTimesec+duration*upperBoundary)+(int(upperBoundary*2)))
        stressValues.append(stopLoad)            
                
            
        return stressValues, runStartTimeList
    
    
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
    Rtype = <MEM, CPU, IO, NET>
    
    IMPORTANT: All argument variable names must be in lower case
    '''
    if Rtype.lower() == "cpu":
        
        argNames={"startload":{"upperBound":100,"lowerBound":0},"stopload":{"upperBound":100,"lowerBound":0}}
        print "Use Arg's: ",argNames," with cpu"
        return argNames
   
    #get free amount of memory and set it to upper bound
    if Rtype.lower() == "mem":
        
        memReading=psutil.phymem_usage()
        
        freeMem =memReading.free/1048576
        print "free mem for border:",freeMem
        

        argNames={"startload":{"upperBound":freeMem,"lowerBound":50},"stopload":{"upperBound":freeMem,"lowerBound":50}}
        print "Use Arg's: ",argNames," with mem"
        return argNames
    
    if Rtype.lower() == "mem%":
        memReading=psutil.phymem_usage()
        freeMemPercent=memReading.percent
        
        argNames={"startload":{"upperBound":freeMemPercent,"lowerBound":1},"stopload":{"upperBound":freeMemPercent,"lowerBound":1}}
        print "Use Arg's: ",argNames," with mem%"
        return argNames
        
    if Rtype.lower() == "io":
        argNames={"startload":{"upperBound":999999,"lowerBound":0},"stopload":{"upperBound":999999,"lowerBound":0}}
        print "Use Arg's: ",argNames," with io"
        return argNames
    
    if Rtype.lower() == "net":
        argNames={"startload":{"upperBound":10,"lowerBound":0},"stopload":{"upperBound":10,"lowerBound":0}}
        print "Use Arg's: ",argNames," with net"
        return argNames
    


if __name__=="__main__":
        
        pass
