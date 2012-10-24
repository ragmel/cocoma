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
import DistributionManager,ccmsh
import Pyro4
import datetime
from datetime import datetime as dt
from subprocess import *

#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'
try:
    HOMEPATH= os.environ['COCOMA']
except:
    print "no $COCOMA environmental variable set"

def getEmulation(emulationName,emulationID,all,active):
    print "Hello this is getEmulation"
    #creating Dictionary to return for JSON
    returnDict={}
    returnList=[]
    
        
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
        c = conn.cursor()
        cRun=conn.cursor()
        
        # 1. By name
        if emulationName !="NULL":
            #c.execute("SELECT * FROM emulation WHERE emulationName='"+str(emulationName)+"'")
            print "DB entries for emulation Name", emulationName
            
            c.execute("""SELECT emulation.emulationID, emulation.emulationName, emulation.emulationType, emulation.resourceType, emulation.active, 
                         distribution.distributionGranularity,distribution.distributionType,DistributionParameters.arg0,DistributionParameters.arg1,
                         DistributionParameters.arg2,DistributionParameters.arg3,DistributionParameters.arg4,DistributionParameters.arg5,
                         DistributionParameters.arg6,DistributionParameters.arg7,DistributionParameters.arg8,DistributionParameters.arg9,
                         emulationLifetime.startTime,emulationLifetime.stopTime,emulationLifetime.emulationLifetimeID 
                         FROM emulation, distribution,emulationLifetime,DistributionParameters
                         WHERE emulation.emulationName=? and emulation.distributionID = distribution.distributionID and
                         emulationLifetime.emulationID = emulation.emulationID and 
                         DistributionParameters.distributionID=distribution.distributionID"""
                         ,[emulationName])
            print "DB entries for emulation Name", emulationName
        
        if emulationID !="NULL":
            #c.execute("SELECT * FROM emulation WHERE emulationID='"+str(emulationID)+"'")
            print "DB entries for emulation ID", emulationID
            c.execute("""SELECT emulation.emulationID,emulation.emulationName, emulation.emulationType, emulation.resourceType, emulation.active, 
                         distribution.distributionGranularity,distribution.distributionType,DistributionParameters.arg0,DistributionParameters.arg1,
                         DistributionParameters.arg2,DistributionParameters.arg3,DistributionParameters.arg4,DistributionParameters.arg5,
                         DistributionParameters.arg6,DistributionParameters.arg7,DistributionParameters.arg8,DistributionParameters.arg9,
                         emulationLifetime.startTime,emulationLifetime.stopTime,emulationLifetime.emulationLifetimeID 
                         FROM emulation, distribution,emulationLifetime,DistributionParameters
                         WHERE emulation.emulationID=? and emulation.distributionID = distribution.distributionID and
                         emulationLifetime.emulationID = emulation.emulationID and 
                         DistributionParameters.distributionID=distribution.distributionID"""
                         ,[emulationID])
            
          
            
        if all==1:
            #c.execute("SELECT * FROM emulation")
            print "DB entries for all emulations"
            
            c.execute("""SELECT emulation.emulationID,emulation.emulationName, emulation.emulationType, emulation.resourceType, emulation.active, 
                         distribution.distributionGranularity,distribution.distributionType,DistributionParameters.arg0,DistributionParameters.arg1,
                         DistributionParameters.arg2,DistributionParameters.arg3,DistributionParameters.arg4,DistributionParameters.arg5,
                         DistributionParameters.arg6,DistributionParameters.arg7,DistributionParameters.arg8,DistributionParameters.arg9,
                         emulationLifetime.startTime,emulationLifetime.stopTime,emulationLifetime.emulationLifetimeID 
                         FROM emulation, distribution,emulationLifetime,DistributionParameters
                         WHERE emulation.distributionID = distribution.distributionID and
                         emulationLifetime.emulationID = emulation.emulationID and 
                         DistributionParameters.distributionID=distribution.distributionID"""
                    )
            
            
        if active ==1:
            #c.execute('SELECT * FROM emulation WHERE active=?',("1"))
            print "DB entries for all active emulations"
            
            c.execute("""SELECT emulation.emulationID,emulation.emulationName, emulation.emulationType, emulation.resourceType, emulation.active, 
                         distribution.distributionGranularity,distribution.distributionType,DistributionParameters.arg0,DistributionParameters.arg1,
                         DistributionParameters.arg2,DistributionParameters.arg3,DistributionParameters.arg4,DistributionParameters.arg5,
                         DistributionParameters.arg6,DistributionParameters.arg7,DistributionParameters.arg8,DistributionParameters.arg9,
                         emulationLifetime.startTime,emulationLifetime.stopTime,emulationLifetime.emulationLifetimeID 
                         FROM emulation, distribution,emulationLifetime,DistributionParameters
                         WHERE emulation.active=? and emulation.distributionID = distribution.distributionID and
                         emulationLifetime.emulationID = emulation.emulationID and 
                         DistributionParameters.distributionID=distribution.distributionID"""
                         ,["1"])

        if active ==0 and all == 1:
            #c.execute('SELECT * FROM emulation WHERE active=?',("1"))
            print "DB entries for all inactive emulations"
            
            c.execute("""SELECT emulation.emulationID,emulation.emulationName, emulation.emulationType, emulation.resourceType, emulation.active, 
                         distribution.distributionGranularity,distribution.distributionType,DistributionParameters.arg0,DistributionParameters.arg1,
                         DistributionParameters.arg2,DistributionParameters.arg3,DistributionParameters.arg4,DistributionParameters.arg5,
                         DistributionParameters.arg6,DistributionParameters.arg7,DistributionParameters.arg8,DistributionParameters.arg9,
                         emulationLifetime.startTime,emulationLifetime.stopTime,emulationLifetime.emulationLifetimeID 
                         FROM emulation, distribution,emulationLifetime,DistributionParameters
                         WHERE emulation.active=? and emulation.distributionID = distribution.distributionID and
                         emulationLifetime.emulationID = emulation.emulationID and 
                         DistributionParameters.distributionID=distribution.distributionID"""
                         ,["0"])
            
        
            
        
        
        emulationTable = c.fetchall()
        
        if emulationTable:
            
        
            for row in emulationTable:
                runCounter=0
                runNoList=[]
                
                cRun.execute("""SELECT runLog.executed,runLog.runNo FROM runLog WHERE runLog.emulationLifetimeID=?""",[row[19]])
                runLogTable = cRun.fetchall()
                for rowRun in runLogTable:
                    
                    if rowRun[0] =="1":
                        runNoList.append(rowRun[1])
                        runCounter += 1
                        
                    
                
                print "------->\nemulation.emulationID",row[0],"\nemulation.emulationName",row[1], "\nemulation.emulationType",row[2], "\nemulation.resourceType",row[3],"\nemulation.active",row[4],"\ndistribution.distributionGranularity",row[5],"\ndistribution.distributionType",row[6],"\nDistributionParameters.arg0",row[7],"\nDistributionParameters.arg1",row[8]
                print "DistributionParameters.arg2",row[9],"\nDistributionParameters.arg3",row[10],"\nDistributionParameters.arg4",row[11],"\nDistributionParameters.arg5",row[12]
                print "DistributionParameters.arg6",row[13],"\nDistributionParameters.arg7",row[14],"\nDistributionParameters.arg8",row[15],"\nDistributionParameters.arg9",row[16]
                print "emulationLifetime.startTime",row[17],"\nemulationLifetime.stopTime",row[18], "\nRuns executed ",runCounter," out of ",row[5], "\nExecuted run numbers list ",runNoList
                returnDict={"emulationID":row[0],"emulationName":row[1],"emulationType":row[2], "resourceType":row[3],"active":row[4],"distributionGranularity":row[5],"distributionType":row[6],"startLoad":row[7],"stopLoad":row[8], "startTime":row[9],"stopTime":row[10]}
                
                returnList.append(returnDict)
        else:
            print "No results found in DB"
        
        
        
    except sqlite.Error, e:
        print "Error getting emulation list %s:" % e.args[0]
        print e
        sys.exit(1)
        
    c.close()
    return returnList



def deleteEmulation(emulationID):
    print "Hello this is deleteEmulation"
     
    
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
        c = conn.cursor()
        c.execute('SELECT distributionID, emulationName FROM emulation WHERE emulationID=?',[str(emulationID)])
                
        distributionIDfetch = c.fetchall()
        
        if distributionIDfetch:
            for row in distributionIDfetch:
                print row
                distributionID= row[0]
                emulationName = row[1]
                
        else:
            print "Emulation ID: "+str(emulationID)+" does not exists" 
            sys.exit(1)
        
        print "distro ID: ",distributionID
        
        c.execute('SELECT distributionType FROM distribution WHERE distributionID=?',[str(distributionID)]) 
        
        distributionTypeFetch = c.fetchall()
        
        if distributionTypeFetch:
            for row in distributionTypeFetch:
                distributionType= row[0]
        print "distro Type: ",distributionType
        
        
        c.execute('SELECT emulationLifetimeID FROM emulationLifetime WHERE emulationID=?',[str(emulationID)])
                
        emulationLifetimeIDfetch = c.fetchall()
        
        if emulationLifetimeIDfetch:
            for row in emulationLifetimeIDfetch:
                emulationLifetimeID= row[0]
        
        
        
        c.execute('DELETE FROM distribution WHERE distributionID=?',[str(distributionID)])
        c.execute('DELETE FROM emulationLifetime WHERE emulationID=?',[str(emulationID)])
        c.execute('DELETE FROM runLog WHERE emulationLifetimeID=?',[str(emulationLifetimeID)])
        c.execute('DELETE FROM DistributionParameters WHERE distributionID=?',[str(distributionID)])
        c.execute('DELETE FROM emulation WHERE emulationID=?',[str(emulationID)])
        
        conn.commit()
    except sqlite.Error, e:
        print "Could not delete emulationID: ",emulationID
        print "Error %s:" % e.args[0]
        print e
        sys.exit(1)
        
    c.close()
    print "Emulation ID: ", emulationID," was deleted"
    
    #Now here we need to remove the emulation from the scheduler
    uri ="PYRO:scheduler.daemon@localhost:51889"
    daemon=Pyro4.Proxy(uri)
    daemon.deleteJobs(emulationID, emulationName)
    
def purgeAll():
    print "Hello this is purgeAll"
     
    
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
        #reset the counter
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="DistributionParameters"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="distribution"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="emulation"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="emulationLifetime"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="runLog"')
        
        
        
        conn.commit()
    except sqlite.Error, e:
        print "Could not delete everything "
        print "Error %s:" % e.args[0]
        print e
        sys.exit(1)
        
    c.close()
    print "Everything was deleted in DB"
    
    #Now here we need to remove the emulation from the scheduler
    #uri ="PYRO:scheduler.daemon@localhost:51889"
    #daemon=Pyro4.Proxy(uri)
    # we need to remove jobs somehow too
    
#TO-DO: logic needs to be updated 
def updateEmulation(emulationID,newEmulationName,newDistributionType,newResourceType,newEmulationType,newStartTime,newStopTime, newDistributionGranularity,arg):
    print "Hello this is updateEmulation"
    
    uri ="PYRO:scheduler.daemon@localhost:51889"
    daemon=Pyro4.Proxy(uri)
    
    #1. Get all the values from the existing table
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
            
        c = conn.cursor()
        
        if emulationID !="NULL":
            #c.execute("SELECT * FROM emulation WHERE emulationID='"+str(emulationID)+"'")
            print "DB entries for emulation ID", emulationID
            c.execute("""SELECT emulation.emulationID,emulation.emulationName, emulation.emulationType, emulation.resourceType, emulation.active, 
                         distribution.distributionGranularity,distribution.distributionType,
                         emulationLifetime.startTime,emulationLifetime.stopTime,emulationLifetime.emulationLifetimeID,distribution.distributionID 
                         FROM emulation, distribution,emulationLifetime,DistributionParameters
                         WHERE emulation.emulationID=? and emulation.distributionID = distribution.distributionID and
                         emulationLifetime.emulationID = emulation.emulationID and 
                         DistributionParameters.distributionID=distribution.distributionID"""
                         ,[emulationID])
            
            emulationTable = c.fetchall()
        
        if emulationTable:
                      
        
            for row in emulationTable:
                
                print "------->\nemulation.emulationID",row[0],"\nemulation.emulationName",row[1], "\nemulation.emulationType",row[2], "\nemulation.resourceType",row[3],"\nemulation.active",row[4],"\ndistribution.distributionGranularity",row[5],"\ndistribution.distributionType",row[6],"\nDistributionParameters.startLoad",row[7],"\nDistributionParameters.stopLoad",row[8], "\nemulationLifetime.startTime",row[9],"\nemulationLifetime.stopTime",row[10]
                
                emulationID=row[0]
                emulationName=row[1]
                emulationType=row[2]
                resourceType=row[3]
                active=row[4]
                distributionGranularity=row[5]
                distributionType=row[6]
                startTime=row[7]
                stopTime=row[8]
                emulationLifetimeID =row[10]
                distributionID= row[11]
                
                #Deleting existing jobs at scheduler
                daemon.deleteJobs(emulationID, emulationName)
                
                #2. Check and assign which changes were made
                if newEmulationName != "NULL":
                    
                
                    emulationName = newEmulationName
                    c.execute('UPDATE emulation SET emulationName=? WHERE emulationID =?',(emulationName,emulationID))
                    conn.commit()
                    
                if newEmulationType != "NULL":
                    emulationType = newEmulationType
                    c.execute('UPDATE emulation SET emulationType=? WHERE emulationID =?',(emulationType,emulationID))
                    conn.commit()
                    
                if newResourceType != "NULL":
                    resourceType = newResourceType
                    c.execute('UPDATE emulation SET resourceType=? WHERE emulationID =?',(resourceType,emulationID))
                    conn.commit()
                    
                if newDistributionType != "NULL":
                    distributionType = newDistributionType
                    c.execute('UPDATE distribution SET distributionType=? WHERE distributionID =?',(distributionType,distributionID))
                    conn.commit()
                    
                if newStartTime != "NULL":
                    startTime = newStartTime
                    c.execute('UPDATE emulationLifetime SET startTime=? WHERE emulationLifetimeID =?',(startTime,emulationLifetimeID))
                    conn.commit()
                    
                if newStopTime != "NULL":
                    stopTime = newStopTime
                    c.execute('UPDATE emulationLifetime SET stopTime=? WHERE emulationLifetimeID =?',(stopTime,emulationLifetimeID))
                
                if newDistributionGranularity != "NULL":
                    distributionGranularity = newDistributionGranularity
                    c.execute('UPDATE distribution SET distributionGranularity=? WHERE distributionID =?',(distributionGranularity,distributionID))
                    conn.commit()
                ncount=0
                for arguments in arg:
                    c.execute('UPDATE DistributionParameters SET arg'+str(ncount)+'=? WHERE distributionID =?',(arguments,distributionID))
                    conn.commit()
                    
         
            
            
                #3. Deleting existing runLog
                c.execute('DELETE FROM runLog WHERE emulationLifetimeID=?',[str(emulationLifetimeID)])
                
                dataCheck(startTime,stopTime)
                conn.commit()
                                                
                #4. Create new runLog
                DistributionManager.distributionManager(emulationID,emulationLifetimeID,emulationName,startTime,stopTime, distributionGranularity,distributionType,arg)   
                
                
                
        else:
            print "emulation ID: \"",emulationID,"\" does not exists"
        
        
        conn.commit()
    except sqlite.Error, e:
        print "Error getting emulation list %s:" % e.args[0]
        print e
        sys.exit(1)
        
    c.close()
    

    
    

def createEmulation(emulationName,distributionType,resourceType,emulationType,startTime,stopTime, distributionGranularity,arg):
                    
    print "Hello this is createEmulation"
    
    #TO-DO: we need to check here if there is another emulation scheduled for the same time and if the date is in the future
    #dateCheck(startTime,stopTime)

    #connecting to the DB and storing parameters
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
            
        c = conn.cursor()
    
        # 1. populate DistributionParameters, of table determined by distributionType name in our test it is "linearDistributionParameters"
        c.execute('INSERT INTO DistributionParameters (arg0,arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6],arg[7],arg[8],arg[9]])

        distributionParametersID=c.lastrowid
                
        # 2. We populate "distribution" table  
        c.execute('INSERT INTO distribution (distributionGranularity, distributionType, distributionParametersID) VALUES (?, ?, ?)', [distributionGranularity, distributionType, distributionParametersID])
    
        distributionID=c.lastrowid
        
                
        # 3. Populate "emulation"
        c.execute('INSERT INTO emulation (emulationName,emulationType,resourceType,distributionID,active) VALUES (?, ?, ?, ?, ?)', [emulationName,emulationType,resourceType,distributionID,1])
        emulationID = c.lastrowid
        
        # 4. Adding missing distribution ID
        c.execute('UPDATE DistributionParameters SET distributionID=? WHERE distributionParametersID =?',(distributionID,distributionParametersID))
        
        # 5. We populate "emulationLifetime" table  
        c.execute('INSERT INTO emulationLifetime (startTime,stopTime,emulationID) VALUES (?, ?, ?)', [startTime,stopTime,emulationID])
        emulationLifetimeID = c.lastrowid
        
        #6. Update emulation with LifetimeID
        
        c.execute('UPDATE emulation SET emulationLifetimeID=? WHERE emulationID =?',(emulationLifetimeID,emulationID))
        
        
                
        
        
        c.execute("SELECT * FROM emulation WHERE emulationID='"+str(emulationID)+"'")
        print "Entry created with emulation ID", emulationID
        
        emulationEntry= c.fetchall()
        for row in emulationEntry: 
            print "emulationID:",row[0],"emulationName:", row[1],"emulationType:", row[2],"resourceType:", row[3], "distributionID:",row[4],"emulationLifetimeID:",row[5] ,"active:",row[6]
        
        dataCheck(startTime,stopTime)
        distributionTypeCheck(distributionType)
        conn.commit()
        
        DistributionManager.distributionManager(emulationID,emulationLifetimeID,emulationName,startTime,stopTime, distributionGranularity,distributionType,arg)
        
    except sqlite.Error, e:
        print "SQL Error %s:" % e.args[0]
        print e
        sys.exit(1)
    
    c.close()

    return emulationID

def distributionTypeCheck(distributionType):
    #check if distribution type available in the framework
    distroList=DistributionManager.listDistributions("all")
    n=0
    for distName in distroList:
        if distributionType==distName:
            n=1
            print "Match: ",distName
    if n==0:
            print "Distribution ",distributionType," does not exist"
            sys.exit(0)
    
def DistributionArgCheck(distributionType,arg):
    
    distrMod = DistributionManager.loadDistributionArgQty(distributionType)
    distrArgQty=distrMod()
    ncount=0
    for param in arg:
        if param != "NULL":
            ncount +=1
    if ncount < distrArgQty:
        print "Error: Arguments given: ",ncount,"\n",distributionType," distribution instnace require ",distrArgQty," arguments." 
        sys.exit(0)
    
    
    

def dataCheck(startTime,stopTime):
    print "Hello this is dataCheck"
   
 
    
    time_re = re.compile('\d{4}[-]\d{2}[-]\d{2}[T]\d{2}[:]\d{2}[:]\d{2}')
    
    
    if time_re.match(startTime) and time_re.match(stopTime) :
        print "date is correct"
    else:
        print "Date incorrect use YYYY-MM-DDTHH:MM:SS format "
        sys.exit(0)
    
    #checking the date overlap
    dateOverlapCheck(startTime, stopTime)
    

   
def dateOverlapCheck(startTime, stopTime):
    print "Hello this is dateOverlapCheck" 
    startTimeSec = DistributionManager.timestamp(DistributionManager.timeConv(startTime))
    stopTimeSec = DistributionManager.timestamp(DistributionManager.timeConv(stopTime))
    print startTimeSec
    print stopTimeSec
    
    dtNowSec = DistributionManager.timestamp(dt.now())
    print "dt.now():",dt.now()
    print "dtNow:",dtNowSec
    
    if startTimeSec <= dtNowSec or stopTimeSec <= dtNowSec:
        print "Error: Dates cannot be in the past"
        return "Error: Dates cannot be in the past"
        sys.exit(1)

    if startTimeSec >= stopTimeSec:
        print "Start Date cannot be the same or later than stop time"
        return 
        sys.exit(1)
     
    
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
            
        c = conn.cursor()
    
        c.execute('SELECT startTime, stopTime FROM emulationLifetime')
                
        emulationLifetimeFetch = c.fetchall()
        
        if emulationLifetimeFetch:
            for row in emulationLifetimeFetch:
                print row
                startTimeDBsec= DistributionManager.timestamp(DistributionManager.timeConv(row[0]))
                stopTimeDBsec = DistributionManager.timestamp(DistributionManager.timeConv(row[1]))
                
                if startTimeSec >= startTimeDBsec and startTimeSec <= stopTimeDBsec:
                    print "Emulation already exist for this date change the date(1)"
                    return "Emulation already exist for this date change the date(1)",sys.exit(1)
                    
                if stopTimeSec >= startTimeDBsec and stopTimeSec <= stopTimeDBsec:
                    print "Emulation already exist for this date change the date(2)"
                    return "Emulation already exist for this date change the date(2)",sys.exit(1)
                    
                
                if startTimeSec <= startTimeDBsec and stopTimeSec >= stopTimeDBsec:
                    print "Emulation already exist for this date change the date(3)"
                    return "Emulation already exist for this date change the date(3)",sys.exit(1)
                    
                
        else:
            print "db is empty any date is OK" 
        
        conn.commit()
        
        
        
    except sqlite.Error, e:
        print "dateOverlapCheck() SQL Error %s:" % e.args[0]
        print e
        sys.exit(1)
    
    c.close()


def checkPid(PROCNAME):        
    #ps ax | grep -v grep | grep Scheduler.py
    #print "ps ax | grep -v grep | grep "+str(PROCNAME)
    procTrace = subprocess.Popen("ps ax | grep -v grep | grep "+str(PROCNAME),shell=True,stdout=PIPE).communicate()[0]
    #print "procTrace: ",procTrace
    if procTrace:
        pid = procTrace[0:5]
        #print "procTracePID: ",pid
        #program running
        return pid
    else:
        #program not running
        return False
    
def services_control(service,action,args):
    if action == "start":
            HOMEPATH= os.environ['COCOMA']
            if service == "scheduler":
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
                        sout=open(HOMEPATH+"/.~sout","wb")
                        procSched = subprocess.Popen(HOMEPATH+"/bin/Scheduler.py",stdout=sout,stderr=sout)
                        procSched.stdout
                        schedPidNo =procSched.pid
                        print "Started Scheduler on PID No: ",schedPidNo
                        os.system("ps -Crp "+str(schedPidNo))
                    
                    except subprocess.CalledProcessError, e:
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
                        aout=open(HOMEPATH+"/.~aout","wb")
                        ccmshAPI = subprocess.Popen(HOMEPATH+"/bin/ccmshAPI.py",stdout=aout,stderr=aout)
                        apiPidNo =ccmshAPI.pid
                        print "Started API on PID No: ",apiPidNo
                        os.system("ps -Crp "+str(apiPidNo))
                    except subprocess.CalledProcessError, e:
                        print "Error in launching ccmshAPI: ",e


    if action == "stop":
        
        if service == "scheduler":
                service ="Scheduler.py"
                runner = checkPid(service)
 
                
                if runner!=False:
                    print "Killing Scheduler on PID: ", runner
                    
                    os.kill(int(runner), 9)
 
                    sys.exit(1)
                else:
                    print "ERROR: Scheduler is not running start it first"
                    sys.exit(1)                
                
                
            
        if service == "api":
            service ="ccmshAPI.py"
            runner = checkPid(service)
            if runner!=False:
                print "Killing API on PID: ", runner
               
                os.kill(int(runner), 9)

                sys.exit(1)
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
                    
def emulationNow(duration):
    print "EmulationManager.emulation.Now"
    #we are adding 5 seconds to compensate for incert
       
    timeNow = dt.now()
    pyStartTimeIn5 = timeNow + datetime.timedelta(seconds=5)
    pyStopTime=pyStartTimeIn5+ datetime.timedelta(minutes=int(duration))
    
    print "timeNow: ",timeNow
    print "startTimeIn5: ",pyStartTimeIn5
    print "stopTime: ",pyStopTime
    
    #converting "2012-10-23 11:40:20.866356" to "2012-10-23T11:40:20"
    def timeFix(pydate):
        print "this is timeConv!!!"
        Date = str(pydate)
        dateNorm =Date[0:10]+"T"+Date[11:19]
        print "dateNorm: ", dateNorm
        return dateNorm 
    
    startTimeIn5 = timeFix(pyStartTimeIn5)
    stopTime = timeFix(pyStopTime)
    print "startTimeIn5: ",startTimeIn5
    print "stopTime: ",stopTime
    
    return startTimeIn5,stopTime
   
    

if __name__ == '__main__':
    
    
    emulationName = "mytest"
    emulationType = "Malicious"
    resourceType = "CPU"
    startTime = "2012-09-10T15:30:00"
    
    stopTime= "2013-09-10T19:59:00"
    dateOverlapCheck(startTime, stopTime)
    distributionGranularity = 10
    distributionType = "linear"
    startLoad = 20
    stopLoad = 100
       
    pass