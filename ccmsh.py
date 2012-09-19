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
    updateEmu.add_option('-u', '--update', action='store_true', dest='updateID',default=False, help='Update already created emulationl')
    
    
    deleteEmu = optparse.OptionGroup(parser, 'Delete emulations')
    deleteEmu.add_option('-d', '--delete', action='store_true',default=False, dest='deleteID', help='[emulationID] Deletes full emulation')
    
    
    
    argsEmu = optparse.OptionGroup(parser, 'Arguments we can use with above Options')
    argsEmu.add_option('-n', '--emulationName', action='store_true', dest='argName',default=False, help='Enter name of emulation')
    argsEmu.add_option('-i', '--distributionType', action='store_true', dest='argDistributionType',default=False, help='Enter type of Distribution')
    argsEmu.add_option('-r', '--resourceType', action='store_true', dest='argResourceType',default=False, help='Enter type of Resource')
    argsEmu.add_option('-e', '--emulationType', action='store_true', dest='argEmulationType',default=False, help='Enter type of Emulation')
    argsEmu.add_option('-s', '--startTime', action='store_true', dest='argStartTime',default=False, help='[YYYY-MM-DDTHH:MM:SS] Enter Start Time of Emulation')
    argsEmu.add_option('-t', '--stopTime', action='store_true', dest='argStopTime',default=False, help='[YYYY-MM-DDTHH:MM:SS] Enter End Time of Emulation')
    argsEmu.add_option('-g', '--granularity', action='store_true', dest='argDistributionGranularity',default=False, help='Enter granularity of Distribution')
    argsEmu.add_option('-a', '--startLoad', action='store_true', dest='argStartLoad',default=False, help='Enter start load for Linear Distribution')
    argsEmu.add_option('-o', '--stopLoad', action='store_true', dest='argStopLoad',default=False, help='Enter stop load for Linear Distribution')
    
        
    parser.add_option_group(listEmu)
    parser.add_option_group(createEmu)
    parser.add_option_group(deleteEmu)
    parser.add_option_group(updateEmu)
    parser.add_option_group(argsEmu)
    

    options, arguments = parser.parse_args()
    
    #catch empty arguments
    if len(arguments) !=1 and options.listAll:
        EmulationManager.getEmulation("NULL","NULL",1,0)
        sys.exit(1)
    
    if len(arguments) !=1 and options.listJobs:
               
        for job in daemon.listJobs():
            print job
        
        
        sys.exit(1)
        
    if len(arguments) !=1 and options.listActive:
        EmulationManager.getEmulation("NULL","NULL",0,1)
        sys.exit(1)
        
                
    if len(arguments) == 1:
        values = arguments
        
        if options.listAll:
            for listAll in values:
                print listAll
                if listAll=="all":
                    EmulationManager.getEmulation("NULL","NULL",1,0)
                else:
                    EmulationManager.getEmulation("NULL",listAll,0,0)
                    
        if options.listJobs:
            for listJobs in values:
                print listJobs
                if listJobs=="all":
                    for job in daemon.listJobs():
                        print job
                    
                else:
                    for job in daemon.listJobs():
                        if job.name==listJobs:
                            print job
                        
                    
        
        if options.listName:
            for listName in values:
                print listName
                EmulationManager.getEmulation(listName,"NULL",0,0)
                
        if options.listActive:
            for listActive in values:
                #TO-DO: List inactive values with 0 param
                print "Listing all active values"
                EmulationManager.getEmulation("NULL","NULL",0,1)
                  
        if options.deleteID:
            for deleteID in values:
                #TO-DO: List inactive values with 0 param
                print "Deleting ID: ",deleteID
                EmulationManager.deleteEmulation(deleteID)
            
        if options.xml:
            for xml in values:
                print xml
                (emulationName, distributionType, resourceType, emulationType, startTime, stopTime, distributionGranularity, startLoad, stopLoad) = XmlParser.xmlReader(xml)
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


