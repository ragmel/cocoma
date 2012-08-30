'''
Created on 29 Aug 2012

@author: ltenru
'''

import CreateRun
from datetime import datetime
import time
from apscheduler.scheduler import Scheduler 
import datetime as dt
import Distribution


def  schedulerControl(startTime,stopTime, granularity,startLoad, stopLoad):   
        print "this is schedulerControl"
                
        if __name__ != '__main__':
            print "executing as not main"
            #converting to Python time format
            startTime= timeConv(startTime)
            stopTime = timeConv(stopTime)
        
        #make sure it is integer
        granularity = int(granularity)
        
        #make copy for counting(qty can also be used)
        granularity_count = granularity
        # Start the scheduler
        sched = Scheduler()
        sched.start()
                
        qty=int(0)
        
        
        
        duration = (timestamp(stopTime) - timestamp(startTime))/granularity
        
        print "Duration is seconds:"
        print duration
  
        while(granularity_count>=0):
            
            print "Run No: "
            print qty
            
            '''
            $duration = (endTime-startTime)/granularity (seconds)
            $qty 
            $stressValue= functionName (i.e. linearCalculate(startLoad, stopLoad, distributionGranularity,runNo))
                       
            '''
            #This needs to be changed
            
            runStartTime=timestamp(startTime)+duration*qty
            print "This run start time: "
            print runStartTime
            print "This is time passed to scheduler:"
            print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime))
            
                
            stressValue= Distribution.linearCalculate(startLoad, stopLoad, granularity,qty)
            print "This run stress Value: "
            print stressValue
            
            #job=sched.add_date_job(createRun, exec_date, [duration,stressValue])
            job=sched.add_date_job(CreateRun.createRun, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime)), [duration,stressValue])
            
            #increasing to next run            
            qty=int(qty)+1
            print "list of jobs:"
            sched.print_jobs()
            
            print "granularity_count:"
            granularity_count= int(granularity_count)-1
            print granularity_count

#we can return single values, seconds and proper python date            
def timeConv(dbtimestamp):
    print "this is timeConv!!!"
    Year = int(dbtimestamp[0:4])
    Month = int(dbtimestamp[4+1:7])
    Day = int(dbtimestamp[7+1:10])
    Hour =int(dbtimestamp[11:13])
    Min =int(dbtimestamp[14:16])
    Sec =int(dbtimestamp[17:19])

    #convert date from DB to python date
    pytime=dt.datetime(Year,Month,Day,Hour,Min,Sec)
    return pytime
        
    
#convert date to seconds
def timestamp(date):
    print"This is timestamp"
    return time.mktime(date.timetuple())

           
if __name__ == '__main__':
    print "main"
    startTime= timeConv("2012-08-29T20:03:04")
    stopTime = timeConv("2012-08-30T20:03:04")
    #for linear function
    startLoad = 10
    stopLoad = 90
    granularity=int(10)
    schedulerControl(startTime,stopTime, granularity, startLoad, stopLoad)
    