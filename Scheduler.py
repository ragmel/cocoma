#!/usr/bin/env python
'''
Created on 6 Sep 2012

@author: i046533
'''

import sys, os, time, atexit
from signal import SIGTERM 

from datetime import datetime
from apscheduler.scheduler import Scheduler 
import datetime as dt
import Distribution,Run
import sqlite3 as sqlite
#from __future__ import print_function
import Pyro4



class schedulerDaemon(object):
    
    def __init__(self):
                       
        #starting scheduler 
        self.sched = Scheduler()
        self.sched.start()
        self.recoverySchedulerDaemon()

    def listJobs(self):
        print "sending list of jobs"
        if self.sched.get_jobs():
            return self.sched.get_jobs()
        else:
            return "No jobs are scheduled"
       
    def stopSchedulerDaemon(self):
        print "stopping Daemon"
        sys.exit(1)   
        sys.exit(0) 
    
    def hello(self):
        greeting = "Hello, Yes this is schedulerDaemon"
        print greeting 
        return greeting
    
    def deleteJobs(self,emulationID,emulationName):
        print "This is deleteJobs"
        #stringify
        emulationID =str(emulationID)
        emulationName=str(emulationName)
        
        
        for job in self.sched.get_jobs():
            
            if job.name == emulationID+"-"+emulationName :
                self.sched.unschedule_job(job)
                print "Job: "+job.name+" emulationID+emulationName: "+emulationID+"-"+emulationName
                print "Deleted"
            
            else:
                print "These jobs remains: "+job.name
    
    def purgeAllJobs(self):
        print "This is purgeAllJobs daemon"
        self.sched.shutdown(False, True, True)
        
        
        
    def schedulerControl(self,emulationID,emulationLifetimeID,emulationName,startTime,stopTime, distributionGranularity,startLoad, stopLoad,newEmulation):   
            print "this is schedulerControl"
            
            
            startTime= self.timeConv(startTime)
            stopTime = self.timeConv(stopTime)
        
            #make sure it is integer
            distributionGranularity = int(distributionGranularity)
        
            #make copy for counting(qty can also be used)
            distributionGranularity_count = distributionGranularity
            
            
            
                
            qty=int(0)
        
        
        
            duration = (self.timestamp(stopTime) - self.timestamp(startTime))/distributionGranularity
            duration = int(duration)
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
                
                runNo =qty
                                
                #job=sched.add_date_job(createRun, exec_date, [duration,stressValue])
                self.sched.add_date_job(Run.createRun, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime)), args=[emulationID,emulationLifetimeID,duration,stressValue,runNo], name=str(emulationID)+"-"+emulationName)
                
                #scheduler.add_date_job(alarm, alarm_time, name='alarm',jobstore='shelve', args=[datetime.now()])
                
                #RunID(AI),emulationLifetimeID(FK), RunNo,
                if newEmulation ==1:
                    try:
                        conn = sqlite.connect('cocoma.sqlite')
                        c = conn.cursor()
                                           
                        c.execute('INSERT INTO runLog (emulationLifetimeID,runNo,duration,stressValue) VALUES (?, ?, ?, ?)', [emulationLifetimeID,runNo,duration,stressValue])
                                                
                        conn.commit()
        
                    except sqlite.Error, e:
                        print "Error %s:" % e.args[0]
                        print e
                        sys.exit(1)
    
                    c.close()
                
                #increasing to next run            
                qty=int(qty)+1
                
            
                print "distributionGranularity_count:"
                distributionGranularity_count= int(distributionGranularity_count)-1
                print distributionGranularity_count
                                    
            
            print "list of jobs:"
            self.sched.print_jobs()
            
            return ("Job: "+str(emulationID)+"-"+emulationName+" start date "+str(startTime)+" end date "+str(stopTime)+" created!")
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
        
        try:
            pytime=dt.datetime(Year,Month,Day,Hour,Min,Sec)
            return pytime
        
        except ValueError:
            print "Date incorrect use YYYY-MM-DDTHH:MM:SS format"
            sys.exit(0) 


        
            
        
    
    #convert date to seconds
    def timestamp(self,date):
        print"This is timestamp"
        print date
        gmtTime = time.mktime(date.timetuple())+3600
        return gmtTime

    def recoverySchedulerDaemon(self):
        print "Recovering list of emulations"
    
        '''
        1. Get current timestamp
        2. Compare it with all emulationLifetime start dates 2013-09-10T15:30:00
        3. Use createRun(emulationID,emulationLifetimeID,duration, stressValue,runNo): to re-create runs
    
        '''
    
        try:
            conn = sqlite.connect('cocoma.sqlite')
            c = conn.cursor()
            ca = conn.cursor() 
            c.execute('SELECT startTime,emulationID,emulationLifetimeID FROM emulationLifetime')
            
            
            
                
            emulationLifetimeFetch = c.fetchall()
        
            if emulationLifetimeFetch:
                for row in emulationLifetimeFetch:
                    print row
                    startTime= row[0]
                    emulationID = row[1]
                    emulationLifetimeID = row[2]
                    #Compare starting times and re-launch 
                    #TO-DO: We can recover some individual runs if the emulation lifetime end date is still in future
                    if self.timestamp(self.timeConv(startTime))>self.timestamp(dt.datetime.now()):
                        print "DB Start time in seconds"
                        print self.timestamp(self.timeConv(startTime))
                        print "Current time in seconds"
                        print self.timestamp(dt.datetime.now())
                        
                        ca.execute('SELECT runLog.duration,runLog.stressValue,runLog.runNo,emulation.emulationName FROM runLog,emulation WHERE emulation.emulationLifetimeID =? and runLog.emulationLifetimeID=?',[str(emulationLifetimeID),str(emulationLifetimeID)])
                        runLogFetch = ca.fetchall()
        
                        if runLogFetch:
                            for row in runLogFetch:
                                print row
                                duration = row[0]
                                stressValue = row[1]
                                runNo = row[2]
                                emulationName =row[3]
                        
                                startTimeSec= self.timeConv(startTime)
                                
                                runStartTime=self.timestamp(startTimeSec)+(int(duration)*int(runNo))
                                self.sched.add_date_job(Run.createRun, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime)), args=[emulationID,emulationLifetimeID,duration,stressValue,runNo], name=str(emulationID)+"-"+emulationName)
                    else:
                            print "No Active EmulationLifetime Runs were found to recover(1)"
                
            else:
                print "No Emulations were found to recover(2)" 
                
    
        except sqlite.Error, e:
            print "Could retrieve SQL for startTime,emulationID FROM emulationLifetime "
            print "Error %s:" % e.args[0]
            print e
            sys.exit(1)    
    
        c.close()
        ca.close()
    
    
    


def main():
    
    daemon=schedulerDaemon()
    Pyro4.config.HOST="localhost"
    Pyro4.Daemon.serveSimple(
            {
                daemon: "scheduler.daemon"
            },
            port = 51889, ns=False)
    
    #we start daemon locally
    
    
    
    
    
        

   

    

if __name__=="__main__":
    main()
    
                       
