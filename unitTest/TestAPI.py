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

import sys
sys.path.insert(0,'tests/')
import unittest, time
from emulationTests import *


class TestAPI(unittest.TestCase):
    
    global HOMEPATH
    HOMEPATH = EmulationTests.getHomepath()
    
    if __name__ == '__main__':  #Used for running the tests through CLI
        unittest.main()
    
    @classmethod
    def setUpClass(cls):    #Starts a Scheduler & API when the class is ran
        EMUTests = EmulationTests()
        schedulerStarted = EMUTests.testCLICalls("ccmsh --show scheduler", "Scheduler.py")
        if schedulerStarted == -1:
            EMUTests.testCLICalls("ccmsh --start scheduler lo", "")
        else:
            EMUTests.testCLICalls("ccmsh --stop scheduler", "")
            EMUTests.testCLICalls("ccmsh --start scheduler lo", "")
        apiStarted = EMUTests.testCLICalls("ccmsh --show api", "ccmshAPI.py")
        if apiStarted == -1:
            EMUTests.testCLICalls("ccmsh --start api lo", "")
        else:
            EMUTests.testCLICalls("ccmsh --stop api", "")
            EMUTests.testCLICalls("ccmsh --start api lo", "")
        time.sleep(1)   #sleeps for 1 second (allows API to be finish being created before tests run)
        
    @classmethod
    def tearDownClass(cls): #Purges system and stops Scheduler & API when testing is finished
        EMUTests = EmulationTests()
        EMUTests.testCLIInputCalls("ccmsh -p", "y", "")
        EMUTests.testCLICalls("ccmsh --stop api", "")
        EMUTests.testCLICalls("ccmsh --stop scheduler", "")  
    
         
    def test_List_Emulation(self):   #Tests call for Emulation list
        testClass = EmulationTests()
        result = EmulationTests.testAPICalls(testClass, "emulations")
        self.assertEqual(result, 200, "Emulation list call failed")
            
    def test_List_Emulator(self):    #Tests call for Emulator list
        testClass = EmulationTests()
        result = EmulationTests.testAPICalls(testClass, "emulators")
        self.assertEqual(result, 200, "Emulator list call failed")
            
    def test_List_Distributions(self):    #Tests call for Distribution list
        testClass = EmulationTests()
        result = EmulationTests.testAPICalls(testClass, "distributions")
        self.assertEqual(result, 200, "Distribution list call failed")
            
    def test_List_Results(self): #Tests call for Results list
        testClass = EmulationTests()
        result = EmulationTests.testAPICalls(testClass, "results")
        self.assertEqual(result, 200, "Results list call failed")
        
    def test_List_Jobs(self): #Tests call for Results list
        testClass = EmulationTests()
        result = EmulationTests.testAPICalls(testClass, "jobs")
        self.assertEqual(result, 200, "Jobs list call failed")
            
    def test_List_Logs(self): #Tests call for Log list
        testClass = EmulationTests()
        result = EmulationTests.testAPICalls(testClass, "logs")
        self.assertEqual(result, 200, "Logs list call failed")
            
    def test_List_SysLogs(self): #Tests call for System logs
        testClass = EmulationTests()
        result = EmulationTests.testAPICalls(testClass, "logs/system")
        self.assertEqual(result, 200, "System logs list call failed")
            
    def test_List_EmuLogs(self): #Tests call for Emulation logs
        testClass = EmulationTests()
        result = EmulationTests.testAPICalls(testClass, "logs/emulations")
        self.assertEqual(result, 200, "Emulation logs call failed")
        
    def test_List_Tests(self):   #Tests call for list of available test AML's
        testClass = EmulationTests()
        result = EmulationTests.testAPICalls(testClass, "tests")
        self.assertEqual(result, 200, "Tests list call failed")
            
    def test_EMU_Items(self):
        testClass = EmulationTests()
        emulationArray = EmulationTests.getEmulationList(testClass)
        i=0
        for emulation in emulationArray:
            result = EmulationTests.testAPICalls(testClass, "emulations/"+ emulation)
            self.assertEqual(result, 200, "Emulation list item "+str(i)+" failed")
            i+=1
               
    def test_Dist_Items(self):
        testClass = EmulationTests()
        distArray = EmulationTests.getDistList(testClass)
        i=0
        for dist in distArray:
            result = EmulationTests.testAPICalls(testClass, "distributions/"+ dist)
            self.assertEqual(result, 200, "Dist list item "+str(i)+" failed")
            i+=1
       
    def test_Emulators(self):
        testClass = EmulationTests()
        emuArray = EmulationTests.getEmulatorList(testClass)
        i=0
        for emulator in emuArray:
            result = EmulationTests.testAPICalls(testClass, "emulators/"+ emulator)
            self.assertEqual(result, 200, "Emulator list item "+str(i)+" failed")
            i+=1
                
    def test_Tests(self):
        testClass = EmulationTests()
        testArray = EmulationTests.getTestList(testClass)
        i=0
        for test in testArray:
            result = EmulationTests.testAPICalls(testClass, "tests/"+ test)
            self.assertEqual(result, 200, "Test list item "+str(i)+" failed")
            i+=1
        
    def test_Results(self):
        testClass = EmulationTests()
        resultArray = EmulationTests.getResultsList(testClass)
        i=0
        for results in resultArray:
            result = EmulationTests.testAPICalls(testClass, "results/"+ results)
            self.assertEqual(result, 200, "Results list item "+str(i)+" failed")
            i+=1
        
    def test_EMU_Logs(self):
        testClass = EmulationTests()
        emuLogsArray = EmulationTests.getEmuLogsList(testClass)
        i=0
        for emuLog in emuLogsArray:
            result = EmulationTests.testAPICalls(testClass, "logs/emulations/"+ emuLog)
            self.assertEqual(result, 200, "Emulations logs list item "+str(i)+" failed")
            i+=1
                
    ###Test emulation creation using xml examples        
           
        
    def test_EMUcr_CPU(self):
        testClass = EmulationTests()
        xmlPath = HOMEPATH + "/unitTest/XMLExamples/shortTests/CPU.xml"
        f = open(xmlPath, 'r')
        result, resultStr = EmulationTests.postXMLEmulation(testClass, f.read())
        length = testClass.getTestDuration(xmlPath)
        length = int(length) + 3
        time.sleep(int(length))
        self.assertEqual(result, 201, xmlPath + "\n" + resultStr)           
                
    def test_EMUcr_IO(self):
        testClass = EmulationTests()
        xmlPath = HOMEPATH + "/unitTest/XMLExamples/shortTests/IO.xml"
        f = open(xmlPath, 'r')
        result, resultStr = EmulationTests.postXMLEmulation(testClass, f.read())
        length = testClass.getTestDuration(xmlPath)
        length = int(length) + 3
        time.sleep(int(length))
        self.assertEqual(result, 201, xmlPath + "\n" + resultStr) 
    
    def test_EMUcr_IOtrap(self):
        testClass = EmulationTests()
        xmlPath = HOMEPATH + "/unitTest/XMLExamples/shortTests/IOTrap.xml"
        f = open(xmlPath, 'r')
        result, resultStr = EmulationTests.postXMLEmulation(testClass, f.read())
        length = testClass.getTestDuration(xmlPath)
        length = int(length) + 3
        time.sleep(int(length))
        self.assertEqual(result, 201, xmlPath + "\n" + resultStr)        
            
    def test_EMUcr_MEM(self):
        testClass = EmulationTests()
        xmlPath = HOMEPATH + "/unitTest/XMLExamples/shortTests/Mem.xml"
        f = open(xmlPath, 'r')
        result, resultStr = EmulationTests.postXMLEmulation(testClass, f.read())
        length = testClass.getTestDuration(xmlPath)
        length = int(length) + 3
        time.sleep(int(length))
        self.assertEqual(result, 201, xmlPath + "\n" + resultStr)        
           
    def test_EMUcr_MEMtrap(self):
        testClass = EmulationTests()
        xmlPath = HOMEPATH + "/unitTest/XMLExamples/shortTests/MemTrap.xml"
        f = open(xmlPath, 'r')
        result, resultStr = EmulationTests.postXMLEmulation(testClass, f.read())
        length = testClass.getTestDuration(xmlPath)
        length = int(length) + 3
        time.sleep(int(length))
        self.assertEqual(result, 201, xmlPath + "\n" + resultStr)
           
    def test_EMUcr_NETWORK(self):
        testClass = EmulationTests()
        xmlPath = HOMEPATH + "/unitTest/XMLExamples/shortTests/Network.xml"
        f = open(xmlPath, 'r')
        result, resultStr = EmulationTests.postXMLEmulation(testClass, f.read())
        length = testClass.getTestDuration(xmlPath)
        length = int(length) + 3
        time.sleep(int(length))
        self.assertEqual(result, 201, xmlPath + "\n" + resultStr)
           
    def test_EMUcr_MULTI1(self):
        testClass = EmulationTests()
        xmlPath = HOMEPATH + "/unitTest/XMLExamples/shortTests/MultiDist1.xml"
        f = open(xmlPath, 'r')
        result, resultStr = EmulationTests.postXMLEmulation(testClass, f.read())
        length = testClass.getTestDuration(xmlPath)
        length = int(length) + 3
        time.sleep(int(length))
        self.assertEqual(result, 201, xmlPath + "\n" + resultStr)
            
    def test_EMUcr_MULTI2(self):
        testClass = EmulationTests()
        xmlPath = HOMEPATH + "/unitTest/XMLExamples/shortTests/MultiDist2.xml"
        f = open(xmlPath, 'r')
        result, resultStr = EmulationTests.postXMLEmulation(testClass, f.read())
        length = testClass.getTestDuration(xmlPath)
        length = int(length) + 3
        time.sleep(int(length))
        self.assertEqual(result, 201, xmlPath + "\n" + resultStr)
