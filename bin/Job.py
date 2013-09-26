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

import os,sys,subprocess,imp
import sqlite3 as sqlite
import threading,psutil, Library
from threading import Thread

    
def createRun(emulationID,distributionID,emulationLifetimeID,duration,emulator,emulatorArg,resourceTypeDist, stressValue,runNo,emuDuration):
        try:
            HOMEPATH= os.environ['COCOMA']
        except:
            print "no $COCOMA environmental variable set"
            
        dbWriter(distributionID,runNo,"Currently executing","Executing")
        
        duration=str(duration)
        stressValue = str(stressValue)
#        print duration
#        print stressValue
                
        
        
        '''
        ###############################
        Emulator module load
        ##############################
        '''
        def loadEmulator(modName):
            try:
                '''
                We are Loading module by file name. File name will be determined by emulator type (i.e. stressapptest)
                '''
                if HOMEPATH:
                    modfile = HOMEPATH+"/emulators/run_"+modName+".py"
                    modname = "run_"+modName
                else:
                    modfile = "./emulators/run_"+modName+".py"
                    modname = "run_"+modName
                
                modhandle = imp.load_source(modname, modfile)
                    
                return modhandle.emulatorMod
            except Exception, e:
                print "Run() exception: ", e

        #1. Get required module loaded
        modhandleMy=loadEmulator(str(emulator))
        #2. Use this module for executing the stress   
        newEmulatorSelect=modhandleMy(emulationID,distributionID,emulationLifetimeID,resourceTypeDist,duration,emulatorArg,stressValue,runNo,emuDuration)

def dbWriter (distributionID,runNo,message,executed):
    try:
        conn =Library.dbconn()
        c = conn.cursor()
        c.execute('UPDATE runLog SET executed=? ,message=? WHERE distributionID =? and runNo=?',(executed,message,distributionID,runNo))
        conn.commit()
    except sqlite.Error, e:
        c.close()
        conn.close()
        schedFileLogger.debug("Values: "+str(distributionID)+"-"+str(runNo)+"-"+str(message)+"-"+str(executed))
        schedFileLogger.error("Unable to connect to DB")
        schedFileLogger.exception(str(e))
        sys.exit(1)
    c.close()

if __name__ == '__main__':
    print "main"
    
    duration = 2
    stressValue = 50
    runNo=1
    emulationID = 1
    emulationLifetimeID =1
#    createRun(emulationID,emulationLifetimeID,duration, stressValue,runNo)
    
