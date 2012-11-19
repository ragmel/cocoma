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
import Pyro4,imp,time,sys
import sqlite3 as sqlite
import datetime as dt
#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'


class distributionMod(object):
    
    
    def __init__(self,emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,emulator,distributionArg,HOMEPATH):
        
        self.startLoad = distributionArg["startLoad"]
        self.stopLoad = distributionArg["stopLoad"]
        self.distributionGranularity = distributionGranularity
        self.distributionGranularity_count=distributionGranularity
        self.startTimesec = startTimesec
        self.duration = duration
        self.emulator = emulator
        self.runNo=int(0)
        
        print "Hello this is dist_parabola"
        
                          
        while(self.distributionGranularity_count>=0):
    
            print "Run No: "
            print self.runNo
            runStartTime=self.startTimesec+(duration*self.runNo)
            print "This run start time: "
            print runStartTime
            print "This is time passed to scheduler:"
            print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime))
        
            '''
            1. Distribution formula goes here
            '''
                            
            self.linearStep=((int(self.startLoad)-int(self.stopLoad))/int(self.distributionGranularity))
            self.linearStep=math.fabs((int(self.linearStep)))
            print "LINEAR STEP SHOULD BE THE SAME"
            print self.linearStep
            self.linearStress= ((self.linearStep*int(self.runNo)))+int(self.startLoad)
            #make sure we return integer
            self.linearStress=int(self.linearStress)
            print "LINEAR STRESS SHOULD CHANGE"
            print self.linearStress
            
            stressValue = self.linearStress
            print "This run stress Value: "
            print stressValue
            
            '''
            2. Formula ends and we start feeding runs to Scheduler
            '''
            
            
            uri ="PYRO:scheduler.daemon@localhost:51889"
    
            daemon=Pyro4.Proxy(uri)
            try:
                
                print daemon.hello()
                print daemon.createJob(emulationID,emulationName,emulationLifetimeID,duration,emulator,stressValue,runStartTime,str(self.runNo))
                
            except  Pyro4.errors.CommunicationError, e:
                print e
                print "\n---Check if SchedulerDaemon is started. Connection error cannot create jobs---"
            
            '''
            3. Updating Run log in DB. 
                        
            '''

                
            try:
                conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
                c = conn.cursor()
                print "Path:",HOMEPATH+'/data/cocoma.sqlite'
                print "insert to runlog"               
                c.execute('INSERT INTO runLog (emulationLifetimeID,runNo,duration,stressValue) VALUES (?, ?, ?, ?)', [emulationLifetimeID,self.runNo,duration,stressValue])
                                    
                conn.commit()
                c.close()
            except sqlite.Error, e:
                print "Error %s:" % e.args[0]
                print e
                sys.exit(1)

            #increasing to next run            
            self.runNo=int(self.runNo)+1
            
        
            print "distributionGranularity_count:"
            self.distributionGranularity_count= int(self.distributionGranularity_count)-1
            print self.distributionGranularity_count
        
def distHelp():
    print "Parabola Distribution How-To:"
    print "Enter arg0 for first point and arg1 for 2nd point"
    
    print "Have fun"
    return "Parabola Distribution How-To: Enter arg0 for first point and arg1 for 2nd point"
    
'''
here we specify how many arguments distribution instance require to run properly
'''
def argNames():
    
    argNames=["curve","bend","sphere"]
    print "Use Arg's: ",argNames
    return argNames

