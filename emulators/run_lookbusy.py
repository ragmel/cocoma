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
'''

usage: lookbusy [ -h ] [ options ]
General options:
  -h, --help           Commandline help (you're reading it)
  -v, --verbose        Verbose output (may be repeated)
  -q, --quiet          Be quiet, produce output on errors only
CPU usage options:
  -c, --cpu-util=PCT,  Desired utilization of each CPU, in percent (default
      --cpu-util=RANGE   50%).  If 'curve' CPU usage mode is chosen, a range
                         of the form MIN-MAX should be given.
  -n, --ncpus=NUM      Number of CPUs to keep busy (default: autodetected)
  -r, --cpu-mode=MODE  Utilization mode ('fixed' or 'curve', see lookbusy(1))
  -p, --cpu-curve-peak=TIME
                       Offset of peak utilization within curve period, in
                         seconds (append 'm', 'h', 'd' for other units)
  -P, --cpu-curve-period=TIME
                       Duration of utilization curve period, in seconds (append
               'm', 'h', 'd' for other units)
Memory usage options:
  -m, --mem-util=SIZE   Amount of memory to use (in bytes, followed by KB, MB,
                         or GB for other units; see lookbusy(1))
  -M, --mem-sleep=TIME Time to sleep between iterations, in usec (default 1000)
Disk usage options:
  -d, --disk-util=SIZE Size of files to use for disk churn (in bytes,
                         followed by KB, MB, GB or TB for other units)
  -b, --disk-block-size=SIZE
                       Size of blocks to use for I/O (in bytes, followed
                         by KB, MB or GB)
  -D, --disk-sleep=TIME
                       Time to sleep between iterations, in msec (default 100)
  -f, --disk-path=PATH Path to a file/directory to use as a buffer (default
                         /tmp); specify multiple times for additional paths


'''
import math,time,multiprocessing
import Pyro4,imp,time,sys,os,psutil
import sqlite3 as sqlite
import datetime as dt
import subprocess
from signal import *
from subprocess import *

#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'
try:
    HOMEPATH= os.environ['COCOMA']
except:
    print "no $COCOMA environmental variable set"    

class emulatorMod(object):
    
    
    def __init__(self,emulationID,distributionID,emulationLifetimeID,resourceTypeDist,duration,emulatorArg, stressValues,runNo):
        #emulationID,emulationLifetimeID,duration, stressValue,runNo
        self.emulationID = emulationID
        self.emulationLifetimeID = emulationLifetimeID
        self.duration = duration
        duration =float(duration)
        self.stressValues = stressValues
        self.runNo=runNo
        self.distributionID=distributionID
        
        
        
        
        print "Hello this is run_lookbusy: emulationID,emulationLifetimeID,resourceTypeDist,duration, stressValues,runNo: ",emulationID,emulationLifetimeID,resourceTypeDist,duration, stressValues,runNo
        
        if resourceTypeDist.lower() == "cpu":
            print "CPU load selected"
            #cpuLoad(stressValues,emulatorArg["ncpus"],duration)
            
            m = multiprocessing.Process(target = cpuLoad, args=(distributionID,runNo,stressValues,emulatorArg["ncpus"],duration))
            m.start()
            print(m.is_alive())
            m.join()
        
        if resourceTypeDist.lower() == "mem":
            print "MEM load selected"
            memMulti = multiprocessing.Process(target = memLoad, args=(distributionID,runNo,stressValues,emulatorArg["memSleep"],duration))
            memMulti.start()
            print(memMulti.is_alive())
            memMulti.join()
        
        if resourceTypeDist.lower() == "mem%":
            print "MEM load selected"
            memMulti = multiprocessing.Process(target = memLoad, args=(distributionID,runNo,stressValues,emulatorArg["memSleep"],duration))
            memMulti.start()
            print(memMulti.is_alive())
            memMulti.join()
            
            #memLoad(stressValues[0],stressValues[1],duration)
        
        if resourceTypeDist.lower() == "io":
            print "I/O load selected"
            print "vals"
            print stressValues,emulatorArg["ioBlockSize"],emulatorArg["ioSleep"],duration

            ioMulti = multiprocessing.Process(target = ioLoad, args=(self.distributionID,self.runNo,stressValues,emulatorArg["ioBlockSize"],emulatorArg["ioSleep"],duration))
            ioMulti.start()
            print(ioMulti.is_alive())
            ioMulti.join()
            
            
                


            #cpuLoad(stressValues[0],stressValues[1],stressValues[2],duration)
        
        
        
def memLoad(distributionID,runNo,memUtil,memSleep,duration):
            #memUtil,memSleep,duration= str(memUtil),str(memSleep),str(duration)
            runLookbusyPidNo=0
            try:
                print "\n\nthis is mem load:memUtil,memSleep,duration",memUtil,memSleep,duration,"\n\n"
                
                if memSleep ==0 :
                    
                    runLookbusy = subprocess.Popen(["lookbusy","-c","0", "-m",str(memUtil)+"MB","&"])
                
                    runLookbusyPidNo =runLookbusy.pid
                    print "Started lookbusy on PID No: ",runLookbusyPidNo
                else:
                    runLookbusy = subprocess.Popen(["lookbusy", "-c","0","-m",str(memUtil)+"MB","-M",str(memSleep),"&"])
                    runLookbusyPidNo =runLookbusy.pid
                    print "Started lookbusy on PID No: ",runLookbusyPidNo
        
                
            except Exception, e:
                "run_lookbusy job memLoad exception: ", e
            
            time.sleep(duration)
            #catching failed runs
            if zombieBuster(runLookbusyPidNo):
                print "Job failed, sending wait()."
                runLookbusy.wait()
                print "writing fail into DB..."
                message="Fail"
                executed="False"
            else:
                runLookbusy.terminate()
            
                print "writing success into DB..."
                message="Success"
                executed="True"
                
            dbWriter(distributionID,runNo,message,executed)
                
#stressValues,emulatorArg["ioBlockSize"],emulatorArg["ioSleep"],duration        
def ioLoad(distributionID,runNo,ioUtil,ioBlockSize,ioSleep,duration):
            #ioUtil,ioBlockSize,ioSleep,duration = str(ioUtil),str(ioBlockSize),str(ioSleep),str(duration)
        
            print "this is io load"

            if ioSleep ==0 or ioSleep =="0":
                try:
                    runLookbusy = subprocess.Popen(["lookbusy", "-c","0", "-d",str(ioUtil)+"MB","-b",str(ioBlockSize)+"MB"])
                    runLookbusyPidNo =runLookbusy.pid
                    
                    print "Started lookbusy on PID No: ",runLookbusyPidNo
                    print "falling a sleep for: ",duration
                    
                    
                    
                    time.sleep(duration)
                    #catching failed runs
                    if zombieBuster(runLookbusyPidNo):
                        print "Job failed, sending wait()."
                        runLookbusy.wait()
                        message="Error in the emulator execution"
                        executed="False"
                        dbWriter(distributionID,runNo,message,executed)
                        return False
                    else:
                        runLookbusy.terminate()
                    
                        print "writing success into DB..."
                        message="Success"
                        executed="True"
                        dbWriter(distributionID,runNo,message,executed)
                        return True
        
                    
                        
                        
                except Exception, e:
                    print "run_lookbusy job ioLoad exception: ", e

            else:
                try:
                    runLookbusy = subprocess.Popen(["lookbusy", "-c","0", "-d",str(ioUtil)+"MB","-b",str(ioBlockSize)+"MB","-D",ioSleep])
                    runLookbusyPidNo =runLookbusy.pid
                    
                    print "Started lookbusy on PID No: ",runLookbusyPidNo
                    #catching failed runs
                    if zombieBuster(runLookbusyPidNo):
                        print "Job failed, sending wait()."
                        runLookbusy.wait()
                        print "writing fail into DB..."
                        message="Error in the emulator execution"
                        executed="False"
                        dbWriter(distributionID,runNo,message,executed)
                    else:
                        runLookbusy.terminate()
                    
                        print "writing success into DB..."
                        message="Success"
                        executed="True"
                        dbWriter(distributionID,runNo,message,executed)
                    
                except Exception, e:
                    print "run_lookbusy job ioLoad exception: ", e


            

def cpuLoad(distributionID,runNo,cpuUtil,ncpus,duration):
    #cpuUtil,ncpus,duration = str(cpuUtil),str(ncpus),str(duration)
    print "\n\ncpuUtil,ncpus,duration",cpuUtil,ncpus,duration,"\n\n"

    if str(ncpus) =="0" :
        print "run_lookbusy executing this ncpus=", ncpus
        try:
            print "Running with these parameters: "+"lookbusy-c "+str(cpuUtil)
            runLookbusy = subprocess.Popen(["lookbusy", "-c",str(cpuUtil),"&"])
            print runLookbusy.stdout
            runLookbusyPidNo =runLookbusy.pid
            print "Started lookbusy on PID No: ",runLookbusyPidNo
            
            

        except Exception,e:
            print "error in cpuload:",e
            
    
        
    else:
        print "Running with these parameters: "+"lookbusy-c "+str(cpuUtil)+"-n "+str(ncpus)
        print "run_lookbusy executing this ncpus=", ncpus
        runLookbusy = subprocess.Popen(["lookbusy", "-c",str(cpuUtil),"-n",str(ncpus),"&"])
        runLookbusy.stdout
        runLookbusyPidNo =runLookbusy.pid
        print "Started lookbusy on PID No: ",runLookbusyPidNo

    
    print "sleep:", duration
    time.sleep(duration)
    #catching failed runs
    if zombieBuster(runLookbusyPidNo):
        print "Job failed, sending wait()."
        runLookbusy.wait()
        print "writing fail into DB..."
           
        message="Error in the emulator execution"
        executed="False"
        dbWriter(distributionID,runNo,message,executed)
    else:
        runLookbusy.terminate()
    
        print "writing success into DB..."
        message="Success"
        executed="True"
        dbWriter(distributionID,runNo,message,executed)
        

        
def emulatorHelp():

    return """
    Emulator "lookbusy" can be used for following resources:
    1)CPU with parameters:
      ncpus - Number of CPUs to keep busy (default: autodetected)
      
    2)Memory(MEM) with parameters:
      memSleep - Time to sleep between iterations, in usec (default 1000)
      
    3)IO with parameters:
      ioBlockSize - Size of blocks to use for I/O in MB
      ioSleep - Time to sleep between iterations, in msec (default 100)
    
    
    XML block example:
    <emulator-params>
        <resourceType>CPU</resourceType>
        <ncpus>0</ncpus>
    </emulator-params>
    
    """
    
'''
here we specify how many arguments emulator instance require to run properly
'''
def emulatorArgNames(Rtype):
    '''
    type = <MEM, CPU, IO>
    
    IMPORTANT: All argument variable names must be in lower case
    
    '''
    if Rtype.lower() == "cpu":
        
        argNames={"ncpus":{"upperBound":100,"lowerBound":0}}
        print "Use Arg's: ",argNames
        return argNames
    
    if Rtype.lower() == "mem":
        argNames={"memsleep":{"upperBound":999999999,"lowerBound":0}}
        print "Use Arg's: ",argNames
        return argNames
    
    if Rtype.lower() == "io":
        argNames={"ioblocksize":{"upperBound":9999999,"lowerBound":0},"iosleep":{"upperBound":999999999,"lowerBound":0}}
        print "Use Arg's: ",argNames
        return argNames


def dbWriter(distributionID,runNo,message,executed):
        #connecting to the DB and storing parameters
        try:
            if HOMEPATH:
                conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
            else:
                conn = sqlite.connect('./data/cocoma.sqlite')
                
            c = conn.cursor()
                    
            # 1. Populate "emulation"
            c.execute('UPDATE runLog SET executed=? ,message=? WHERE distributionID =? and runNo=?',(executed,message,distributionID,runNo))
            
            conn.commit()
            c.close()
        except sqlite.Error, e:
            print "Error %s:" % e.args[0]
            print e
            sys.exit(1)             


def zombieBuster(PID_ID):

    #catching failed runs
    p = psutil.Process(PID_ID)
    print "Process name: ",p.name,"\nProcess status: ",p.status
    if str(p.status) =="zombie":
        return True
    else:
        return False



if __name__ == '__main__':
    try:
        filename = "xmldoc.xml"
        util ="50"
        ncpus ="b"
        m = multiprocessing.Process(target = cpuLoad, args=("50","0",10))
        m.start()
        print(m.is_alive())
        m.join()
    except Exception, e:
        print "run_lookbusy job main exception: ", e
    #cpuLoad("50","0",10)
    
    
    
    
    pass


    