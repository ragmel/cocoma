#!/usr/bin/env python
'''
Created on 6 Sep 2012

@author: i046533
'''


import sys, time, Pyro4, Scheduler

def distributionManager(emulationName,distributionType,resourceType,emulationType,startTime,stopTime, distributionGranularity,startLoad, stopLoad):
    print "Hello this is distributionManager"
    #starting manualy daemon
    #Scheduler.startSchedulerDaemon()
    uri ="PYRO:scheduler.daemon@localhost:51889"
    #daemon=Pyro4.config.HOST="localhost"
    daemon=Pyro4.Proxy(uri)
    daemon.hello()
    #daemon.checkPid()
    daemon.schedulerControl(emulationName,startTime, stopTime, distributionGranularity, startLoad, stopLoad) #schedulerControl(startTime,stopTime, distributionGranularity, startLoad, stopLoad)
    

if __name__ == "__main__":
    distributionManager("asdf","sadf","cpu","linear","2013-08-30T20:03:04","2013-08-30T20:10:03", 3,10, 90)