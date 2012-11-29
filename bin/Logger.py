#!/usr/bin/env python
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

import psutil,sys,os,time
from datetime import datetime




def loadMon(duration,interval,emulationName):
    try:
        HOMEPATH= os.environ['COCOMA']
    except:
        print "no $COCOMA environmental variable set"
    
    emulationName=str(emulationName)
    interval=int(interval)
    
    '''
    starting cpu monitoring in the loop
    '''
    iterationsNo=int(duration)/int(interval)
   
    try:
        f = open(HOMEPATH+'/logs/log_emuID'+str(emulationName)+"_"+str(datetime.now())+'.csv', 'a')    
        f.write(emulationName+";\nCountdown;Time;CPU(%);MEM(%);IOread(bytes);IOwrite(bytes);NET(bytes_sent)\n")
        #start time
        initTime=time.time()
        while iterationsNo !=0:
            CPU=str(psutil.cpu_percent(interval, False))
            MEM=str(psutil.virtual_memory().percent)
            IOr=str(psutil.disk_io_counters().read_time)
            IOw=str(psutil.disk_io_counters().write_time)
            NET=str(psutil.network_io_counters(False).bytes_sent)

            #print (emulationName+";\nTime;CPU(%);MEM(%);IOread(bytes);IOwrite(bytes);NET(bytes_sent)\n"+str(time.time())+";"+CPU+";"+MEM+";"+IOr+";"+IOw+";"+NET)
            probeTime=time.time()-initTime
            
            f.write(str(int(probeTime))+";"+str(time.time())+";"+CPU+";"+MEM+";"+IOr+";"+IOw+";"+NET+"\n")

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