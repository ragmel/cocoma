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
        
        
        
        
        print "Hello this is run_stressapptest: emulationID,emulationLifetimeID,resourceTypeDist,duration, stressValues,runNo: ",emulationID,emulationLifetimeID,resourceTypeDist,duration, stressValues,runNo

        
        if resourceTypeDist.lower() == "mem":
            print "MEM load selected"
            memMulti = multiprocessing.Process(target = memLoad, args=(distributionID,runNo,stressValues,emulatorArg["memThreads"],duration))
            memMulti.start()
            print(memMulti.is_alive())
            memMulti.join()

        if resourceTypeDist.lower() == "io":
            print "IO load selected"
            ioMulti = multiprocessing.Process(target = ioLoad, args=(distributionID,runNo,stressValues,emulatorArg["fileQty"],duration))
            ioMulti.start()
            print(ioMulti.is_alive())
            ioMulti.join()


def pidFinder(PROCNAME):
        for proc in psutil.process_iter():
            if proc.name == PROCNAME:
                p = proc.pid
                print "Process found on PID: ",p
                return p
        
        
def memLoad(distributionID,runNo,memSize,memThreads,duration):
    runStressapptestPidNo=0
            
    try:
        print "\n\nthis is mem load:memSize,memThreads,duration",memSize,memThreads,duration,"\n\n"
        
        if int(memThreads) ==0 :
            cmd="stressapptest "+" -M "+str(memSize)+" -s "+str(duration)+"&"
            print cmd
            #runStressapptest = subprocess.Popen(["stressapptest", "-M",memSize,"-s",duration])
            
            runStressapptest=os.system(cmd)
            #runStressapptestPidNo =runStressapptest.pid
            
            runStressapptestPidNo =pidFinder("stressapptest")
            
            print "Started Stressapptest on PID No: ",runStressapptestPidNo
        else:
            cmd="stressapptest "+" -M "+str(memSize)+" -i "+str(memThreads)+" -s "+str(duration)+"&"
            
            print cmd
            
            #runStressapptest = subprocess.Popen(["stressapptest","-M",memSize,"-i",memThreads,"-s",duration])
            
            runStressapptest=os.system(cmd)
            
            #runStressapptestPidNo =runStressapptest.pid
            runStressapptestPidNo =pidFinder("stressapptest")
            
            print "Started Stressapptest on PID No: ",runStressapptestPidNo
    
            
    except Exception, e:
        "run_Stressapptest job memLoad exception: ", e
        
   
        
    #catching failed runs
    
    if zombieBuster(runStressapptestPidNo):
        print "Job failed, sending wait()."
        runStressapptest.wait()
        print "writing fail into DB..."
        message="Fail"
        executed="False"
    else:
        print "writing success into DB..."
        message="Success"
        executed="True"
        
    dbWriter(distributionID,runNo,message,executed)
    time.sleep(duration)            

def ioLoad(distributionID,runNo,memSize,fileQty,duration):
    runStressapptestPidNo=0
            
    try:
        print "\n\nthis is ioLoad load:memSize,fileQty,duration",memSize,fileQty,duration,"\n\n"
        
        if int(fileQty) ==0 :
            cmd="stressapptest "+" -M "+str(memSize)+" -f /tmp/stressapptestFile1"+" -s "+str(duration)+" --stop_on_errors&"
            print cmd
            #runStressapptest = subprocess.Popen(["stressapptest", "-M",memSize,"-s",duration])
            
            runStressapptest=os.system(cmd)
            #runStressapptestPidNo =runStressapptest.pid
            
            runStressapptestPidNo =pidFinder("stressapptest")
            
            print "Started Stressapptest on PID No: ",runStressapptestPidNo
        else:
            #print"MULTIPLE FILES NOT WORKING! SELECT ZERO"
            fileStr=""
            
            fileQty=int(fileQty)
            #fileStr=fileStr+" -f /tmp/stressapptestFile"+str(fileQty)
            print "fileStr: ",fileStr
            
            while fileQty !=0:
                fileStr=fileStr+" -f /tmp/stressapptestFile"+str(fileQty)
                fileQty =fileQty-1
                
            
            cmd="stressapptest "+" -M "+str(memSize)+" "+fileStr+" -s "+str(duration)+" --stop_on_errors&"
            #stressapptest -M 100 -f /tmp/stressapptestFile1 -f /tmp/stressapptestFile2 -s 240
            print "The command we execute: ",cmd
            
            #runStressapptest = subprocess.Popen(["stressapptest","-M",memSize,"-i",memThreads,"-s",duration])
            
            runStressapptest=os.system(cmd)
            
            #runStressapptestPidNo =runStressapptest.pid
            runStressapptestPidNo =pidFinder("stressapptest")
            
            print "Started Stressapptest on PID No: ",runStressapptestPidNo
            
            
    except Exception, e:
        "run_Stressapptest job memLoad exception: ", e
        
   
        
    #catching failed runs
    
    if zombieBuster(runStressapptestPidNo):
        print "Job failed, sending wait()."
        runStressapptest.wait()
        print "writing fail into DB..."
        message="Fail"
        executed="False"
    else:
        print "writing success into DB..."
        message="Success"
        executed="True"
        
    dbWriter(distributionID,runNo,message,executed)
    time.sleep(duration)            
    
        
def emulatorHelp():

    return """
    Emulator "stressapptest" can be used for following resources:
    
    Memory(MEM) with parameters:
        memThreads - number of memory invert threads to run (default number of cpu's)
      

    XML block example:
    <emulator-params>
        <resourceType>MEM</resourceType>
        <memThreads>0</memThreads>
    </emulator-params>
    
    
    Input Output(IO) with parameters:
        fileQty - number of files to write simultaneously( default is one file)
    
    XML Block Example: 
    <emulator-params>
        <resourceType>IO</resourceType>
        <fileQty>3</fileQty>
    </emulator-params>
    
    """
    
'''
here we specify how many arguments emulator instance require to run properly
'''
def emulatorArgNames(Rtype):
    '''
    type = <MEM,IO>
    
    '''
    
    if Rtype.lower() == "mem":
        argNames=["memThreads"]
        print "Use Arg's: ",argNames
        return argNames
    
    if Rtype.lower() == "io":
        argNames=["fileQty"]
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

    
    
    
    
    pass


    