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

import math
import Pyro4,imp,time,sys,os,psutil
import sqlite3 as sqlite
import datetime as dt
#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'


class emulatorMod(object):
    
    
    def __init__(self,emulationID,emulationLifetimeID,duration, stressValue,runNo):
        #emulationID,emulationLifetimeID,duration, stressValue,runNo
        self.emulationID = emulationID
        self.emulationLifetimeID = emulationLifetimeID
        self.duration = duration
        self.stressValue = stressValue
        self.runNo=runNo
        #self.HOMEPATH = HOMEPATH
        
        
        
        print "Hello this is run_stressapptest"
        os.system("killall cpulimit")
        os.system("killall stressapptest")
        print "cpulimit -e stressapptest -l "+stressValue
        os.system("cpulimit -b -e stressapptest -l "+stressValue )
        
        PROCNAME = "cpulimit"
        def pidFinder(PROCNAME):
            for proc in psutil.process_iter():
                if proc.name == PROCNAME:
                    p = proc.pid
                    print "cpulimit found on PID: ",p
                    return p
                
        p =pidFinder("cpulimit")
        print "this is our p:", p
                  
        
        print "stressapptest -H 10 -M 10 -s "+duration
        os.system("stressapptest -H 10 -M 10 -s "+duration)
        print "kill -9 "+str(p)
        os.system("kill -9 "+str(p))
        
def emulatorHelp():
    print "Stressapptest emulator How-To:"
    print "Module gets emulationID,emulationLifetimeID,duration, stressValue,runNo,HOMEPATH and loads system accordingly using \"cpulimit\" and \"stressapptest\""
    
    print "Have fun"
    