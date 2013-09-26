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
import Library

class distribution(object):
    '''
    Class object containing all the distribution variables. Will be passed around the application instead of arrays.
    '''

    stressValues = []
    runStartTime = []
    runDurations = []

    def __init__(self, durationDistro, distrType, granularity, startTimeDistro, emulatorArg, emulatorArgNotes, emulatorName, resourceTypeDist, distroArgs, distroArgsNotes, distributionsName, distributionID):
        '''
        Data container for distribution
        [{'durationDistro': u'120', 'distrType': u'linear', 'granularity': u'24', 'startTimeDistro': u'0', 'emulatorArg': {'ncpus': 0}, 'emulatorArgNotes': ['\nOK'], 'emulatorName': u'lookbusy', 'resourceTypeDist': u'cpu', 'distroArgs': {'startload': 10, 'stopload': 95}, 'distroArgsNotes': ['\nOK', '\nOK'], 'distributionsName': u'CPU_Distro'}]
        '''
        
        self.ID="none"
        self.name= self.setDistributionsName(distributionsName)
        self.duration= self.setDurationDistro(durationDistro)
        self.type= self.setDistrType(distrType)
        self.granularity= self.setGranularity(granularity)
        self.startTime= self.setStartTimeDistro(startTimeDistro)
        self.emulatorArg= self.setEmulatorArg(emulatorArg)
        self.emulatorArgNotes= self.setEmulatorArgNotes(emulatorArgNotes)
        self.emulatorName= self.setEmulatorName(emulatorName)
        self.resourceType= self.setResourceTypeDist(resourceTypeDist)
        self.distroArgs= self.setDistroArgs(distroArgs)
        self.distroArgsNotes= self.setDistroArgsNotes(distroArgsNotes)

        """
        #SETTERS
        """

    def setDistributionID(self, distributionID):
        if distributionID:
            self.ID = distributionID
        else:
            raise Exception("Distribution ID '%s' cannot be set." % (distributionID))

    def getDistributionID(self):
        
        if self.ID !="none":
            print  "self.ID",self.ID
            return self.ID
        else:
            return "none"
        
    def setDistributionsName(self, distributionsName):
        return distributionsName
                    
    def setDurationDistro(self, durationDistro):
        return durationDistro
        pass
     
    def setDistrType(self, distrType):
        distroList = Library.listDistributions("all")
        for distName in distroList:
            if distrType.lower() == distName.lower():
                return distrType
        
        raise Exception("Distribution module '%s' does not exist. Check the name" % (distrType))
            
    def setGranularity(self, granularity):
        return granularity
    
    def setStartTimeDistro(self, startTimeDistro):

        return startTimeDistro
            
    def setEmulatorArg(self, emulatorArg):
        return emulatorArg
        
    def setEmulatorArgNotes(self, emulatorArgNotes):
        return emulatorArgNotes

    def setEmulatorName(self, emulatorName):
        return emulatorName

    def setResourceTypeDist(self, resourceTypeDist):
        return resourceTypeDist
        
    
    def setDistroArgs(self, distroArgs):
        return distroArgs
           
    def setDistroArgsNotes(self, distroArgsNotes):
        return distroArgsNotes

    def setStressValues(self, StressValues):
        self.stressValues = StressValues
        
    def setRunStartTime(self, RunStartTime):
        self.runStartTime = RunStartTime
        
    def setRunDurations(self, RunDurations):
        self.runDurations = RunDurations
        
        """
        #GETTERS
        """
        
    def getStartTime(self):  # Run time for the overall distribution
        return self.startTime
    
    def getDuration(self):  # Duration for the overall distribution
        return self.duration
    
    def getID(self):
    	return self.ID
    
    def getResourceType(self):
        return self.resourceType
    
    def getStressValues(self):
        return self.stressValues
        
    def getRunStartTime(self):  # Run times for the individual resource loads
        return self.runStartTime
        
    def getRunDurations(self):  # RunDurations  for the individual resource loads
        return self.runDurations
    
    def getGranularity(self):
        return self.granularity
    
    def getStartTime(self):
        return self.startTime
