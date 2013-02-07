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
    
    
    def __init__(self,emulationID,distributionID,emulationLifetimeID,resourceTypeDist,duration,emulatorArg, stressValues,runNo,emuDuration):
        #emulationID,emulationLifetimeID,duration, stressValue,runNo
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
                print "Net selected"                                     #(distributionID,runNo,stressValues,clientPort,serverPort,udppackets,clientIp,serverIP,duration)
                netClientProc = multiprocessing.Process(target = netClientLoad, args=(distributionID,runNo,stressValues,emulatorArg["clientport"],emulatorArg["serverport"],emulatorArg["udppackets"],emulatorArg["clientip"],emulatorArg["serverip"],emulationID,emulatorArg,emuDuration,duration))
                netClientProc.start()
                print(netClientProc.is_alive())
                netClientProc.join()
                
        
        elif emulatorArg["server"]==1:
                print "Launching Server..."                                     #(distributionID,runNo,stressValues,clientPort,serverPort,udppackets,clientIp,serverIP,duration)
                netServerProc = multiprocessing.Process(target = netServerLoad, args=(distributionID,runNo,emulatorArg["serverport"],emulatorArg["udppackets"],emuDuration))
                netServerProc.start()
                print(netServerProc.is_alive())
                netServerProc.join()
            
        
def netServerLoad(distributionID,runNo,netPort,netUdppackets,emuDuration):
            
            
            runIperfPidNo=0
            try:
                print "\n\nthis is netServerLoad:\ndistributionID,runNo,netIp,netPort,netUdppackets,emuDuration\n",distributionID,runNo,netPort,netUdppackets,emuDuration,"\n\n"
                
                if netUdppackets ==1 :
                    try:
                        runIperf = subprocess.Popen(["iperf","-s","-u", "-p",str(netPort),"&"])
                    except Exception, e:
                        print e
                
                    runIperfPidNo =runIperf.pid
                    print "Started Iperf Server for UDP on PID No: ",runIperfPidNo
                else:
                    runIperf = subprocess.Popen(["iperf","-s", "-p",str(netPort),"&"])
                    runIperfPidNo =runIperf.pid
                    print "Started Iperf Server for TCP on PID No: ",runIperfPidNo
        
                
            except Exception, e:
                "run_runIperf job exception: ", e
            
            time.sleep(float(emuDuration))
            #catching failed runs
            if zombieBuster(runIperfPidNo):
                print "Job failed, sending wait()."
                runIperf.wait()
                print "writing fail into DB..."
                message="Fail"
                executed="False"
            else:
                runIperf.terminate()
            
                print "writing success into DB..."
                message="Success"
                executed="True"
                
            dbWriter(distributionID,runNo,message,executed)
                
  
def netClientLoad(distributionID,runNo,stressValues,clientPort,serverPort,udppackets,clientIp,serverIP,emulationID,emulatorArg,emuDuration,duration):
            
            #check if we need/can to schedule server to run
            if runNo == str(0):
                print "First run. Checking if can start the server..."
                serverUri = "PYRO:scheduler.daemon@"+str(serverIP)+":51889"   
                serverDaemon=Pyro4.Proxy(serverUri)
                
                
                fakeemulationLifetimeID=1
                
                fakeemulatorArg = emulatorArg
                fakeemulatorArg.update({'server': 1})
                fakeresourceTypeDist ="net"
                fakestressValue = 1
                fakeRunNo = 1 #must not be zero
                emulator="iperf"
                
                
                PROCNAME = "iperf -s"
                serverJobStatus=serverDaemon.createCustomJob(emulationID,distributionID,fakeemulationLifetimeID,duration,emulator,fakeemulatorArg,fakeresourceTypeDist,fakestressValue,fakeRunNo,PROCNAME,emuDuration)
                if serverJobStatus == 1:
                    print "Server "+ "PYRO:scheduler.daemon@"+str(serverIP)+":51889" +" job was created! for duration of Emulation"
                    print "Started server for "+str(emuDuration)+" sec"
                elif serverJobStatus == 2:
                    print "Server "+ "PYRO:scheduler.daemon@"+str(serverIP)+":51889" +" job already running"
                elif serverJobStatus == 0:
                    print "Unable to start iperf server on: "+str(serverIP)+":"+str(serverPort)+"\n NET distribution(-s) Failed"
    
            time.sleep(5)
            print "\n\nThis is netClientLoad:\ndistributionID,runNo,stressValues,clientPort,serverPort,udppackets,clientIp,serverIP,emulationID,duration\n",distributionID,runNo,stressValues,clientPort,serverPort,udppackets,clientIp,serverIP,emulationID,duration,"\n\n"
            bandwith =stressValues
            if udppackets ==1 and bandwith!=0:
                
                try:
                    runIperf = subprocess.Popen(["iperf","-c",str(serverIP),"-p",str(serverPort),"-b",str(bandwith)+"gb","-t",str(duration),"&"])
                    runIperfPidNo =runIperf.pid
                    
                    print "Started Iperf client on PID No: ",runIperfPidNo
                    print "falling a sleep for: ",duration
                    
                    time.sleep(duration)
                    #catching failed runs
                    if zombieBuster(runIperfPidNo):
                        print "Job failed, sending wait()."
                        runIperf.wait()
                        message="Error in the emulator execution"
                        executed="False"
                        dbWriter(distributionID,runNo,message,executed)
                        return False
                    else:
                        runIperf.terminate()
                    
                        print "writing success into DB..."
                        message="Success"
                        executed="True"
                        dbWriter(distributionID,runNo,message,executed)
                        return True
        
                except Exception, e:
                    print "run_Iperf job exception: ", e
            
            

            else:
                try:
                    runIperf = subprocess.Popen(["iperf","-c",str(serverIP),"-p",str(serverPort),"-t",duration,"&"])
                    runIperfPidNo =runIperf.pid
                    
                    print "Started Iperf on PID No: ",runIperfPidNo
                    #catching failed runs
                    if zombieBuster(runIperfPidNo):
                        print "Job failed, sending wait()."
                        runIperf.wait()
                        print "writing fail into DB..."
                        message="Error in the emulator execution"
                        executed="False"
                        dbWriter(distributionID,runNo,message,executed)
                    else:
                        runIperf.terminate()
                    
                        print "writing success into DB..."
                        message="Success"
                        executed="True"
                        dbWriter(distributionID,runNo,message,executed)
                    
                except Exception, e:
                    print "run_Iperf job exception: ", e
     

def emulatorHelp():

    return """
    Emulator "iperf" can be used for following resources:
 
<distributions> 
   <name>NET_distro</name>
     <startTime>0</startTime>
     <!--duration in seconds -->
     <duration>10</duration>
     <granularity>1</granularity>
     <distribution href="/distributions/linear" name="linear" />
    <!--cpu utilization distribution range-->
      <startLoad>10</startLoad>
      <stopLoad>10</stopLoad>
      <emulator href="/emulators/iperf" name="iperf" />
      
    <emulator-params>
        <resourceType>NET</resourceType>
        <serverip>10.55.168.166</serverip>
        <!--Leave "0" for default 5001 port -->
        <serverport>0</serverport>
        <clientip>10.55.168.167</clientip>
        <!--Leave "0" for default 5001 port -->
        <clientport>0</clientport>
        <udppackets>1</udppackets>
        <bandwith>0</bandwith>
    </emulator-params>
  
  </distributions>

    
    
    """
    
'''
here we specify how many arguments emulator instance require to run properly
'''
def emulatorArgNames(Rtype):
    '''
    type = <NET>
    
    IMPORTANT: All argument variable names must be in lower case
    
    '''
    if Rtype.lower() == "net":
        
        argNames={"serverport":{"upperBound":10000,"lowerBound":0},"clientport":{"upperBound":10000,"lowerBound":0},"udppackets":{"upperBound":1,"lowerBound":0},"serverip":{"upperBound":10000,"lowerBound":1},"clientip":{"upperBound":1,"lowerBound":0},"bandwith":{"upperBound":10000,"lowerBound":0}}
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


    