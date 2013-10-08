import Pyro4, os, sys, imp
import sqlite3 as sqlite
import subprocess, psutil
from subprocess import PIPE
import datetime, time
from datetime import datetime as dt
import logging
from logging import handlers

import EMQproducer

global producer


producer = EMQproducer.Producer()
emuLoggerEM = None

Pyro4.config.HMAC_KEY='pRivAt3Key'
#in Pyro 4.21 "serpent" is default serializer, which is safer but less flexible comparing to "pickle"
Pyro4.config.SERIALIZER='pickle'

def getHomepath():
    try:
        HOMEPATH = os.environ['COCOMA']
        return HOMEPATH
    except:
        print "no $COCOMA environmental variable set"

global HOMEPATH
HOMEPATH = getHomepath()

def dbconn():
    try:
        conn = sqlite.connect(HOMEPATH + '/data/cocoma.sqlite')
        return conn
    except sqlite.Error, e:
        print "Could not connect to DB "
        print "Error %s:" % e.args[0]
        print e
        return "DB connection Error"
        

def services_control(service, action, args):
    if action == "start":
            if service == "scheduler".lower():
                # converting to our format
                service = "Scheduler.py"
                print "Starting ", service
                # check if pid running
                
                if checkPid(service):
                    print "ERROR: Scheduler must be already running:"
                    os.system("ps ax | grep -v grep | grep " + str(service))
                    sys.exit(1)
                else:
                    try:
                        sout = open(HOMEPATH + "/logs/COCOMAlogfile_Scheduler_sout.txt", "wb")
                        
                        procSched = subprocess.Popen(HOMEPATH + "/bin/Scheduler.py " + args, shell = True, stdout = sout, stderr = sout)
                        procSched.stdout
                        schedPidNo = procSched.pid
                        print "Started Scheduler on PID No: ", schedPidNo
                        os.system("ps -Crp " + str(schedPidNo))
                    
                    except subprocess.CalledProcessError, e :
                        print "Error in launching scheduler: ", e
                

            if service == "api":
                service = "ccmshAPI.py"
                
                print "Starting ", service
                
                if checkPid("Scheduler.py") == False:
                    print "ERROR: Scheduler must be started first!"
                    sys.exit(1)
                
                # get pid ID from DB
                if checkPid(service):
                    print "ERROR: API must be already running:"
                    os.system("ps ax | grep -v grep | grep " + str(service))
                    sys.exit(1)
 
                else:
                    try:
                        aout = open(HOMEPATH + "/logs/COCOMAlogfile_API_sout.txt", "wb")
                        # print "args",args
                        ccmshAPI = subprocess.Popen(HOMEPATH + "/bin/ccmshAPI.py " + args, shell = True, stdout = aout, stderr = aout)
                        apiPidNo = ccmshAPI.pid
                        print "Started API on PID No: ", apiPidNo
                        os.system("ps -Crp " + str(apiPidNo))
                    except subprocess.CalledProcessError, e:
                        print "Error in launching ccmshAPI: ", e


    if action == "stop":
        
        if service == "scheduler":
                service = "Scheduler.py"
                if checkPid(service) == False: 
                    print "Scheduler is not running"
                    sys.exit(1)
                while checkPid(service) != False:
                    runner = checkPid(service)
 
                
                    if runner != False:
                        print "Killing Scheduler on PID: ", runner
                    
                        os.kill(int(runner), 9)
 
                        
                    else:
                        print "Scheduler is not running"
                        sys.exit(1)                
                
                
            
        if service == "api":
            service = "ccmshAPI.py"
            runner = checkPid(service)
            while runner != False:
                print "Killing API on PID: ", runner
               
                os.kill(int(runner), 9)

                runner = checkPid(service)
            else:
                print "ERROR: API is not running start it first"
                sys.exit(1)                

    if action == "show":
        if service == "scheduler":
            service = "Scheduler.py"
            # get pid ID from DB
            if checkPid(service):
                
                os.system("ps ax | grep -v grep | grep " + str(service))
                sys.exit(1)
            else:
                print "Scheduler is not running"

        if service == "api":
            service = "ccmshAPI.py"
            # get pid ID from DB
            if checkPid(service):
                
                os.system("ps ax | grep -v grep | grep " + str(service))
                sys.exit(1)
            else:
                print "API is not running" 

def removeExtraJobs(EmulationName):

    #Used for deleting Extra jobs Which will not be run
    try:
        conn = dbconn()
        c = conn.cursor()
        c.execute("SELECT emulationID FROM emulation WHERE emulationName=?", [EmulationName])
        EmulationID = c.fetchall()
        EmulationID = EmulationID[0][0]
        
        c.execute("SELECT distributionID FROM distribution WHERE emulationID=?", [EmulationID])
        distributionIDList = c.fetchall()
        
        daemon = getDaemon()
        daemon.deleteJobs(EmulationID, EmulationName)
        for distributionID in distributionIDList:
            c.execute("DELETE FROM runLog WHERE executed='Pending' AND distributionID=?", [distributionID[0]])
                
        conn.commit()
        c.close()
    except sqlite.Error, e:
        print "Couldn't delete extra jobs"
        print "Error %s:" % e.args[0]
        print e
        sys.exit(1)

def purgeAll():
    
    try:
        conn = dbconn()
        c = conn.cursor()
        c.execute('DELETE FROM distribution')
        c.execute('DELETE FROM emulationLifetime ')
        c.execute('DELETE FROM runLog')
        c.execute('DELETE FROM DistributionParameters')
        c.execute('DELETE FROM emulation')
        c.execute('DELETE FROM EmulatorParameters')
        # reset the counter
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="DistributionParameters"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="distribution"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="emulation"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="emulationLifetime"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="runLog"')
        c.execute('UPDATE sqlite_sequence SET seq=0 WHERE name="EmulatorParameters"')
        
        
        
        conn.commit()
        c.close()
        conn.close()
    except sqlite.Error, e:
        print "Could not delete everything "
        print "Error %s:" % e.args[0]
        print e
        sys.exit(1)
    
    # try:
    #    producer.sendmsg(myName,"USER REQUEST: "+sys._getframe().f_code.co_name+" "+name)
    # except Exception,e:
    #    print "NO USER INPUT"
 
    
    print "Deleting all DB entries"
    
    daemon = getDaemon()
    try:
        print "Deleting all jobs"
        daemon.deleteJobs("all", "all")
    except Exception, e:
        print "Scheduler is not reachable: ", e

    # try:
    #    producer.sendmsg(myName,"USER REQUEST: "+sys._getframe().f_code.co_name)
    # except Exception,e:
    #    print "NO USER INPUT"
    # print "Removing all log files"
    # delLogsCmd ="rm "+HOMEPATH+"/logs/*" 
    # os.system(delLogsCmd)
    
def emulationNow(delay):
    # print "EmulationManager.emulation.Now"
    # we are adding 5 seconds to compensate for incert
       
    timeNow = dt.now()
    pyStartTimeIn5 = timeNow + datetime.timedelta(seconds = int(delay))
    # pyStopTime=pyStartTimeIn5+ datetime.timedelta(minutes=int(duration))
    
    # print "timeNow: ",timeNow
    # print "startTimeIn5: ",pyStartTimeIn5
    # print "stopTime: ",pyStopTime
    
    # converting "2012-10-23 11:40:20.866356" to "2012-10-23T11:40:20"
    def timeFix(pydate):
        # print "this is timeConv!!!"
        Date = str(pydate)
        dateNorm = Date[0:10] + "T" + Date[11:19]
        # print "dateNorm: ", dateNorm
        return dateNorm 
    
    startTimeIn5 = timeFix(pyStartTimeIn5)
    # stopTime = timeFix(pyStopTime)
    # print "startTimeIn5: ",startTimeIn5
    # print "stopTime: ",stopTime
    
    return startTimeIn5


def readLogLevel(column):
    '''
    Gets log level name from database 
    '''
    try:
        c = dbconn().cursor()
        c.execute('SELECT ' + str(column) + ' FROM config')
        logLevelList = c.fetchall()
        c.close()
                
    except sqlite.Error, e:
        print "Error getting \"config\" table data %s:" % e.args[0]
        print e
        return False
    
    if logLevelList:
        for row in logLevelList:
            logLevel = row[0]
    
    return logLevel

def readIfaceIP(column):
    '''
    Gets interface name from database and retrieves IP adress for the service
    '''
    try:
        c = dbconn().cursor()
        
        c.execute('SELECT ' + str(column) + ' FROM config')
        
        ifaceVal = c.fetchall()
       
        c.close()
        
    except sqlite.Error, e:
        print "Error getting \"config\" table data %s:" % e.args[0]
        print e
        return False
    
    
    if ifaceVal:
        for row in ifaceVal:
            iface = row[0]
    
    IP = getifip(str(iface))
    
    
    return IP

def readBackfuzzPath():
    '''
    Gets the path to the backfuzz emulator from the Database
    '''
    try:
        c = dbconn().cursor()
        
        c.execute('SELECT backfuzz_path FROM config')
        
        path = c.fetchall()
       
        c.close()
        
    except sqlite.Error, e:
        print "Error getting \"config\" table data %s:" % e.args[0]
        print e
        return False
    
    
    if path:
        for row in path:
            path = row[0]

    return path

def getEmulationList(name):
    
    activeEmu = []
    dtNowSec = timestamp(dt.now())
    
    try:
        c = dbconn().cursor()
        
        if name == "all":
            c.execute('SELECT startTime, stopTime, emulationID FROM emulationLifetime')
        else:
            c.execute("SELECT emulationID FROM emulation WHERE emulationName=?", [name])
            emulationIdArray = c.fetchone()
        
            if emulationIdArray:
                emulationID = emulationIdArray[0]
            else:
                raise sqlite.Error("Emulation " + str(name) + " not found")
            
            c.execute("SELECT startTime, stopTime, emulationID FROM emulationLifetime WHERE emulationID=?", [emulationID])

        dbconn().commit()                
        emulationLifetimeFetch = c.fetchall()
        
        if emulationLifetimeFetch:
            for row in emulationLifetimeFetch:
                runsTotal = 0
                runsExecuted = 0
                failedRunsInfo = []
                    
                startTimeDBsec = timestamp(timeConv(row[0]))
                stopTimeDBsec = startTimeDBsec + float(row[1])

                c.execute('SELECT emulationID,emulationName FROM emulation WHERE emulationID=?', [str(row[2])])
                emunameFetch = c.fetchall()
                
                # getting number of executed runs 
                c.execute('SELECT distributionID,distributionName FROM distribution WHERE emulationID=?', [str(row[2])])
                distroFetch = c.fetchall()
                for distro in distroFetch:
                    c.execute('SELECT runNo,stressValue,executed,message FROM runLog WHERE distributionID=?', [str(distro[0])])
                    runLogFetch = c.fetchall()
                    for run in runLogFetch:
                        runsTotal = runsTotal + 1
                        if run[2] == "False":
                            failedRunsInfo.append({"distributionID":distro[0], "distributionName":distro[1], "runNo":run[0], "stressValue":run[1], "message":run[3]})
                        
                        if run[2] == "True":
                            runsExecuted = runsExecuted + 1
                            
                stateStr = ""
                if startTimeDBsec < dtNowSec:
                    if stopTimeDBsec > dtNowSec:
                        stateStr = "Running"
                    else:
                        if failedRunsInfo != []:
                            stateStr = "Failed run(s)"
                        else:
                            if runsTotal != runsExecuted:
                                stateStr = "Unexecuted run(s)"
                            else:
                                stateStr = "Executed"
                else:
                    stateStr = "Pending Execution"
                for items in emunameFetch:
                    activeEmu.append({"ID":items[0], "Name":items[1], "State":stateStr, "runsTotal":runsTotal, "runsExecuted":runsExecuted, "failedRunsInfo":failedRunsInfo})
        
        c.close()
        # [{'State': 'active', 'ID': 11, 'Name': u'myMixEmu'}, {'State': 'active', 'ID': 12, 'Name': u'myMixEmu'}]
        return activeEmu
   
    except sqlite.Error, e:
        print "dateOverlapCheck() SQL Error %s:" % e.args[0]
        print e
        return "<error>str(e)</error>"
        sys.exit(1)


def daemonCheck():
    '''
    Checking if Scheduler Daemon(bin/Scheduler.py is running. Returning "1" if true and "0" if not.
    '''
    
    
    
    try:
        daemon = getDaemon()
        daemon.hello()
        return(1)
    
    except  Pyro4.errors.CommunicationError, e:
        
        print e

        print "\n---Unable to find Scheduler on remote IP.---"
        return False

def getDaemon():

    uri = "PYRO:scheduler.daemon@" + str(readIfaceIP("schedinterface")) + ":" + str(readLogLevel("schedport"))
    # perhaps needs to be setup somewhere else

    
    daemon = Pyro4.Proxy(uri)
    
    return daemon


def listEmulators(name):
    
    emulatorList = []
    if name.lower() == "all":
        path = HOMEPATH + "/emulators/"  # root folder of project
            
        dirList = os.listdir(path)
        for fname in dirList:
            if fname.startswith("run_") and fname.endswith(".py"):
                 distName = str(fname[4:-3])
                 emulatorList.append(distName)
        
        return emulatorList
    
    else:
        
        EmuhelpMod = loadEmulatorHelp(name)
        return EmuhelpMod()   
    
def listDistributions(name):
    
    distroList = []
    if name.lower() == "all":
        path = HOMEPATH + "/distributions/"  # root folder of project
            
        dirList = os.listdir(path)
        for fname in dirList:
            if fname.startswith("dist_") and fname.endswith(".py"):
                distName = str(fname[5:-3])
                distroList.append(distName)
        
        return distroList 
    else:
        loadMod = loadDistributionHelp(name)
        return loadMod()
    
def timeConv(dbtimestamp):
        # print "this is timeConv!!!"
        Year = int(dbtimestamp[0:4])
        Month = int(dbtimestamp[4 + 1:7])
        Day = int(dbtimestamp[7 + 1:10])
        Hour = int(dbtimestamp[11:13])
        Min = int(dbtimestamp[14:16])
        Sec = int(dbtimestamp[17:19])
        # convert date from DB to python date
        
        try:
            pytime = dt(Year, Month, Day, Hour, Min, Sec)
            return pytime
        
        except ValueError:
            print "Date incorrect use YYYY-MM-DDTHH:MM:SS format"
            sys.exit(0) 

# convert date to seconds
def timestamp(date):
    gmtTime = (date - dt(1970, 1, 1)).total_seconds()
    return gmtTime

'''
###############################
Emulator ARG module load
##############################
'''


def loadEmulatorHelp(modName):
    '''
    We are Loading module by file name. File name will be determined by emulator type (i.e. stressapptest)
    '''
    modfile = HOMEPATH + "/emulators/run_" + modName + ".py"
    modname = "run_" + modName
    modhandle = imp.load_source(modname, modfile)
        
    return modhandle.emulatorHelp


def loadEmulatorArgNames(modName):
    '''
    We are Loading module by file name. File name will be determined by emulator type (i.e. stressapptest)
    '''

    modfile = HOMEPATH + "/emulators/run_" + modName + ".py"
    modname = "run_" + modName
    modhandle = imp.load_source(modname, modfile)
    
    absEmu = imp.load_source("abstract_emu.py", HOMEPATH + "/emulators/abstract_emu.py")
    if (issubclass(modhandle.__class__, absEmu.__class__)):
        return modhandle.emulatorArgNames
    else:
        return str("ERROR: " + modName + " must inherit from abstract_emu")



'''
###############################
Handling Distribution module load
##############################
'''

def loadDistributionHelp(modName):
            '''
            We are Loading module by file name for Help content. File name will be determined by distribution type (i.e. linear)
            '''

            modfile = HOMEPATH + "/distributions/dist_" + modName + ".py"
            modname = "dist_" + modName
            modhandle = imp.load_source(modname, modfile)
            
            return modhandle.distHelp   
        
def loadDistributionArgNames(modName):
            '''
            We are Loading module by file name for Help content. File name will be determined by distribution type (i.e. linear)
            '''

            modfile = HOMEPATH + "/distributions/dist_" + modName + ".py"
            modname = "dist_" + modName
            modhandle = imp.load_source(modname, modfile)
            return modhandle.argNames  


def loadDistribution(modName):
            '''
            We are Loading module by file name. File name will be determined by distribution type (i.e. linear)
            '''
            modfile = HOMEPATH + "/distributions/dist_" + modName + ".py"
            modname = "dist_" + modName
            modhandle = imp.load_source(modname, modfile)
            
            #Checks if the loaded class inherits abstract_dist
            absDist = imp.load_source("abstract_dist.py", HOMEPATH + "/distributions/abstract_dist.py")
            if (issubclass(modhandle.__class__, absDist.__class__)):
                return modhandle.functionCount
            else:
                print "ERROR: " + modName + " must inherit from abstract_dist"
                return str("ERROR: " + modName + " must inherit from abstract_dist")


def listTests(name):
    
    testsList = []
    # print "This is listTests\n"
    if name.lower() == "all":

        path = HOMEPATH + "/tests/"  # root folder of project

            
        dirList = os.listdir(path)
        for fname in dirList:
            if fname.endswith(".xml") or fname.endswith(".XML"):
                distName = str(fname)  # str(fname[0:-4])
                testsList.append(distName)
        
        return testsList 
    else:
        print "Display XML content"

def checkPid(PROCNAME):        
    # ps ax | grep -v grep | grep Scheduler.py
    # print "ps ax | grep -v grep | grep "+str(PROCNAME)
    procTrace = subprocess.Popen("ps ax | grep -v grep | grep " + "\"" + str(PROCNAME) + "\"", shell = True, stdout = PIPE).communicate()[0]
    # print "procTrace: ",procTrace
    if procTrace:
        pid = procTrace[0:5]
        # program running
        return pid
    else:
        # program not running
        return False

def loggerSet(loggerName, filename = None):
    
    LOG_LEVEL = logging.INFO
    
    LogLevel = readLogLevel("coreloglevel")
    if LogLevel == "info":
        LOG_LEVEL = logging.INFO
    if LogLevel == "debug":
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    
    initLogger = logToFile(loggerName, LOG_LEVEL, filename)
    return initLogger

def writeInterfaceData(iface, column):
    '''
    Writes name of the interface into dedicated column in database
    '''
    try:
        db = dbconn()
        c = db.cursor()
        sqlStatement = "UPDATE config SET " + str(column) + "='" + str(iface) + "'"
        c.execute(sqlStatement)
        db.commit()
        c.close()
        return True
    except sqlite.Error, e:
        print "Error writing config to database %s:" % e.args[0]
        print e
        return False


def logToFile(elementName, level, filename = None):
    # file writing handler
    fileLogger = logging.getLogger(elementName)
    fileLogger.setLevel(level)
    
    # adding producer handler
#    bHandler = EMQproducer.BroadcastLogHandler(elementName, producer)
#    fileLogger.addHandler(bHandler)

    
    if filename == None:
        # setting log rotation for 10 files each up to 10000000 bytes (10MB)
        fileHandler = handlers.RotatingFileHandler(HOMEPATH + "/logs/COCOMAlogfile.csv", 'a', 10000000, 10)
        fileLoggerFormatter = logging.Formatter ('%(asctime)s;%(name)s;%(levelname)s;%(message)s', datefmt = '%m/%d/%Y %H:%M:%S')
        fileHandler.setFormatter(fileLoggerFormatter)
        fileLogger.addHandler(fileHandler)
        
        
        # cli writing handler
        # cliLoggerFormatter=logging.Formatter ('%(asctime)s - [%(name)s] - %(levelname)s : %(message)s',datefmt='%m/%d/%Y %H:%M:%S')
        # cliHandler = logging.StreamHandler()
        # cliHandler.setFormatter(cliLoggerFormatter)
        # fileLogger.addHandler(cliHandler)
    
    else:
        fileHandler = logging.FileHandler(HOMEPATH + "/logs/" + str(filename))
        
        fileLoggerFormatter = logging.Formatter ('%(asctime)s;%(name)s;%(levelname)s;%(message)s', datefmt = '%m/%d/%Y %H:%M:%S')
        fileHandler.setFormatter(fileLoggerFormatter)
        fileLogger.addHandler(fileHandler)
        
    return fileLogger 

def getifip(ifn):
    '''
    Provided network interface returns IP adress to bind on
    '''
    import socket, fcntl, struct
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(sck.fileno(), 0x8915, struct.pack('256s', ifn[:15]))[20:24])

def boundsCompare(xmlValue, LimitsDictValues, variableName = None):
    '''
    Comparing XML variables with emulator or distribution set bounds.
    NOTE: in future might be better moved to the wrapper modules
    '''
    
    if  variableName == "serverip" or variableName == "clientip" or variableName == "packettype":
        return_note = "\nOK"
        return xmlValue, return_note
    
    upperBound = int(LimitsDictValues["upperBound"])
    lowerBound = int(LimitsDictValues["lowerBound"])

    xmlValue = int(xmlValue)
    
    if xmlValue >= lowerBound:
        if xmlValue <= upperBound:
            return_note = "\nOK"
            return xmlValue, return_note
            
        else:
            return_note = "\nThe specified value " + str(xmlValue) + " was higher than the maximum limit " + str(upperBound) + " changing to the maximum limit"
            return upperBound , return_note 
    else:
        return_note = "\nThe specified value " + str(xmlValue) + " was lower than the minimum limit " + str(lowerBound) + " changing to the maximum limit"
        return lowerBound, return_note
            
def getTotalMem():  #Returns an integer value of the total physical memory
    return psutil.TOTAL_PHYMEM / (1024 ** 2)

def getMemUsed():
    return int(psutil.phymem_usage().used / (1024 ** 2))

def getResourceLimit(ResourceName):
    if ResourceName.upper() == "MEM":
        return getTotalMem()
    elif ResourceName.upper() == "CPU":
        return 100
    else:
        return 999999

def getCurrentJobs():
    currentJobs = []
    try:
        conn = dbconn()
        c = conn.cursor()
        c.execute('SELECT distributionID, runNo, message, runStartTime, runDuration, stressValue FROM runLog WHERE message="Currently executing"')
        runLogs = c.fetchall()
        for runLog in runLogs:
            c.execute("SELECT emulation.emulationName, distribution.distributionID, distribution.distributionName, EmulatorParameters.resourceType FROM emulation INNER JOIN distribution ON emulation.emulationID=distribution.emulationID INNER JOIN EmulatorParameters ON distribution.distributionID=EmulatorParameters.distributionID WHERE distribution.distributionID=?", [str(runLog[0])])
            currentRuns = c.fetchall()
            for currentRun in currentRuns:
                jobName = currentRun[0] + "-" + str(runLog[0]) + "-" + str(runLog[1]) + "-" + currentRun[2]
                startTime = float(runLog[3]) - 3600
                stopTime = startTime + float(runLog[4])
                jobInfo = "startTime: " + dt.fromtimestamp(startTime).strftime('%Y-%m-%d %H:%M:%S') + ", duration: " + runLog[4] + " sec, stopTime: " + dt.fromtimestamp(stopTime).strftime('%Y-%m-%d %H:%M:%S') + ", resourceType: " + currentRun[3].upper() + ", stressValue: " + runLog[5]
                job = "Job: " + jobName + " { " + jobInfo + " }"
                if not(job in currentJobs): currentJobs.append(job) #Add the job to the list , if it isn't already in the list
    except sqlite.Error, e:
        sys.exit(1)
    conn.commit()
    c.close()
    return currentJobs