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
    
def getActiveEmulationList():
    
    activeEmu=[]
    dtNowSec = DistributionManager.timestamp(dt.now())
    print "dt.now():",dt.now()
    print "dtNow:",dtNowSec
    
    
    
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
            
        c = conn.cursor()
        
        
        c.execute('SELECT startTime, stopTime, emulationID FROM emulationLifetime')
        conn.commit()
                
        emulationLifetimeFetch = c.fetchall()
        
        if emulationLifetimeFetch:
            print "emulation Found"
            for row in emulationLifetimeFetch:
                
                startTimeDBsec= DistributionManager.timestamp(DistributionManager.timeConv(row[0]))
                #we already have it in sec
                #stopTimeDBsec = DistributionManager.timestamp(DistributionManager.timeConv(row[1]))
                stopTimeDBsec=startTimeDBsec+float(row[1])
                
                if stopTimeDBsec > dtNowSec:
                    print "Emulation ID: "+str(row[2])+" is active"
                    
                    c.execute('SELECT emulationID,emulationName FROM emulation WHERE emulationID=?',[str(row[2])])
                    emunameFetch = c.fetchall()
                    
                    activeEmu.extend(emunameFetch)

                    
                
        else:
            print "no active emulations exists" 
        
        print activeEmu
        return activeEmu
        
        
        
    except sqlite.Error, e:
        print "dateOverlapCheck() SQL Error %s:" % e.args[0]
        print e
        sys.exit(1)
    
    c.close()
    

def getEmulation(emulationID):
    print "Hello this is getEmulation by ID"
    
    distroList=[]
    """
    distroDict={"distributionsName":distributionsName,"startTimeDistro":startTimeDistro,"durationDistro":durationDistro,"granularity":granularity,
    "distrType":distrType,"distroArgs":distroArgs,"emulatorName":emulatorName,"emulatorArg":emulatorArg,"resourceTypeDist":resourceTypeDist}
    
    """
    distroArgs={}
    emulatorArg={}
    
    """
    #name,emutype,resourcetype,starttime
    myMixEmu Mix Mix now [{'distroArgs': {'startLoad': u'11', 'stopLoad': u'91'}, 'emulatorName': u'lookbusy',
    'distrType': u'linear', 'resourceTypeDist': u'CPU', 'startTimeDistro': u'0', 'distributionsName': u' myMixEmu-dis-1',
     'durationDistro': u'120', 'emulatorArg': {'ncpus': u'0'}, 'granularity': u'10'}]
    """
    
        
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
        c = conn.cursor()
        
        

       
        
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
                    print "emuParams"
                    print emuParams
                    
                    resourceTypeDist =emuParams[0]
                    
                    emulatorArg.update({emuParams[1]:emuParams[2]})
                    print"emulatorArg"
                    print emulatorArg
                    
        #saving single distribution elements to dictionary
                distroDict={"distributionsID":distributions[0], "distributionsName":distributions[1],"startTimeDistro":distributions[2],"durationDistro":distributions[3],"granularity":distributions[4],"distrType":distributions[5],"emulatorName":distributions[6],"resourceTypeDist":resourceTypeDist,"emulatorArg":emulatorArg,"distroArgs":distroArgs}
                
                    
                distroList.append(distroDict)
        '''
        print"distroDict:"
        print distroDict
        print "distroList:"
        print distroList
        
        
        
        print "emulationTable:"
        print emulationTable
        
        print "distributionTable:"
        print distributionTable
        
        print "distroParamsTable:"
        print distroParamsTable
        
        print "emuParamsTable:"
        print emuParamsTable
        '''

        
        c.close()
    except sqlite.Error, e:
        print "Error getting emulation list %s:" % e.args[0]
        print e
        sys.exit(1)
        
    print emulationID,emulationName,emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList
    return (emulationID,emulationName,emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList)

        
def deleteEmulation(emulationID):
    print "Hello this is deleteEmulation"
         
    distributionName=[]
    
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
        c = conn.cursor()
        c.execute('SELECT distributionID,distributionName FROM distribution WHERE emulationID=?',[str(emulationID)])
                
        distributionIDfetch = c.fetchall()
        
        #getting list of distributions for emulation
        if distributionIDfetch:
            for row in distributionIDfetch:
                print row
                distributionID= row[0]
                distributionName.append(row[1])
                
                #deleting distribution related data
                c.execute('DELETE FROM DistributionParameters WHERE distributionID=?',[str(distributionID)])
                c.execute('DELETE FROM EmulatorParameters WHERE distributionID=?',[str(distributionID)])
                
        else:
            print "Emulation ID: "+str(emulationID)+" does not exists" 
            return "Emulation ID: "+str(emulationID)+" does not exists"
            sys.exit(1)
        
        
        

        c.execute('DELETE FROM distribution WHERE emulationID=?',[str(emulationID)])
        c.execute('DELETE FROM emulationLifetime WHERE emulationID=?',[str(emulationID)])
        c.execute('DELETE FROM emulation WHERE emulationID=?',[str(emulationID)])
        
        
        conn.commit()
    except sqlite.Error, e:
        print "Could not delete emulationID: ",emulationID
        print "Error %s:" % e.args[0]
        print e
        return "Database error: "+str(e)
        sys.exit(1)
        
    c.close()
    print "Emulation ID: ", emulationID," was deleted from DB"
    
    #Now here we need to remove the emulation from the scheduler if exist
    uri ="PYRO:scheduler.daemon@localhost:51889"
    daemon=Pyro4.Proxy(uri)
    for items in distributionName:
        daemon.deleteJobs(emulationID, distributionName)
    
    return "success"
    
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
    

    
    

def createEmulation(emulationName, emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList):
                    
    print "Hello this is createEmulation"


        # 3. We add end to emulationLifetime date by the longest distribution
    emulationLifetimeEndTime =int(stopTimeEmu)
    for n in distroList:
        compareEndTime = int(n["startTimeDistro"])+int(n["durationDistro"]) 
        print "compareEndTime",compareEndTime
        if compareEndTime > emulationLifetimeEndTime:
            print "Distribution has date longer than emulation.Check distribution name: "+n["distributionsName"]
            return "Distribution has date longer than emulation.Check distribution name: "+n["distributionsName"]
            sys.exit(0)
    
    uri ="PYRO:scheduler.daemon@localhost:51889"

    daemon=Pyro4.Proxy(uri)
    try:
        print daemon.hello()
    except  Pyro4.errors.CommunicationError, e:
            print e
            print "\n---Check if SchedulerDaemon is started. Connection error cannot create jobs---\n"
            return "\n---Check if SchedulerDaemon is started. Connection error cannot create jobs---\n"
            sys.exit(0)
            




    
    #TO-DO: we need to check here if there is another emulation scheduled for the same time and if the date is in the future
    #dateCheck(startTime,stopTime)

    #connecting to the DB and storing parameters
    try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
        else:
            conn = sqlite.connect('./data/cocoma.sqlite')
            
        c = conn.cursor()
                
        # 1. Populate "emulation"
        c.execute('INSERT INTO emulation (emulationName,emulationType,resourceType,active) VALUES (?, ?, ?, ?)', [emulationName,emulationType,resourceTypeEmulation,1])
        emulationID = c.lastrowid
        
        # 2. We populate "emulationLifetime" table  
        c.execute('INSERT INTO emulationLifetime (startTime,stopTime,emulationID) VALUES (?,?,?)', [startTimeEmu,stopTimeEmu,emulationID])
        emulationLifetimeID = c.lastrowid
        

        
        print "longest time: ",emulationLifetimeEndTime
        
        c.execute('UPDATE emulationLifetime SET stopTime=? WHERE emulationLifetimeID =?',(emulationLifetimeEndTime,emulationLifetimeID))
        c.execute('UPDATE emulation SET emulationLifetimeID=? WHERE emulationID=?',(emulationLifetimeID,emulationID))    
        
        # 4. Adding missing distribution ID
        #c.execute('UPDATE DistributionParameters SET distributionID=? WHERE distributionParametersID =?',(distributionID,distributionParametersID))
        
        
        
        #6. Update emulation with LifetimeID
        
        #c.execute('UPDATE emulation SET emulationLifetimeID=? WHERE emulationID =?',(emulationLifetimeID,emulationID))
        
        
                
        
        
        #c.execute("SELECT * FROM emulation WHERE emulationID='"+str(emulationID)+"'")
        print "Entry created with emulation ID", emulationID
        
       # emulationEntry= c.fetchall()
       # for row in emulationEntry: 
        #    print "emulationID:",row[0],"emulationName:", row[1],"emulationType:", row[2],"resourceType:", row[3],"emulator:",row[4], "distributionID:",row[5],"emulationLifetimeID:",row[6] ,"active:",row[7]
        
        #dataCheck(startTime,stopTime)
        #distributionTypeCheck(distributionType)
        conn.commit()
        '''
        {'emulatorName': u'stressapptest', 'distrType': u'linear', 'distrinutionsName': u' myMixEmu-dis-1',
         'durationDistro': u'120', 'resourceTypeEmu': u'CPU', 'startTimeDistro': u'0', 'granularity': u'10', 'arg': [u'10', u'90']}'''
        
        
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
            return emulationID
            
        #emulationID,emulationLifetimeID,emulationName,distributionName,startTime,stopTime,emulator, distributionGranularity,distributionType,arg
            c.close()
    except sqlite.Error, e:
        print "SQL Error %s:" % e.args[0]
        print e
        return "SQL error:",e
        sys.exit(1)
    
    

    

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
            print "Homepath", HOMEPATH
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
                        sout=open(HOMEPATH+"/.~sout","wb")
                        
                        procSched = subprocess.Popen(HOMEPATH+"/bin/Scheduler.py",stdout=sout,stderr=sout)
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
                        aout=open(HOMEPATH+"/.~aout","wb")
                        print "args",args
                        ccmshAPI = subprocess.Popen("python "+HOMEPATH+"/bin/ccmshAPI.py "+args,shell=True,stdout=aout,stderr=aout)
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
    
    
    #emulationName = "mytest"
    #emulationType = "Malicious"
    #resourceType = "CPU"
    #startTime = "2012-09-10T15:30:00"
    
    #stopTime= "2013-09-10T19:59:00"
    #dateOverlapCheck(startTime, stopTime)
    #distributionGranularity = 10
    #distributionType = "linear"
    #startLoad = 20
    #stopLoad = 100
    #print getEmulationList()
    #getEmulation(2)
    getActiveEmulationList()
    
    pass