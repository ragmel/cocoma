#!/usr/bin/env python
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



import optparse,sys,Pyro4,os,ConfigParser
import sqlite3 as sqlite
#import argparse - new version of optparse
import EmulationManager,XmlParser,DistributionManager,subprocess


Pyro4.config.HMAC_KEY='pRivAt3Key'


def checkPid(pid):        
    try:
        os.kill(int(pid), 0)
    except OSError:
        print "checkPid(pid) says pid is not running"
        return False
    else:
        print "checkPid(pid) says pid is running"
        return True




def main():
    
    uri ="PYRO:scheduler.daemon@localhost:51889"
    #perhaps needs to be setup somewhere else
    
    daemon=Pyro4.Proxy(uri)    

    #Trying to group things
    parser = optparse.OptionParser()
    
    listEmu = optparse.OptionGroup(parser, 'List existing emulations')
    listEmu.add_option('-l', '--list', action='store_true', default=False,dest='listAll',help='[emulationID] [all]  List of emulations by ID or all')
    listEmu.add_option('--list-name', action='store_true', default=False,dest='listName', help='[emulationName] List of emulations by name')
    listEmu.add_option('--list-active', action='store_true', default=False,dest='listActive', help='List of active emulations')
    listEmu.add_option('--list-inactive', action='store_true', default=False,dest='listInactive', help='List of inactive emulations')
    listEmu.add_option('--list-jobs', action='store_true', default=False,dest='listJobs', help='List of active Jobs running on Scheduler daemon')
        
    
    createEmu = optparse.OptionGroup(parser, 'Create new emulations')
    createEmu.add_option('-x', '--xml', action='store_true', dest='xml',default=False, help='[file.xml] enter name XML document')
    
    updateEmu = optparse.OptionGroup(parser, 'Update emulations')
    updateEmu.add_option('-u', '--update', action='store_true', dest='updateID',default=False, help='Update already created emulation. Usage: -u [emulationID] [emulationName] [distributionType] [resourceType] [emulationType] [startTime] [stopTime] [distributionGranularity] [startLoad] [stopLoad] . If no value needs to be changed enter NULL')
    
    
    deleteEmu = optparse.OptionGroup(parser, 'Delete emulations')
    deleteEmu.add_option('-d', '--delete', action='store_true',default=False, dest='deleteID', help='[emulationID] Deletes full emulation')
    deleteEmu.add_option('--purge', action='store_true',default=False, dest='purge_all', help='[all] clears everything. !!USE WITH CAUTION!!')
    
    listDistro = optparse.OptionGroup(parser, 'List available distributions')  
    listDistro.add_option('-i', '--dist', action='store_true', default=False,dest='listAllDistro',help='[all]  List of all available distributions')
    listDistro.add_option('--dist-help', action='store_true', default=False,dest='listDistroOptions',help='[name]  List of all available distribution arguments')
    
    serviceControl = optparse.OptionGroup(parser, 'Services Control')
    serviceControl.add_option('--start', action='store_true', default=False,dest='startServices',help='[scheduler][api] start services')
    serviceControl.add_option('--stop', action='store_true', default=False,dest='stopServices',help='[scheduler][api] stop services')
    
    
    
        
    parser.add_option_group(listEmu)
    parser.add_option_group(listDistro)
    parser.add_option_group(createEmu)
    parser.add_option_group(deleteEmu)
    parser.add_option_group(updateEmu)
    parser.add_option_group(serviceControl)
       

    options, arguments = parser.parse_args()
    #catch empty arguments
    if len(arguments)>0:
        
        '''
        ################################
        updateEmu
        ###############################
        '''
        
        if options.updateID and len(arguments) ==10:
              
            emulationID=arguments[0]
            emulationName=arguments[1]
            distributionType=arguments[2]
            resourceType=arguments[3]
            emulationType=arguments[4]
            startTime=arguments[5]
            stopTime=arguments[6]
            distributionGranularity=arguments[7]
            startLoad=arguments[8]
            stopLoad=arguments[9]
            print options
            print arguments
            EmulationManager.updateEmulation(emulationID,emulationName,distributionType,resourceType,emulationType,startTime,stopTime, distributionGranularity,startLoad, stopLoad)
        
        if options.updateID and len(arguments) !=10:
            parser.print_help()
        
        '''
        ################################
        serviceControl
        ###############################
        '''
        
        if options.startServices:
            if arguments[0] == "scheduler":
                print "Starting ",arguments[0]
                
                #get pid ID from DB
                try:
                    HOMEPATH= os.environ['COCOMA']
                    conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
                    c = conn.cursor()
                    c.execute("SELECT schedulerPID FROM pid WHERE ID=1")
                    schedPidNo = c.fetchone()
                    print "sched DB PID:", schedPidNo[0]
                    conn.commit()
                    c.close()
                    
                except sqlite.Error, e:
                    c.close()
                    print "Select PID SQL Error %s:" % e.args[0]
                    print e
                    sys.exit(1)
                
                #check if pid running
                if checkPid(schedPidNo[0]):
                    print "ERROR: Scheduler must be already running check \"ps -AF\" for PID ", schedPidNo[0]
                    os.system("ps -Crp "+str(schedPidNo[0]))
                    sys.exit(1)
                else:
                    try:
                        HOMEPATH= os.environ['COCOMA']
                        sout=open(HOMEPATH+"/.~sout","wb")
                        procSched = subprocess.Popen(HOMEPATH+"/bin/Scheduler.py",stdout=sout,stderr=sout)
                        procSched.stdout
                        schedPidNo =procSched.pid
                        print "Started Scheduler on PID No: ",schedPidNo
                        os.system("ps -Crp "+str(schedPidNo))
                    
                    except subprocess.CalledProcessError, e:
                        print "Error in launching scheduler: ",e
                    
                #write new pid to db               
                    try:
                        conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
                        c = conn.cursor()
                        c.execute('UPDATE pid SET schedulerPID=? WHERE ID=1 ',[schedPidNo])                         
                        conn.commit()
                        c.close()
                    except sqlite.Error, e:
                        c.close()
                        print "insert PID SQL Error %s:" % e.args[0]
                        print e
                        sys.exit(1)
                
             
            if arguments[0] == "api":
                print "Starting ",arguments[0]
                
                #get pid ID from DB
                try:
                    HOMEPATH= os.environ['COCOMA']
                    conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
                    c = conn.cursor()
                    c.execute("SELECT apiPID FROM pid WHERE ID=1")
                    apiPidNo = c.fetchone()
                    print "api DB PID:", apiPidNo[0]
                    conn.commit()
                    c.close()
                    
                except sqlite.Error, e:
                    c.close()
                    print "Select PID SQL Error %s:" % e.args[0]
                    print e
                    sys.exit(1)
                
                #check if pid running
                if checkPid(apiPidNo[0]):
                    print "ERROR:ccmsAPI must be already running check \"ps -AF\" for PID ", apiPidNo[0]
                    os.system("ps -Crp "+str(apiPidNo[0]))
                    
                    sys.exit(1)
                else:
                    try:
                        HOMEPATH= os.environ['COCOMA']
                        aout=open(HOMEPATH+"/.~aout","wb")
                        
                        ccmshAPI = subprocess.Popen(HOMEPATH+"/bin/ccmshAPI.py",stdout=aout,stderr=aout)
                        apiPidNo =ccmshAPI.pid
                        print "Started API on PID No: ",apiPidNo
                        os.system("ps -Crp "+str(apiPidNo))
                    except subprocess.CalledProcessError, e:
                        print "Error in launching ccmshAPI: ",e
                    
                #write new pid to db               
                    try:
                        conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
                        c = conn.cursor()
                        c.execute('UPDATE pid SET apiPID=? WHERE ID=1 ',[apiPidNo])                         
                        conn.commit()
                        c.close()
                    except sqlite.Error, e:
                        c.close()
                        print "insert apiPID SQL Error %s:" % e.args[0]
                        print e
                        sys.exit(1)


 
                    
        if options.stopServices:
            if arguments[0] == "scheduler":
                
                #get pid ID from DB
                try:
                    HOMEPATH= os.environ['COCOMA']
                    conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
                    c = conn.cursor()
                    c.execute("SELECT schedulerPID FROM pid WHERE ID=1")
                    schedPidNo = c.fetchone()
                    print "sched DB PID:", schedPidNo[0]
                    conn.commit()
                    c.close()
                    
                except sqlite.Error, e:
                    c.close()
                    print "Select PID SQL Error %s:" % e.args[0]
                    print e
                    sys.exit(1)
 
                
                if checkPid(schedPidNo[0])!=False:
                    print "Killing Scheduler on PID: ", schedPidNo[0]
                    try:
                        os.kill(int(schedPidNo[0]), 9)
                        
                        #update table once we killed process
                    
                        try:
                            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
                            c = conn.cursor()
                            c.execute('UPDATE pid SET schedulerPID=? WHERE ID=1 ',[99999999])                         
                            conn.commit()
                            c.close()
                        except sqlite.Error, e:
                            c.close()
                            print "insert schedulerPID SQL Error %s:" % e.args[0]
                            print e
                        
                        
                        
                    except os.error, e:
                        print "kill error: ",e
                    
                    
                    sys.exit(1)
                else:
                    print "ERROR: Scheduler is not running on PID ",schedPidNo[0]," start it first"
                    sys.exit(1)                
                
                
            
            if arguments[0] == "api":
                
                #get pid ID from DB
                try:
                    HOMEPATH= os.environ['COCOMA']
                    conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
                    c = conn.cursor()
                    c.execute("SELECT apiPID FROM pid WHERE ID=1")
                    apiPidNo = c.fetchone()
                    conn.commit()
                    print "api DB PID:", apiPidNo[0]
                    
                    c.close()
                    
                except sqlite.Error, e:
                    c.close()
                    print "Select PID SQL Error %s:" % e.args[0]
                    print e
                    sys.exit(1)
                
                #check if pid running
                
                if checkPid(apiPidNo[0])!=False:
                    
                    try:
                        os.kill(int(apiPidNo[0]), 9)
                        print "Killing API on PID: ", apiPidNo[0]
                        #update table once we killed process
                        try:
                            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')
                            c = conn.cursor()
                            c.execute('UPDATE pid SET apiPID=? WHERE ID=1 ',[99999999])                         
                            conn.commit()
                            c.close()
                        except sqlite.Error, e:
                            c.close()
                            print "insert apiPID SQL Error %s:" % e.args[0]
                            print e
                        
                        
                    except os.error, e:
                        print "ERROR killing api: ",e
                        
                    
                    sys.exit(1)
                
                else:
                    print "ERROR: API is not running on PID ",apiPidNo[0]," start it first"
                    
                    sys.exit(1)
                    
                #2.check if pid is running
                #3.execute os.system("kill "+str(procAPI.pid))
                


                    
        '''
        ################################
        listEmu
        ###############################
        '''
                  
        if options.listActive:
            EmulationManager.getEmulation("NULL","NULL",1,1)
            sys.exit(1)
         
        if options.listInactive:
            EmulationManager.getEmulation("NULL","NULL",1,0)
            sys.exit(1)
        
       
        if options.listAll:
            if arguments[0]=="all":
                EmulationManager.getEmulation("NULL","NULL",1,"NULL")
            else:
                EmulationManager.getEmulation("NULL",arguments[0],0,"NULL")
                    
        if options.listJobs:
            connectionCheck=daemonCheck()
            if  connectionCheck !=1:
                sys.exit(1) 
                
            if arguments[0]=="all":
                try:
                    for job in daemon.listJobs():
                    
                        print job
                except :
                    print "\nNo jobs are scheduled\n"
                    
            else:
                
                for job in daemon.listJobs():
                    if job.name==arguments[0]:
                        print job
        
        if options.listName:
            EmulationManager.getEmulation(arguments[0],"NULL",0,"NULL")
                
        if options.listActive:
            if arguments[0]=="all":
                #TO-DO: List inactive values with 0 param
                print "Listing all active values"
                EmulationManager.getEmulation("NULL","NULL",0,1)



        '''
        ################################
        deleteEmu
        ###############################
        '''


                  
        if options.deleteID:
            #TO-DO: List inactive values with 0 param
            print "Deleting ID: ",arguments[0]
            EmulationManager.deleteEmulation(arguments[0])
        
        
        if options.purge_all:
            print "this is purge all ccmsh"
            if arguments[0]=="all":
                EmulationManager.purgeAll()
        


        '''
        ################################
        listDistro
        ###############################
        '''




        if options.listAllDistro:
            distroList=DistributionManager.listDistributions("all")
            print "\nThese are available distributions:"
            for distName in distroList:
                print distName
        
        if options.listDistroOptions:
            print "This is listDistroOptions"
            #1. check name
            EmulationManager.distributionTypeCheck(arguments[0])
            #2. Load module
            distroModHelp=DistributionManager.loadDistributionHelp(arguments[0])
            #3. Call distHelp()
            print "\n"
            distroModHelp()
            print "\n"
            


        '''
        ################################
        createEmu
        ###############################
        '''

        
              
        if options.xml:  
                (emulationName, distributionType, resourceType, emulationType, startTime, stopTime, distributionGranularity,arg) = XmlParser.xmlReader(arguments[0])
                EmulationManager.dataCheck(startTime,stopTime)
                EmulationManager.distributionTypeCheck(distributionType)
                EmulationManager.DistributionArgCheck(distributionType,arg)
                EmulationManager.createEmulation(emulationName, distributionType, resourceType, emulationType, startTime, stopTime, distributionGranularity,arg)
        
    else:
        parser.print_help()
        
def daemonCheck():
    '''
    Checking if Scheduler Daemon is started
    '''
    uri ="PYRO:scheduler.daemon@localhost:51889"
    #perhaps needs to be setup somewhere else
    
    daemon=Pyro4.Proxy(uri)
    
    try:
        
        print daemon.hello()
        return(1)
    
    except  Pyro4.errors.CommunicationError, e:
        
        
        print e
        print "\n---Check if Scheduler Daemon is started. Connection error---"
        
        return (0)
        
    
    

if __name__ == '__main__':
    main()


