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

Usage: iperf [-s|-c host] [options]
       iperf [-h|--help] [-v|--version]

Client/Server:
  -f, --format    [kmKM]   format to report: Kbits, Mbits, KBytes, MBytes
  -i, --interval  #        seconds between periodic bandwidth reports
  -l, --len       #[KM]    length of buffer to read or write (default 8 KB)
  -m, --print_mss          print TCP maximum segment size (MTU - TCP/IP header)
  -o, --output    <filename> output the report or error message to this specified file
  -p, --port      #        server port to listen on/connect to
  -u, --udp                use UDP rather than TCP
  -w, --window    #[KM]    TCP window size (socket buffer size)
  -B, --bind      <host>   bind to <host>, an interface or multicast address
  -C, --compatibility      for use with older versions does not sent extra msgs
  -M, --mss       #        set TCP maximum segment size (MTU - 40 bytes)
  -N, --nodelay            set TCP no delay, disabling Nagle's Algorithm
  -V, --IPv6Version        Set the domain to IPv6

Server specific:
  -s, --server             run in server mode
  -U, --single_udp         run in single threaded UDP mode
  -D, --daemon             run the server as a daemon

Client specific:
  -b, --bandwidth #[KM]    for UDP, bandwidth to send at in bits/sec
                           (default 1 Mbit/sec, implies -u)
  -c, --client    <host>   run in client mode, connecting to <host>
  -d, --dualtest           Do a bidirectional test simultaneously
  -n, --num       #[KM]    number of bytes to transmit (instead of -t)
  -r, --tradeoff           Do a bidirectional test individually
  -t, --time      #        time in seconds to transmit for (default 10 secs)
  -F, --fileinput <name>   input the data to be transmitted from a file
  -I, --stdin              input the data to be transmitted from stdin
  -L, --listenport #       port to receive bidirectional tests back on
  -P, --parallel  #        number of parallel client threads to run
  -T, --ttl       #        time-to-live, for multicast (default 1)
  -Z, --linux-congestion <algo>  set TCP congestion control algorithm (Linux only)

Miscellaneous:
  -x, --reportexclude [CDMSV]   exclude C(connection) D(data) M(multicast) S(settings) V(server) reports
  -y, --reportstyle C      report as a Comma-Separated Values
  -h, --help               print this message and quit
  -v, --version            print version information and quit

[KM] Indicates options that support a K or M suffix for kilo- or mega-

The TCP window size option can be set by the environment variable
TCP_WINDOW_SIZE. Most other options can be set by an environment variable
IPERF_<long option name>, such as IPERF_BANDWIDTH.


'''
import math,time,multiprocessing,logging
from xml.etree import ElementTree
from xml.dom import minidom
import xml.etree.ElementTree as ET
import Pyro4,imp,time,sys,os,psutil
import sqlite3 as sqlite
import datetime as dt
import subprocess
from signal import *
from subprocess import *

sys.path.insert(0,'/home/jordan/git/cocoma/bin/') #REMOVE
import Library #REMOVE
from Library import getHomepath

#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'
#Pyro4.config.SERIALIZER='pickle'
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
        
        #injecting server value
        try:
            print emulatorArg["server"]
        except:
            emulatorArg.update({"server":0})
            
  
 
        if resourceTypeDist.lower() == "net" and emulatorArg["server"]==0:
                netClientProc = multiprocessing.Process(target = netClientLoad, args=(distributionID,runNo,stressValues,emulatorArg["serverport"],emulatorArg["packettype"],emulatorArg["serverip"],emulationID,emulatorArg,emuDuration,duration))
                netClientProc.start()
                netClientProc.join()
                
        
        elif emulatorArg["server"]==1:
                netServerProc = multiprocessing.Process(target = netServerLoad, args=(distributionID,runNo,emulatorArg["serverport"],emulatorArg["packettype"],emuDuration))
                netServerProc.start()
                netServerProc.join()
                
  
def netClientLoad(distributionID,runNo,stressValues,serverPort,packettype,serverIP,emulationID,emulatorArg,emuDuration,duration):
            
            daemonPort=str(readLogLevel("schedport"))

            #check if the iperf server process already running
            PROCNAME = "iperf -s -p "+str(emulatorArg["serverport"])
            serverUri = "PYRO:scheduler.daemon@"+str(serverIP)+":"+daemonPort
            serverDaemon=Pyro4.Proxy(serverUri)

            fakeemulationLifetimeID="1"
            
            fakeemulatorArg = emulatorArg
            fakeemulatorArg.update({'server': 1})
            fakeresourceTypeDist ="net"
            fakestressValue = 1
            fakeRunNo = 1 #must not be zero
            emulator="iperf"
            

            serverJobStatus=serverDaemon.createCustomJob(emulationID,distributionID,fakeemulationLifetimeID,duration,emulator,fakeemulatorArg,fakeresourceTypeDist,fakestressValue,fakeRunNo,PROCNAME,emuDuration)
            if serverJobStatus == 1:
                print "!!!Server "+ "PYRO:scheduler.daemon@"+str(serverIP)+daemonPort +" job was created! for duration of Distribution"
                print "!!!Started server for "+str(emuDuration)+" sec"
            elif serverJobStatus == 2:
                print "!!!Server "+ "PYRO:scheduler.daemon@"+str(serverIP)+daemonPort +" job already running"
            elif serverJobStatus == 0:
                print "!!!Unable to start iperf server on: "+str(serverIP)+":"+str(serverPort)+"\n NET distribution(-s) Failed"
            
            if runNo == str(0):
                time.sleep(2)
            print "\n\nThis is netClientLoad:\ndistributionID,runNo,stressValues,serverPort,packettype,serverIP,emulationID,duration\n",distributionID,runNo,stressValues,serverPort,packettype,serverIP,emulationID,duration,"\n\n"
            bandwith =stressValues
            if packettype.lower() == "udp":
                
                try:
                    runIperf = subprocess.Popen(["iperf","-c",str(serverIP),"-p",str(serverPort),"-b",str(bandwith)+"mb","-t",str(duration)])
                    runIperfPidNo =runIperf.pid
                    
                    time.sleep(float(duration))
                    #catching failed runs
                    if zombieBuster(runIperfPidNo, "iperf"):
                        runIperf.wait()
                        message="Error in the emulator execution"
                        executed="False"
                        dbWriter(distributionID,runNo,message,executed)
                        return False
                    else:
                        runIperf.terminate()
                    
                        message="Success"
                        executed="True"
                        dbWriter(distributionID,runNo,message,executed)
                        return True
        
                except Exception, e:
                    print "run_Iperf job exception: ", e
            
            
            if packettype.lower() == "tcp":
                
                try:
                    runIperf = subprocess.Popen(["iperf","-c",str(serverIP),"-p",str(serverPort),"-n",str(bandwith)+"mb"])
                    runIperfPidNo =runIperf.pid
                    
                    time.sleep(float(duration))
                    #catching failed runs
                    if zombieBuster(runIperfPidNo, "iperf"):
                        print "Job failed, sending wait()."
                        runIperf.wait()
                        message="Error in the emulator execution"
                        executed="False"
                        dbWriter(distributionID,runNo,message,executed)
                        return False
                    else:
                        runIperf.terminate()
                    
                        message="Success"
                        executed="True"
                        dbWriter(distributionID,runNo,message,executed)
                        return True
        
                except Exception, e:
                    print "run_Iperf job exception: ", e
            
            

            else:
                try:
                    runIperf = subprocess.Popen(["iperf","-c",str(serverIP),"-p",str(serverPort),"-t",duration])
                    runIperfPidNo =runIperf.pid
                    
                    #catching failed runs
                    if zombieBuster(runIperfPidNo, "iperf"):
                        runIperf.wait()
                        message="Error in the emulator execution"
                        executed="False"
                        dbWriter(distributionID,runNo,message,executed)
                    else:
                        runIperf.terminate()
                    
                        message="Success"
                        executed="True"
                        dbWriter(distributionID,runNo,message,executed)
                    
                except Exception, e:
                    print "run_Iperf job exception: ", e

def netServerLoad(distributionID,runNo,netPort,packettype,emuDuration):
            
            runIperfPidNo=0
            try:
                if packettype.lower() =="udp" :
                    try:
                        runIperf = subprocess.Popen(["iperf","-s", "-p",str(netPort),"-u"])
                    except Exception, e:
                        print e
                
                    runIperfPidNo =runIperf.pid
                else:
                    runIperf = subprocess.Popen(["iperf","-s", "-p",str(netPort)])
                    runIperfPidNo =runIperf.pid
                
            except Exception, e:
                "run_runIperf job exception: ", e
            
            time.sleep(float(emuDuration)+5)
            #catching failed runs
            if zombieBuster(runIperfPidNo, "iperf"):
                runIperf.wait()
                message="Fail"
                executed="False"
            else:
                print "trying to kill process"
                runIperf.terminate()
                message="Success"
                executed="True"
                
            dbWriter(distributionID,runNo,message,executed)

def emulatorHelp():

    plainText= """
 Iperf emulator is used to generate workload over network between two COCOMA VM's - Client and Server. Emulation parameters (XML document) which include IP addresses 
of Client and Server COCOMA are sent to Client VM. Client VM then connects to Server VM starts Iperf in server mode ready to accept packages.
 Two types of packets can be selected within distribution UDP or TCP. In case of UDP packets we are changing bandwidth load in "mb". In case of TCP we vary size of the 
transmitted packet per run.

1) UDP setup example:   
<distributions>
     <name>NET_distro</name>
     <startTime>0</startTime>
     <!--duration in seconds -->
     <duration>10</duration>
     <granularity>1</granularity>
     <distribution href="/distributions/linear" name="linear" />
     <!--network bandwidth utilizationrange-->
     <startLoad>10</startLoad>
     <stopLoad>10</stopLoad>
     <emulator href="/emulators/iperf" name="iperf" />
      
    <emulator-params>
        <resourceType>NET</resourceType>
        <serverip>10.55.168.166</serverip>
        <!--Leave "0" for default 5001 port -->
        <serverport>0</serverport>
        <!--if TCP is needed just change "UDP" to "TCP"-->
        <packettype>UDP</packettype>
    </emulator-params>
  
  </distributions>
  """
    return plainText
    
'''
here we specify how many arguments emulator instance require to run properly
'''
def emulatorArgNames(Rtype=None):
    '''
    type = <NET>
    
    IMPORTANT: All argument variable names must be in lower case
    
    '''
    #discovery of supported resources
    if Rtype == None:
        argNames = ["net"]
        return argNames
    
    if Rtype.lower() == "net":
        
        argNames={"serverport":{"upperBound":10000,"lowerBound":0},"packettype":{"upperBound":"udp","lowerBound":"tcp"},"serverip":{"upperBound":10000,"lowerBound":1}}
        logging.debug( "Use Arg's: "+str(argNames))
        return argNames

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

if __name__ == '__main__':
    pass
