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

import psutil,time,Library,logging,EMQproducer
from datetime import datetime as dt


from logging import handlers
from EMQproducer import Producer

global producer
producer = Producer()

global myName
myName = "Logger"

emulationEndLogger = None
   

def singleLogger(elementName,level=None,filename=None):
    #file writing handler
    producer=Producer()
    HOMEPATH= Library.getHomepath()
    global emulationEndLogger
    emulationEndLogger=Library.loggerSet("Logger")

    def logLevelGet():
        
        LOG_LEVEL=logging.INFO
        
        LogLevel=Library.readLogLevel("coreloglevel")
        if LogLevel=="info":
            LOG_LEVEL=logging.INFO
        if LogLevel=="debug":
            LOG_LEVEL=logging.DEBUG
        else:
            LOG_LEVEL=logging.INFO
        
        
        return LOG_LEVEL

    if level==None:
        level=logLevelGet()
    
    fileLogger=logging.getLogger(elementName)
    fileLogger.setLevel(level)
    #we do not add additional handlers if they are there
    if not len(fileLogger.handlers):
    
        #adding producer handler
        #bHandler= EMQproducer.BroadcastLogHandler(elementName,producer)
        #fileLogger.addHandler(bHandler)
        #EMQproducer.StreamAndBroadcastHandler("TEST",producer)
        
        if filename == None:
            #setting log rotation for 10 files each up to 10000000 bytes (10MB)
            fileHandler = handlers.RotatingFileHandler(HOMEPATH+"/logs/COCOMAlogfile.csv",'a', 10000000, 10)
            fileLoggerFormatter=logging.Formatter ('%(asctime)s;%(name)s;%(levelname)s;%(message)s',datefmt='%m/%d/%Y %H:%M:%S')
            fileHandler.setFormatter(fileLoggerFormatter)
            fileLogger.addHandler(fileHandler)
            
            
            #cli writing handler
            cliLoggerFormatter=logging.Formatter ('%(asctime)s - [%(name)s] - %(levelname)s : %(message)s',datefmt='%m/%d/%Y %H:%M:%S')
            cliHandler = logging.StreamHandler()
            cliHandler.setFormatter(cliLoggerFormatter)
            fileLogger.addHandler(cliHandler)
        
        else:
            fileHandler= logging.FileHandler(HOMEPATH+"/logs/"+str(filename))
            
            fileLoggerFormatter=logging.Formatter ('%(asctime)s;%(name)s;%(levelname)s;%(message)s',datefmt='%m/%d/%Y %H:%M:%S')
            fileHandler.setFormatter(fileLoggerFormatter)
            fileLogger.addHandler(fileHandler)
    
    
    return fileLogger 

    



#Logger job that collects system stats during emulation , run by scheduler


def emulationEnd(emulationName):
    """
    IN: job that executes at the end of emulation
    DOING: just producing logger notification
    OUT: nothing
    """
    try:
        print "Emulation Time expired, removing extra jobs and stopping running processes"
        global emulationEndLogger
        msg = {"Action":"Emulation finished","EmulationName":str(emulationName)}
        producer.sendmsg(myName,msg)
        emulationEndLogger.info(msg)
        #emulationEndLogger.info("Emulation '"+str(emulationName)+"' finished.")
        Library.removeExtraJobs(emulationName)
        Library.killRemainingProcesses()
        Library.deleteFiles("/tmp/stressapptestFile",  "*") # Remove any stressappTest files left behind from I/O loading
        return True
    except:
        return False




def loadMon(duration,interval,emulationID,emulationName,emuStartTime):
    
    HOMEPATH= Library.getHomepath()
    emulationName=str(emulationName)
    interval=int(interval)
    
    '''
    starting cpu monitoring in the loop
    '''
    iterationsNo=int(duration)/int(interval)
   
    try:
        f = open(HOMEPATH+"/logs/"+str(emulationID)+"-"+str(emulationName)+"-res"+"_"+str(emuStartTime)+".csv", 'a')    
        f.write(emulationName+";\nCountdown;Time;CPU(%);MEM(%);IOread(bytes);IOwrite(bytes);NET(bytes_sent)\n")
        #start time
        initTime=time.time()
        while iterationsNo !=0:
            CPU=str(psutil.cpu_percent(interval, False))
            #MEM=str(psutil.virtual_memory().percent)
            MEM=str(psutil.avail_virtmem())
            IOr=str(psutil.disk_io_counters().read_time)
            IOw=str(psutil.disk_io_counters().write_time)
            NET=str(psutil.network_io_counters(False).bytes_sent)

            #print (emulationName+";\nTime;CPU(%);MEM(%);IOread(bytes);IOwrite(bytes);NET(bytes_sent)\n"+str(time.time())+";"+CPU+";"+MEM+";"+IOr+";"+IOw+";"+NET)
            probeTime=time.time()-initTime
            timeStamp=dt.now()
            
            f.write(str(int(probeTime))+";"+str(timeStamp.strftime("%Y-%m-%d %H:%M:%S.%f"))+";"+CPU+";"+MEM+";"+IOr+";"+IOw+";"+NET+"\n")

            iterationsNo=iterationsNo-1
    except Exception,e:
        print "Unable to create log file\nError: ",e
   
    f.closed
   


if __name__ == '__main__':

    duration = 20
    interval = 1
    emulationName = "Emulation-1"
    loadMon(duration,interval,emulationName)
    

    pass
