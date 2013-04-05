#!/usr/bin/env python
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


import Pyro4,imp,time,sys,os,EmulationManager
import datetime as dt
import sqlite3 as sqlite

#perhaps needs to be set somewhere else
Pyro4.config.HMAC_KEY='pRivAt3Key'
distLoggerDM=None

try:
    HOMEPATH= os.environ['COCOMA']
except:
    print "no $COCOMA environmental variable set"    

def distributionManager(emulationID,emulationLifetimeID,emulationName,distributionName,startTime,startTimeDistro,duration,emulator, distributionGranularity,distributionType,resourceTypeDist,distributionArg,emulatorArg):   
        
        #emulation run log record initiation
        global distLoggerDM
        if distLoggerDM is None:
            distLoggerDM=EmulationManager.loggerSet("Distriburion Manager",str(emulationID)+"-"+str(emulationName)+"-syslog"+"_"+str(startTime)+".csv")

        #print "this is distributionManager"
            
        try:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
            c = conn.cursor()
                
            # 1. We populate "distribution" table      
            c.execute('INSERT INTO distribution (distributionGranularity, distributionType,emulator,distributionName,startTime,duration,emulationID) VALUES (?, ?, ?, ?,?, ?,?)', [distributionGranularity, distributionType, emulator,distributionName,startTimeDistro,duration,emulationID])
        
            distributionID=c.lastrowid
            '''
            {'startLoad': u'10', 'stopLoad': u'90'}
            '''
            #print "distributionArg:", distributionArg
            #print "emulatorArg:",emulatorArg
            
            #2. populate DistributionParameters, of table determined by distributionType name in our test it is "linearDistributionParameters"
            for d in distributionArg :
                c.execute('INSERT INTO DistributionParameters (paramName,value,distributionID) VALUES (?, ?, ?)',[d,distributionArg[d],distributionID])
            distributionParametersID=c.lastrowid
            
            
            c.execute('UPDATE distribution SET distributionParametersID=? WHERE distributionID =?',(distributionParametersID,distributionID))
            
            
            for emu in emulatorArg :
                c.execute('INSERT INTO EmulatorParameters (paramName,value,resourceType,distributionID) VALUES (?, ?, ?,?)',[emu,emulatorArg[emu],resourceTypeDist,distributionID])
            distributionParametersID=c.lastrowid
            
            conn.commit()
            c.close()
        except sqlite.Error, e:
            print "Error %s:" % e.args[0]
            print e
            sys.exit(1)                        
               
        startTime= timeConv(startTime)
        startTimesec=timestamp(startTime)+float(startTimeDistro)
        #print "startTime:",startTime
        
        #make sure it is integer
        distributionGranularity = int(distributionGranularity)
         
        # This has to be moved inside the dist_linear
#        runDuration = int(duration)/distributionGranularity
#        print "Duration is seconds:"
#        print duration
        duration = int(duration)
          
        '''
        1. Load the module according to Distribution Type to create runs
        '''
                              
        #1. Get required module loaded
        modhandleMy=loadDistribution(distributionType)
        #2. Use this module for calculation and run creation   
        (stressValues,runStartTime,runDurations)=modhandleMy(emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,HOMEPATH)
        
        uri ="PYRO:scheduler.daemon@"+str(EmulationManager.readIfaceIP("schedinterface"))+":"+str(EmulationManager.readLogLevel("schedport"))
    
        daemon=Pyro4.Proxy(uri)
        
        n=0
        for vals in stressValues:
            #print "stressValues: ",vals
            try:
                #print "Things that are sent to daemon:\n",emulationID,emulationName,distributionName,emulationLifetimeID,runDurations[n],emulator,emulatorArg,resourceTypeDist,vals,runStartTime[n],str(n)
                daemon.hello()
                #Sending emulation name already including ID stamp
                emulationNameID =str(emulationID)+"-"+str(emulationName)
                
                schedulerReply = str(daemon.createJob(emulationID,emulationNameID,distributionID,distributionName,emulationLifetimeID,runDurations[n],emulator,emulatorArg,resourceTypeDist,vals,runStartTime[n],str(n),runDurations[n]))
                

                distLoggerDM.info("Scheduler reply: "+str(schedulerReply))
                
                
                #adding values to the table for recovery
                try:
                    conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
                    c = conn.cursor()
                        
                    # 1. We populate "distribution" table :stressValue,runStartTime,runNo     
                    c.execute('INSERT INTO runLog (stressValue, runStartTime,runNo,distributionID, runDuration) VALUES (?, ?, ?, ?,?)', [vals, runStartTime[n],str(n),distributionID,runDurations[n]])
                
                                    
                    conn.commit()
                    c.close()
                except sqlite.Error, e:
                    print "Error %s:" % e.args[0]
                    print e
                    sys.exit(1)                         
                
                n= n+1
                
                
                
            except  Pyro4.errors.CommunicationError, e:
                print e
                print "\n---Check if SchedulerDaemon is started. Connection error cannot create jobs---"
        

'''
###############################
Handling Distribution module load
##############################
'''
def loadDistribution(modName):
            '''
            We are Loading module by file name. File name will be determined by distribution type (i.e. linear)
            '''
            if HOMEPATH:
                modfile = HOMEPATH+"/distributions/dist_"+modName+".py"
                modname = "dist_"+modName
            else:
                modfile = "./distributions/dist_"+modName+".py"
                modname = "dist_"+modName
                
            modhandle = imp.load_source(modname, modfile)    
            return modhandle.functionCount

def loadDistributionHelp(modName):
            '''
            We are Loading module by file name for Help content. File name will be determined by distribution type (i.e. linear)
            '''
            if HOMEPATH:
                modfile = HOMEPATH+"/distributions/dist_"+modName+".py"
                modname = "dist_"+modName
            else:
                modfile = "./distributions/dist_"+modName+".py"
                modname = "dist_"+modName
                
            modhandle = imp.load_source(modname, modfile)
            #print modhandle
          
            return modhandle.distHelp   
        
def loadDistributionArgNames(modName):
            '''
            We are Loading module by file name for Help content. File name will be determined by distribution type (i.e. linear)
            '''
            if HOMEPATH:
                modfile = HOMEPATH+"/distributions/dist_"+modName+".py"
                modname = "dist_"+modName
            else:
                modfile = "./distributions/dist_"+modName+".py"
                modname = "dist_"+modName
                
            modhandle = imp.load_source(modname, modfile)
            #print modhandle             
            return modhandle.argNames  

def listDistributions(name):
    
    distroList=[]
    if name.lower()=="all":
        if HOMEPATH:
            path=HOMEPATH+"/distributions/"  # root folder of project
        else:
            path="./distributions/"  # root folder of project
            
        dirList=os.listdir(path)
        for fname in dirList:
            if fname.startswith("dist_") and fname.endswith(".py"):
                distName = str(fname[5:-3])
                distroList.append(distName)
        
        return distroList 
    else:
        loadMod=loadDistributionHelp(name)
        return loadMod()

def listTests(name):
    
    testsList=[]
    #print "This is listTests\n"
    if name.lower()=="all":
        if HOMEPATH:
            path=HOMEPATH+"/tests/"  # root folder of project
        else:
            path="./tests/"  # root folder of project
            
        dirList=os.listdir(path)
        for fname in dirList:
            if fname.endswith(".xml") or fname.endswith(".XML"):
                distName = str(fname)#str(fname[0:-4])
                testsList.append(distName)
        
        return testsList 
    else:
        print "Display XML content"
    
def listEmulators(name):
    
    emulatorList=[]
    if name.lower()=="all":
        if HOMEPATH:
            path=HOMEPATH+"/emulators/"  # root folder of project
        else:
            path="./emulators/"  # root folder of project
            
        dirList=os.listdir(path)
        for fname in dirList:
            if fname.startswith("run_") and fname.endswith(".py"):
                distName = str(fname[4:-3])
                emulatorList.append(distName)
        
        return emulatorList
    
    else:
        
        EmuhelpMod=loadEmulatorHelp(name)
        return EmuhelpMod()   

'''
###############################
Emulator ARG module load
##############################
'''
def loadEmulatorArgNames(modName):
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
        
    return modhandle.emulatorArgNames

def loadEmulatorHelp(modName):
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
        
    return modhandle.emulatorHelp

def timeConv(dbtimestamp):
        #print "this is timeConv!!!"
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
    gmtTime=(date-dt.datetime(1970,1,1)).total_seconds()
    return gmtTime

if __name__ == "__main__":
    
    pass