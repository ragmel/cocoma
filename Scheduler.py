'''
Created on 6 Sep 2012

@author: i046533
'''

#!/usr/bin/env python

import sys, os, time, atexit
from signal import SIGTERM 

from datetime import datetime
from apscheduler.scheduler import Scheduler 
import datetime as dt
import Distribution,Run
#from __future__ import print_function
import Pyro4



class schedulerDaemon(object):
    
    def __init__(self):
        self.contents=["chair","bike","flashlight","laptop","couch"]
        
        #starting scheduler 
        self.sched = Scheduler()
        self.sched.start()

    def list_contents(self):
        return self.contents
    
    def stopSchedulerDaemon(self):
        self.close()
   
    
    def hello(self):
        print "hello mortals"
        
    def schedulerControl(self,emulationName,startTime,stopTime, distributionGranularity,startLoad, stopLoad):   
            print "this is schedulerControl"
            
            
            startTime= self.timeConv(startTime)
            stopTime = self.timeConv(stopTime)
        
            #make sure it is integer
            distributionGranularity = int(distributionGranularity)
        
            #make copy for counting(qty can also be used)
            distributionGranularity_count = distributionGranularity
            
            
            
                
            qty=int(0)
        
        
        
            duration = (self.timestamp(stopTime) - self.timestamp(startTime))/distributionGranularity
        
            print "Duration is seconds:"
            print duration
  
            while(distributionGranularity_count>=0):
            
                print "Run No: "
                print qty
            
            
                #This needs to be changed
            
                runStartTime=self.timestamp(startTime)+(duration*qty)
                print "This run start time: "
                print runStartTime
                print "This is time passed to scheduler:"
                print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime))
            
                
                stressValue= Distribution.linearCalculate(startLoad, stopLoad, distributionGranularity,qty)
                print "This run stress Value: "
                print stressValue
            
                #job=sched.add_date_job(createRun, exec_date, [duration,stressValue])
                self.sched.add_date_job(Run.createRun, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime)), args=[duration,stressValue], name=emulationName)
                #scheduler.add_date_job(alarm, alarm_time, name='alarm',jobstore='shelve', args=[datetime.now()])
                
                
                
                #self.sched.add_cron_job(func=Run.createRun, name=emulationName,start_date=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime)), args=[duration,stressValue])
                
                #increasing to next run            
                qty=int(qty)+1
                
            
                print "distributionGranularity_count:"
                distributionGranularity_count= int(distributionGranularity_count)-1
                print distributionGranularity_count
                                    
            
            print "list of jobs:"
            self.sched.print_jobs()
            
                #we can return single values, seconds and proper python date            
    def timeConv(self,dbtimestamp):
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
    def timestamp(self,date):
        print"This is timestamp"
        print date
        gmtTime = time.mktime(date.timetuple())+3600
        return gmtTime

def main():
    daemon=schedulerDaemon()
    Pyro4.config.HOST="localhost"
    Pyro4.Daemon.serveSimple(
            {
                daemon: "scheduler.daemon"
            },
            port = 51889, ns=False)
    
#we start daemon locally
def startSchedulerDaemon():
    main()    
    

    

if __name__=="__main__":
    main()                   
