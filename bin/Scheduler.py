#!/usr/bin/env python
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


import sys, os, time,imp
from signal import SIGTERM 

from datetime import datetime
from apscheduler.scheduler import Scheduler 
import datetime as dt
import Run
import sqlite3 as sqlite
#from __future__ import print_function
import Pyro4

#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'
try:
    HOMEPATH= os.environ['COCOMA']
except:
    print "no $COCOMA environmental variable set"

class schedulerDaemon(object):
    
    def __init__(self):
                       
        #starting scheduler 
        self.sched = Scheduler()
        self.sched.start()
        #self.recoverySchedulerDaemon()

    def listJobs(self):
        print "sending list of jobs"
        if self.sched.get_jobs():
            return self.sched.get_jobs()
       
       
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
    
    #def purgeAllJobs(self):
    #    print "This is purgeAllJobs daemon"
    #    self.sched.shutdown(False, True, True)
    
    def createJob(self,emulationID,emulationName,emulationLifetimeID,duration,emulator,stressValue,runStartTime,runNo):
        
        
        print "Hello this is Scheduler createJob()"
        
        
        try:
            print "Job added with:\n StartTime:",time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime))
            
            print "emulationID ",emulationID
            print "emulationLifetimeID",emulationLifetimeID
            print "stressValue",stressValue
            print "duration",duration
            print "runNo",runNo
            self.sched.add_date_job(Run.createRun, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime)), args=[emulationID,emulationLifetimeID,duration,emulator,stressValue,runNo], name=str(emulationID)+"-"+emulationName)
            print sys.stdout
            valBack=str(("Job: "+str(emulationID)+"-"+emulationName+" with run No: "+str(runNo)+" start date "+str(runStartTime)+" created"))
            print valBack
            return valBack
        except :    
            print "Scheduler createJob(): error creating Job "
            return "Scheduler createJob(): error creating Job check dates "

        
        
        
    
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
            if HOMEPATH:
                print "DB location path:", HOMEPATH+'/data/cocoma.sqlite'
                conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
            else:
                conn = sqlite.connect('./data/cocoma.sqlite')
                
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
                        print runLogFetch
        
                        if runLogFetch:
                            print "run log has values"
                            for row in runLogFetch:
                                print row
                                duration = row[0]
                                stressValue = row[1]
                                runNo = row[2]
                                emulationName =row[3]
                        
                                startTimeSec= self.timeConv(startTime)
                                
                                runStartTime=self.timestamp(startTimeSec)+(int(duration)*int(runNo))
                                print "Job added with:\n StartTime:",time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime))
            
                                print "emulationID ",emulationID
                                print "emulationLifetimeID",emulationLifetimeID
                                print "stressValue",stressValue
                                print "duration",duration
                                print "runNo",runNo
                                
                                self.createJob(emulationID,emulationName,emulationLifetimeID,duration,stressValue,runStartTime,runNo)
                                
                                
                                
                    else:
                            print "No Active EmulationLifetime Runs were found to recover(1)"
                            # setting the emulation as inactive if the start date is in the past
                            c.execute('UPDATE emulation SET active=0 WHERE emulationID=?',[emulationID])
                            conn.commit()
                             
                            
                
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
    
                       
