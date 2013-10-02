#!/usr/bin/env python
# Copyright 2012-2013 SAP Ltd
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

import Library, re
from datetime import datetime as dt

# distroList = []


class emulation(object):
    '''
    Class object containing all the emulation variables. Will be passed around the application instead of arrays.
    '''

                    
    def __init__(self, emulationName = None, emulationType = None, emulationLog = None, emulationLogFrequency = None, emulationLogLevel = None, resourceTypeEmulation = None, startTimeEmu = None, stopTimeEmu = None, xmlData = None, distroList = None, error = None, emulationID = None):
        '''
        Data container for emulation
        '''
        self.emulationName = self.setEmulationName(emulationName)
        self.emulationType = self.setEmulationType(emulationType)
        self.emulationLog = self.setEmulationLog(emulationLog)
        self.emulationLogFrequency = self.setEmulationLogFrequency(emulationLogFrequency)
        self.emulationLogLevel = self.setEmulationLogLevel(emulationLogLevel)
        self.resourceTypeEmulation = self.setResourceTypeEmulation(resourceTypeEmulation)
        
        self.startTimeEmu, self.stopTimeEmu = self.dataCheck(startTimeEmu, stopTimeEmu)
        
        self.distroList=[]# holds list of distributions objects
        self.xmlData=self.setXmlData(xmlData)
        self.emulationID=""
        self.emulationLifetimeID=""
        
    def setEmulationLifetimeID(self,emulationLifetimeID):
        self.emulationLifetimeID=emulationLifetimeID
        
    def getEmulationLifetimeID(self):
        rerturn = self.emulationLifetimeID
        
    def setEmulationName(self,emulationName):
        if len(emulationName)<50:
            return emulationName
        else:
            raise Exception("Name of emulation is too long")
        
    def setEmulationType(self, emulationType):
        if len(emulationType) < 50:
            return emulationType
        else:
            raise Exception("Name of emulationType is too long")
                
    def setEmulationLog(self, emulationLog):
        if emulationLog.isdigit():
            return emulationLog
        else:
            raise Exception("Log 'enable' parameter can be 1 or 0 only")
        
    def setEmulationLogFrequency(self, emulationLogFrequency):
        if emulationLogFrequency.isdigit():
            return emulationLogFrequency
        else:
            raise Exception("Wrong value for log frequency")

    def setEmulationLogLevel(self, emulationLogLevel):
        logLevels = ["debug", "info"]
        for lvl in logLevels:
            if emulationLogLevel.lower() == lvl:
                return emulationLogLevel
            
        raise Exception("Wrong value for log level, can be only: " + str(logLevels))
        
    def setResourceTypeEmulation(self, resourceTypeEmulation):
        resourceTypes = ["cpu", "mem", "net", "io", "mix"]
        for resType in resourceTypes:
            if resourceTypeEmulation.lower() == resType:
                return resourceTypeEmulation
            
        raise Exception("Wrong value for resourceTypeEmulation, can be only: " + str(resourceTypes))        
            
    def addDistribution(self, newDistribution):
        
        if newDistribution.name == None or "":
            raise Exception("Cannot add distribution without name")
        
        emulationLifetimeEndTime = int(self.stopTimeEmu)
        compareEndTime = int(newDistribution.startTime) + int(newDistribution.duration) 
        if compareEndTime > emulationLifetimeEndTime:
            raise Exception("Distribution has date longer than emulation.Check distribution name: " + newDistribution.name) 
    
        
        self.distroList.append(newDistribution)
    
    def setXmlData(self, xmlData):
        if xmlData:
            return xmlData
        else:
            raise Exception("XML data is empty, please check.")
    
    def setEmulationID(self, emulationID):
        if emulationID:
            self.emulationID = emulationID
        else:
            raise Exception("Wrong value for emulation ID:"+str(emulationID))
    
    def getEmulationID(self):
        if self.emulationID !="":
            return self.emulationID
        else:
            raise Exception("Wrong emulation ID not yet set value for emulation ID:")

    def dateOverlapCheck(self, startTime, stopTime): 
        
        startTimeSec = Library.timestamp(Library.timeConv(startTime))
        stopTimeSec = startTimeSec + float(stopTime)
        # print startTimeSec
        # print stopTimeSec
        
        dtNowSec = Library.timestamp(dt.now())
        # print "dt.now():",dt.now()
        # print "dtNow:",dtNowSec
        
        if startTimeSec <= dtNowSec or stopTimeSec <= dtNowSec:
            print "Error: Dates cannot be in the past"
            return "Error: Dates cannot be in the past"
            
    
        if startTimeSec >= stopTimeSec:
            print "Start Date cannot be the same or later than stop time"
            return 
            
         
        n = "1"
        try:
            conn = Library.dbconn()
            c = conn.cursor()
        
            c.execute('SELECT startTime, stopTime FROM emulationLifetime')
                    
            emulationLifetimeFetch = c.fetchall()
            
            if emulationLifetimeFetch:
                for row in emulationLifetimeFetch:
                    # print row
                    startTimeDBsec = Library.timestamp(Library.timeConv(row[0]))
                    stopTimeDBsec = startTimeDBsec + float(row[1])
                    
                    if startTimeSec >= startTimeDBsec and startTimeSec <= stopTimeDBsec:
                        # print "Emulation already exist for this date change the date(1)"
                        
                        n = "Emulation already exist for this date change the date(1)"
                    
                        
                        
                    if stopTimeSec >= startTimeDBsec and stopTimeSec <= stopTimeDBsec:
                        # print "Emulation already exist for this date change the date(2)"
                        n = "Emulation already exist for this date change the date(2)"
                        
                        
                    
                    if startTimeSec <= startTimeDBsec and stopTimeSec >= stopTimeDBsec:
                        # print "Emulation already exist for this date change the date(3)"
                        
                        n = "Emulation already exist for this date change the date(3)"
                        
                        
                    
            else:
                pass    
            conn.commit()
            c.close()
        except Exception, e:
            print "dateOverlapCheck() SQL Error %s:" % e.args[0]
            print e
            return str(e)
            
            
        if n == "1":
            return startTime, stopTime
        else:
            raise Exception(n)
        
    def dataCheck(self, startTime, stopTime):
        
        time_re = re.compile('\d{4}[-]\d{2}[-]\d{2}[T,t]\d{2}[:]\d{2}[:]\d{2}')
        
        
        if time_re.match(startTime): 
        # and time_re.match(stopTime) :
            # print "date is correct"
            # checking the date overlap
            return self.dateOverlapCheck(startTime, stopTime)
        else:
            print "Date incorrect use YYYY-MM-DDTHH:MM:SS format "
            raise Exception("Date incorrect use YYYY-MM-DDTHH:MM:SS format ")
