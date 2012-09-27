#!/usr/bin/env python
'''
Created on 6 Sep 2012

@author: i046533
'''


import Pyro4

def distributionManager(emulationID,emulationLifetimeID,emulationName,distributionType,resourceType,emulationType,startTime,stopTime, distributionGranularity,startLoad, stopLoad):
    print "Hello this is distributionManager"
    uri ="PYRO:scheduler.daemon@localhost:51889"

    daemon=Pyro4.Proxy(uri)
    
    try:
        newEmulation=1
        print daemon.hello()
        print daemon.schedulerControl(emulationID,emulationLifetimeID,emulationName,startTime, stopTime, distributionGranularity,distributionType, startLoad, stopLoad,newEmulation) #schedulerControl(startTime,stopTime, distributionGranularity, startLoad, stopLoad)
    
    except  Pyro4.errors.CommunicationError, e:
                
        print e
        print "\n---Check if SchedulerDaemon is started. Connection error---"
        
        

if __name__ == "__main__":
    distributionManager("asdf","sadf","cpu","linear","2013-08-30T20:03:04","2013-08-30T20:10:03", 3,10, 90)