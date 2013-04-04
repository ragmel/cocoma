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


import sqlite3 as sqlite
import sys,re,os,subprocess,psutil
import DistributionManager,ccmsh,XmlParser
import Pyro4
import datetime,ccmshAPI
from datetime import datetime as dt
from subprocess import *
import logging
from logging import handlers

emuLoggerEM = None
#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'
try:
    HOMEPATH= os.environ['COCOMA']
except:
    print "no $COCOMA environmental variable set"

def getAllEmulationList():
    emulationList=[]
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
        c = conn.cursor()
        
        c.execute('SELECT emulationID, emulationName FROM emulation')
        
        emulationList = c.fetchall()
       
        c.close()
    except sqlite.Error, e:
        print "Error getting emulations list %s:" % e.args[0]
        print e
        sys.exit(1)

    return emulationList
    
def getActiveEmulationList(name):
    
    activeEmu=[]
    dtNowSec = DistributionManager.timestamp(dt.now())
    
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
            
        c = conn.cursor()
        
        if name=="all":
            c.execute('SELECT startTime, stopTime, emulationID FROM emulationLifetime')
            
        else:
            c.execute("SELECT emulationID FROM emulation WHERE emulationName=?",[name])
            emulationIdArray = c.fetchone()
        
            if emulationIdArray:
                emulationID=emulationIdArray[0]
            else:
                raise sqlite.Error("Emulation "+str(name)+" not found")
            
            c.execute("SELECT startTime, stopTime, emulationID FROM emulationLifetime WHERE emulationID=?",[emulationID])
            
        conn.commit()                
        emulationLifetimeFetch = c.fetchall()
        
        if emulationLifetimeFetch:
            for row in emulationLifetimeFetch:
                runsTotal=0
                runsExecuted=0
                failedRunsInfo=[]
                    
                startTimeDBsec= DistributionManager.timestamp(DistributionManager.timeConv(row[0]))
                stopTimeDBsec=startTimeDBsec+float(row[1])

                c.execute('SELECT emulationID,emulationName FROM emulation WHERE emulationID=?',[str(row[2])])
                emunameFetch = c.fetchall()
                
                #getting number of executed runs 
                c.execute('SELECT distributionID,distributionName FROM distribution WHERE emulationID=?',[str(row[2])])
                distroFetch = c.fetchall()
                for distro in distroFetch:
                    c.execute('SELECT runNo,stressValue,executed,message FROM runLog WHERE distributionID=?',[str(distro[0])])
                    runLogFetch = c.fetchall()
                    for run in runLogFetch:
                        runsTotal=runsTotal+1
                        if run[2]== "False":
                            failedRunsInfo.append({"distributionID":distro[0],"distributionName":distro[1],"runNo":run[0],"stressValue":run[1],"message":run[3]})
                        
                        if run[2]== "True":
                            runsExecuted=runsExecuted+1
                            
                            
                if stopTimeDBsec > dtNowSec:
                    for items in emunameFetch:
                        activeEmu.append({"ID":items[0],"Name":items[1],"State":"active","runsTotal":runsTotal,"runsExecuted":runsExecuted,"failedRunsInfo":failedRunsInfo})
                else:
                    for items in emunameFetch:
                        
                        activeEmu.append({"ID":items[0],"Name":items[1],"State":"inactive","runsTotal":runsTotal,"runsExecuted":runsExecuted,"failedRunsInfo":failedRunsInfo})                    
 
        
        c.close()
        #[{'State': 'active', 'ID': 11, 'Name': u'myMixEmu'}, {'State': 'active', 'ID': 12, 'Name': u'myMixEmu'}]
        return activeEmu
   
    except sqlite.Error, e:
        print "dateOverlapCheck() SQL Error %s:" % e.args[0]
        print e
        return "<error>str(e)</error>"
        sys.exit(1)
    
    
    

def getEmulation(emulationName):
    #print "Hello this is getEmulation by name"
    
    distroList=[]
    distroArgs={}
    emulatorArg={}
    
   
        
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
        c = conn.cursor()
        
        c.execute("SELECT emulationID FROM emulation WHERE emulationName=?",[emulationName])
        emulationIdArray = c.fetchone()
        
        if emulationIdArray:
            emulationID=emulationIdArray[0]
        else:
            raise sqlite.Error("Emulation "+str(emulationName)+" not found")
            
        
        #EMULATION & EMULATION LIFETIME
        c.execute("""SELECT emulation.emulationID,emulation.emulationName, emulation.emulationType, emulation.resourceType,emulationLifetime.startTime,emulationLifetime.stopTime
         FROM emulation,emulationLifetime 
         WHERE emulation.emulationID=? and emulationLifetime.emulationID = emulation.emulationID""",[emulationID])
         
        emulationTable = c.fetchall()
        if emulationTable:
            for row in emulationTable:
        
        
                emulationID=row[0]
                emulationName=row[1]
                emulationType=row[2]
                resourceTypeEmulation=row[3]
                startTimeEmu=row[4]
                stopTimeEmu=row[5]
        
                  
        #DISTRIBUTION
        c.execute("""SELECT 
        distribution.distributionID,
        distribution.distributionName,
        distribution.startTime,
        distribution.duration,
        distribution.distributionGranularity,
        distribution.distributionType,
        distribution.emulator
        
        FROM distribution
        WHERE emulationID = ? """
        ,[emulationID])
        
        distributionTable = c.fetchall()
        
        
        for distributions in distributionTable:
            
            #single distribution level
                
                #GET DISTRIBUTION PARAMETERS
                c.execute("""SELECT 
                DistributionParameters.paramName, 
                DistributionParameters.Value
                FROM DistributionParameters
                WHERE distributionID=?""",[distributions[0]])    
                
                distroParamsTable = c.fetchall()
                
                
                for distributionParams in distroParamsTable:
                    
                    distroArgs.update({distributionParams[0]:distributionParams[1]})
            
                
                #GET EMULATOR PARAMETERS
                c.execute("""SELECT 
                EmulatorParameters.resourceType,
                EmulatorParameters.paramName,
                EmulatorParameters.value
                
                FROM EmulatorParameters
                WHERE distributionID=?""",[distributions[0]]) 
                
                emuParamsTable = c.fetchall()                
                emulatorArg={}
                for emuParams in emuParamsTable:
                    #print "emuParams"
                    print emuParams
                    
                    resourceTypeDist =emuParams[0]
                    
                    emulatorArg.update({emuParams[1]:emuParams[2]})
                    #print"emulatorArg"
                    #print emulatorArg
                    
        #saving single distribution elements to dictionary
                distroDict={"distributionsID":distributions[0], "distributionsName":distributions[1],"startTimeDistro":distributions[2],"durationDistro":distributions[3],"granularity":distributions[4],"distrType":distributions[5],"emulatorName":distributions[6],"resourceTypeDist":resourceTypeDist,"emulatorArg":emulatorArg,"distroArgs":distroArgs}                    
                distroList.append(distroDict)
        
        c.close()
        #print emulationID,emulationName,emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList
        return (emulationID,emulationName,emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList)

    except sqlite.Error, e:
        print "Error getting emulation list %s:" % e.args[0]
        print e
        return str(e)
        sys.exit(1)
        

        
def deleteEmulation(emulationID):
    '''
    Deleting specific emulation by ID number 
    '''
         
    distributionName=[]
    
    try:
        conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        c = conn.cursor()
        c.execute('SELECT distributionID,distributionName FROM distribution WHERE emulationID=?',[str(emulationID)])
                
        distributionIDfetch = c.fetchall()
        
        #getting list of distributions for emulation
        if distributionIDfetch:
            for row in distributionIDfetch:
                
                distributionID= row[0]
                distributionName.append(row[1])
                
                #deleting distribution related data
                c.execute('DELETE FROM DistributionParameters WHERE distributionID=?',[str(distributionID)])
                c.execute('DELETE FROM EmulatorParameters WHERE distributionID=?',[str(distributionID)])
                c.execute('DELETE FROM runLog WHERE distributionID=?',[str(distributionID)])
            
            c.execute('DELETE FROM distribution WHERE emulationID=?',[str(emulationID)])
            c.execute('DELETE FROM emulationLifetime WHERE emulationID=?',[str(emulationID)])
            c.execute('DELETE FROM emulation WHERE emulationID=?',[str(emulationID)])
            
            conn.commit()
            c.close()
            print "Emulation ID: ", emulationID," was deleted from DB"
                
        else:
            #print "Emulation ID: "+str(emulationID)+" does not exists looking for name" 
            c.execute('SELECT emulationID FROM emulation WHERE emulationName=?',[str(emulationID)])
            emulationIDfetch = c.fetchall()

            for row in emulationIDfetch:
                emulationID = row[0]
            c.execute('SELECT distributionID,distributionName FROM distribution WHERE emulationID=?',[str(emulationID)])
                    
            distributionIDfetch = c.fetchall()
            
            #getting list of distributions for emulation
            if distributionIDfetch:
                for row in distributionIDfetch:
                    distributionID= row[0]
                    distributionName.append(row[1])
                    
                    #deleting distribution related data
                    c.execute('DELETE FROM DistributionParameters WHERE distributionID=?',[str(distributionID)])
                    c.execute('DELETE FROM EmulatorParameters WHERE distributionID=?',[str(distributionID)])
                    c.execute('DELETE FROM runLog WHERE distributionID=?',[str(distributionID)])
                
                c.execute('DELETE FROM distribution WHERE emulationID=?',[str(emulationID)])
                c.execute('DELETE FROM emulationLifetime WHERE emulationID=?',[str(emulationID)])
                c.execute('DELETE FROM emulation WHERE emulationID=?',[str(emulationID)])
                    
            else:
                print "Emulation Name or ID \""+str(emulationID)+"\" does not exists" 
                return "Emulation Name or ID: "+str(emulationID)+" does not exists" 
                sys.exit(1)
            
            conn.commit()
            c.close()
            print "Emulation Name: ", emulationID," was deleted from DB"
        

    except sqlite.Error, e:
        print "Could not delete emulation: ",emulationID
        print "Error %s:" % e.args[0]
        print e
        return "Database error: "+str(e)
        sys.exit(1)
        
    
    
    
    #Now here we need to remove the emulation from the scheduler if exist
    uri ="PYRO:scheduler.daemon@"+str(readIfaceIP("schedinterface"))+":"+str(readLogLevel("schedport"))
    daemon=Pyro4.Proxy(uri)
    try:
        for Names in distributionName:
            daemon.deleteJobs(emulationID, Names)
    except:
        print "Scheduler is offline. Job cancelled."
    
    return "success"
    
def purgeAll():
    #print "Hello this is purgeAll"
     
    
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
            
        c = conn.cursor()
        c.execute('DELETE FROM distribution')
        c.execute('DELETE FROM emulationLifetime ')
        c.execute('DELETE FROM runLog')
        c.execute('DELETE FROM DistributionParameters')
        c.execute('DELETE FROM emulation')
        c.execute('DELETE FROM EmulatorParameters')
        #reset the counter
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="DistributionParameters"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="distribution"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="emulation"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="emulationLifetime"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="runLog"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="EmulatorParameters"')
        
        
        
        conn.commit()
    except sqlite.Error, e:
        print "Could not delete everything "
        print "Error %s:" % e.args[0]
        print e
        sys.exit(1)
        
    c.close()
    print "Deleting all DB entries"
    
    uri ="PYRO:scheduler.daemon@"+str(readIfaceIP("schedinterface"))+":"+str(readLogLevel("schedport"))
    daemon=Pyro4.Proxy(uri)
    try:
        print "Deleting all jobs"
        daemon.deleteJobs("all", "all")
    except Exception, e:
        print "Scheduler is not reachable: ",e
    print "Removing all log files"
    delLogsCmd ="rm "+HOMEPATH+"/logs/*" 
    os.system(delLogsCmd)

def createEmulation(emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData):
    #data checks
    #print "startTimeEmu: ",startTimeEmu.lower()
    if startTimeEmu.lower() == "now":
        startTimeEmu = emulationNow(2)
    
    try:
        check= dataCheck(startTimeEmu,float(stopTimeEmu))
        if check != "success":
            
            raise Exception('Another emulation already exists in this time frame')
            
    except Exception, e:
        return "Check the dates:"+str(startTimeEmu)+"\n"+str(e)
    
    try:
        
        result,lclmessage = checkDistroOverlap(startTimeEmu,distroList)
        if result==True:
            return lclmessage
        
    except Exception,e:
        return "Error: Check the sent XML format unable to process the distributions times",str(e) 
    
    # 3. We add end to emulationLifetime date by the longest distribution
    emulationLifetimeEndTime =int(stopTimeEmu)
    for n in distroList:
        compareEndTime = int(n["startTimeDistro"])+int(n["durationDistro"]) 
        if compareEndTime > emulationLifetimeEndTime:
            return "Distribution has date longer than emulation.Check distribution name: "+n["distributionsName"]
            sys.exit(0)
    
    uri ="PYRO:scheduler.daemon@"+str(readIfaceIP("schedinterface"))+":"+str(readLogLevel("schedport"))

    daemon=Pyro4.Proxy(uri)
    try:
        daemon.hello()
    except  Pyro4.errors.CommunicationError, e:
            return "\n---Check if SchedulerDaemon is started. Connection error cannot create jobs---\n"
            sys.exit(0)

    #connecting to the DB and storing parameters
    loggerJobReply="No logger scheduled"
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
            
        c = conn.cursor()
                
        # 1. Populate "emulation"
        c.execute('INSERT INTO emulation (emulationName,emulationType,resourceType,active,logging,logFrequency,logLevel) VALUES (?, ?, ?, ?, ?, ?, ?)', [emulationName,emulationType,resourceTypeEmulation,1,emulationLog,emulationLogFrequency,emulationLogLevel])
        emulationID = c.lastrowid
        returnEmulationName=(str(emulationID)+"-"+emulationName)
        c.execute('UPDATE emulation SET emulationName=? WHERE emulationID =?',(str(emulationID)+"-"+emulationName,emulationID))
        
        # 2. We populate "emulationLifetime" table  
        c.execute('INSERT INTO emulationLifetime (startTime,stopTime,emulationID) VALUES (?,?,?)', [startTimeEmu,stopTimeEmu,emulationID])
        emulationLifetimeID = c.lastrowid
        c.execute('UPDATE emulationLifetime SET stopTime=? WHERE emulationLifetimeID =?',(emulationLifetimeEndTime,emulationLifetimeID))
        c.execute('UPDATE emulation SET emulationLifetimeID=? WHERE emulationID=?',(emulationLifetimeID,emulationID))    
        
        conn.commit()
        '''
        {'emulatorName': u'stressapptest', 'distrType': u'linear', 'distrinutionsName': u' myMixEmu-dis-1',
         'durationDistro': u'120', 'resourceTypeEmu': u'CPU', 'startTimeDistro': u'0', 'granularity': u'10', 'arg': [u'10', u'90']}'''
        if emulationLog=="1":
            daemon=Pyro4.Proxy(uri)
            #creating run for logger with probe interval of 2 seconds
            interval=int(emulationLogFrequency)
            singleRunStartTime =DistributionManager.timestamp(DistributionManager.timeConv(startTimeEmu))
            loggerJobReply=daemon.createLoggerJob(singleRunStartTime,emulationLifetimeEndTime,interval,emulationID,emulationName,startTimeEmu)       
        
        for n in distroList:
            emulator=n["emulatorName"]
            duration = n["durationDistro"]
            distributionName = n["distributionsName"]
            resourceTypeDist = n["resourceTypeDist"]
            
            startTime = startTimeEmu
            startTimeDistro = n["startTimeDistro"]
            distributionGranularity = n["granularity"]
            distributionType = n["distrType"]
            distributionArg= n["distroArgs"]
            emulatorArg=n["emulatorArg"]
            
            #print "sending to DM these: ",emulationID,emulationLifetimeID,emulationName,distributionName,startTime,duration,emulator, distributionGranularity,distributionType,arg
            DistributionManager.distributionManager(emulationID,emulationLifetimeID,emulationName,distributionName,startTime,startTimeDistro,duration,emulator, distributionGranularity,distributionType,resourceTypeDist,distributionArg,emulatorArg)
            
            
        #emulationID,emulationLifetimeID,emulationName,distributionName,startTime,stopTime,emulator, distributionGranularity,distributionType,arg
            c.close()
    except sqlite.Error, e:
        print e
        return "SQL error:",e
        sys.exit(1)
        
    #emulation log creator
    global emuLoggerEM
    if emuLoggerEM is None:
        emuLoggerEM=loggerSet("Emulation Manager",str(emulationID)+"-"+str(emulationName)+"-syslog"+"_"+str(startTimeEmu)+".csv")     
     
    emuLoggerEM.info("##Emulation "+str(returnEmulationName)+" created")   
    emuLoggerEM.info(loggerJobReply) 
    emuLoggerEM.debug("Emulation Parameters:"+str(emulationID)+"-"+str(emulationLifetimeID)+"-"+str(emulationName)+"-"+str(startTime)+"-"+str(emulator)+"-"+str(emulatorArg))
    emuLoggerEM.debug("Distribution Parameters:"+str(distroList))
    #create log file with XML data
    try:
        f = open(HOMEPATH+"/logs/"+str(emulationID)+"-"+str(emulationName)+"-config"+"_"+str(startTime)+".xml", 'a')    
        f.write(xmlData)
        f.closed
    except Exception,e:
        emuLoggerEM.error("Unable to create config log file."+str(e))
    
    return returnEmulationName

def distributionTypeCheck(distributionType):
    #check if distribution type available in the framework
    distroList=DistributionManager.listDistributions("all")
    n=0
    for distName in distroList:
        if distributionType==distName:
            n=1
            
    if n==0:
            print "Distribution ",distributionType," does not exist"
            sys.exit(0)
      
def dataCheck(startTime,stopTime):
    
    time_re = re.compile('\d{4}[-]\d{2}[-]\d{2}[T,t]\d{2}[:]\d{2}[:]\d{2}')
    
    
    if time_re.match(startTime): 
    #and time_re.match(stopTime) :
        #print "date is correct"
        #checking the date overlap
        return dateOverlapCheck(startTime, stopTime)
    else:
        print "Date incorrect use YYYY-MM-DDTHH:MM:SS format "
        return "Date incorrect use YYYY-MM-DDTHH:MM:SS format "
        sys.exit(0)
    

    

   
def dateOverlapCheck(startTime, stopTime): 
    startTimeSec = DistributionManager.timestamp(DistributionManager.timeConv(startTime))
    stopTimeSec = startTimeSec+float(stopTime)
    #print startTimeSec
    #print stopTimeSec
    
    dtNowSec = DistributionManager.timestamp(dt.now())
    #print "dt.now():",dt.now()
    #print "dtNow:",dtNowSec
    
    if startTimeSec <= dtNowSec or stopTimeSec <= dtNowSec:
        print "Error: Dates cannot be in the past"
        return "Error: Dates cannot be in the past"
        sys.exit(1)

    if startTimeSec >= stopTimeSec:
        print "Start Date cannot be the same or later than stop time"
        return 
        sys.exit(1)
     
    n= "1"
    try:
        conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        c = conn.cursor()
    
        c.execute('SELECT startTime, stopTime FROM emulationLifetime')
                
        emulationLifetimeFetch = c.fetchall()
        
        if emulationLifetimeFetch:
            for row in emulationLifetimeFetch:
                #print row
                startTimeDBsec= DistributionManager.timestamp(DistributionManager.timeConv(row[0]))
                stopTimeDBsec = startTimeDBsec+float(row[1])
                
                if startTimeSec >= startTimeDBsec and startTimeSec <= stopTimeDBsec:
                    #print "Emulation already exist for this date change the date(1)"
                    
                    n= "Emulation already exist for this date change the date(1)"
                
                    
                    
                if stopTimeSec >= startTimeDBsec and stopTimeSec <= stopTimeDBsec:
                    #print "Emulation already exist for this date change the date(2)"
                    n= "Emulation already exist for this date change the date(2)"
                    
                    
                
                if startTimeSec <= startTimeDBsec and stopTimeSec >= stopTimeDBsec:
                    #print "Emulation already exist for this date change the date(3)"
                    
                    n= "Emulation already exist for this date change the date(3)"
                    
                    
                
        else:
            pass    
        conn.commit()
        c.close()
    except sqlite.Error, e:
        print "dateOverlapCheck() SQL Error %s:" % e.args[0]
        print e
        return str(e)
        sys.exit(1)
        
    if n=="1":
        return "success"
    else:
        return n
    


def checkPid(PROCNAME):        
    #ps ax | grep -v grep | grep Scheduler.py
    #print "ps ax | grep -v grep | grep "+str(PROCNAME)
    procTrace = subprocess.Popen("ps ax | grep -v grep | grep "+"\""+str(PROCNAME)+"\"",shell=True,stdout=PIPE).communicate()[0]
    #print "procTrace: ",procTrace
    if procTrace:
        pid = procTrace[0:5]
        #program running
        return pid
    else:
        #program not running
        return False
    
def services_control(service,action,args):
    if action == "start":
            HOMEPATH= os.environ['COCOMA']
            #print "Homepath", HOMEPATH
            if service == "scheduler".lower():
                #converting to our format
                service = "Scheduler.py"
                print "Starting ",service
                #check if pid running
                
                if checkPid(service):
                    print "ERROR: Scheduler must be already running:"
                    os.system("ps ax | grep -v grep | grep "+str(service))
                    sys.exit(1)
                else:
                    try:
                        HOMEPATH= os.environ['COCOMA']
                        sout=open(HOMEPATH+"/logs/COCOMAlogfile_Scheduler_sout.txt","wb")
                        
                        procSched = subprocess.Popen(HOMEPATH+"/bin/Scheduler.py "+args,shell=True,stdout=sout,stderr=sout)
                        procSched.stdout
                        schedPidNo =procSched.pid
                        print "Started Scheduler on PID No: ",schedPidNo
                        os.system("ps -Crp "+str(schedPidNo))
                    
                    except subprocess.CalledProcessError, e :
                        print "Error in launching scheduler: ",e
                

            if service == "api":
                service="ccmshAPI.py"
                
                print "Starting ",service
                
                if checkPid("Scheduler.py")==False:
                    print "ERROR: Scheduler must be started first!"
                    sys.exit(1)
                
                #get pid ID from DB
                if checkPid(service):
                    print "ERROR: API must be already running:"
                    os.system("ps ax | grep -v grep | grep "+str(service))
                    sys.exit(1)
 
                else:
                    try:
                        HOMEPATH= os.environ['COCOMA']
                        aout=open(HOMEPATH+"/logs/COCOMAlogfile_API_sout.txt","wb")
                        #print "args",args
                        ccmshAPI = subprocess.Popen(HOMEPATH+"/bin/ccmshAPI.py "+args,shell=True,stdout=aout,stderr=aout)
                        apiPidNo =ccmshAPI.pid
                        print "Started API on PID No: ",apiPidNo
                        os.system("ps -Crp "+str(apiPidNo))
                    except subprocess.CalledProcessError, e:
                        print "Error in launching ccmshAPI: ",e


    if action == "stop":
        
        if service == "scheduler":
                service ="Scheduler.py"
                if checkPid(service) ==False: 
                    print "Scheduler is not running"
                    sys.exit(1)
                while checkPid(service) !=False:
                    runner= checkPid(service)
 
                
                    if runner!=False:
                        print "Killing Scheduler on PID: ", runner
                    
                        os.kill(int(runner), 9)
 
                        
                    else:
                        print "Scheduler is not running"
                        sys.exit(1)                
                
                
            
        if service == "api":
            service ="ccmshAPI.py"
            runner = checkPid(service)
            while runner!=False:
                print "Killing API on PID: ", runner
               
                os.kill(int(runner), 9)

                runner = checkPid(service)
            else:
                print "ERROR: API is not running start it first"
                sys.exit(1)                

    if action == "show":
        if service == "scheduler":
            service = "Scheduler.py"
            #get pid ID from DB
            if checkPid(service):
                
                os.system("ps ax | grep -v grep | grep "+str(service))
                sys.exit(1)
            else:
                print "Scheduler is not running"

        if service == "api":
            service = "ccmshAPI.py"
            #get pid ID from DB
            if checkPid(service):
                
                os.system("ps ax | grep -v grep | grep "+str(service))
                sys.exit(1)
            else:
                print "API is not running" 
"""
def checkDistroOverlap2(startTimeEmu,distroList):
    '''
    1) Get all distributions of the same resource
    2) Create a list of time overlapping ones
    3) Create list of all their runs properties(times and resources)
    4) Create list of time overlapping runs
    5) Sum all overlapping runs stress load
   distroList= [{'durationDistro': u'60', 'distrType': u'trapezoidal', 'granularity': u'5', 'startTimeDistro': u'0', 'emulatorArg': {'memsleep': 0}, 'emulatorArgNotes': ['\nOK'], 'emulatorName': u'lookbusy', 'resourceTypeDist': u'mem', 'distroArgs': {'startload': 100, 'stopload': 1000}, 'distroArgsNotes': ['\nOK', '\nOK'], 'distributionsName': u'MEM_Distro'}]

    '''
    
    
    #creating arrays to sort distributions
    netArr=[]
    cpuArr=[]
    ioArr=[]
    memArr=[]
    

    
    '''
    1) Get all the parameters from XML parser
    2) Check if distributions have overlapping time frames
    3) If so check if have the same resource and are within available resource bounds  
    '''
    #[{'durationDistro': u'60', 'distrType': u'trapezoidal', 'granularity': u'5', 'startTimeDistro': u'0', 'emulatorArg': {'memsleep': 0}, 'emulatorArgNotes': ['\nOK'], 'emulatorName': u'lookbusy', 'resourceTypeDist': u'mem', 'distroArgs': {'startload': 100, 'stopload': 1000}, 'distroArgsNotes': ['\nOK', '\nOK'], 'distributionsName': u'MEM_Distro'}]

    n= len(distroList) 
    k=0
    for item in distroList:
        
        compareStartTime=int(item["startTimeDistro"])
        compareEndTime = int(item["startTimeDistro"])+int(item["durationDistro"]) 
        
        m=0
        while n!=m:
            compareStartTimeNext=int(distroList[m]["startTimeDistro"])
            compareEndTimeNext=int(compareStartTimeNext)+int(distroList[m]["durationDistro"])
            
            #if item is not itself
            if m!=k:
                #if the time intersects
                
                if compareStartTime<compareEndTimeNext and compareEndTime > compareStartTimeNext :
                    
                    #if they both are using the same resource
                    if item["resourceTypeDist"] == distroList[m]["resourceTypeDist"]:
                        
        
                        if item["resourceTypeDis"] =="mem":
                            memArr.add(distroList[m])
                            #if last element
                            if n==m:
                                memArr.add(item)
                                
                        if item["resourceTypeDis"] =="io":
                            ioArr.add(distroList[m])
                            if n==m:
                                memArr.add(item)
                            
                        if item["resourceTypeDis"] =="net":
                            netArr.add(distroList[m])
                            if n==m:
                                memArr.add(item)
                                
                        if item["resourceTypeDis"] =="cpu":
                            cpuArr.add(distroList[m])
                            if n==m:
                                memArr.add(item)
                        
                        
    #if array has more than two elements check the time overlap
    if len(ioArr)>1:
        #load distro module
        #get times and stress values of every run in every distribution
        #check if runs overlap form overlapping runs value array
        #sum all values in the array
        
    elif len(memArr)>1:
    
    elif len(cpuArr)>1:
    
    elif len(netArr)>1:
    
    else:
        #single items only in the array, no conflicts possible
        return False,"OK"                
                        
    def runOverlapCheck(distroArray):
        #[{'durationDistro': u'60', 'distrType': u'trapezoidal', 'granularity': u'5', 'startTimeDistro': u'0', 'emulatorArg': {'memsleep': 0}, 'emulatorArgNotes': ['\nOK'],
        #l 'emulatorName': u'lookbusy', 'resourceTypeDist': u'mem', 'distroArgs': {'startload': 100, 'stopload': 1000}, 'distroArgsNotes': ['\nOK', '\nOK'], 'distributionsName': u'MEM_Distro'}]
        #loading distro
        #HOMEPATH+"/distributions/dist_"+modName+".py"
        
        while item in distroArray:
        distroCountModule=DistributionManager.loadDistribution(item["distrType"])
        #<MEM, CPU, IO, NET> = argNames={"startload":{"upperBound":freeMem,"lowerBound":50,},"stopload":{"upperBound":freeMem,"lowerBound":50}}
        distroArgNamesMod=DistributionManager.loadDistributionArgNames(distroArray[0]["distrType"])
        distroArgsLimitsDict=distroArgNamesMod(distroArray[0]["resourceTypeDist"])
        #dictionary with args
        moduleArgs=distroArgsLimitsDict.keys()
        stressValues1,runStartTime1,runDurations1=distroCountModule(None,None,None,compareStartTime,int(item["durationDistro"]), int(item["granularity"]),item["distroArgs"],HOMEPATH)
        
        
                            '''
                        1)Now load "dist_["resourceTypeDist"]" module first with parameters from one distribution then with 
                          parameters from other distribution
                        2)Check if start time of runs intersects with other runs and when it does check the workload 
                        '''
                        #loading distro
                        #HOMEPATH+"/distributions/dist_"+modName+".py"
                        distroCountModule=DistributionManager.loadDistribution(item["distrType"])
                        #<MEM, CPU, IO, NET> = argNames={"startload":{"upperBound":freeMem,"lowerBound":50,},"stopload":{"upperBound":freeMem,"lowerBound":50}}
                        distroArgNamesMod=DistributionManager.loadDistributionArgNames(item["distrType"])
                        distroArgsLimitsDict=distroArgNamesMod(item["resourceTypeDist"])
                        #dictionary with args
                        moduleArgs=distroArgsLimitsDict.keys()
                        
                        #"distributionsName":distributionsName,"startTimeDistro":startTimeDistro,"durationDistro":durationDistro,"granularity":granularity,
                        #"distrType":distrType,"distroArgs":distroArgs,"emulatorName":emulatorName,"emulatorArg":emulatorArg,"resourceTypeDist":resourceTypeDist,
                        #"emulatorArgNotes":emulatorArgNotes,"distroArgsNotes":distroArgsNotes
                        
                        #getting run values of one distribution and conflicting one(not all parameters are being used)
                        #(emulationID="",emulationName="",emulationLifetimeID="",compareStartTime,int(item["durationDistro"]), int(item["granularity"]),item["distroArgs"],HOMEPATH
                        stressValues1,runStartTime1,runDurations1=distroCountModule(None,None,None,compareStartTime,int(item["durationDistro"]), int(item["granularity"]),item["distroArgs"],HOMEPATH)
                        stressValues2,runStartTime2,runDurations2=distroCountModule(None,None,None,compareStartTimeNext,int(distroList[m]["durationDistro"]), int(distroList[m]["granularity"]),distroList[m]["distroArgs"],HOMEPATH)
                        
                        #check which runs overlap
                        distroRunsLen1=len(runStartTime1)
                        distroRunsLen2=len(runStartTime2)
                        c1=0
                        c2=0
                        while c1!=distroRunsLen1:
                            while c2!=distroRunsLen2:
                                compareEndTime1=runStartTime1[c1]+runDurations1[c1]
                                compareStartTime2=runStartTime2[c2]
                                if compareStartTime2<compareEndTime1:
                                    #overlapping runs found check commutative workload
                                    combinedWorkload=int(stressValues1[c1])+int(stressValues2[c2])
                                        
                                    #function to compare argument bounds 
                                    a=0                    
                                    for args in moduleArgs:
                                        
                                        try:
                                            #startload
                                            arg0 = moduleArgs[a].lower()
                                            
                                            #dict: {'lowerBound': 0, 'upperBound': 100}
                                            distributionsLimitsDictValues = distroArgsLimitsDict[arg0]
                                            #print "boundsCompare(arg0,distributionsLimitsDictValues):",boundsCompare(arg0,distributionsLimitsDictValues)
                            
                                            #xmlValue,LimitsDictValues,variableName = None
                                            checked_distroArgs,checkDistroNote = XmlParser.boundsCompare(combinedWorkload,distributionsLimitsDictValues,arg0)         
                                            
                                            if checkDistroNote !="\nOK":
                                                print "Distributions resources Out of Bounds: "+item["distributionsName"]+" and "+distroList[m]["distributionsName"]+". The specified value "+str(combinedWorkload)+" was higher than the maximum limit "+str(checked_distroArgs)
                                                return True,"Distributions resources Out of Bounds: "+item["distributionsName"]+" and "+distroList[m]["distributionsName"]+". The specified value "+str(combinedWorkload)+" was higher than the maximum limit "+str(checked_distroArgs)
                                                sys.exit(0)           
                                            
                                            a+=1
                                            
                                        except Exception,e:
                                                logging.exception("error getting distribution arguments")
                                                sys.exit(0)
                                
                                
                                c2+=1
                            c1+=1
                            
                
                #print "Distributions Overlap: "+item["distributionsName"]+" and "+distroList[m]["distributionsName"]
                
            m+=1
    
        k+=1
    
    #if no problem has been found
    return False,"OK"    




    
    
    #1. Get required module loaded
    
    modhandleMy=DistributionManager.loadDistribution(distributionType)
    #2. Use this module for calculation and run creation   
    (stressValues,runStartTime,runDurations)=modhandleMy(emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,HOMEPATH)
    
    uri ="PYRO:scheduler.daemon@"+str(EmulationManager.readIfaceIP("schedinterface"))+":"+str(EmulationManager.readLogLevel("schedport"))

    daemon=Pyro4.Proxy(uri)
    
    n=0
    for vals in stressValues:
        print "stressValues: ",vals
        try:
            print "Things that are sent to daemon:\n",emulationID,emulationName,distributionName,emulationLifetimeID,runDurations[n],emulator,emulatorArg,resourceTypeDist,vals,runStartTime[n],str(n)
            print daemon.hello()
            #Sending emulation name already including ID stamp
            emulationNameID =str(emulationID)+"-"+str(emulationName)
            
            schedulerReply = str(daemon.createJob(emulationID,emulationNameID,distributionID,distributionName,emulationLifetimeID,runDurations[n],emulator,emulatorArg,resourceTypeDist,vals,runStartTime[n],str(n),runDurations[n]))
            

            distLoggerDM.info("Scheduler reply: "+str(schedulerReply))
    
"""                   
def checkDistroOverlap(startTimeEmu,distroList):
    '''
    1) Get all the parameters from XML parser
    2) Check if distributions have overlapping time frames
    3) If so check if have the same resource and are within available resource bounds  
    '''
    #[{'durationDistro': u'60', 'distrType': u'trapezoidal', 'granularity': u'5', 'startTimeDistro': u'0', 'emulatorArg': {'memsleep': 0}, 'emulatorArgNotes': ['\nOK'], 'emulatorName': u'lookbusy', 'resourceTypeDist': u'mem', 'distroArgs': {'startload': 100, 'stopload': 1000}, 'distroArgsNotes': ['\nOK', '\nOK'], 'distributionsName': u'MEM_Distro'}]

    n= len(distroList) 
    k=0
    for item in distroList:
        
        compareStartTime=int(item["startTimeDistro"])
        compareEndTime = int(item["startTimeDistro"])+int(item["durationDistro"]) 
        
        m=0
        while n!=m:
            compareStartTimeNext=int(distroList[m]["startTimeDistro"])
            compareEndTimeNext=int(compareStartTimeNext)+int(distroList[m]["durationDistro"])
            
            #if item is not itself
            if m!=k:
                #if the time intersects
                
                if compareStartTime<compareEndTimeNext and compareEndTime > compareStartTimeNext :
                    
                    #if they both are using the same resource
                    if item["resourceTypeDist"] == distroList[m]["resourceTypeDist"]:
                        '''
                        1)Now load "dist_["resourceTypeDist"]" module first with parameters from one distribution then with 
                          parameters from other distribution
                        2)Check if start time of runs intersects with other runs and when it does check the workload 
                        '''
                        #loading distro
                        #HOMEPATH+"/distributions/dist_"+modName+".py"
                        distroCountModule=DistributionManager.loadDistribution(item["distrType"])
                        #<MEM, CPU, IO, NET> = argNames={"startload":{"upperBound":freeMem,"lowerBound":50,},"stopload":{"upperBound":freeMem,"lowerBound":50}}
                        distroArgNamesMod=DistributionManager.loadDistributionArgNames(item["distrType"])
                        distroArgsLimitsDict=distroArgNamesMod(item["resourceTypeDist"])
                        #dictionary with args
                        moduleArgs=distroArgsLimitsDict.keys()
                        
                        #"distributionsName":distributionsName,"startTimeDistro":startTimeDistro,"durationDistro":durationDistro,"granularity":granularity,
                        #"distrType":distrType,"distroArgs":distroArgs,"emulatorName":emulatorName,"emulatorArg":emulatorArg,"resourceTypeDist":resourceTypeDist,
                        #"emulatorArgNotes":emulatorArgNotes,"distroArgsNotes":distroArgsNotes
                        
                        #getting run values of one distribution and conflicting one(not all parameters are being used)
                        #(emulationID="",emulationName="",emulationLifetimeID="",compareStartTime,int(item["durationDistro"]), int(item["granularity"]),item["distroArgs"],HOMEPATH
                        stressValues1,runStartTime1,runDurations1=distroCountModule(None,None,None,compareStartTime,int(item["durationDistro"]), int(item["granularity"]),item["distroArgs"],HOMEPATH)
                        stressValues2,runStartTime2,runDurations2=distroCountModule(None,None,None,compareStartTimeNext,int(distroList[m]["durationDistro"]), int(distroList[m]["granularity"]),distroList[m]["distroArgs"],HOMEPATH)
                        
                        #check which runs overlap
                        distroRunsLen1=len(runStartTime1)
                        distroRunsLen2=len(runStartTime2)
                        c1=0
                        c2=0
                        while c1!=distroRunsLen1:
                            while c2!=distroRunsLen2:
                                compareEndTime1=runStartTime1[c1]+runDurations1[c1]
                                compareStartTime2=runStartTime2[c2]
                                if compareStartTime2<compareEndTime1 and compareEndTime1>compareStartTime2:
                                    #overlapping runs found check commutative workload
                                    #adding to the value list
                                    combinedWorkload=int(stressValues1[c1])+int(stressValues2[c2])
                                        
                                    #function to compare argument bounds 
                                    a=0                    
                                    for args in moduleArgs:
                                        
                                        try:
                                            #startload
                                            arg0 = moduleArgs[a].lower()
                                            
                                            #dict: {'lowerBound': 0, 'upperBound': 100}
                                            distributionsLimitsDictValues = distroArgsLimitsDict[arg0]
                                            #print "boundsCompare(arg0,distributionsLimitsDictValues):",boundsCompare(arg0,distributionsLimitsDictValues)
                            
                                            #xmlValue,LimitsDictValues,variableName = None
                                            checked_distroArgs,checkDistroNote = XmlParser.boundsCompare(combinedWorkload,distributionsLimitsDictValues,arg0)         
                                            
                                            if checkDistroNote !="\nOK":
                                                print "Distributions resources Out of Bounds: "+item["distributionsName"]+" and "+distroList[m]["distributionsName"]+". The specified value "+str(combinedWorkload)+" was higher than the maximum limit "+str(checked_distroArgs)
                                                return True,"Distributions resources Out of Bounds: "+item["distributionsName"]+" and "+distroList[m]["distributionsName"]+". The specified value "+str(combinedWorkload)+" was higher than the maximum limit "+str(checked_distroArgs)
                                                sys.exit(0)           
                                            
                                            a+=1
                                            
                                        except Exception,e:
                                                logging.exception("error getting distribution arguments")
                                                sys.exit(0)
                                
                                
                                c2+=1
                            c1+=1
                            
                
                #print "Distributions Overlap: "+item["distributionsName"]+" and "+distroList[m]["distributionsName"]
                
            m+=1
    
        k+=1
    
    #if no problem has been found
    return False,"OK"    
        
                    
def emulationNow(delay):
    #print "EmulationManager.emulation.Now"
    #we are adding 5 seconds to compensate for incert
       
    timeNow = dt.now()
    pyStartTimeIn5 = timeNow + datetime.timedelta(seconds=int(delay))
    #pyStopTime=pyStartTimeIn5+ datetime.timedelta(minutes=int(duration))
    
    #print "timeNow: ",timeNow
    #print "startTimeIn5: ",pyStartTimeIn5
    #print "stopTime: ",pyStopTime
    
    #converting "2012-10-23 11:40:20.866356" to "2012-10-23T11:40:20"
    def timeFix(pydate):
        #print "this is timeConv!!!"
        Date = str(pydate)
        dateNorm =Date[0:10]+"T"+Date[11:19]
        #print "dateNorm: ", dateNorm
        return dateNorm 
    
    startTimeIn5 = timeFix(pyStartTimeIn5)
    #stopTime = timeFix(pyStopTime)
    #print "startTimeIn5: ",startTimeIn5
    #print "stopTime: ",stopTime
    
    return startTimeIn5

def writeInterfaceData(iface,column):
    '''
    Writes name of the interface into dedicated column in database
    '''
    try:
        conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        c = conn.cursor()
        sqlStatement="UPDATE config SET "+str(column)+"='"+str(iface)+"'"
        c.execute(sqlStatement)
        conn.commit()
        c.close()
        return True
    except sqlite.Error, e:
        print "Error writing config to database %s:" % e.args[0]
        print e
        return False
        
def readIfaceIP(column):
    '''
    Gets interface name from database and retrieves IP adress for the service
    '''
    try:
        conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        c = conn.cursor()
        
        c.execute('SELECT '+str(column)+' FROM config')
        
        ifaceVal = c.fetchall()
       
        c.close()
        
    except sqlite.Error, e:
        print "Error getting \"config\" table data %s:" % e.args[0]
        print e
        return False
    
    
    if ifaceVal:
        for row in ifaceVal:
            iface=row[0]
    
    IP=ccmshAPI.getifip(str(iface))
    
    
    return IP

def readLogLevel(column):
    '''
    Gets log level name from database 
    '''
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
        
        c = conn.cursor()
        c.execute('SELECT '+str(column)+' FROM config')
        logLevelList = c.fetchall()
        c.close()
                
    except sqlite.Error, e:
        print "Error getting \"config\" table data %s:" % e.args[0]
        print e
        return False
    
    if logLevelList:
        for row in logLevelList:
            logLevel=row[0]
    
    return logLevel
        


def logToFile(elementName,level,filename=None):
    #file writing handler
    fileLogger=logging.getLogger(elementName)
    fileLogger.setLevel(level)
    if filename == None:
        #setting log rotation for 10 files each up to 10000000 bytes (10MB)
        fileHandler = handlers.RotatingFileHandler(HOMEPATH+"/logs/COCOMAlogfile.csv",'a', 10000000, 10)
        fileLoggerFormatter=logging.Formatter ('%(asctime)s;%(name)s;%(levelname)s;%(message)s',datefmt='%m/%d/%Y %H:%M:%S')
        fileHandler.setFormatter(fileLoggerFormatter)
        fileLogger.addHandler(fileHandler)
        
        #cli writing handler
        #cliLoggerFormatter=logging.Formatter ('%(asctime)s - [%(name)s] - %(levelname)s : %(message)s',datefmt='%m/%d/%Y %H:%M:%S')
        #cliHandler = logging.StreamHandler()
        #cliHandler.setFormatter(cliLoggerFormatter)
        #fileLogger.addHandler(cliHandler)
    
    else:
        fileHandler= logging.FileHandler(HOMEPATH+"/logs/"+str(filename))
        
        fileLoggerFormatter=logging.Formatter ('%(asctime)s;%(name)s;%(levelname)s;%(message)s',datefmt='%m/%d/%Y %H:%M:%S')
        fileHandler.setFormatter(fileLoggerFormatter)
        fileLogger.addHandler(fileHandler)
    
    return fileLogger 


def loggerSet(loggerName,filename=None):
    
    LOG_LEVEL=logging.INFO
    
    LogLevel=readLogLevel("coreloglevel")
    if LogLevel=="info":
        LOG_LEVEL=logging.INFO
    if LogLevel=="debug":
        LOG_LEVEL=logging.DEBUG
    else:
        LOG_LEVEL=logging.INFO
    
    initLogger=logToFile(loggerName,LOG_LEVEL,filename)
    return initLogger


if __name__ == '__main__':

    getActiveEmulationList()
    
    pass