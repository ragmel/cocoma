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
You can control the behavior of backfuzz just passing command-line arguments. Here is a list of the most common arguments (default arguments in parentheses):

##################################################
# Back to the FUZZ'er - protocol fuzzing toolkit #
##################################################

Version: 0.3

Arguments (Normal Plugins):
===========================

-h   [IP] [Required] 
-p   [PORT] [Required] 
-min [START LENGHT] [Required] 
-max [END LENGHT] [Required] 
-s   [SALT BETWEEN FUZZ STRINGS] [Required] 
-pl  [PLUGIN TO USE] [Required] 
-pf  [PATTERN-FLAVOUR TO USE (default: Cyclic)] [Optional] 
-t   [TIMEOUT (Seconds) (default: 0.8)] [Optional] 

Arguments (Special Plugins):
============================

-SPECIAL [Required] 
-pl [SPECIAL PLUGIN TO USE] [Required] 
-min [START LENGHT] [Required] 
-max [END LENGHT] [Required] 
-s [SALT BETWEEN FUZZ STRINGS] [Required] 
-pf [PATTERN-FLAVOUR TO USE (default: Cyclic)] [Optional] 

Pattern Flavours are:
=====================

Cyclic :          Aa0Aa1Aa2Aa3Aa4Aa [...]
Cyclic Extended : Aa.Aa;Aa+Aa=Aa-Aa [...]
Single :          AAAAAAAAAAAAAAAAA [...]
FormatString :    %n%x%n%x%s%x%s%n  [...]

Available plugins:
==================

FTP  : FTP Fuzzer  | Fuzz an FTP server  | Author: localh0t
HTTP : HTTP Fuzzer | Fuzz an HTTP server | Author: localh0t
IMAP : IMAP Fuzzer | Fuzz an IMAP server | Author: localh0t
IRC  : IRC Fuzzer  | Fuzz an IRC server  | Author: localh0t
POP3 : POP3 Fuzzer | Fuzz an POP3 server | Author: localh0t
SMTP : SMTP Fuzzer | Fuzz an SMTP server | Author: localh0t
SSH  : SSH Fuzzer  | Fuzz an SSH server  | Author: localh0t
TCP  : TCP Fuzzer  | Send garbage to a TCP connection  | Author: localh0t
TFTP : TFTP Fuzzer | Fuzz an TFTP Server  | Author: localh0t
TNET : Telnet Fuzzer | Fuzz a Telnet server | Author: localh0t
UDP  : UDP Fuzzer  | Send garbage to a UDP connection  | Author: localh0t

Special plugins:
================

FILE : File Fuzzer | Generate multiple files with payload | Author: localh0t

[!] Exiting help ...


'''
import math,time,multiprocessing
import Pyro4,imp,time,sys,os,psutil
import Library
import sqlite3 as sqlite
import datetime as dt
import subprocess
from signal import *
from subprocess import *
import random

from Library import getHomepath, readBackfuzzPath


#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'
Pyro4.config.SERIALIZER='pickle'

try:
#    HOMEPATH= os.environ['COCOMA']
    HOMEPATH = getHomepath()
except:
    print "no $COCOMA environmental variable set"

sys.path.insert(0, getHomepath() + '/emulators/') #Adds dir to PYTHONPATH, needed to import abstract_emu
from abstract_emu import *

global BACKFUZZ_PATH
BACKFUZZ_PATH = readBackfuzzPath()

class emulatorMod(abstract_emu):


    def __init__(self,emulationID,distributionID,emulationLifetimeID,resourceTypeDist,duration,emulatorArg, stressValues,runNo,emuDuration):
        
        if not (os.path.isfile(Library.readBackfuzzPath())):
            print "Backfuzz_path is incorrect. Use 'ccmsh -b' to set it"
            sys.exit(0)
        
        if resourceTypeDist.lower() == "net":
            netFuzzProc = multiprocessing.Process(target = fuzzLoad, args=(emulationID, distributionID, runNo, emulatorArg["min"],emulatorArg["fuzzrange"], emulatorArg["serverip"], emulatorArg["serverport"], emulatorArg["packettype"], emulatorArg["salt"], emulatorArg["timedelay"]))
            netFuzzProc.start()
            
            wrtiePIDtable (netFuzzProc.pid, "Scheduler") #Stops event based scheduling once EMU time expires
            
            print(netFuzzProc.is_alive())
            netFuzzProc.join()


def fuzzLoad(emulationID, distributionID, runNo, min, fuzzRange, serverip, serverport, packettype, salt, timedelay):
    runBackfuzzPidNo=0

    if timedelay == "0":
        timedelay = "0.8"

    try:
        print "python", BACKFUZZ_PATH, "-h", str(serverip), "-p", str(serverport), "-min", str(min), "-max", str(int(min) + int(fuzzRange)), "-s ", str(salt), "-pl", str(packettype).upper(), "-t", str(timedelay)

        runBackfuzz = subprocess.Popen(["python",BACKFUZZ_PATH, "-h", str(serverip), "-p", str(serverport), "-min", str(min), "-max", str(int(min) + int(fuzzRange)), "-s", str(salt), "-pl", str(packettype).upper(), "-t", str(timedelay), "&&"], cwd= BACKFUZZ_PATH[:-11], stdin=subprocess.PIPE)#,stdout=subprocess.PIPE)
        runBackfuzz.stdin.flush()
        runBackfuzz.stdin.write("\r\n")
        runBackfuzzPidNo =runBackfuzz.pid

        if zombieBuster(runBackfuzzPidNo, "backfuzz"):
            print "Job failed, sending wait()."
            runBackfuzz.wait()
            message="Error in the emulator execution"
            executed="False"
            dbWriter(distributionID,runNo,message,executed)
            return False
        else:
            print "Success! waiting on process to finish running"
            runBackfuzz.wait()
            
            print "Process finished, writing into DB"
            message="Success"
            executed="True"
            dbWriter(distributionID,runNo,message,executed)
            
            print "Process stopped, trying to schedule next job"
            try:
                import Library,DistributionManager 
            
                daemon=Library.getDaemon()
                newEmulation=daemon.getEmuObject(emulationID)
                DistributionManager.createDistributionRuns(newEmulation)
            except Exception,e:
                print "Emulation object error: ",e
            
            return True

    except Exception, e:
        return "run_backfuzzer job exception: ", e

    #catching failed runs
    try:
        if zombieBuster(runBackfuzzPidNo, "backfuzz"):
            runBackfuzz.wait()
            message="Fail"
            executed="False"
        else:
            message="Success"
            executed="True"
    except Exception, e:
        print "No failed runs to catch"
    dbWriter(distributionID,runNo,message,executed)

def emulatorHelp():

    return """
    Emulator "backfuzz" can be used to generate network workload for victims running services


    XML Block Example: 
    <emulator-params>
        <resourceType>NET</resourceType>
        <serverip>10.55.164.223</serverip>
        <serverport>5001</serverport>      
        <packettype>HTTP</packettype>
        <salt>2</salt>

    </emulator-params>
    
    """

def emulatorArgNames(Rtype=None):
    '''
    Here we specify how many arguments emulator instance require to run properly
    type = <NET>

    IMPORTANT: All argument variable names must be in lower case

    '''
    if Rtype == None:
        argNames = ["net"]
        return argNames

    if Rtype.lower() == "net":

        argNames={"min":{"upperBound":100000000,"lowerBound":1, "argHelp":"Start Length of fuzz string to send"}, "fuzzRange":{"upperBound":100000000,"lowerBound":1, "argHelp":"Range for fuzzing to run. Adding this to the 'min' will give the max fuzz string length"}, "serverport":{"upperBound":10000,"lowerBound":0, "argHelp": "Server port to connect to"}, "serverip":{"upperBound":10000,"lowerBound":1, "argHelp": "Server IP to connect to"}, "packettype":{"upperBound":10000,"lowerBound":1, "argHelp":"Packet-Type to fuzz.\n Accepted: FTP, HTTP, IMAP, IRC, POP3, SMTP, SSH, TCP, TFTP, TNET, UDP (may not all work)"}, "timedelay":{"upperBound":100,"lowerBound":0, "argHelp": "Delay between fuzz strings being sent.\nUnits: s (default = 0.8)"}, "salt":{"upperBound":100000,"lowerBound":1, "argHelp": "Length to increase fuzz string by on each iteration"}}

        return argNames

if __name__ == '__main__':
    pass