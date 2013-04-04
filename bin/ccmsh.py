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



import optparse,sys,Pyro4,os,ConfigParser
import sqlite3 as sqlite
#import argparse - new version of optparlse
import EmulationManager,XmlParser,DistributionManager,subprocess,ccmshAPI
import logging

Pyro4.config.HMAC_KEY='pRivAt3Key'

logging.basicConfig(level=logging.INFO)

def main():
    '''
    CLI module of COCOMA framework which defines key options available for local execution.
    For full list of commands please use "ccmsh -h".
    '''
    
    uri ="PYRO:scheduler.daemon@"+str(EmulationManager.readIfaceIP("schedinterface"))+":"+str(EmulationManager.readLogLevel("schedport"))
    #perhaps needs to be setup somewhere else
    
    daemon=Pyro4.Proxy(uri)    

    #Grouping Options
    #a usage string for your program
    usage = "Usage: %prog [option] arg"
    #paragraph of help text to print after option help
    epilog= "Copyright 2012-2013 SAP Ltd"
    #A paragraph of text giving a brief overview of your program
    description="""COCOMA is a toolkit for generating COntrolled COntentious and MAlicious patterns in multi-tenant environment."""
    parser = optparse.OptionParser(usage=usage,epilog=epilog,description=description)
    
    parser.add_option('-v','--version', action='store_true', default=False,dest='version',help='show version information')
    
    
    listEmu = optparse.OptionGroup(parser, 'List existing resources')
    listEmu.add_option('-l', '--list', action='store_true', default=False,dest='listAll',help='list all emulations or specific emulation by name')
    listEmu.add_option('-r', '--results', action='store_true', default=False,dest='resAll',help='list all emulations results or specific emulation results by name')
    listEmu.add_option('-j', '--list-jobs', action='store_true', default=False,dest='listJobs', help='List of all scheduled jobs')
        
    createEmu = optparse.OptionGroup(parser, 'Create new emulations')
    createEmu.add_option('-x', '--xml', action='store_true', dest='xml',default=False, help='provide path to XML file with emulation details')
    createEmu.add_option('-n', '--now', action='store_true', dest='emuNow',default=False, help='add to the "-x" argument to override emulation start date and execute test immediately')
        
    deleteEmu = optparse.OptionGroup(parser, 'Delete emulations')
    deleteEmu.add_option('-d', '--delete', action='store_true',default=False, dest='deleteID', help='delete emulation by name')
    deleteEmu.add_option('-p','--purge', action='store_true',default=False, dest='purge_all', help='wipes all DB entries, removes all scheduled jobs and log files')
    
    listDistro = optparse.OptionGroup(parser, 'List available distributions')  
    listDistro.add_option('-i', '--dist', action='store_true', default=False,dest='listAllDistro',help='lists all available distributions and gives distribution details by name')
        
    serviceControl = optparse.OptionGroup(parser, 'Services Control')
    serviceControl.add_option('--start', action='store_true', default=False,dest='startServices',help='launch Scheduler or API daemon. Additionally you can specify interface and port. Example: "ccmsh --start api eth0 2020"')
    serviceControl.add_option('--stop', action='store_true', default=False,dest='stopServices',help='stop Scheduler or API daemon')
    serviceControl.add_option('--show', action='store_true', default=False,dest='showServices',help='show OS information on Scheduler or API daemon')
        
    listEmulator = optparse.OptionGroup(parser, 'List available emulators')  
    listEmulator.add_option('-e', '--emu', action='store_true', default=False,dest='listAllEmulators',help='lists all available emulators and gives emulator details by name')
    
        
    parser.add_option_group(listEmu)
    parser.add_option_group(listDistro)
    parser.add_option_group(listEmulator)
    parser.add_option_group(createEmu)
    parser.add_option_group(deleteEmu)
    parser.add_option_group(serviceControl)
       

    options, arguments = parser.parse_args()



    if options.version:
        os.system("clear")
        print '''
            
      ___  _____  ___  _____  __  __    __       
     / __)(  _  )/ __)(  _  )(  \/  )  /__\     
    ( (__  )(_)(( (__  )(_)(  )    (  /(__)\    
     \___)(_____)\___)(_____)(_/\/\_)(__)(__) Ver. RC1.0
                                                                                  
                                                                                  
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
    #if len(arguments)>0:
        
    '''
    ################################
    serviceControl
    ###############################
    '''

        
    if options.startServices:
        if len(arguments)>0:
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
        else:
            print "No arguments supplied, check help"
                    
            #EmulationManager.services_control("api","start","")

                
    if options.stopServices:
        if len(arguments)>0:
            if arguments[0] == "scheduler":
                EmulationManager.services_control("scheduler","stop"," ")
            
            elif arguments[0] == "api":
                EmulationManager.services_control("api","stop"," ")
            
            else:
                print "Wrong arguments check help"
            
        else:
            print "No arguments supplied, check help"
                
    if options.showServices:
        if len(arguments)>0:
            if arguments[0] == "scheduler":
                EmulationManager.services_control("scheduler","show"," ")
            
            elif arguments[0] == "api":
                EmulationManager.services_control("api","show"," ")
            else:
                print "Wrong arguments, check help"
        else:
            print "No arguments supplied, check help"
        
              
                 
    '''
    ################################
    listEmu
    ###############################
    '''
    
    if options.resAll:
        if len(arguments)>0:
            try:
                emuList=EmulationManager.getActiveEmulationList(arguments[0])
                for elem in emuList :
                    failedRunsInfo=elem["failedRunsInfo"]
                    totalFailedRuns = int(elem["runsTotal"])-int(elem["runsExecuted"])
                    #check if the emulation was completed already
                    if str(elem["State"]) == "inactive":
                        print "---->\nID: "+str(elem["ID"])+"\nName: "+str(elem["Name"])+"\nState: "+str(elem["State"])+"\nTotal Runs: "+str(elem["runsTotal"])+"\nExecuted Runs: "+str(elem["runsExecuted"])+"\nFailed Runs: "+str(totalFailedRuns)
                    else:
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
           
                    print "\nEmulation name:"+str(arguments[0])+" not found.\n(Error:"+str(e)+")"
                    sys.exit(0)
            

        else:
            
            emuList=EmulationManager.getActiveEmulationList("all")
            
            
            for elem in emuList :
                failedRunsInfo=elem["failedRunsInfo"]
                totalFailedRuns = int(elem["runsTotal"])-int(elem["runsExecuted"])
                #check if the emulation was completed already
                if str(elem["State"]) == "inactive":
                    print "---->\nID: "+str(elem["ID"])+"\nName: "+str(elem["Name"])+"\nState: "+str(elem["State"])+"\nTotal Runs: "+str(elem["runsTotal"])+"\nExecuted Runs: "+str(elem["runsExecuted"])+"\nFailed Runs: "+str(totalFailedRuns)
                else:
                    print "---->\nID: "+str(elem["ID"])+"\nName: "+str(elem["Name"])+"\nState: "+str(elem["State"])+"\nTotal Runs: "+str(elem["runsTotal"])+"\nExecuted Runs: "+str(elem["runsExecuted"])+"\nFailed Runs: "+str(len(failedRunsInfo)) 
                
                if failedRunsInfo:
                    print "###Failed Runs Info###"
                    for Runs in failedRunsInfo:
                        print "#\nRun No: ", Runs["runNo"]
                        print "Distribution ID: ",Runs["distributionID"]
                        print "Distribution Name: ",Runs["distributionName"]
                        
                        print "Stress Value: ", Runs["stressValue"]
                        print "Error Message: ", Runs["message"]

            
            

            
    if options.listAll:
        
        if len(arguments)>0:
            try:
                (emulationID,emulationName,emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList)=EmulationManager.getEmulation(arguments[0])
                print "--->\nID: "+str(emulationID)+"\nName: "+str(emulationName)+"\nType: "+str(emulationType)+"\nResourceType: "+str(resourceTypeEmulation)+"\nStartTime: "+str(startTimeEmu)+"\nstopTime: "+str(stopTimeEmu)


                for dist in distroList:
                    print "---\nDistrName: "+str(dist['distributionsName'])+"\nDistrType: "+str(dist['distrType'])+"\nDistrResourceType: "+str(dist['resourceTypeDist'])+"\nDistroStartTime: "+str(dist['startTimeDistro'])+"\nDistroDuration: "+str(dist['durationDistro'])+"\nDistroArgs: "+str(dist['distroArgs'])+"\nEmulatorName: "+str(dist['emulatorName'])+"\nEmulatorArgs: "+str(dist['emulatorArg'])
                
                
                
            except Exception,e:
           
                    print "\nEmulation Name:"+str(arguments[0])+" not found.\nError:"+str(e)
                    sys.exit(0)
            
            
                        
        else:
            emuList=EmulationManager.getActiveEmulationList("all")
            
            
            for elem in emuList :
                failedRunsInfo=elem["failedRunsInfo"]
                totalFailedRuns = int(elem["runsTotal"])-int(elem["runsExecuted"])
                #check if the emulation was completed already
                if str(elem["State"]) == "inactive":
                    print "---->\nID: "+str(elem["ID"])+"\nName: "+str(elem["Name"])+"\nState: "+str(elem["State"])+"\nTotal Runs: "+str(elem["runsTotal"])+"\nExecuted Runs: "+str(elem["runsExecuted"])+"\nFailed Runs: "+str(totalFailedRuns)
                else:
                    print "---->\nID: "+str(elem["ID"])+"\nName: "+str(elem["Name"])+"\nState: "+str(elem["State"])+"\nTotal Runs: "+str(elem["runsTotal"])+"\nExecuted Runs: "+str(elem["runsExecuted"])+"\nFailed Runs: "+str(len(failedRunsInfo)) 
                
                if failedRunsInfo:
                    print "###Failed Runs Info###"
                    for Runs in failedRunsInfo:
                        print "#\nRun No: ", Runs["runNo"]
                        print "Distribution ID: ",Runs["distributionID"]
                        print "Distribution Name: ",Runs["distributionName"]
                        
                        print "Stress Value: ", Runs["stressValue"]
                        print "Error Message: ", Runs["message"]
            

                
    if options.listJobs:
        connectionCheck=daemonCheck()
        if  connectionCheck !=1:
            sys.exit(1)
             
        if len(daemon.listJobs())>0:
            if len(arguments)>0:
                n=0   
                for job in daemon.listJobs():
                    if job.name==arguments[0]:
                        n+=1
                        print job
                if n==0:        
                    print "Job \""+str(arguments[0])+"\" was not found" 
        
             
        
            else:
                for job in daemon.listJobs():
                    print "job",job
        else:
            print "\nNo jobs are scheduled\n"
                
    
    '''
    ################################
    deleteEmu
    ###############################
    '''
              
    if options.deleteID:
        if len(arguments)>0:
            #TO-DO: List inactive values with 0 param
            print "Deleting emulation: ",arguments[0]
            EmulationManager.deleteEmulation(arguments[0])
        else:
            print "Specify emulation ID or name. See help for details"
    
    
    if options.purge_all:
        print "WARNING:\nThis action will wipe every single log file, scheduled job and database entry do you wish to proceed?\n(y/n)"
        yes = set(['yes','y', 'ye','yey'])
        no = set(['no','n','nay'])
        try:
            choice = raw_input().lower()
            if choice in yes:
                EmulationManager.purgeAll()
                return True
            elif choice in no:
                print "Action cancelled"
                return False
            else:
                print "Please respond with 'yes' or 'no'"
        except KeyboardInterrupt,e:
            print "\nAction cancelled"



    '''
    ################################
    listDistro
    ###############################
    '''

    if options.listAllDistro:
        if len(arguments)>0:
            try:
                distroList=DistributionManager.listDistributions(arguments[0])
                print distroList
            except Exception, e:
                print "Error: ",e
                print "Distribution \"%s\" not found. Check name."%(arguments[0])
        else:
            distroList=DistributionManager.listDistributions("all")

            print "\nAvailable distributions:"
            for distName in distroList:
                print distName
        
            
                 
    '''
    ################################
    listEmulators
    ###############################
    '''

    if options.listAllEmulators:
        if len(arguments)>0:
            try:
                emuList2=DistributionManager.listEmulators(arguments[0])
                print emuList2
            except Exception, e:
                print "Error: ",e
                print "Emulator \"%s\" not found. Check name."%(arguments[0]) 
        else:
            emuList=DistributionManager.listEmulators("all")
            print "\nAvailable Emulators:"
            for emuName in emuList:
                print emuName
        
           


    '''
    ################################
    createEmu
    ###############################
    '''
      
    if options.xml and not options.emuNow:  
            if len(arguments)>0:
                
                if daemonCheck()!=False:
                    try:
                        (emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData) = XmlParser.xmlReader(arguments[0])
                        if startTimeEmu.lower() =="now":
                            startTimeEmu1 = EmulationManager.emulationNow(2)
                            print EmulationManager.createEmulation(emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData)
                        else:
                            print EmulationManager.createEmulation(emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData)
                    except Exception, e:
                        logging.exception("Problem description:")
                        logging.error("Unable to use this file.Error:"+str(e)) 
                        
                        
                        
           
            else:
                print "Specify XML file location. See help for details"

    
    if options.emuNow and options.xml:
        print "Starting Now"
        
        (emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData) = XmlParser.xmlReader(arguments[0])
        startTimeEmu = EmulationManager.emulationNow(2)
        
        print EmulationManager.createEmulation(emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData)
        
    #else:
        #parser.print_help()

        
def daemonCheck():
    '''
    Checking if Scheduler Daemon(bin/Scheduler.py is running. Returning "1" if true and "0" if not.
    '''
    
    uri ="PYRO:scheduler.daemon@"+str(EmulationManager.readIfaceIP("schedinterface"))+":"+str(EmulationManager.readLogLevel("schedport"))
    #perhaps needs to be setup somewhere else
    
    daemon=Pyro4.Proxy(uri)
    
    try:
        
        daemon.hello()
        return(1)
    
    except  Pyro4.errors.CommunicationError, e:
        
        print e

        print "\n---Unable to find Scheduler on remote IP.---"
        return False
    

if __name__ == '__main__':
    main()


