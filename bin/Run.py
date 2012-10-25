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

import os,sys,subprocess,imp
import sqlite3 as sqlite
import threading,psutil
from threading import Thread


    
def createRun(emulationID,emulationLifetimeID,duration, stressValue,runNo):
    
        try:
            HOMEPATH= os.environ['COCOMA']
        except:
            print "no $COCOMA environmental variable set"
               
        duration=str(duration)
        stressValue = str(stressValue)
        print duration
        print stressValue
                
        
        
        '''
        ###############################
        Emulator module load
        ##############################
        '''
        def loadEmulator(modName):
            '''
            We are Loading module by file name. File name will be determined by emulator type (i.e. stressapptest)
            '''
            if HOMEPATH:
                modfile = HOMEPATH+"/emulators/run_"+modName+".py"
                modname = "run_"+modName
            else:
                modfile = "./emulators/dist_"+modName+".py"
                modname = "run_"+modName
            
            modhandle = imp.load_source(modname, modfile)
                
            return modhandle.emulatorMod

        #1. Get required module loaded
        modhandleMy=loadEmulator("stressapptest")
        #2. Use this module for executing the stress   
        newEmulatorSelect=modhandleMy(emulationID,emulationLifetimeID,duration, stressValue,runNo)
           
            
        
        
        def cpulimitFunc():
            #print "cpulimit -e stress -l "+stressValue+" -z"
            #procLimit=subprocess.Popen("cpulimit -e stressapptest -l "+stressValue+" \"`jobs -p`\"&", shell=True)
            #procLimitPid= procLimit.pid
            #print "cpu limit executed on PID: ",procLimitPid
            
            #procStress=subprocess.Popen("stressapptest -H 10 -M 10 -s "+duration, shell=True)
            
            #cpulimit -l $LIMIT -e stressapptest "`jobs -p`"&

            #stressapptest -H $H -M $MEM -s $DURATION

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
            
            #find and destroy process
            

             
        
        
        
        #threading.Thread(target = stressFunc).start()
        #threading.Thread(target = cpulimitFunc).start()
        
         
        sys.exit(0)
        
        #Connect to DB and write info into runs table
        '''
        try:
            if HOMEPATH:
                conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
            else:
                conn = sqlite.connect('./data/cocoma.sqlite')
                
            c = conn.cursor()
            #check if this is the last run in batch and update emulation table
            if runNo == 0:
                c.execute('UPDATE emulation SET executed=? , active =? WHERE emulationID =?',["1","0",emulationID])
                c.execute('Update runLog SET executed=? WHERE emulationLifetimeID=? and runNo=?', ["1",emulationLifetimeID,runNo])
            conn.commit()
        
        except sqlite.Error, e:
            print "Error %s:" % e.args[0]
            print e
            sys.exit(1)
        
        c.close()
        '''
           
if __name__ == '__main__':
    print "main"
    
    duration = 2
    stressValue = 50
    runNo=1
    emulationID = 1
    emulationLifetimeID =1
    createRun(emulationID,emulationLifetimeID,duration, stressValue,runNo)
    