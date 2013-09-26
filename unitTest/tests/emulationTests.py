import unittest, requests
import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import subprocess
from subprocess import *

class EmulationTests():    
        
    global URL
    URL = "http://127.0.0.1:5050/"

class EmulationTests():
            
    def getEmulationList(self):  # fetch list of all emulation names
        r = requests.get(URL + "emulations")
        xml = r.text
        emulations = []
        root = ET.fromstring(xml)
        for emulation in root[0]:
            emulations.append(emulation.get('name'))
        return emulations
    
    def getDistList(self):  # fetch list of all distribution names          
        r = requests.get(URL + "distributions")
        xml = r.text
        distributions = []
        root = ET.fromstring(xml)
        for dist in root[0]:
            distributions.append(dist.get('name'))
        return distributions
    
    def getEmulatorList(self):  # fetch list of all emulator names          
        r = requests.get(URL + "emulators")
        xml = r.text
        emulators = []
        root = ET.fromstring(xml)
        for emu in root[0]:
            emulators.append(emu.get('name'))
        return emulators
    
    def getTestList(self):  # fetch list of all test names          
        r = requests.get(URL + "tests")
        xml = r.text
        tests = []
        root = ET.fromstring(xml)
        for test in root[0]:
            tests.append(test.get('name'))
        return tests
    
    def getResultsList(self):  # fetch list of all result names          
        r = requests.get(URL + "results")
        xml = r.text
        results = []
        root = ET.fromstring(xml)
        for result in root[0]:
            results.append(result.get('name'))
        return results
    
    def getEmuLogsList(self):  # fetch list of all emulator logs    
        r = requests.get(URL + "logs/emulations")
        xml = r.text
        emulogs = []
        root = ET.fromstring(xml)
        for emulog in root[0]:
            emulogs.append(emulog.get('name'))
        return emulogs
            
    def testAPICalls(self, method):
        r = requests.get(URL + method)
        return r.status_code
    
    # ##Test emulation creation using xml examples
    
    def postXMLEmulation(self, xml):
        r = requests.post(URL + "emulations", data = xml)
        return (r.status_code, r.text)     
         
    def getTestDuration (self, xmlFilePath):  # Finds the duration of an Emulation from its XML file
        xmlFile = open(xmlFilePath, 'r')  # Only works when emuStartTime=NOW
        xmlParse = xmlFile.read()
        xmlFile.close()
        xmlString = parseString(xmlParse)
        durationTag = xmlString.getElementsByTagName('emustopTime')[0].toxml()
        duration = durationTag.replace('<emustopTime>', '').replace('</emustopTime>', '')
        return duration

    def testCLIInputCalls(self, Command, InputString, ExpectedOutput):  # Calls passes commands through the CLI, accepts a passed string checks for ExpectedOutput
        procTrace = subprocess.Popen(Command, shell = True, stdout = PIPE, stdin = PIPE, stderr = PIPE)
        procTraceOutput = procTrace.communicate(input = InputString)
        result = -1  # returns -1 if ExpectedOutput not found
        for x in xrange(0, len(procTraceOutput)):
            result = procTraceOutput[x].rfind(ExpectedOutput)  # checks terminal output for ExpectedOutput
            if result != -1:  # stops loop when string is found
                break
        return result  # returns >0 if ExpectedOutput found

    def testCLICalls(self, Command, ExpectedOutput):  # Calls passes commands through the CLI, checks for ExpectedOutput
        procTrace = subprocess.Popen(Command, shell = True, stdout = PIPE, stderr = PIPE)
        procTraceOutput = procTrace.communicate()
        result = -1  # returns -1 if ExpectedOutput not found
        for x in xrange(0, len(procTraceOutput)):
            result = procTraceOutput[x].rfind(ExpectedOutput)  # checks terminal output for ExpectedOutput
            if result != -1:  # stops loop when string is found
                break
        return result  # returns >0 if ExpectedOutput found
    
    @staticmethod
    def getHomepath():  # Attempts to return $COCOMA environmental variable (/home/<USER>/git/cocoma)
        try:
            HOMEPATH = os.environ['COCOMA']
            return HOMEPATH
        except:
            print "no $COCOMA environmental variable set"
