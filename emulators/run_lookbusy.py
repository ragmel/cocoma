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
import signal

from Library import getHomepath

#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'
try:
#    HOMEPATH= os.environ['COCOMA']
    HOMEPATH = getHomepath()
except:
    print "no $COCOMA environmental variable set"

sys.path.insert(0, getHomepath() + '/emulators/') #Adds dir to PYTHONPATH, needed to import abstract_emu
from abstract_emu import *


class emulatorMod(abstract_emu):
    
    def __init__(self,emulationID,distributionID,emulationLifetimeID,resourceTypeDist,duration,emulatorArg, stressValues,runNo,emuDuration):
        self.emulationID = emulationID
        self.emulationLifetimeID = emulationLifetimeID
        self.duration = duration
        duration =float(duration)
        self.stressValues = stressValues
        self.runNo=runNo
        self.distributionID=distributionID
        if resourceTypeDist.lower() == "cpu":

            m = multiprocessing.Process(target = cpuLoad, args=(distributionID,runNo,stressValues,emulatorArg["ncpus"],duration))
            m.start()
            m.join()
        
        if resourceTypeDist.lower() == "mem":
            memMulti = multiprocessing.Process(target = memLoad, args=(distributionID,runNo,stressValues,emulatorArg["memsleep"],duration))
            memMulti.start()
            memMulti.join()
            
        if resourceTypeDist.lower() == "io":
            ioMulti = multiprocessing.Process(target = ioLoad, args=(self.distributionID,self.runNo,stressValues,emulatorArg["ioblocksize"],emulatorArg["iosleep"],duration))
            ioMulti.start()
            ioMulti.join()
    pass
        
def memLoad(distributionID,runNo,memUtil,memSleep,duration):
            runLookbusyPidNo=0
            try:
                if memSleep ==0 :
                    
                    runLookbusy = subprocess.Popen(["lookbusy","-c","0", "-m",str(memUtil)+"MB","&"])
                
                    runLookbusyPidNo =runLookbusy.pid
                    print "Started lookbusy on PID No: ",runLookbusyPidNo
                else:
                    runLookbusy = subprocess.Popen(["lookbusy", "-c","0","-m",str(memUtil)+"MB","-M",str(memSleep),"&"])
                    runLookbusyPidNo =runLookbusy.pid
                
            except Exception, e:
                return "run_lookbusy job memLoad exception: ", e
            
            time.sleep(float(duration))
            #catching failed runs
            if zombieBuster(runLookbusyPidNo, "lookbusy"):
                runLookbusy.wait()
                message="Fail"
                executed="False"
            else:
                os.kill(runLookbusy.pid, SIGINT)
            
                message="Success"
                executed="True"
                
            dbWriter(distributionID,runNo,message,executed)
                
def ioLoad(distributionID,runNo,ioUtil,ioBlockSize,ioSleep,duration):
            print "IO Executed"
            if ioSleep ==0 or ioSleep =="0":
                try:
                    runLookbusy = subprocess.Popen(["lookbusy", "-c","0", "-d",str(ioUtil)+"MB","-b",str(ioBlockSize)+"MB"])
                    runLookbusyPidNo =runLookbusy.pid
                    
                    print "Started lookbusy on PID No: ",runLookbusyPidNo
                    print "falling a sleep for: ",duration
                    
                    time.sleep(float(duration))
                    #catching failed runs
                    if zombieBuster(runLookbusyPidNo, "lookbusy"):
                        print "Job failed, sending wait()."
                        runLookbusy.wait()
                        message="Error in the emulator execution"
                        executed="False"
                        dbWriter(distributionID,runNo,message,executed)
                        return False
                    else:
                        runLookbusy.terminate()
                    
                        message="Success"
                        executed="True"
                        dbWriter(distributionID,runNo,message,executed)
                        return True
                        
                except Exception, e:
                    print "run_lookbusy job ioLoad exception: ", e

            else:
                try:
                    print "executing:", "lookbusy", "-c","0", "-d",str(ioUtil)+"MB","-b",str(ioBlockSize)+"MB","-D",ioSleep
                    runLookbusy = subprocess.Popen(["lookbusy", "-c","0", "-d",str(ioUtil)+"MB","-b",str(ioBlockSize)+"MB","-D",str(ioSleep)])
                    runLookbusyPidNo =runLookbusy.pid
                    
                    print "Started lookbusy on PID No: ",runLookbusyPidNo
                    #catching failed runs
                    if zombieBuster(runLookbusyPidNo, "lookbusy"):
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
    if str(ncpus) =="0" :
        try:
            runLookbusy = subprocess.Popen(["lookbusy", "-c",str(cpuUtil),"&"])
            runLookbusyPidNo =runLookbusy.pid
            
        except Exception,e:
            print "error in cpuload:",e
            
    else:
        runLookbusy = subprocess.Popen(["lookbusy", "-c",str(cpuUtil),"-n",str(ncpus),"&"])
        runLookbusy.stdout
        runLookbusyPidNo =runLookbusy.pid
    
    time.sleep(float(duration))
    if zombieBuster(runLookbusyPidNo, "lookbusy"):
        runLookbusy.wait()
           
        message="Error in the emulator execution"
        executed="False"
        dbWriter(distributionID,runNo,message,executed)
    else:
        runLookbusy.terminate()
        message="Success"
        executed="True"
        dbWriter(distributionID,runNo,message,executed)
        
def emulatorHelp():

    return """
    Emulator lookbusy can be used for following resources:
    1)Loads CPU with parameters:
      ncpus - Number of CPUs to keep busy (default: autodetected)
      
    2)Loads Memory(MEM) with parameters:
      memSleep - Time to sleep between iterations, in usec (default 1000)
      
    3)Changing size of files to use during IO with parameters:
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

def emulatorArgNames(Rtype=None):
    '''
    type = <MEM, CPU, IO>
    
    IMPORTANT: All argument variable names must be in lower case
    
    '''
    if Rtype == None:
        argNames = ["cpu","io","mem"]
        return argNames
        
    if Rtype.lower() == "cpu":
        
        argNames={"ncpus":{"upperBound":100,"lowerBound":0}}
        return argNames
    
    if Rtype.lower() == "mem":
        argNames={"memsleep":{"upperBound":999999999,"lowerBound":0}}
        return argNames
    
    if Rtype.lower() == "io":
        argNames={"ioblocksize":{"upperBound":9999999,"lowerBound":0},"iosleep":{"upperBound":999999999,"lowerBound":0}}
        return argNames


if __name__ == '__main__':
    try:
        filename = "xmldoc.xml"
        util ="50"
        ncpus ="b"
        m = multiprocessing.Process(target = cpuLoad, args=("50","0",10))
        m.start()
        m.join()
    except Exception, e:
        print "run_lookbusy job main exception: ", e
    
    pass
