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
import EmulationManager,XmlParser,DistributionManager,subprocess,ccmshAPI


Pyro4.config.HMAC_KEY='pRivAt3Key'


def main():
    '''
    CLI module of COCOMA framework which defines key options available for local execution.
    For full list of commands please use "ccmsh -h".
    '''
    
    uri ="PYRO:scheduler.daemon@"+str(EmulationManager.readIfaceIP("schedinterface"))+":51889"
    #perhaps needs to be setup somewhere else
    
    daemon=Pyro4.Proxy(uri)    

    #Trying to group things
    parser = optparse.OptionParser()
    
    listEmu = optparse.OptionGroup(parser, 'List existing emulations')
    listEmu.add_option('-l', '--list', action='store_true', default=False,dest='listAll',help='[emulationName]  List of emulations by ID or all')
    listEmu.add_option('-r', '--results', action='store_true', default=False,dest='resAll',help='[emulationName] [all]  List of emulation results')
    
    #listEmu.add_option('--list-active', action='store_true', default=False,dest='listActive', help='List of active emulations')
    #listEmu.add_option('--list-inactive', action='store_true', default=False,dest='listInactive', help='List of inactive emulations')
    listEmu.add_option('--list-jobs', action='store_true', default=False,dest='listJobs', help='[all] List of all active Jobs running on Scheduler daemon')
        
    
    createEmu = optparse.OptionGroup(parser, 'Create new emulations')
    createEmu.add_option('-x', '--xml', action='store_true', dest='xml',default=False, help='[file.xml] enter name XML document')
    createEmu.add_option('-n', '--now', action='store_true', dest='emuNow',default=False, help='[-x filename] plus [-n] emulation starts immediately')
    
    #updateEmu = optparse.OptionGroup(parser, 'Update emulations')
    #updateEmu.add_option('-u', '--update', action='store_true', dest='updateID',default=False, help='Update already created emulation. Usage: -u [emulationID] [emulationName] [distributionType] [resourceType] [emulationType] [startTime] [stopTime] [distributionGranularity] [startLoad] [stopLoad] . If no value needs to be changed enter NULL')
    
    
    deleteEmu = optparse.OptionGroup(parser, 'Delete emulations')
    deleteEmu.add_option('-d', '--delete', action='store_true',default=False, dest='deleteID', help='[emulationID] Deletes full emulation')
    deleteEmu.add_option('--purge', action='store_true',default=False, dest='purge_all', help='[all] clears everything in DB. !!USE WITH CAUTION!!')
    
    listDistro = optparse.OptionGroup(parser, 'List available distributions')  
    listDistro.add_option('-i', '--dist', action='store_true', default=False,dest='listAllDistro',help='[all] or [name] List of all available distributions')
    
    
    serviceControl = optparse.OptionGroup(parser, 'Services Control')
    serviceControl.add_option('--start', action='store_true', default=False,dest='startServices',help='[scheduler][api] followed by interface and port to start services. Example: ccmsh --start api eth1 2020')
    serviceControl.add_option('--stop', action='store_true', default=False,dest='stopServices',help='[scheduler][api] stop services')
    serviceControl.add_option('--show', action='store_true', default=False,dest='showServices',help='[scheduler][api] show services')
    serviceControl.add_option('-v','--version', action='store_true', default=False,dest='version',help='Display version info')
    
    listEmulator = optparse.OptionGroup(parser, 'List available emulators')  
    listEmulator.add_option('-e', '--emu', action='store_true', default=False,dest='listAllEmulators',help='[all] or [name]  List of all available emulators')
    
    
    
    
        
    parser.add_option_group(listEmu)
    parser.add_option_group(listDistro)
    parser.add_option_group(listEmulator)
    parser.add_option_group(createEmu)
    parser.add_option_group(deleteEmu)
    #parser.add_option_group(updateEmu)
    parser.add_option_group(serviceControl)
       

    options, arguments = parser.parse_args()
    
    if options.version:
        os.system("clear")
        print '''
            
     _______  _______  _______  _______  _______  _______              
    (  ____ \(  ___  )(  ____ \(  ___  )(       )(  ___  )  
    | (    \/| (   ) || (    \/| (   ) || () () || (   ) |  
    | |      | |   | || |      | |   | || || || || (___) |  
    | |      | |   | || |      | |   | || |(_)| ||  ___  |  
    | |      | |   | || |      | |   | || |   | || (   ) |   
    | (____/\| (___) || (____/\| (___) || )   ( || )   ( |    
    (_______/(_______)(_______/(_______)|/     \||/     \| Ver. 0.0001
                                                                                  
                                                                                  
Copyright 2012-2013 SAP Ltd

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

 
COCOMA is a framework for COntrolled COntentious and MAlicious patterns
                                                                                  

            '''
        sys.exit(1) 
    
    #catch empty arguments
    if len(arguments)>0:
        
        '''
        ################################
        serviceControl
        ###############################
        '''

            
        if options.startServices:
            cliCommand=""
            if arguments[0] == "scheduler":
                print "Starting ",arguments[0]
                #generate CLI command
                
                try:
                    n=1
                    while n !=len(arguments):
                        
                        cliCommand =cliCommand+" "+arguments[n]+" "
                        n+=1
                except Exception,e :
                    print "No additional arguments were supplied to scheduler:",e
                    EmulationManager.services_control("scheduler","start"," ")
                
                EmulationManager.services_control("scheduler","start",cliCommand)
                    
                
                
     
            if arguments[0] == "api":
                
                print "Starting ",arguments[0]
                #generate CLI command
                
                try:
                    n=1
                    while n !=len(arguments):
                        if n==2:
                            cliCommand+=" -p "+arguments[n]
                        
                        if n==1:
                            cliCommand = "-i "+arguments[n]
                        
                        n+=1
                except Exception,e :
                    print "No additional arguments were supplied to API:",e
                    EmulationManager.services_control("api","start"," ")        
                    
                    
                    
                print "Starting ",arguments[0],cliCommand
                EmulationManager.services_control("api","start",cliCommand)
                
                    
            #EmulationManager.services_control("api","start","")
 
                    
        if options.stopServices:
            if arguments[0] == "scheduler":
                EmulationManager.services_control("scheduler","stop"," ")
            
            if arguments[0] == "api":
                EmulationManager.services_control("api","stop"," ")
                
        if options.showServices:
            if arguments[0] == "scheduler":
                EmulationManager.services_control("scheduler","show"," ")
            
            if arguments[0] == "api":
                EmulationManager.services_control("api","show"," ")
                  
                     
        '''
        ################################
        listEmu
        ###############################
        '''
        
        if options.resAll:
            if arguments[0]=="all":
                emuList=EmulationManager.getActiveEmulationList("all")
                
                
                for elem in emuList :
                    failedRunsInfo=elem["failedRunsInfo"]
                    
                    print "---->\nID: "+str(elem["ID"])+"\nName: "+str(elem["Name"])+"\nState: "+str(elem["State"])+"\nTotal Runs: "+str(elem["runsTotal"])+"\nExecuted Runs: "+str(elem["runsExecuted"])+"\nFailed Runs: "+str(len(failedRunsInfo))
                    
                    if failedRunsInfo:
                        print "###Failed Runs Info###"
                        for Runs in failedRunsInfo:
                            print "#\nRun No: ", Runs["runNo"]
                            print "Distribution ID: ",Runs["distributionID"]
                            print "Distribution Name: ",Runs["distributionName"]
                            
                            print "Stress Value: ", Runs["stressValue"]
                            print "Error Message: ", Runs["message"]

            else:
                try:
                    emuList=EmulationManager.getActiveEmulationList(arguments[0])
                    for elem in emuList :
                        failedRunsInfo=elem["failedRunsInfo"]
                    
                    print "---->\nID: "+str(elem["ID"])+"\nName: "+str(elem["Name"])+"\nState: "+str(elem["State"])+"\nTotal Runs: "+str(elem["runsTotal"])+"\nExecuted Runs: "+str(elem["runsExecuted"])+"\nFailed Runs: "+str(len(failedRunsInfo))
                    
                    if failedRunsInfo:
                        print "###Failed Runs Info###"
                        for Runs in failedRunsInfo:
                            print "#\nRun No: ", Runs["runNo"]
                            print "Distribution ID: ",Runs["distributionID"]
                            print "Distribution Name: ",Runs["distributionName"]
                            
                            print "Stress Value: ", Runs["stressValue"]
                            print "Error Message: ", Runs["message"]
                except Exception,e:
               
                        print "\nEmulation ID:"+str(arguments[0])+" not found.\nError:"+str(e)
                        sys.exit(0)
                
                
 
                
        if options.listAll:

            if arguments[0]=="all":
                emuList=EmulationManager.getActiveEmulationList("all")
                
                
                for elem in emuList :
                    failedRunsInfo=elem["failedRunsInfo"]
                    
                    print "---->\nID: "+str(elem["ID"])+"\nName: "+str(elem["Name"])+"\nState: "+str(elem["State"])+"\nTotal Runs: "+str(elem["runsTotal"])+"\nExecuted Runs: "+str(elem["runsExecuted"])+"\nFailed Runs: "+str(len(failedRunsInfo))
                    
                    if failedRunsInfo:
                        print "###Failed Runs Info###"
                        for Runs in failedRunsInfo:
                            print "#\nRun No: ", Runs["runNo"]
                            print "Distribution ID: ",Runs["distributionID"]
                            print "Distribution Name: ",Runs["distributionName"]
                            
                            print "Stress Value: ", Runs["stressValue"]
                            print "Error Message: ", Runs["message"]
                            
            else:
                try:
                    (emulationID,emulationName,emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList)=EmulationManager.getEmulation(arguments[0])
                    print "--->\nID: "+str(emulationID)+"\nName: "+str(emulationName)+"\nType: "+str(emulationType)+"\nResourceType: "+str(resourceTypeEmulation)+"\nStartTime: "+str(startTimeEmu)+"\nstopTime: "+str(stopTimeEmu)


                    for dist in distroList:
                        print "---\nDistrName: "+str(dist['distributionsName'])+"\nDistrType: "+str(dist['distrType'])+"\nDistrResourceType: "+str(dist['resourceTypeDist'])+"\nDistroStartTime: "+str(dist['startTimeDistro'])+"\nDistroDuration: "+str(dist['durationDistro'])+"\nDistroArgs: "+str(dist['distroArgs'])+"\nEmulatorName: "+str(dist['emulatorName'])+"\nEmulatorArgs: "+str(dist['emulatorArg'])
                    
                    
                    
                except Exception,e:
               
                        print "\nEmulation Name:"+str(arguments[0])+" not found.\nError:"+str(e)
                        sys.exit(0)
                    
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
            if arguments[0].lower()=="all":
                distroList=DistributionManager.listDistributions(arguments[0])

                print "\nThese are available distributions:"
                for distName in distroList:
                    print distName
            else:
                try:
                    distroList=DistributionManager.listDistributions(arguments[0])
                    print distroList
                except Exception, e:
                    print "Error: ",e
                    print "Distribution \"%s\" not found. Check name."%(arguments[0])
                     
        '''
        ################################
        listEmulators
        ###############################
        '''

        if options.listAllEmulators:
            if arguments[0].lower()=="all":
                emuList=DistributionManager.listEmulators(arguments[0])

                print "\nThese are available Emulators:"
                for emuName in emuList:
                    print emuName
            else:
                try:
                    
                    emuList2=DistributionManager.listEmulators(arguments[0])
                    print emuList2
                except Exception, e:
                    print "Error: ",e
                    print "Emulator \"%s\" not found. Check name."%(arguments[0])            


        '''
        ################################
        createEmu
        ###############################
        '''
          
        if options.xml and not options.emuNow:  
                
                (emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData) = XmlParser.xmlReader(arguments[0])
                if startTimeEmu.lower() =="now":
                    startTimeEmu1 = EmulationManager.emulationNow(2)
                    EmulationManager.createEmulation(emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData)
                else:
                    EmulationManager.createEmulation(emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData)
                
    
        
        if options.emuNow and options.xml:
            print "Starting Now"
            
            (emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData) = XmlParser.xmlReader(arguments[0])
            startTimeEmu = EmulationManager.emulationNow(2)
            
            EmulationManager.createEmulation(emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData)
            
    else:
        parser.print_help()

        
def daemonCheck():
    '''
    Checking if Scheduler Daemon(bin/Scheduler.py is running. Returning "1" if true and "0" if not.
    '''
    uri ="PYRO:scheduler.daemon@"+str(EmulationManager.readIfaceIP("schedinterface"))+":51889"
    #perhaps needs to be setup somewhere else
    
    daemon=Pyro4.Proxy(uri)
    
    try:
        
        print daemon.hello()
        return(1)
    
    except  Pyro4.errors.CommunicationError, e:
        
        print e

        print "\n---Unable to find Scheduler on remote IP. Trying localhost---"
        try:
            daemon=Pyro4.Proxy(uri)
            print daemon.hello()
            return(1)
        except  Pyro4.errors.CommunicationError, e:
            print "\n---Unable to find Scheduler on localhost---"
            return (0)
        


    
    

if __name__ == '__main__':
    main()


