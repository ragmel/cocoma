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


import sqlite3 as sqlite
import sys, re, os, subprocess, psutil, Library
import DistributionManager, ccmsh, XmlParser
import Pyro4
import datetime, ccmshAPI
from datetime import datetime as dt
from subprocess import *
import logging
from logging import handlers
import pdb
from Logger import  singleLogger
import time

import Emulation
from Distribution import distribution
######
# import pika, time, datetime
import EMQproducer
######

global myName
myName = "Emulation Manager"

global HOMEPATH
HOMEPATH = Library.getHomepath()

    

def getEmulation(emulationName):
    # print "Hello this is getEmulation by name"
    
    distroList = []
    distroArgs = {}
    emulatorArg = {}
    
   
        
    try:
        conn = Library.dbconn()
        c = conn.cursor()
        
        c.execute("SELECT emulationID FROM emulation WHERE emulationName=?", [emulationName])
        emulationIdArray = c.fetchone()
        
        if emulationIdArray:
            emulationID = emulationIdArray[0]
        else:
            raise sqlite.Error("Emulation " + str(emulationName) + " not found")
            
        
        # EMULATION & EMULATION LIFETIME
        c.execute("""SELECT emulation.emulationID,emulation.emulationName, emulation.emulationType, emulation.resourceType,emulationLifetime.startTime,emulationLifetime.stopTime,emulation.xmlData,emulation.logging,emulation.logFrequency,emulation.logLevel
         FROM emulation,emulationLifetime 
         WHERE emulation.emulationID=? and emulationLifetime.emulationID = emulation.emulationID""", [emulationID])
         
        emulationTable = c.fetchall()
        if emulationTable:
            for row in emulationTable:
        
        
                emulationID = row[0]
                emulationName = row[1]
                emulationType = row[2]
                resourceTypeEmulation = row[3]
                startTimeEmu = row[4]
                stopTimeEmu = row[5]
                xmlData = row[6]
                
                logging = str(row[7])
                logFrequency = str(row[8])
                logLevel = str(row[9])
        
                  
        # DISTRIBUTION
        c.execute("""SELECT 
        distribution.distributionID,
        distribution.distributionName,
        distribution.startTime,
        distribution.duration,
        distribution.distributionGranularity,
        distribution.distributionType,
        distribution.emulator
        
        FROM distribution
        WHERE emulationID = ? """
        , [emulationID])
        
        distributionTable = c.fetchall()
        
        
        for distributions in distributionTable:
            
            # single distribution level
                
                # GET DISTRIBUTION PARAMETERS
                c.execute("""SELECT 
                DistributionParameters.paramName, 
                DistributionParameters.Value
                FROM DistributionParameters
                WHERE distributionID=?""", [distributions[0]])    
                
                distroParamsTable = c.fetchall()
                
                
                for distributionParams in distroParamsTable:
                    
                    distroArgs.update({distributionParams[0]:distributionParams[1]})
            
                
                # GET EMULATOR PARAMETERS
                c.execute("""SELECT 
                EmulatorParameters.resourceType,
                EmulatorParameters.paramName,
                EmulatorParameters.value
                
                FROM EmulatorParameters
                WHERE distributionID=?""", [distributions[0]]) 
                
                emuParamsTable = c.fetchall()                
                emulatorArg = {}
                for emuParams in emuParamsTable:
                    # print "emuParams"
                    print emuParams
                    
                    resourceTypeDist = emuParams[0]
                    
                    emulatorArg.update({emuParams[1]:emuParams[2]})
                    # print"emulatorArg"
                    # print emulatorArg
                    
                # saving single distribution elements to dictionary
                distroDict = {"distributionsID":distributions[0], "distributionsName":distributions[1], "startTimeDistro":distributions[2], "durationDistro":distributions[3], "granularity":distributions[4], "distrType":distributions[5], "emulatorName":distributions[6], "resourceTypeDist":resourceTypeDist, "emulatorArg":emulatorArg, "distroArgs":distroArgs}                    
                distroList.append(distroDict)
        
        # GET MQ params
        c.execute("SELECT enabled,vhost,exchange,user,password,host,topic FROM MQconfig")  
        mqParamsTableArr = c.fetchall()
        if len(mqParamsTableArr) == 7:
            for mqParamsTable in mqParamsTableArr:      
                enabled = str(mqParamsTable[0])
                vhost = str(mqParamsTable[1])
                exchange = str(mqParamsTable[2])
                user = str(mqParamsTable[3])
                password = str(mqParamsTable[4])
                host = str(mqParamsTable[5])
                topic = str(mqParamsTable[6])
        else:
                enabled = "no"
                vhost = ""
                exchange = ""
                user = ""
                password = ""
                host = ""
                topic = ""            
        
        
        c.close()

        return (emulationID, emulationName, emulationType, resourceTypeEmulation, startTimeEmu, stopTimeEmu, distroList, xmlData, logging, logFrequency, logLevel, enabled, vhost, exchange, user, password, host, topic)

    except sqlite.Error, e:
        print "Error getting emulation list %s:" % e.args[0]
        print e
        return str(e)
        sys.exit(1)
        

        
def deleteEmulation(emulationID):
    '''
    Deleting specific emulation by ID number 
    '''
         
    distributionName = []
    
    try:
        conn = Library.dbconn()
        c = conn.cursor()
        c.execute('SELECT distributionID,distributionName FROM distribution WHERE emulationID=?', [str(emulationID)])
                
        distributionIDfetch = c.fetchall()
        
        # getting list of distributions for emulation
        if distributionIDfetch:
            for row in distributionIDfetch:
                
                distributionID = row[0]
                distributionName.append(row[1])
                
                # deleting distribution related data
                c.execute('DELETE FROM DistributionParameters WHERE distributionID=?', [str(distributionID)])
                c.execute('DELETE FROM EmulatorParameters WHERE distributionID=?', [str(distributionID)])
                c.execute('DELETE FROM runLog WHERE distributionID=?', [str(distributionID)])
            
            c.execute('DELETE FROM distribution WHERE emulationID=?', [str(emulationID)])
            c.execute('DELETE FROM emulationLifetime WHERE emulationID=?', [str(emulationID)])
            c.execute('DELETE FROM emulation WHERE emulationID=?', [str(emulationID)])
            
            conn.commit()
            c.close()
            print "Emulation ID: ", emulationID, " was deleted from DB"
                
        else:
            # print "Emulation ID: "+str(emulationID)+" does not exists looking for name" 
            c.execute('SELECT emulationID FROM emulation WHERE emulationName=?', [str(emulationID)])
            emulationIDfetch = c.fetchall()

            for row in emulationIDfetch:
                emulationID = row[0]
            c.execute('SELECT distributionID,distributionName FROM distribution WHERE emulationID=?', [str(emulationID)])
                    
            distributionIDfetch = c.fetchall()
            
            # getting list of distributions for emulation
            if distributionIDfetch:
                for row in distributionIDfetch:
                    distributionID = row[0]
                    distributionName.append(row[1])
                    
                    # deleting distribution related data
                    c.execute('DELETE FROM DistributionParameters WHERE distributionID=?', [str(distributionID)])
                    c.execute('DELETE FROM EmulatorParameters WHERE distributionID=?', [str(distributionID)])
                    c.execute('DELETE FROM runLog WHERE distributionID=?', [str(distributionID)])
                
                c.execute('DELETE FROM distribution WHERE emulationID=?', [str(emulationID)])
                c.execute('DELETE FROM emulationLifetime WHERE emulationID=?', [str(emulationID)])
                c.execute('DELETE FROM emulation WHERE emulationID=?', [str(emulationID)])
                    
            else:
                print "Emulation Name or ID \"" + str(emulationID) + "\" does not exists" 
                return "Emulation Name or ID: " + str(emulationID) + " does not exists" 
                sys.exit(1)
            
            conn.commit()
            c.close()
            print "Emulation Name: ", emulationID, " was deleted from DB"
        # try:
        #    producer.sendmsg(myName,"USER REQUEST: "+sys._getframe().f_code.co_name+" "+str(emulationID))
        # except Exception,e:
        #    print "EXCEPTION USER INPUT: "+str(e)

    except sqlite.Error, e:
        print "Could not delete emulation: ", emulationID
        print "Error %s:" % e.args[0]
        print e
        return "Database error: " + str(e)
        sys.exit(1)
        
    
    
    
    # Now here we need to remove the emulation from the scheduler if exist
    
    daemon = Library.getDaemon()
    try:
        for Names in distributionName:
            daemon.deleteJobs(emulationID, Names)
    except:
        print "Scheduler is offline. Job cancelled."
    
    return "success"
    


def createEmulation(emulationName, emulationType, emulationLog, emulationLogFrequency, emulationLogLevel, resourceTypeEmulation, startTimeEmu, stopTimeEmu, distroList, xmlData, MQproducerValues):
    
    global producer
    producer = EMQproducer.Producer()
    # print "Who calls "+sys._getframe(0).f_code.co_name+": "+sys._getframe(1).f_code.co_name
    producer.init()

    #producer.sendmsg("Emulation Manager",str(emulationName)+": request received")
    msg = {"Action":"Emulation request received","UserEmulationName":str(emulationName)}
    producer.sendmsg(myName,msg)
    
    if startTimeEmu.lower() == "now":
        startTimeEmu = Library.emulationNow(2)
    
    try:
        # here we creating emulation object
        newEmulation = Emulation.emulation(emulationName, emulationType, emulationLog, emulationLogFrequency, emulationLogLevel, resourceTypeEmulation, startTimeEmu, stopTimeEmu, xmlData)
            
    except Exception, e:
        return "Unable to create emulation:\n" + str(e)


    distroObjList = []
    resourceOverloaded = False
    if (type(distroList)==unicode):
        sys.exit()

    try:
        for n in distroList:
            emulatorName = n["emulatorName"]
            durationDistro = n["durationDistro"]
            distributionsName = n["distributionsName"]
            resourceTypeDist = n["resourceTypeDist"]
            
            
            startTimeDistro = n["startTimeDistro"]
            granularity = n["granularity"]
            distrType = n["distrType"]
            distroArgs = n["distroArgs"]
            emulatorArg = n["emulatorArg"]
            
            newDistribution = distribution(durationDistro, distrType, granularity, startTimeDistro, emulatorArg, None, emulatorName, resourceTypeDist, distroArgs, None, distributionsName, None)    
            
            # 1. Get required module loaded
            modhandleMy = Library.loadDistribution(distrType)
            #Check if error returned
            if (type(modhandleMy) is str):
                raise Exception (modhandleMy)
            
	        # 2. Use this module for calculation and run creation   
            (stressValues, runStartTime, runDurations, triggerType) = modhandleMy(newEmulation.emulationID, newEmulation.emulationName, 0, Library.timeSinceEpoch(0), durationDistro, int(granularity), distroArgs, resourceTypeDist, HOMEPATH)
            
            newDistribution.setStressValues(stressValues)
            newDistribution.setRunStartTime(runStartTime)
            newDistribution.setRunDurations(runDurations)
            
            distroObjList.append(newDistribution)
#            resourceOverloaded, overloadedResource = checkResourceOverload(distroObjList)
            resourceOverloaded, overloadedResource = splitDistroList(distroObjList) #check if resources will become overloaded
            
            if (resourceOverloaded == False):
				newEmulation.addDistribution(newDistribution)
            else:
 				raise Exception (str(overloadedResource) + " resource will become Overloaded: Stopping execution")

        # passing on to distribution management
        DistributionManager.createDistribution(newEmulation)
#         stressValues, runStartTime, runDurations = DistributionManager.createDistribution(newEmulation)
        
    except Exception, e:
        return "Unable to create distribution:\n" + str(e)
    
            
    # emulation log creator
    
    #str(newEmulation.emulationID)+"-"+str(newEmulation.emulationName)+"-syslog"+"_"+str(newEmulation.startTimeEmu)+".csv"
    emuLoggerEM=singleLogger(myName,None,None)

       

    # create log file with XML data
    fullEmuName = str(newEmulation.emulationID) + "-" + str(newEmulation.emulationName)
    try:
        if newEmulation.emulationLog == "1":
            f = open(HOMEPATH + "/logs/" + fullEmuName + "-config" + "_" + str(newEmulation.startTimeEmu) + ".xml", 'a')    
            f.write(xmlData)
            f.closed
    except Exception, e:
        emuLoggerEM.error("Unable to create config log file." + str(e))
    
    msg = {"Action":"Emulation created","EmulationName":str(newEmulation.emulationName)}
    producer.sendmsg(myName,msg)
    emuLoggerEM.info(msg)
    #emuLoggerEM.info("Emulation '"+fullEmuName+"' was created")

    return fullEmuName

def splitDistroList(distroList):    #Splits a list of distribution objects, grouping by resource type
    distroListCPU = []
    distroListMEM = []
    
    for distroItem in distroList:
        
        if (distroItem.getResourceType().upper() == "CPU"):
            distroListCPU.append(distroItem)
            
        if (distroItem.getResourceType().upper() == "MEM"):
            distroListMEM.append(distroItem)

    resourceOverloaded, overloadedResource = checkResourceOverload(distroListCPU)
    if resourceOverloaded == False:
        resourceOverloaded, overloadedResource = checkResourceOverload(distroListMEM)
    
    return (resourceOverloaded, overloadedResource)

def checkResourceOverload(distroList):  # Checks whether an emulation will exhaust system resources
        resourceOverlap = False
        overloadedResource = ""
        maxResourceLoad = 999999  # Needs fixed
        
        for index, distroItem in enumerate(distroList):

            overloadedResource = distroItem.getResourceType().upper()
            maxResourceLoad = Library.getResourceLimit(overloadedResource)  # Sets maxResourceLoad to the system's amount of physical memory
            startTimeCurrent = int(distroItem.getStartTime())
            endTimeCurrent = startTimeCurrent + int(distroItem.getDuration())
            
            currentItemStressValues = distroItem.getStressValues()
            currentItemDurations = distroItem.getRunDurations()
            currentItemStartTimes = distroItem.getRunStartTime()
            
            for stressValue in currentItemStressValues: # Checks if a single stress value would overload the resource
                if int(stressValue) > int(maxResourceLoad):
                    resourceOverlap = True
            
            for w in xrange(0, len(distroList)):
                if int(index) != int(w):  # If the item isn't itself
                    startTimeNext = int(distroList[w].getStartTime())
                    endTimeNext = startTimeNext + int(distroList[w].getDuration())

                    if startTimeCurrent <= endTimeNext and endTimeCurrent >= startTimeNext:  # If the distributions overlap
                        if distroItem.getResourceType() == distroList[w].getResourceType():  # If the distributions are on the same resource


                            nextItemStressValues = distroList[w].getStressValues()
                            nextItemStartTimes = distroList[w].getRunStartTime()

                            for x in xrange(0, len(currentItemStartTimes)):
                                resourceLoad = distroItem.getStressValues()[x]

                                for y in xrange (0, len(nextItemStartTimes)):

                                        timeOverlap = (int(currentItemStartTimes[x]) <= int(nextItemStartTimes[y])) and \
                                        			(int(currentItemStartTimes[x]) + int(currentItemDurations[x]) >= int(nextItemStartTimes[y]))
                                                    
                                        if (timeOverlap):
                                                resourceLoad += nextItemStressValues[y]

                                        if resourceLoad > maxResourceLoad :
                                                resourceOverlap = True
                                                
	return resourceOverlap, overloadedResource  # False if no resources overlap

if __name__ == '__main__':
    distroList = [{"durationDistro": "60", "distrType": "linear_incr", "granularity": "20", "startTimeDistro": "0", "emulatorArg": {"memsleep": "0"}, "emulatorArgNotes": ["\nOK", "0"], "emulatorName": "lookbusy", "resourceTypeDist": "mem", "distroArgs": {"startload": "1000", "stopload": "100", "malloclimit": "4095"}, "distroArgsNotes": ["\nOK", "1000", "\nOK", "100"], "distributionsName": "mem_distro"}]
    createEmulation("MEM_EM", "mix", "0", "3", "debug", "mem", "now", "60", distroList, "XML", {}) # <REMOVE^
    pass
