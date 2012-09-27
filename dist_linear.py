'''
Created on 25 Sep 2012

@author: i046533
'''
import math
import Pyro4,imp,time,sys
import sqlite3 as sqlite
import datetime as dt


class distributionMod(object):
    
    
    def __init__(self,arg1, arg2,emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity):
        
        self.startLoad = arg1
        self.stopLoad = arg2
        self.distributionGranularity = distributionGranularity
        self.distributionGranularity_count=distributionGranularity
        self.startTimesec = startTimesec
        self.duration = duration
        self.runNo=int(0)
        
                          
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
                daemon.createJob(emulationID,emulationName,emulationLifetimeID,duration,stressValue,runStartTime,str(self.runNo))
                
            except  Pyro4.errors.CommunicationError, e:
                print e
                print "\n---Check if SchedulerDaemon is started. Connection error cannot create jobs---"
            
            '''
            3. Updating Run log in DB. 
                        
            '''
            try:
                conn = sqlite.connect('cocoma.sqlite')
                c = conn.cursor()
                                   
                c.execute('INSERT INTO runLog (emulationLifetimeID,runNo,duration,stressValue) VALUES (?, ?, ?, ?)', [emulationLifetimeID,self.runNo,duration,stressValue])
                                        
                conn.commit()

            except sqlite.Error, e:
                print "Error %s:" % e.args[0]
                print e
                sys.exit(1)

            c.close()
            
            #increasing to next run            
            self.runNo=int(self.runNo)+1
            
        
            print "distributionGranularity_count:"
            self.distributionGranularity_count= int(self.distributionGranularity_count)-1
            print self.distributionGranularity_count
    

