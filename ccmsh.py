#!/usr/bin/env python
'''
Created on 4 Sep 2012

@author: i046533
'''


import optparse,sys,Pyro4
#import argparse - new version of optparse
import EmulationManager,XmlParser

def main():
    #checking for daemon
    if daemonCheck()==0:
        sys.exit(0)
    #define daemon
    uri ="PYRO:scheduler.daemon@localhost:51889"
    daemon=Pyro4.Proxy(uri)

    #Trying to group things
    parser = optparse.OptionParser()
    
    listEmu = optparse.OptionGroup(parser, 'List existing emulations')
    listEmu.add_option('-l', '--list', action='store_true', default=False,dest='listAll',help='[emulationID] [all]  List of emulations by ID or all')
    listEmu.add_option('--list-name', action='store_true', default=False,dest='listName', help='[emulationName] List of emulations by name')
    listEmu.add_option('--list-active', action='store_true', default=False,dest='listActive', help='List of active emulations')
    listEmu.add_option('--list-jobs', action='store_true', default=False,dest='listJobs', help='List of active Jobs running on Scheduler daemon')
        
    
    createEmu = optparse.OptionGroup(parser, 'Create new emulations')
    createEmu.add_option('-x', '--xml', action='store_true', dest='xml',default=False, help='[file.xml] enter name XML document')
    
    updateEmu = optparse.OptionGroup(parser, 'Update emulations')
    updateEmu.add_option('-u', '--update', action='store_true', dest='updateID',default=False, help='Update already created emulation. Usage: -u [emulationID] [emulationName] [distributionType] [resourceType] [emulationType] [startTime] [stopTime] [distributionGranularity] [startLoad] [stopLoad] . If no value needs to be changed enter NULL')
    
    
    deleteEmu = optparse.OptionGroup(parser, 'Delete emulations')
    deleteEmu.add_option('-d', '--delete', action='store_true',default=False, dest='deleteID', help='[emulationID] Deletes full emulation')
    deleteEmu.add_option('--purge', action='store_true',default=False, dest='purge_all', help='[all] clears everything. !!USE WITH CAUTION!!')
    
    
        
    parser.add_option_group(listEmu)
    parser.add_option_group(createEmu)
    parser.add_option_group(deleteEmu)
    parser.add_option_group(updateEmu)
       

    options, arguments = parser.parse_args()
    #catch empty arguments
    if len(arguments)>0:
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
            
               
        if options.listActive:
            EmulationManager.getEmulation("NULL","NULL",0,1)
            sys.exit(1)
        
        if options.listAll:
            if arguments[0]=="all":
                EmulationManager.getEmulation("NULL","NULL",1,0)
            else:
                EmulationManager.getEmulation("NULL",arguments[0],0,0)
                    
        if options.listJobs:
            if arguments[0]=="all":
                for job in daemon.listJobs():
                    
                    print job
                    
            else:
                
                for job in daemon.listJobs():
                    if job.name==arguments[0]:
                        print job
        
        if options.listName:
            EmulationManager.getEmulation(arguments[0],"NULL",0,0)
                
        if options.listActive:
            if arguments[0]=="all":
                #TO-DO: List inactive values with 0 param
                print "Listing all active values"
                EmulationManager.getEmulation("NULL","NULL",0,1)
                  
        if options.deleteID:
            #TO-DO: List inactive values with 0 param
            print "Deleting ID: ",arguments[0]
            EmulationManager.deleteEmulation(arguments[0])
        
        if options.purge_all:
            print "this is purge all ccmsh"
            if arguments[0]=="all":
                EmulationManager.purgeAll()
                
              
        if options.xml:  
                EmulationManager.dataCheck(startTime,stopTime)
                (emulationName, distributionType, resourceType, emulationType, startTime, stopTime, distributionGranularity, startLoad, stopLoad) = XmlParser.xmlReader(arguments[0])
                EmulationManager.createEmulation(emulationName, distributionType, resourceType, emulationType, startTime, stopTime, distributionGranularity,startLoad, stopLoad)
        
    else:
        parser.print_help()
        
def daemonCheck():
    '''
    Checking if Scheduler Daemon is started
    '''
    uri ="PYRO:scheduler.daemon@localhost:51889"

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


