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

import unittest, time
sys.path.insert(0,'tests/')
from emulationTests import *

class TestCLI (unittest.TestCase):
    
    def getHomepath(self):
        try:
            HOMEPATH = os.environ['COCOMA']
            print HOMEPATH
            return HOMEPATH
        except:
            print "no $COCOMA environmental variable set"
            print "Using: ", HOMEPATH 
            return HOMEPATH
                   
    if __name__ == '__main__':  # Used for running the tests through CLI
        unittest.main()
  
    @classmethod
    def setUpClass(cls):  # Starts a Scheduler & API when the class is ran
        EMUTests = EmulationTests()
        EMUTests.testCLICalls("ccmsh --start scheduler lo", "")
        EMUTests.testCLICalls("ccmsh --start api lo", "")
        global runEmulation, emulationStarted
        runEmulation = "ccmsh -x " + EmulationTests.getHomepath() + "/unitTest/"
        emulationStarted = "Emulation created"
        
    @classmethod
    def tearDownClass(cls):  # Purges system and stops Scheduler & API when testing is finished
        EMUTests = EmulationTests()
        EMUTests.testCLIInputCalls("ccmsh -p", "y", "")
        EMUTests.testCLICalls("ccmsh --stop api", "")
        EMUTests.testCLICalls("ccmsh --stop scheduler", "")
        
    def setUp(self):  # Starts a scheduler & ccmshAPI if not already running at the start of each test
        EMUTests = EmulationTests()
        schedulerStarted = EMUTests.testCLICalls("ccmsh --show scheduler", "Scheduler.py")
        if schedulerStarted == -1:
            EMUTests.testCLICalls("ccmsh --start scheduler lo", "")
        apiStarted = EMUTests.testCLICalls("ccmsh --show api", "ccmshAPI.py")
        if apiStarted == -1:
            EMUTests.testCLICalls("ccmsh --start api lo", "")
            
    def tearDown(self):  # Purges the system after each test
        EMUTests = EmulationTests()
        EMUTests.testCLIInputCalls("ccmsh -p", "y", "")
          
    # ##Test Emulation creation
    
    def test_EMU_Overload(self):  # REMOVE: For testing resource overload
          EMUTests = EmulationTests()
          XML = "XMLExamples/shortTests/Overload_CPU.xml"
          result = EMUTests.testCLICalls(runEmulation + XML, "force")
          self.assertNotEquals(result, -1, "CPU Overload test Failed")
          
    def test_EMU_Force(self): #Tries to run an emulation which requires '-f' to run
          EMUTests = EmulationTests()
          XML = "XMLExamples/shortTests/Force_CPU.xml"
          result = EMUTests.testCLICalls(runEmulation + XML, "Re-send with force")
#          result = EMUTests.testCLICalls(runEmulation + XML + " -f", "Re-send with force")
          self.assertNotEquals(result, -1, "Use of force operator (-f) failed")
           
    def test_EMU_CPU(self):  # Creates a CPU emulation using CLI
          EMUTests = EmulationTests()
          XML = "XMLExamples/shortTests/CPU.xml"
          result = EMUTests.testCLICalls(runEmulation + XML, emulationStarted)
          length = EMUTests.getTestDuration(XML)
          length = int(length) + 1
          time.sleep(int(length))
          self.assertNotEquals(result, -1, "CPU-EMU creation Failed")
 
    def test_EMU_IO(self):  # Creates an IO emulation using CLI
          EMUTests = EmulationTests()
          XML = "XMLExamples/shortTests/IO.xml"
          result = EMUTests.testCLICalls(runEmulation + XML, emulationStarted)
          length = EMUTests.getTestDuration(XML)
          length = int(length) + 1
          time.sleep(int(length))
          self.assertNotEquals(result, -1, "IO-EMU creation Failed")
                   
    def test_EMU_MEM(self):  # Creates a MEM emulation using CLI
          EMUTests = EmulationTests()
          XML = "XMLExamples/shortTests/Mem.xml"
          result = EMUTests.testCLICalls(runEmulation + XML, emulationStarted)
          length = EMUTests.getTestDuration(XML)
          length = int(length) + 1
          time.sleep(int(length))
          self.assertNotEquals(result, -1, "MEM-EMU creation Failed")
                  
    def test_EMU_MEMTrap(self):  # Creates a MEM Trap emulation using CLI
          EMUTests = EmulationTests()
          XML = "XMLExamples/shortTests/MemTrap.xml"
          result = EMUTests.testCLICalls(runEmulation + XML, emulationStarted)
          length = EMUTests.getTestDuration(XML)
          length = int(length) + 1
          time.sleep(int(length))
          self.assertNotEquals(result, -1, "MEM Trap-EMU creation Failed")
                   
    def test_EMU_MULTI1(self):  # Creates a Multiple Distribution emulation using CLI
          EMUTests = EmulationTests()
          XML = "XMLExamples/shortTests/MultiDist1.xml"
          result = EMUTests.testCLICalls(runEmulation + XML, emulationStarted)
          length = EMUTests.getTestDuration(XML)
          length = int(length) + 1
          time.sleep(int(length))
          self.assertNotEquals(result, -1, "Multi Dist 1-EMU creation Failed")
                       
    def test_EMU_MULTI2(self):  # Creates a Multiple Distribution emulation using CLI
          EMUTests = EmulationTests()
          XML = "XMLExamples/shortTests/MultiDist2.xml"
          result = EMUTests.testCLICalls(runEmulation + XML, emulationStarted)
          length = EMUTests.getTestDuration(XML)
          length = int(length) + 1
          time.sleep(int(length))
          self.assertNotEquals(result, -1, "Multi Dist 2-EMU creation Failed")
             
    def test_EMU_NETWORK(self):  # Creates a Network emulation using CLI
          EMUTests = EmulationTests()
          XML = "XMLExamples/shortTests/Network.xml"
          result = EMUTests.testCLICalls(runEmulation + XML, emulationStarted)
          length = EMUTests.getTestDuration(XML)
          length = int(length) + 1
          time.sleep(int(length))
          self.assertNotEquals(result, -1, "Network-EMU creation Failed")
               
    def test_EMU_NowOperator(self):  # tries to create an Emulation with the '-n' operator 
         EMUTests = EmulationTests()
         XML = "XMLExamples/Delay_CPU.xml"
         EMUTests.testCLICalls(runEmulation + XML + " -n", "")
         length = EMUTests.getTestDuration(XML)
         length = int(length) + 5
         time.sleep(int(length))
         result = EMUTests.testCLICalls("ccmsh -l", "Executed")
         self.assertNotEquals(result, -1, "Use of '-n' (now operator)  failed")
    
    def test_EMU_Logging(self):
         EMUTests = EmulationTests()
         XML = "XMLExamples/Logging_test.xml"
         result = EMUTests.testCLICalls(runEmulation + XML, "")
         length = EMUTests.getTestDuration(XML)
         length = int(length) + 5
         time.sleep(int(length))
         result = EMUTests.testCLICalls("ls $COCOMA/logs/", "LOGGING_TEST")
         EMUTests.testCLICalls("rm $COCOMA/logs/*LOGGING_TEST*", "")
         self.assertNotEquals(result, -1, "Enable logging in XML failed")


     # ##Test general calls to the CLI

    def test_Scheduler_Start(self):  # Tests the call to start scheduler
          EMUTests = EmulationTests()
          result = EMUTests.testCLICalls("ccmsh --start scheduler lo", "Started Scheduler")
          if result == -1:
              result = EMUTests.testCLICalls("ccmsh --start scheduler lo", "already running")
          self.assertNotEquals(result, -1, "Call to start scheduler Failed")       
                
    def test_Scheduler_Show(self):  # Tests the call to Show scheduler info
          EMUTests = EmulationTests()
          result = EMUTests.testCLICalls("ccmsh --show scheduler", "Scheduler.py")
          self.assertNotEquals(result, -1, "Call to Show scheduler Failed")
                          
    def test_Scheduler_Stop(self):  # Tests the call to stop scheduler
          EMUTests = EmulationTests()
          result = EMUTests.testCLICalls("ccmsh --stop scheduler", "Killing Scheduler")
          self.assertNotEquals(result, -1, "Call to stop scheduler Failed")
                   
    def test_API_Start(self):  # Tests the call to start API
          EMUTests = EmulationTests()
          result = EMUTests.testCLICalls("ccmsh --start api lo", "Started API")  ####FIX
          if result == -1:
              result = EMUTests.testCLICalls("ccmsh --start api lo", "already running")
          self.assertNotEquals(result, -1, "Call to start API Failed")
                  
    def test_API_Show(self):  # Tests the call to Show API info
          EMUTests = EmulationTests()
          result = EMUTests.testCLICalls("ccmsh --show api", "ccmshAPI.py")
          self.assertNotEquals(result, -1, "Call to Show API Failed")
                          
    def test_API_Stop(self):  # Tests the call to stop API
          EMUTests = EmulationTests()
          result = EMUTests.testCLICalls("ccmsh --stop api", "Killing API")  ####FIX
          self.assertNotEquals(result, -1, "Call to stop api Failed")     
           
    def test_Help(self):  # Tests the call to open Help
          EMUTests = EmulationTests()
          result = EMUTests.testCLICalls("ccmsh -h", "Usage: ccmsh [option] arg")
          self.assertNotEquals(result, -1, "Call to open Help Failed")
                   
    def test_List(self):  # Tests the call to open Emulation List
          EMUTests = EmulationTests()
          EMUTests.testCLICalls(runEmulation + "XMLExamples/shortTests/Mem.xml", emulationStarted)
          result = EMUTests.testCLICalls("ccmsh -l", "---->")
          self.assertNotEquals(result, -1, "Call to open List Failed")
          result = EMUTests.testCLICalls("ccmsh -l 1-MEM_EMU", "--->")
          self.assertNotEquals(result, -1, "Call to open List Item Failed")      
                               
    def test_Result(self):  # Tests the call to open Results
          EMUTests = EmulationTests()
          EMUTests.testCLICalls(runEmulation + "XMLExamples/shortTests/Mem.xml", emulationStarted)
          result = EMUTests.testCLICalls("ccmsh -r", "---->")
          self.assertNotEquals(result, -1, "Call to open Results Failed")   
           
    def test_Distributions(self):  # Tests the call to find available distributions
          EMUTests = EmulationTests()
          availableDistros = EMUTests.getDistList()
          for x in availableDistros:  # Uses an array for all possible distributions
              result = EMUTests.testCLICalls("ccmsh -i", x)
              if result == -1:  # Stops if any one of the distributions is not found
                  break
          self.assertNotEquals(result, -1, "Call to open Distributions Failed")
                   
    def test_Emulators(self):  # Tests the call to find available Emulators
          EMUTests = EmulationTests()
          availableEmus = EMUTests.getEmulatorList()
          for x in availableEmus:  # Uses an array for all possible Emulators
              result = EMUTests.testCLICalls("ccmsh -e", x)
              if result == -1:  # Stops if any one of the Emulators is not found
                  break
          self.assertNotEquals(result, -1, "Call to open Emulators Failed")
           
    def test_DeleteEmu(self):  # Tests the call to Delete an Emulation
          EMUTests = EmulationTests()
          EMUTests.testCLICalls(runEmulation + "XMLExamples/shortTests/Mem.xml", emulationStarted)  # Creates an emulation to be deleted
          result = EMUTests.testCLICalls("ccmsh -d 1", "was deleted from DB")
          self.assertNotEquals(result, -1, "Call to open Delete Emulation Failed")
                         
    def test_Purge(self):  # Tests the call to Delete an Emulation
          EMUTests = EmulationTests()
          result = EMUTests.testCLIInputCalls("ccmsh -p", "y", "This action will wipe every scheduled job")
          self.assertNotEquals(result, -1, "Call to Purge system Failed")
                        
    def test_Jobs(self):  # Tests the call to show jobs
          EMUTests = EmulationTests()
          EMUTests.testCLICalls(runEmulation + "XMLExamples/Delay_CPU.xml", emulationStarted)  # Creates an emulation for a time in the future
          result = EMUTests.testCLICalls("ccmsh -j", "No jobs are scheduled")    
          if result == -1:
              result = EMUTests.testCLICalls("ccmsh -j", "Job:")
          self.assertNotEquals(result, -1, "Call to show jobs Failed")
