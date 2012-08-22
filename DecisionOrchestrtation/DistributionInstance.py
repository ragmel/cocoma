'''
Created on 21 Aug 2012

@author: i046533

note: required information needs to be passed down from emulationProcessor in future as it determines emulatorID we are using
we require :
emulatorID
granularity
start and end time

we need to get here:
run duration in seconds 
then divide it by granularity to know amount of runs
get each run start and end date 
send it to DB(maybe) for scheduler in this format:
emulationID emulatorID runID runStartDate runEndDate

'''
import datetime as dt
import time

class distributionInstance(object):
    def __init__(self, emulatorID, distributionType, distributionGranularity , distributionParameters,startTime, endTime):
        self.distributionType = distributionType, 
        self.distributionGranularity = distributionGranularity
        self.distributionParameters  = distributionParameters
        self.emulatorID =emulatorID
        
        #converting time values
        self.endTime = timeConv(endTime)
        self.startTime = timeConv(startTime)
        
        print (distributionGranularity)
        print (distributionParameters)
        print (distributionType)
        #print difference in the seconds
        print(timestamp(self.endTime)-timestamp(self.startTime))
        
        runTime =int((timestamp(self.endTime)-timestamp(self.startTime)))/int(distributionGranularity)
        print "Time per run:"
        print runTime
        
        granularity =self.distributionGranularity
        qty=1
        while(granularity>0):
            
            print "granularity:"
            granularity= int(granularity)-1
            print granularity
            
            print "run start time"
            runStart=int(timestamp(self.startTime))+(int(qty)*int(runTime))
            print runStart
            
            print "run end time"
            qty=int(qty)+1
            runEnd=int(timestamp(self.startTime))+(int(qty)*int(runTime))
            print runEnd
        
#convert date from DB to python format
def timeConv(dbtimestamp):
    Year = int(dbtimestamp[0:4])
    Month = int(dbtimestamp[4+1:7])
    Day = int(dbtimestamp[7+1:10])
    Hour =int(dbtimestamp[11:13])
    Min =int(dbtimestamp[14:16])
    Sec =int(dbtimestamp[17:19])

    dbtimestamp=dt.datetime(Year,Month,Day,Hour,Min,Sec)
    return dbtimestamp

# string[startIndex:endIndex]
#print Year
#print Month
#print Day
#print Hour
#print Min
#print Sec

#convert date to seconds
def timestamp(date):
    return time.mktime(date.timetuple())
