#!/usr/bin/env python
'''
Created on 6 Sep 2012

@author: i046533
'''


import Pyro4,imp,time,sys
import sqlite3 as sqlite
import datetime as dt

    

def distributionManager(emulationID,emulationLifetimeID,emulationName,startTime,stopTime, distributionGranularity,distributionType,startLoad, stopLoad,newEmulation):   
            print "this is schedulerControl"
                        
            startTime= timeConv(startTime)
            stopTime = timeConv(stopTime)
            startTimesec=timestamp(startTime)
        
            #make sure it is integer
            distributionGranularity = int(distributionGranularity)
        
            #make copy for counting(qty can also be used)
            distributionGranularity_count = distributionGranularity
            
            
                
            duration = (timestamp(stopTime) - timestamp(startTime))/distributionGranularity
            duration = int(duration)
            print "Duration is seconds:"
            print duration
            
            '''
            1. Load the module according to Distribution Type to create runs
             '''
                                
            #1. Get required module loaded
            modhandleMy=loadDistribution(distributionType)
            #2. Use this module for calculation and run creation   
            newCreateRuns=modhandleMy(startLoad, stopLoad,emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity)
  
           
                                    
            uri ="PYRO:scheduler.daemon@localhost:51889"

            daemon=Pyro4.Proxy(uri)
            try:
            
                print daemon.hello()
                for job in daemon.listJobs():
                    print job

            except  Pyro4.errors.CommunicationError, e:
                print e
                print "\n---Check if SchedulerDaemon is started. Connection error cannot create jobs---"
                print "list of jobs:"
           

def loadDistribution(modName):
            '''
            We are Loading module by file name. File name will be determined by distribution type (i.e. linear)
            '''
            modfile = "dist_"+modName+".py"
            modname = "dist_"+modName
            modhandle = imp.load_source(modname, modfile)
            print modhandle
            
            fp, pathname, description = imp.find_module(modname)
            
            print fp, pathname, description
            try:
                modhandle = imp.load_module(modname, fp, pathname, description)
            finally:
                # Since we may exit via an exception, close fp explicitly.
                if fp:
                    fp.close()
                
            return modhandle.distributionMod   

def timeConv(dbtimestamp):
        print "this is timeConv!!!"
        Year = int(dbtimestamp[0:4])
        Month = int(dbtimestamp[4+1:7])
        Day = int(dbtimestamp[7+1:10])
        Hour =int(dbtimestamp[11:13])
        Min =int(dbtimestamp[14:16])
        Sec =int(dbtimestamp[17:19])
        #convert date from DB to python date
        
        try:
            pytime=dt.datetime(Year,Month,Day,Hour,Min,Sec)
            return pytime
        
        except ValueError:
            print "Date incorrect use YYYY-MM-DDTHH:MM:SS format"
            sys.exit(0) 
            
#convert date to seconds
def timestamp(date):
    print"This is timestamp"
    print date
    gmtTime = time.mktime(date.timetuple())+3600
    return gmtTime

if __name__ == "__main__":
    distributionManager("asdf","sadf","cpu","linear","2013-08-30T20:03:04","2013-08-30T20:10:03", 3,10, 90)