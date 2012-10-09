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

import os,sys
import sqlite3 as sqlite

try:
    HOMEPATH= os.environ['COCOMA']
except:
    print "no $COCOMA environmental variable set"
    
def createRun(emulationID,emulationLifetimeID,duration, stressValue,runNo):
    
        duration=str(duration)
        stressValue = str(stressValue)
        print duration
        print stressValue
                
        #for testing reasons commands are commented  and replaced with echo
        #os.system("cpulimit -e stressapptest -l "+stressValue+"&")
        os.system("echo cpulimit -e stressapptest -l "+stressValue+"&")
        print "cpu limit executed"
        #os.system("stressapptest -s "+duration)
        os.system("echo stressapptest -s "+duration)
        
        print"stressapp test executed"
        
        #Connect to DB and write info into runs table
        
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
        
           
if __name__ == '__main__':
    print "main"
    
    duration = 10
    stressValue = 50
    createRun(duration,stressValue)