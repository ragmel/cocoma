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

Command line arguments
You can control the behavior of stressapptest just passing command-line arguments. Here is a list of the most common arguments (default arguments in parentheses):

General arguments

-M mbytes : megabytes of ram to test (auto-detect all memory available)
-s seconds : number of seconds to run (20)
-m threads : number of memory copy threads to run (auto-detect to number of CPUs)
-i threads : number of memory invert threads to run (0)
-C threads : number of memory CPU stress threads to run (0)
--paddr_base : allocate memory starting from this address (0, currently no support for none-0)
-W : Use more CPU-stressful memory copy (false)
-A : run in degraded mode on incompatible systems(off)
-p pagesize : size in bytes of memory chunks (1024LL*1024LL)
-n ipaddr : add a network thread connecting to system at 'ipaddr'. (none)
--listen : run a thread to listen for and respond to network threads. (0)

Error handling

-l logfile : log output to file 'logfile' (none)
--max_errors n : exit early after finding 'n' errors (off)
-v level : verbosity (0-20) (default: 8)
--no_errors : run without checking for errors. (off)
--force_errors : inject false errors to test error handling. (off)
--force_errors_like_crazy : inject a lot of false errors to test error handling. (off)
-F : don't result check each transaction. (false)
--stop_on_errors : Stop after finding the first error. (off)

Disk testing

-d device : add a direct write disk thread with block device (or file) 'device' (0)
--findfiles : find locations to do disk IO automatically (false)
-f filename : add a disk thread with tempfile 'filename' (none)
--filesize size : size of disk I/O tempfiles (8mb)
--read-block-size : size of block for reading (512)
--write-block-size : size of block for writing. (assume read-block-size if not defined)
--segment-size : size of segments to split disk into. (1)
--cache-size : size of disk cache. (16mb)
--blocks-per-segment : number of blocks to read/write per segment per iteration. (32)
--read-threshold : maximum time(in us) a block read should take. (100000 usec)
--write-threshold : maximum time(in us) a block write should take. (100000 usec)
--random-threads : number of random threads for each disk write thread. (0)
--destructive : write/wipe disk partition. (off)

Cache coherency test

--cc_test : do the cache coherency testing (off)
--cc_inc_count : number of times to increment the cacheline's member (1000)
--cc_line_count : number of cache line sized data structures to allocate for the cache coherency threads to operate (2)

Power spike control

--pause_delay : delay (in seconds) between power spikes (600)
--pause_duration : duration (in seconds) of each pause (15)

NUMA control

--local_numa : choose memory regions associated with each CPU to be tested by that CPU (off)
--remote_numa : choose memory regions not associated with each CPU to be tested by that CPU (off)

Example command lines
./stressapptest -s 20 -M 256 -m 8 -C 8 -W # Allocate 256MB of memory and run 8 "warm copy" threads, and 8 cpu load threads. Exit after 20 seconds.
./stressapptest -f /tmp/file1 -f /tmp/file2 # Run 2 file IO threads, and autodetect memory size and core count to select allocated memory and memory copy threads.


'''
import math,time,multiprocessing
import Pyro4,imp,time,sys,os,psutil
import sqlite3 as sqlite
import datetime as dt
import subprocess
from Library import deleteFiles
from signal import *
from subprocess import *
from collections import OrderedDict

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
        
        if resourceTypeDist.lower() == "mem":
            memMulti = multiprocessing.Process(target = memLoad, args=(distributionID,runNo,stressValues,emulatorArg["memthreads"],duration))
            memMulti.start()
            print(memMulti.is_alive())
            memMulti.join()

        if resourceTypeDist.lower() == "io":
            ioMulti = multiprocessing.Process(target = ioLoad, args=(emulationID, distributionID, runNo, stressValues, emulatorArg["memsize"], duration))
            ioMulti.start()
            print(ioMulti.is_alive())
            ioMulti.join()

def memLoad(distributionID,runNo,memSize,memThreads,duration):
    runStressapptestPidNo=0
            
    try:
        if int(memThreads) ==0 :
            cmd="stressapptest "+" -M "+str(memSize)+" -s "+str(duration)+"&"
            runStressapptest=os.system(cmd)
            runStressapptestPidNo =pidFinder("stressapptest")
            
            print "Started Stressapptest on PID No: ",runStressapptestPidNo
        else:
            cmd="stressapptest "+" -M "+str(memSize)+" -m "+str(memThreads)+" -s "+str(duration)+"&"
            runStressapptest=os.system(cmd)
            runStressapptestPidNo =pidFinder("stressapptest")
            
    except Exception, e:
        return "run_Stressapptest job memLoad exception: ", e
        
    #catching failed runs
    if zombieBuster(runStressapptestPidNo, "stressapptest"):
        runStressapptest.wait()
        message="Fail"
        executed="False"
    else:
        message="Success"
        executed="True"
    dbWriter(distributionID,runNo,message,executed)
    time.sleep(float(duration))            
           
def ioLoad(emulationID, distributionID,runNo,fileQty,memSize,duration):
    runStressapptestPidNo=0
            
    try:
        if int(fileQty) ==0:
            cmd="stressapptest "+" -m 0"+" -M "+str(memSize)+" -f /tmp/stressapptestFile"+emulationID + "_" + distributionID + "_" +runNo+" -s "+str(duration)+"&"
            runStressapptest=os.system(cmd)
            runStressapptestPidNo =pidFinder("stressapptest")
        
        elif int(fileQty) !=0:
            fileStr=""
            fileQty=int(fileQty)
    
            while fileQty !=0:
                fileStr = fileStr + " -m 0" + " -f /tmp/stressapptestFile" + str(emulationID) + "_" + str(distributionID) + "_" + str(runNo) + "-" + str(fileQty)
                fileQty =fileQty-1
            
            cmd="stressapptest "+" -M "+str(memSize)+" "+fileStr+" -s "+str(duration)+" --stop_on_errors&"
            runStressapptest=os.system(cmd)
            runStressapptestPidNo =pidFinder("stressapptest")

    except Exception, e:
        "run_Stressapptest job memLoad exception: ", e
        
    #catching failed runs
    if zombieBuster(runStressapptestPidNo, "stressapptest"):
        runStressapptest.wait()
        message="Fail"
        executed="False"
    else:
        message="Success"
        executed="True"
        
    dbWriter(distributionID,runNo,message,executed)
    #Sleep until the job is over, then delete the files stressappTest creates
    time.sleep(float(duration))
    deleteFiles("/tmp/stressapptestFile",  str(emulationID) + "_" + str(distributionID) + "_" + str(runNo) + "*")
        
def emulatorHelp():

    return """
    Emulator "stressapptest" can be used for following resources:
    
    Continuously writing into Memory(MEM) workload with parameters:
        memThreads - number of memory invert threads to run (default number of cpu's)
      

    XML block example:
    <emulator-params>
        <resourceType>MEM</resourceType>
        <memThreads>0</memThreads>
    </emulator-params>
    
    
    Continuously write files on disk(IO) using fixed amount of memory with parameters:
        memSize - Size of memory to use in Mb
        memThreads - number of memory invert threads to run (default number of cpu's)
        
    
    XML Block Example: 
    <emulator-params>
        <resourceType>IO</resourceType>
        <memSize>100</memSize>
    </emulator-params>
    
    """
    
'''
here we specify how many arguments emulator instance require to run properly
'''
def emulatorArgNames(Rtype=None):
    '''
    type = <MEM,IO>
    
    IMPORTANT: All argument variable names must be in lower case
    
    '''
    if Rtype == None:
        argNames = ["io","mem"]
        return argNames
    
    if Rtype.lower() == "mem":
        argNames=[("memthreads", {"upperBound":10,"lowerBound":0, "argHelp":"number of memory copy threads to run (auto-detect to number of CPUs)"})]
        return OrderedDict(argNames)
    
    if Rtype.lower() == "io":
        
        memReading=psutil.phymem_usage()
        allMemory =memReading.total/1048576

        argNames=[("memsize", {"upperBound":allMemory,"lowerBound":1, "argHelp":"megabytes of ram to test (auto-detect all memory available)"})]
        return OrderedDict(argNames)