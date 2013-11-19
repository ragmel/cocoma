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


import Library,optparse,os,sys,EMQproducer,EmulationManager,XmlParser
import sqlite3 as sqlite
#MQ setup
from EMQproducer import Producer
global producer
producer = Producer()
global myName
myName = "ccmsh"

global HOMEPATH
#HOMEPATH = Library.getHomepath()
try:
    HOMEPATH= os.environ['COCOMA']
except:
    print "no $COCOMA environmental variable set"


def main():

    '''
    CLI module of COCOMA framework which defines key options available for local execution.
    For full list of commands please use "ccmsh -h".
    '''
    
#    daemon=Library.getDaemon()

    #Grouping Options
    #a usage string for your program
    usage = "Usage: %prog [option] arg"
    #paragraph of help text to print after option help
    epilog= "Copyright 2012-2013 SAP Ltd"
    #A paragraph of text giving a brief overview of your program
    description="""COCOMA is a toolkit for generating COntrolled COntentious and MAlicious patterns in multi-tenant environment."""
    parser = optparse.OptionParser(usage=usage,epilog=epilog,description=description)
    
    parser.add_option('-v','--version', action='store_true', default=False,dest='version',help='show version information')
    
    config = optparse.OptionGroup(parser, 'COCOMA configurations')
    config.add_option('-q', '--mq', action='store_true', default=False,dest='addConfig',help='add configuration parameters for message queue:      enabled vhost exchange user password host topic ')
    config.add_option('-m', '--rmq', action='store_true', default=False,dest='rmConfig',help='remove configuration parameters for message queue')
    config.add_option('-a', '--enl', action='store_true', default=False,dest='enConfig',help='enable configuration parameters for message queue')
    config.add_option('-s', '--smq', action='store_true', default=False,dest='showConfig',help='show configuration parameters for message queue')
    config.add_option('-b', '--bfz', action='store_true', default=False,dest='setBackfuzzPath',help='Update/Show location of Backfuzz emulator')
    
    listEmu = optparse.OptionGroup(parser, 'List existing resources')
    listEmu.add_option('-l', '--list', action='store_true', default=False,dest='listAll',help='list all emulations or specific emulation by name')
    listEmu.add_option('-r', '--results', action='store_true', default=False,dest='resAll',help='list all emulations results or specific emulation results by name')
    listEmu.add_option('-j', '--list-jobs', action='store_true', default=False,dest='listJobs', help='List of all scheduled and currently running jobs')
        
    createEmu = optparse.OptionGroup(parser, 'Create new emulations')
    createEmu.add_option('-x', '--xml', action='store_true', dest='xml',default=False, help='provide path to XML file with emulation details')
    createEmu.add_option('-n', '--now', action='store_true', dest='emuNow',default=False, help='add to the "-x" argument to override emulation start date and execute test immediately')
    createEmu.add_option('-f', '--force', action='store_true', dest='emuForce',default=False, help='add to the "-x" argument to force running of emulation (when resources are near, but not over their limit)')
        
    deleteEmu = optparse.OptionGroup(parser, 'Delete emulations')
    deleteEmu.add_option('-d', '--delete', action='store_true',default=False, dest='deleteID', help='delete emulation by name')
    deleteEmu.add_option('-p','--purge', action='store_true',default=False, dest='purge_all', help='wipes all DB entries and removes all scheduled jobs')
    deleteEmu.add_option('-c','--clear-logs', action='store_true',default=False, dest='clear_logs', help='Removes COCOMA log files')
    
    listDistro = optparse.OptionGroup(parser, 'List available distributions')  
    listDistro.add_option('-i', '--dist', action='store_true', default=False,dest='listAllDistro',help='lists all available distributions and gives distribution details by name')
        
    serviceControl = optparse.OptionGroup(parser, 'Services Control')
    serviceControl.add_option('--start', action='store_true', default=False,dest='startServices',help='launch Scheduler or API daemon. Additionally you can specify interface and port. Example: "ccmsh --start api eth0 2020"')
    serviceControl.add_option('--stop', action='store_true', default=False,dest='stopServices',help='stop Scheduler or API daemon')
    serviceControl.add_option('--show', action='store_true', default=False,dest='showServices',help='show OS information on Scheduler or API daemon')
        
    listEmulator = optparse.OptionGroup(parser, 'List available emulators')  
    listEmulator.add_option('-e', '--emu', action='store_true', default=False,dest='listAllEmulators',help='lists all available emulators and gives emulator details by name')
    
    parser.add_option_group(config)        
    parser.add_option_group(listEmu)
    parser.add_option_group(listDistro)
    parser.add_option_group(listEmulator)
    parser.add_option_group(createEmu)
    parser.add_option_group(deleteEmu)
    parser.add_option_group(serviceControl)
       

    options, arguments = parser.parse_args()

    if options.version:
        noExtraOptions(options, "version")
        VERSION = getVersion()
        os.system("clear")
        text = '''
            
      ___  _____  ___  _____  __  __    __       
     / __)(  _  )/ __)(  _  )(  \/  )  /__\     
    ( (__  )(_)(( (__  )(_)(  )    (  /(__)\    
     \___)(_____)\___)(_____)(_/\/\_)(__)(__) '''+ "v"+VERSION+'''                                                                              

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


COCOMA is a framework for COntrolled COntentious and MAlicious patterns.
More info @ https://github.com/cragusa/cocoma          

            '''
        print text
        sys.exit(1) 
    
    #catch empty arguments
    #if len(arguments)>0:
        
    '''
    ################################
    serviceControl
    ###############################
    '''

        
    if options.startServices:
        noExtraOptions(options, "startServices")
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
                    Library.services_control("scheduler","start"," ")
                
                Library.services_control("scheduler","start",cliCommand)
                    
                
                
     
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
                    Library.services_control("api","start"," ")        
                    
                    
                    
                print "Starting ",arguments[0],cliCommand
                Library.services_control("api","start",cliCommand)
        else:
            print "No arguments supplied, check help"
                    
            #Library.services_control("api","start","")

                
    if options.stopServices:
        noExtraOptions(options, "stopServices")
        if len(arguments)>0:
            if arguments[0] == "scheduler":
                Library.services_control("scheduler","stop"," ")
                Library.killRemainingProcesses()
            elif arguments[0] == "api":
                Library.services_control("api","stop"," ")
            
            else:
                print "Wrong arguments check help"
            
        else:
            print "No arguments supplied, check help"
                
    if options.showServices:
        noExtraOptions(options, "showServices")
        if len(arguments)>0:
            if arguments[0] == "scheduler":
                Library.services_control("scheduler","show"," ")
            
            elif arguments[0] == "api":
                Library.services_control("api","show"," ")
            else:
                print "Wrong arguments, check help"
        else:
            print "No arguments supplied, check help"
        
    '''
    ################################
    config
    ###############################
    '''


    if options.addConfig:
        noExtraOptions(options, "addConfig")
	mqarguments = {}
	mqarguments["emulationMQenable"] = arguments[0]
	mqarguments["emulationMQvhost"] = arguments[1]
	mqarguments["emulationMQexchange"] = arguments[2]
	mqarguments["emulationMQuser"] = arguments[3]
	mqarguments["emulationMQpassword"] = arguments[4]
	mqarguments["emulationMQhost"] = arguments[5]
	mqarguments["emulationMQtopic"] = arguments[6]
	
	EMQproducer.MQconfig(mqarguments)

    if options.rmConfig:
        noExtraOptions(options, "rmConfig")
	#print "rmConfig"
        if len(arguments)==0:
            #print "got 1 arguments"
            EMQproducer.MQconfigDelete()
        else:
            print "Not all arguments supplied, check help"
    
    if options.enConfig:
        noExtraOptions(options, "enConfig")
	#print "rmConfig"
        if (len(arguments)==1): 
		if (arguments[0]=="yes") or (arguments[0]=="no") :
            		EMQproducer.MQconfigEnable(arguments[0])
		else:
			print "Enabled parameter accepts either 'yes' or 'no'"
        else:
            print "Not all arguments supplied, check help"
    
    if options.showConfig:
        noExtraOptions(options, "showConfig")
        #print "rmConfig"
        if len(arguments)==0:
            #print "got 1 arguments"
            EMQproducer.MQconfigShow()
        else:
            print "Not all arguments supplied, check help"

                 
    '''
    ################################
    listEmu
    ###############################
    '''
    
    if options.setBackfuzzPath:
        noExtraOptions(options, "setBackfuzzPath")
        if len(arguments)>0:
            try:
                Library.writeInterfaceData(arguments[0],"backfuzz_path")
                print "backfuzz_path updated to: ", arguments[0]
            except Exception, e:
                print "unable to update backfuzz_path"
                sys.exit(0)
        else:
            print "backfuzz_path = " + Library.readBackfuzzPath()
            sys.exit(0)
    
    if options.resAll:
        noExtraOptions(options, "resAll")
        if len(arguments)>0:
            try:
                emuList=Library.getEmulationList(arguments[0])
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
            
            emuList=Library.getEmulationList("all")
            
            
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
        noExtraOptions(options, "listAll")
        
        if len(arguments)>0:
            try: 
                (emulationID,emulationName,emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData,logging,logFrequency,logLevel,enabled,vhost,exchange,user,password,host,topic)=EmulationManager.getEmulation(arguments[0])
                print "--->\nID: "+str(emulationID)+"\nName: "+str(emulationName)+"\nType: "+str(emulationType)+"\nResourceType: "+str(resourceTypeEmulation)+"\nStartTime: "+str(startTimeEmu)+"\nstopTime: "+str(stopTimeEmu)


                for dist in distroList:
                    print "---\nDistrName: "+str(dist['distributionsName'])+"\nDistrType: "+str(dist['distrType'])+"\nDistrResourceType: "+str(dist['resourceTypeDist'])+"\nDistroStartTime: "+str(dist['startTimeDistro'])+"\nDistroDuration: "+str(dist['durationDistro'])+"\nDistroArgs: "+str(dist['distroArgs'])+"\nEmulatorName: "+str(dist['emulatorName'])+"\nEmulatorArgs: "+str(dist['emulatorArg'])
                
                print "---\nLogging: "+logging+"\nlogFrequency: "+logFrequency+"\nlogLevel: "+logLevel+"\nenabled: "+enabled+"\nvhost: "+vhost+"\nexchange: "+exchange+"\nuser: "+user+"\npassword: "+password+"\nhost: "+host+"\ntopic: "+topic
                
                
                #producer.sendmsg(myName,"USER REQUEST: "+sys._getframe().f_code.co_name+" list "+arguments[0])
                msg = {"Action":"USER REQUEST list Emulation","EmulationName":arguments[0]}
                producer.sendmsg(myName,msg)
                
            except Exception,e:
           
                    print "\nEmulation Name:"+str(arguments[0])+" not found.\nError:"+str(e)
                    sys.exit(0)
            
            
                        
        else:

            emuList=Library.getEmulationList("all")
            
            
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

            try:
                #producer.sendmsg(myName,"USER REQUEST: "+sys._getframe().f_code.co_name+" list all")
                msg = {"Action":"USER REQUEST list all Emulations"}
                producer.sendmsg(myName,msg)
            except Exception,e:
                print "NO USER INPUT"

                
    if options.listJobs:
        noExtraOptions(options, "listJobs")
        jobList = Library.getJobList()
        for job in jobList:
            print job

    '''
    ################################
    deleteEmu
    ###############################
    '''
              
    if options.deleteID:
        noExtraOptions(options, "deleteID")
        if len(arguments)>0:
            #TO-DO: List inactive values with 0 param
            print "Deleting emulation: ",arguments[0]
            EmulationManager.deleteEmulation(arguments[0])
        try:
            #producer.sendmsg(myName,"USER REQUEST: "+sys._getframe().f_code.co_name+" delete "+arguments[0])
            msg = {"Action":"USER REQUEST delete Emulation","EmulationName":arguments[0]}
            producer.sendmsg(myName,msg)
        except Exception,e:
            print "NO USER INPUT"
        else:
            print "Specify emulation ID or name. See help for details"
    
    
    if options.purge_all:
        noExtraOptions(options, "purge_all")
        print "WARNING:\nThis action will wipe every scheduled job and database entry do you wish to proceed?\n(y/n)"
        yes = set(['yes','y', 'ye','yey'])
        no = set(['no','n','nay'])
        try:
            choice = raw_input().lower()
            if choice in yes:
                Library.purgeAll()
                Library.killRemainingProcesses()
                Library.removeLogs()
                #producer.sendmsg(myName,"USER REQUEST: "+sys._getframe().f_code.co_name+" purge all")
                msg = {"Action":"USER REQUEST purge all Emulations"}
                producer.sendmsg(myName,msg)
                return True
            elif choice in no:
                print "Action cancelled"
                return False
            else:
                print "Please respond with 'yes' or 'no'"

        except KeyboardInterrupt,e:
            print "\nAction cancelled"
    
    if options.clear_logs:
        noExtraOptions(options, "clear_logs")
        print "WARNING:\nThis action will wipe every file in the COCOMA/logs directory, do you wish to proceed?\n(y/n)"
        yes = set(['yes','y', 'ye','yey', 'Y', 'YES'])
        no = set(['no','n','nay', 'NO', 'N'])
        try:
            choice = raw_input().lower()
            if choice in yes:
                Library.removeLogs()
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
        noExtraOptions(options, "listAllDistro")
        if len(arguments)>0:
            try:
                distroList=Library.listDistributions(arguments[0])
                print distroList
            except Exception, e:
                print "Error: ",e
                print "Distribution \"%s\" not found. Check name."%(arguments[0])
        else:
            distroList=Library.listDistributions("all")

            print "\nAvailable distributions:"
            for distName in distroList:
                print distName
        
            
                 
    '''
    ################################
    listEmulators
    ###############################
    '''

    if options.listAllEmulators:
        noExtraOptions(options, "listAllEmulators")
        if len(arguments)>0:
            try:
                emuList2=Library.listEmulators(arguments[0])
                print emuList2
            except Exception, e:
                print "Error: ",e
                print "Emulator \"%s\" not found. Check name."%(arguments[0]) 
        else:
            emuList=Library.listEmulators("all")
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
                
                if Library.daemonCheck()!=False:
                    try:
                        if options.emuForce:
                            noExtraOptions(options, "xml", "emuForce")
                            (emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData,MQproducerValues) = XmlParser.xmlFileParser(arguments[0], True)
                            if (type(distroList[0]) == str): #Print forceErrors
                                for distroItem in distroList: print distroItem + "\n"
                                sys.exit()
                        elif not options.emuForce:
                            noExtraOptions(options, "xml")
                            (emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData,MQproducerValues) = XmlParser.xmlFileParser(arguments[0], False)
                            if (type(distroList[0]) == str): #Print forceErrors
                                for distroItem in distroList: print distroItem + "\n"
                                sys.exit()
                        if startTimeEmu.lower() =="now":

                            startTimeEmu1 = Library.emulationNow(2)
                            #producer.sendmsg(myName,"USER REQUEST: "+sys._getframe().f_code.co_name+" create "+arguments[0])
                            msg = {"Action":"USER REQUEST Create Emulation","File":arguments[0]}
                            producer.sendmsg(myName,msg)
                            messageReturn = EmulationManager.createEmulation(emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu1,stopTimeEmu, distroList,xmlData, MQproducerValues)

                            print messageReturn
                        else:
                            messageReturn = EmulationManager.createEmulation(emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData, MQproducerValues)
                            print messageReturn
                    except Exception, e:
                        print e
                        error = XmlParser.xmlFileParser(arguments[0], False)
                        print error
            else:
                print "Specify XML file location. See help for details"

    
    if options.emuNow and options.xml:
        try:
            if options.emuForce:
                noExtraOptions(options, "xml", "emuNow", "emuForce")
                (emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData,MQproducerValues) = XmlParser.xmlFileParser(arguments[0], True)
            elif not options.emuForce:
                noExtraOptions(options, "xml", "emuNow")
                (emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData,MQproducerValues) = XmlParser.xmlFileParser(arguments[0], False)
            startTimeEmu = Library.emulationNow(2)
            #producer.sendmsg(myName,'USER REQUEST: '+sys._getframe().f_code.co_name+' create '+arguments[0])
            msg = {"Action":"USER REQUEST Create Emulation","File":arguments[0]}
            producer.sendmsg(myName,msg)
            messageReturn=EmulationManager.createEmulation(emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData, MQproducerValues)
            print messageReturn
        except Exception,e:
            print "\n\nERROR2\n\n"
            error = XmlParser.xmlFileParser(arguments[0], True)
            print error


def getVersion():
     try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')

        c = conn.cursor()
        #print "In producer MQconfig: "+enabled+" "+vhost+" "+exchange+" "+user+" "+password+" "+host+" "+topic
        c.execute('SELECT version from config')
        config = c.fetchall()
        #for par in config:
            #print "version in config: "+str(par[0])
            #for i in range(0,6):
            #print "enabled: "+str(par[0])+", vhost: "+par[1]+", exchange: "+par[2]+", user: "+par[3]+", password: "+par[4]+", host: "+par[5]+", topic: "+par[6]
        #print "version in config: "+str(config[0][0])
        conn.commit()
        return str(config[0][0])
        c.close()

     except sqlite.Error, e:
        print " SQL Error %s:" % e.args[0]
        print e
        return "<error>" + str(e) + "</error>"
        sys.exit(1)        

def noExtraOptions(options, *arg):
    options = vars(options)
    for argOption in arg:
        Library.removeFromDict(options, argOption)
    for optionValue in options.values():
        if not (optionValue == False):
            print "Bad option combination"
            sys.exit()

if __name__ == '__main__':
    main()
