#!/usr/bin/env python
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
import struct,fcntl
import sys, os, time,imp,re
from signal import SIGTERM 
import subprocess,socket
from datetime import datetime
from apscheduler.scheduler import Scheduler 
import datetime as dt
import Run,logging
import sqlite3 as sqlite
from subprocess import *

import Pyro4, Logger,EmulationManager,DistributionManager
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_MISSED,EVENT_JOB_ERROR

#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'

class schedulerDaemon(object):
    
    def __init__(self):
                       
        #starting scheduler 
        self.sched = Scheduler()
        self.sched.start()
        self.sched.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)    
        self.recoverySchedulerDaemon()

    def listJobs(self):
        schedFileLogger.debug("-> listJobs(self)")
        if self.sched.get_jobs():
            schedFileLogger.debug("sending list of jobs")
            return self.sched.get_jobs()
        else:
            schedFileLogger.debug("No jobs to send")
            return []
    
        
       
    def stopSchedulerDaemon(self):
        schedFileLogger.debug("-> stopSchedulerDaemon(self)")
        schedFileLogger.info("stopping Daemon")
        sys.exit(1)   
        sys.exit(0) 
    
    def hello(self):
        schedFileLogger.debug("-> hello(self)") 
        greeting = "Pong!"
        schedFileLogger.debug(greeting)
        return greeting
    
    def deleteJobs(self,emulationID,distribitionName):
        schedFileLogger.debug("-> deleteJobs(self,emulationID,distribitionName)")
        #stringify
        emulationID =str(emulationID)
        distribitionName=str(distribitionName)
        
        schedFileLogger.debug("Looking for job name:"+emulationID+"-"+distribitionName)
        
        if emulationID=="all":
            schedFileLogger.info("Jobs deleted:")
            for job in self.sched.get_jobs():
                self.sched.unschedule_job(job)
                schedFileLogger.info(str(job.name))
                
        else:
            for job in self.sched.get_jobs():
                ID_params=re.split(r"-",job.name)
                if str(ID_params[0]) == emulationID :
                    self.sched.unschedule_job(job)
                    schedFileLogger.info( "Job: "+job.name+" Deleted")
                    
                
                else:
                    schedFileLogger.info( "These jobs remain: "+job.name)
    
    def createJob(self,emulationID,emulationName,distributionID,distributionName,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runStartTime,runNo,emuDuration):
        
        
        schedFileLogger.debug("-> createJob(self,emulationID,distributionID,distributionName,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runStartTime,runNo,emuDuration)")
        
        
        try:
            schedFileLogger.debug("Job added with: StartTime:"+str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime))))
            
            schedFileLogger.debug("emulationID "+str(emulationID))
            schedFileLogger.debug("emulationLifetimeID "+str(emulationLifetimeID))
            schedFileLogger.debug("distributionName "+str(distributionName))
            schedFileLogger.debug("stressValue "+str(stressValue))
            schedFileLogger.debug("duration "+str(duration))
            schedFileLogger.debug("runNo "+str(runNo))
            
            #self.sched.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)  
            runEndTimeStr=str(time.strftime("%H:%M:%S", time.gmtime(runStartTime+float(duration))))
            jobName = str(emulationName)+"-"+str(distributionID)+"-"+str(runNo)+"-"+distributionName+"-"+str(emulator)+"-"+str(resourceTypeDist)+": "+str(stressValue)+" Duration: "+str(duration)+"sec. End Time: "+runEndTimeStr
            self.sched.add_date_job(Run.createRun, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime)), args=[emulationID,distributionID,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runNo,emuDuration], name=jobName)
            schedFileLogger.debug(str(sys.stdout))
            valBack=str(emulationName)+"-"+str(distributionID)+"-"+str(runNo)+"-"+distributionName+"-"+str(emulator)+"-"+str(resourceTypeDist)+": "+str(stressValue)+" Duration: "+str(duration)+"sec."+"Start Time: "+str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime)))+" End Time: "+runEndTimeStr
            schedFileLogger.debug("Scheduler Return: "+valBack)
            return valBack
        except Exception, e:
            schedFileLogger.debug("Values:"+str(emulationID)+"-"+str(distributionID)+"-"+str(distributionName)+"-"+str(emulationLifetimeID)+"-"+str(duration)+"-"+str(emulator)+"-"+str(emulatorArg)+"-"+str(resourceTypeDist)+"-"+str(stressValue)+"-"+str(runStartTime)+"-"+str(runNo)+"-"+str(emuDuration))
            schedFileLogger.error("Scheduler createJob(): error creating Job check dates")
            schedFileLogger.exception(str(e))  
            return "Scheduler createJob(): error creating Job check dates "+str(e)

        
    def createLoggerJob(self,singleRunStartTime,duration,interval,emulationID,emulationName,emuStartTime):
        schedFileLogger.debug("-> createLoggerJob(self,singleRunStartTime,duration,interval,emulationID)")
        interval=int(interval)
        
        loggetJobName=str(emulationID)+"-"+str(emulationName)+"-logger interval-"+str(interval)+"sec."
        try:
            self.sched.add_date_job(Logger.loadMon, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(singleRunStartTime)), args=[duration,interval,emulationID,emulationName,emuStartTime], name=loggetJobName)
            schedFileLogger.debug("Started logger:"+loggetJobName+"StartTime:"+str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(singleRunStartTime))))
            return "Started logger:"+loggetJobName+"StartTime:"+str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(singleRunStartTime)))
        except Exception,e :
            valReturn="Error starting logger:"+loggetJobName+"StartTime:"+str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(singleRunStartTime)))
            schedFileLogger.debug(valReturn)
            schedFileLogger.error("Scheduler createLoggerJob(): error creating Job ")
            schedFileLogger.exception(str(e))
            return valReturn+" Error:"+str(e)

    def checkProcessRunning(self,PROCNAME):
        schedFileLogger.debug("-> checkProcessRunning(self,PROCNAME)")
        schedFileLogger.debug("Looking for:"+str(PROCNAME)) 
        procTrace = subprocess.Popen("ps ax | grep -v grep | grep "+"\""+str(PROCNAME)+"\"",shell=True,stdout=PIPE).communicate()[0]
        if procTrace:
            pid = procTrace[0:5]
            #program running
            return pid
        else:
            #program not running
            return False        
        

    def createCustomJob(self,emulationID,distributionID,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runNo,PROCNAME,emuDuration):
        
        schedFileLogger.debug("-> createCustomJob(self,emulationID,distributionID,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runNo,PROCNAME,emuDuration)")
        distributionName= emulator+"customJob"
        
        if EmulationManager.checkPid(PROCNAME):
            return 2
        else:
            try:
                self.sched.add_date_job(Run.createRun, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.timestamp(DistributionManager.timeConv(EmulationManager.emulationNow(2))))), args=[emulationID,distributionID,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runNo,emuDuration], name=str(emulationID)+distributionName+"-"+str(distributionID)+"-"+str(runNo)+"-"+distributionName+"-"+str(emulator)+"-"+str(resourceTypeDist)+": "+str(stressValue))
                schedFileLogger.info("Created Custom Job: "+str(emulationID)+distributionName+"-"+str(distributionID)+"-"+str(runNo)+"-"+distributionName+"-"+str(emulator)+"-"+str(resourceTypeDist)+": "+str(stressValue))
                return 1
            except Exception,e:
                schedFileLogger.debug("Values:"+str(emulationID)+"-"+str(distributionID)+"-"+str(distributionName)+"-"+str(emulationLifetimeID)+"-"+str(duration)+"-"+str(emulator)+"-"+str(emulatorArg)+"-"+str(resourceTypeDist)+"-"+str(stressValue)+"-"+str(runNo)+"-"+str(emuDuration))
                schedFileLogger.error("Scheduler reateCustomJob(): error creating Job check values")
                schedFileLogger.exception(str(e))
                return 0
        
    
    def timeConv(self,dbtimestamp):
        schedFileLogger.debug("-> timeConv(self,dbtimestamp). Converting date from DB to python date dt")
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
        
        except ValueError,e:
            schedFileLogger.debug("Values:"+str(dbtimestamp))
            schedFileLogger.error("Date incorrect use YYYY-MM-DDTHH:MM:SS format")
            schedFileLogger.exception(str(e))
            sys.exit(0) 


    #convert date to seconds
    def timestamp(self,date):
        schedFileLogger.debug("-> timestamp(self,date) converting python date to seconds")
        gmtTime = time.mktime(date.timetuple())+3600
        return gmtTime

    def recoverySchedulerDaemon(self):
        schedFileLogger.debug("-> recoverySchedulerDaemon(self)")
        print'''
      ___  _____  ___  _____  __  __    __       
     / __)(  _  )/ __)(  _  )(  \/  )  /__\     
    ( (__  )(_)(( (__  )(_)(  )    (  /(__)\    
     \___)(_____)\___)(_____)(_/\/\_)(__)(__) SCHEDULER   

        
        
        '''
        schedFileLogger.debug("HOMEPATH:"+str(HOMEPATH))
        
        schedFileLogger.debug("Checking if there are any Emulations in DB scheduled in future that needs to be added to scheduler")
    
        '''
        1. Get current timestamp
        2. Compare it with all emulationLifetime start dates 2013-09-10T15:30:00
        3. Use createRun(emulationID,emulationLifetimeID,duration, stressValue,runNo): to re-create runs
    
        '''
    
        try:
            if HOMEPATH:
                schedFileLogger.debug("DB location path:"+HOMEPATH+"/data/cocoma.sqlite")
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
                    #print row
                    startTime= row[0]
                    emulationID = row[1]
                    c.execute('SELECT emulationName FROM emulation WHERE emulationID=?',[str(emulationID)])
                    emulationNameArray = c.fetchall()
                    emulationName = emulationNameArray[0][0]
                    emuDuration = int(row[3])     
                    emulationLifetimeID = row[2]
                    #Compare starting times and re-launch 
                    #TO-DO: We can recover some individual runs if the emulation lifetime end date is still in future
                    if self.timestamp(self.timeConv(startTime))>self.timestamp(dt.datetime.now()):
                        schedFileLogger.info("Recovery Emulation found. ID: "+str(emulationID))
                        #If active emulation is found starting logger
                        #2sec interval
                        c.execute('SELECT logging,logFrequency FROM emulation WHERE emulationID=?',[str(emulationID)])
                        emulationLogging = c.fetchall()
                        
                        for row in emulationLogging:
                            
                            if str(row[0]) =="1":
                                interval=int(row[1])                                                                                                                                                                              
                                self.sched.add_date_job(Logger.loadMon, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.timestamp(self.timeConv(startTime)))), args=[emuDuration,interval,emulationID], name=str(emulationID)+"-"+str(emulationName)+"-logger interval-"+str(interval)+"sec.")
                        
                        #If active emulation is found. Getting info from active emulation to restore runs 
                        ca.execute('SELECT distributionID,distributionName,duration,emulator FROM distribution WHERE emulationID=?',[str(emulationID)])
                        distroParamsFetch = ca.fetchall()
                        for items in distroParamsFetch:
                            distributionID =items[0]
                            distributionName=items[1]
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

                            ca.execute('SELECT stressValue,runStartTime,runNo,runDuration FROM runLog WHERE distributionID =?',[str(distributionID)])
                            runLogFetch = ca.fetchall()
                            #print runLogFetch
            
                            if runLogFetch:
                                for row in runLogFetch:
                                    #print row
                                    stressValue = row[0]
                                    runStartTime = float(row[1])
                                    runNo = row[2]
                                    duration=row[3]

                                    #                       8           MEM-dis-1              8             10     lookbusy {'memSleep': u'100'}      MEM              64         1359680491.0   3
                                    #createJob(self,emulationID,emulationName,distributionID,distributionName,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runStartTime,runNo,emuDuration                       
                                    self.createJob(emulationID,emulationName,distributionID,distributionName,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist,stressValue,runStartTime,runNo,emuDuration)
                                    

                                
                                
                    else:
                            schedFileLogger.debug("No Active EmulationLifetime Runs were found to recover(1)")
                            # setting the emulation as inactive if the start date is in the past
                            c.execute('UPDATE emulation SET active=0 WHERE emulationID=?',[emulationID])
                            conn.commit()
                             
                            
                
            else:
                schedFileLogger.debug("No Emulations were found to recover(2)") 
                
    
        except Exception, e:
            schedFileLogger.warning("Could not recover Emulations")
            schedFileLogger.exception(str(e))            
            #sys.exit(1)    
    
        c.close()
        ca.close()
    
def dbWriter(distributionID,runNo,message,executed):
        schedFileLogger.debug("-> dbWriter(distributionID,runNo,message,executed)")
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
                        schedFileLogger.warning("Job already marked as failed. Run No:"+str(runNo))
            
            # 2. Populate "emulation"
            else:
                c.execute('UPDATE runLog SET executed=? ,message=? WHERE distributionID =? and runNo=?',(executed,message,distributionID,runNo))
            
            
            #c.close()
            
        except sqlite.Error, e:
            schedFileLogger.debug("Values: "+str(distributionID)+"-"+str(runNo)+"-"+str(message)+"-"+str(executed))
            schedFileLogger.error("Unable to connect to DB")
            schedFileLogger.exception(str(e))
            sys.exit(1)    
        
        finally:
            if conn:
                conn.close()
            
def job_listener(event):
    schedFileLogger.debug("-> job_listener(event)")
    
    if str(event.exception) !="None":
        
        #possible job options 
        #print '\n'+str(event.job.name)+'The job crashed :(\n'
        #print "event.retval: ",event.retval
        #print "event.exception: ",event.exception
        #print "event.traceback: ",event.traceback.j
        #print "event.scheduled_run_time: ",event.scheduled_run_time
        #print "event.SchedulerEvent: ",event.SchedulerEvent
        executed="False"
        message="Job crashed by scheduler"
        loggerSearch=re.search("logger", str(event.job.name))

        if not loggerSearch:
            paramsArray=re.split(r"-",str(event.job.name))
            distributionID=paramsArray[1]
            runNo=paramsArray[2]   
            schedFileLogger.warn("Job: "+str(event.job.name)+" -crashed by scheduler execution")
            dbWriter(distributionID,runNo,message,executed)
            
        
    else:
        
        executed="True"
        message="Job launched by scheduler"
        loggerSearch=re.search("logger", str(event.job.name))
        if not loggerSearch:
            paramsArray=re.split(r"-",str(event.job.name))
            distributionID=paramsArray[1]
            runNo=paramsArray[2]
            schedFileLogger.info("Job: "+str(event.job.name)+" -executed successfully by scheduler ")
            dbWriter(distributionID,runNo,message,executed)   
    
def getifip(ifn):
    schedFileLogger.debug("-> getifip(ifn)")
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(sck.fileno(),0x8915,struct.pack('256s', ifn[:15]))[20:24])

def main(IP_ADDR,PORT_ADDR):
    
    schedFileLogger.debug("-> main(IP_ADDR,PORT_ADDR)")
    daemon=schedulerDaemon()
    Pyro4.config.HOST=IP_ADDR
    
    Pyro4.Daemon.serveSimple(
            {
                daemon: "scheduler.daemon"
            },
            port = PORT_ADDR, ns=False)
    
    #we start daemon locally
 
if __name__=="__main__":
    schedFileLogger = logging.getLogger("")
    LOG_LEVEL=logging.INFO
    #1st setting logger
    #schedFileLogger.debug("")
    #schedFileLogger.info("")
    #schedFileLogger.error("")
    #schedFileLogger.warn("")
    try:
        if sys.argv[1].lower() == "debug":
            #Writing log level to DB
            LOG_LEVEL=logging.DEBUG
    except Exception, e:
        print""
    try:
        if sys.argv[2].lower() == "debug":
            
            LOG_LEVEL=logging.DEBUG
            
    except Exception, e:
        print""
    
    try:
        if sys.argv[3].lower() == "debug":
            
            LOG_LEVEL=logging.DEBUG
            
    except Exception, e:
        print""    
    
    if LOG_LEVEL == 10:
        EmulationManager.writeInterfaceData("debug","coreloglevel")
    if LOG_LEVEL == 20:
        EmulationManager.writeInterfaceData("info","coreloglevel")
    #Creating log handlers
    schedFileLogger=EmulationManager.logToFile("SCHEDULER",LOG_LEVEL)
    #Setting environmental variable    
    try:
        HOMEPATH= os.environ['COCOMA']
        
    except:
        schedFileLogger.error("no $COCOMA environmental variable set")

    
    
    schedFileLogger.debug("### Scheduler Start in DEBUG mode###")
    
    try: 
        if sys.argv[1] == "-h":
            print "[interface][port][loglevel] Use Scheduler <name of network interface> . Default network interface is eth0."

        else:
            try:
                schedFileLogger.info("Interface: "+str(sys.argv[1]))
                IP_ADDR=getifip(sys.argv[1])
                EmulationManager.writeInterfaceData(sys.argv[1],"schedinterface")
            except:
                IP_ADDR=getifip("eth0")
                EmulationManager.writeInterfaceData("eth0","schedinterface")
                
            
            try:
                if sys.argv[2]:
                    PORT_ADDR=int(sys.argv[2])
                    EmulationManager.writeInterfaceData(sys.argv[2],"schedport")
            except:
                PORT_ADDR=51889
                EmulationManager.writeInterfaceData("51889","schedport")
    except Exception, e:
        
        schedFileLogger.info("Interface: eth0, port:51889")
        EmulationManager.writeInterfaceData("eth0","schedinterface")
        EmulationManager.writeInterfaceData("51889","schedport" )
        IP_ADDR=getifip("eth0")
        PORT_ADDR=51889
      

    
    try:    
        main(IP_ADDR,PORT_ADDR)
    except socket.error:
        print "Unable to start Scheduler port already in use"
        

    
                       
