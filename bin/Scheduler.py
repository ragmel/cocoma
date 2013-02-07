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


import sys, os, time,imp,re
from signal import SIGTERM 

from datetime import datetime
from apscheduler.scheduler import Scheduler 
import datetime as dt
import Run
import sqlite3 as sqlite
#from __future__ import print_function
import Pyro4, Logger,EmulationManager,DistributionManager
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_MISSED,EVENT_JOB_ERROR

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
        self.sched.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)    
        self.recoverySchedulerDaemon()

    def listJobs(self):
        print "sending list of jobs"
        if self.sched.get_jobs():
            return self.sched.get_jobs()
    
        
       
    def stopSchedulerDaemon(self):
        print "stopping Daemon"
        sys.exit(1)   
        sys.exit(0) 
    
    def hello(self):
        greeting = "Hello, Yes this is schedulerDaemon. I am online send me some jobs!"
        print greeting 
        return greeting
    
    def deleteJobs(self,emulationID,distribitionName):
        print "This is deleteJobs"
        #stringify
        emulationID =str(emulationID)
        distribitionName=str(distribitionName)
        
        print "Looking for job name:", emulationID+"-"+distribitionName
        
        if emulationID=="all":
            print "Jobs deleted:"
            for job in self.sched.get_jobs():
                self.sched.unschedule_job(job)
                print job.name
                
        else:
            for job in self.sched.get_jobs():
                ID_params=re.split(r"-",job.name)
                if str(ID_params[0]) == emulationID :
                    self.sched.unschedule_job(job)
                    print "Job: "+job.name
                    print "Deleted"
                
                else:
                    print "These jobs remains: "+job.name
        
    #def purgeAllJobs(self):
    #    print "This is purgeAllJobs daemon"
    #    self.sched.shutdown(False, True, True)
    
    def createJob(self,emulationID,distributionID,distributionName,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runStartTime,runNo,emuDuration):
        
        
        print "Hello this is Scheduler createJob()"
        
        
        try:
            print "Job added with:\n StartTime:",time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime))
            
            print "emulationID ",emulationID
            print "emulationLifetimeID",emulationLifetimeID
            print "distributionName", distributionName
            print "stressValue",stressValue
            print "duration",duration
            print "runNo",runNo
            #self.sched.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)     
            self.sched.add_date_job(Run.createRun, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime)), args=[emulationID,distributionID,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runNo,emuDuration], name=str(emulationID)+"-"+str(distributionID)+"-"+str(runNo)+"-"+distributionName+"-"+str(emulator)+"-"+str(resourceTypeDist)+": "+str(stressValue))
            print sys.stdout
            valBack=str(("Job: "+str(emulationID)+"-"+distributionName+" with run No: "+str(runNo)+" start date "+str(runStartTime)+" created"))
            print valBack
            return valBack
        except :    
            print "Scheduler createJob(): error creating Job "
            return "Scheduler createJob(): error creating Job check dates "

        
    def createLoggerJob(self,singleRunStartTime,duration,interval,emulationID):
        print "Hello this is createLoggerJob"
        interval=int(interval)
        
        
        self.sched.add_date_job(Logger.loadMon, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(singleRunStartTime)), args=[duration,interval,emulationID], name=str(emulationID)+"-logger interval-"+str(interval)+"sec.")
        return "Started logger"
 


    def createCustomJob(self,emulationID,distributionID,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runNo,PROCNAME,emuDuration):
        EmulationManager.checkPid(PROCNAME)
        print "createCustomJob!!!"
        distributionName= emulator+"customJob"
        
        if EmulationManager.checkPid(PROCNAME):
            return 2
        else:
            try:
                self.sched.add_date_job(Run.createRun, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.timestamp(DistributionManager.timeConv(EmulationManager.emulationNow())))), args=[emulationID,distributionID,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runNo,emuDuration], name=str(emulationID)+distributionName+"-"+str(distributionID)+"-"+str(runNo)+"-"+distributionName+"-"+str(emulator)+"-"+str(resourceTypeDist)+": "+str(stressValue))
                return 1
            except:
                return 0
        
    
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
        gmtTime = time.mktime(date.timetuple())#+3600
        return gmtTime

    def recoverySchedulerDaemon(self):
        os.system("clear")
        print'''
      ___  _____  ___  _____  __  __    __       
     / __)(  _  )/ __)(  _  )(  \/  )  /__\     
    ( (__  )(_)(( (__  )(_)(  )    (  /(__)\    
     \___)(_____)\___)(_____)(_/\/\_)(__)(__) SCHEDULER   

        
        
        '''
        
        
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
            c.execute('SELECT startTime,emulationID,emulationLifetimeID,stopTime FROM emulationLifetime')
            
            
            
                
            emulationLifetimeFetch = c.fetchall()
            #if a
            if emulationLifetimeFetch:
                for row in emulationLifetimeFetch:
                    print row
                    startTime= row[0]
                    emulationID = row[1]
                    emulationLifetimeID = row[2]
                    duration= int(row[3])
                    #Compare starting times and re-launch 
                    #TO-DO: We can recover some individual runs if the emulation lifetime end date is still in future
                    if self.timestamp(self.timeConv(startTime))>self.timestamp(dt.datetime.now()):
                        print "DB Start time in seconds"
                        print self.timestamp(self.timeConv(startTime))
                        print "Current time in seconds"
                        print self.timestamp(dt.datetime.now())
                        
                        
                        #If active emulation is found starting logger
                        #2sec interval
                        c.execute('SELECT logging,logFrequency FROM emulation WHERE emulationID=?',[str(emulationID)])
                        emulationLogging = c.fetchall()
                        
                        for row in emulationLogging:
                            
                            if str(row[0]) =="1":
                                interval=int(row[1])
                                self.sched.add_date_job(Logger.loadMon, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.timestamp(self.timeConv(startTime)))), args=[duration,interval,emulationID], name=str(emulationID)+"-logger interval-"+str(interval)+"sec.")
                        
                        #If active emulation is found. Getting info from active emulation to restore runs 
                        ca.execute('SELECT distributionID,distributionName,duration,emulator FROM distribution WHERE emulationID=?',[str(emulationID)])
                        distroParamsFetch = ca.fetchall()
                        for items in distroParamsFetch:
                            distributionID =items[0]
                            distributionName=items[1]
                            duration=items[2]
                            emulator=items[3]
    
                            emulatorArg={}
                            resourceTypeDist=""
                            ca.execute('SELECT paramName,value,resourceType FROM EmulatorParameters WHERE distributionID=?',[str(distributionID)])
                            emuParamsFetch = ca.fetchall()
                            for items in emuParamsFetch:
                                paramName=items[0]
                                value=items[1]
                                resourceType=items[2]
                                resourceTypeDist=resourceType#not100%
                                emulatorArg.update({paramName:value})
                            print "emulatorArg@ ",emulatorArg
                                
                            #EmulatorParameters.emulatorArg {'memSleep': u'100'} distroID
                            
    
                            ca.execute('SELECT stressValue,runStartTime,runNo FROM runLog WHERE distributionID =?',[str(distributionID)])
                            runLogFetch = ca.fetchall()
                            print runLogFetch
            
                            if runLogFetch:
                                print "run log has values"
                                for row in runLogFetch:
                                    print row
                                    stressValue = row[0]
                                    runStartTime = float(row[1])
                                    runNo = row[2]
                                            
                                    
                                    print "Job added with:\n StartTime:",time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime))
                
                                    print "emulationID ",emulationID
                                    print "emulationLifetimeID",emulationLifetimeID
                                    print "stressValue",stressValue
                                    print "duration",duration
                                    print "runNo",runNo
                                    #
                                    #                       8           MEM-dis-1              8             10     lookbusy {'memSleep': u'100'}      MEM              64         1359680491.0   3
                                    self.createJob(emulationID,distributionID,distributionName,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runStartTime,runNo)
                                    

                                
                                
                    else:
                            print "No Active EmulationLifetime Runs were found to recover(1)"
                            # setting the emulation as inactive if the start date is in the past
                            c.execute('UPDATE emulation SET active=0 WHERE emulationID=?',[emulationID])
                            conn.commit()
                             
                            
                
            else:
                print "No Emulations were found to recover(2)" 
                
    
        except sqlite.Error, e:
            print "Could not retrieve SQL for startTime,emulationID FROM emulationLifetime "
            print "Error %s:" % e.args[0]
            print e
            sys.exit(1)    
    
        c.close()
        ca.close()
    
def dbWriter(distributionID,runNo,message,executed):
        #connecting to the DB and storing parameters
        try:
            if HOMEPATH:
                conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite',timeout=1)
            else:
                conn = sqlite.connect('./data/cocoma.sqlite')
                
            c = conn.cursor()
            
            
            # 1. Check if info is in the table before updating it
            c.execute('SELECT executed FROM runLog WHERE distributionID =? and runNo=?',[str(distributionID),str(runNo)])
            runLogFetch = c.fetchall()
            if runLogFetch:
                for row in runLogFetch:
                    if row[0]=="False":
                        print "Job already failed"
            
            # 2. Populate "emulation"
            else:
                c.execute('UPDATE runLog SET executed=? ,message=? WHERE distributionID =? and runNo=?',(executed,message,distributionID,runNo))
            
            
            #c.close()
            
        except sqlite.Error, e:
            print "Error %s:" % e.args[0]
            print e
            sys.exit(1)    
        
        finally:
            if conn:
                conn.close()
            
def job_listener(event):
    
    if str(event.exception) !="None":
        
        
        print '\n'+str(event.job.name)+'The job crashed :(\n'
        print "event.retval: ",event.retval
        print "event.exception: ",event.exception
        print "event.traceback: ",event.traceback.j
        print "event.scheduled_run_time: ",event.scheduled_run_time
        print "event.SchedulerEvent: ",event.SchedulerEvent
        executed="False"
        message="Job crashed by scheduler"
        loggerSearch=re.search("logger", str(event.job.name))
        print "Logger Search result: ",loggerSearch
        if not loggerSearch:
            paramsArray=re.split(r"-",str(event.job.name))
            distributionID=paramsArray[1]
            runNo=paramsArray[2]
            print "Writing to DB distributionID,runNo,message,executed:",distributionID,runNo,message,executed
            dbWriter(distributionID,runNo,message,executed)
            
        
    else:
        
        
        print 'Positive event.exception: ',event.exception
        print '\nThe job'+str(event.job.name)+' worked :)\n'
        executed="True"
        message="Job launched by scheduler"
        loggerSearch=re.search("logger", str(event.job.name))
        print "Logger Search result: ",loggerSearch
        if not loggerSearch:
            
            paramsArray=re.split(r"-",str(event.job.name))
            distributionID=paramsArray[1]
            runNo=paramsArray[2]
            print "Writing to DB distributionID,runNo,message,executed:",distributionID,runNo,message,executed
            dbWriter(distributionID,runNo,message,executed)   
    


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
    
                       
