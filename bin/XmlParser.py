#Copyright 2012 SAP Ltd
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

#Copyright 2012 SAP Ltd
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

'''
----------------------------------SPAIN-----------------------------------

<?xml version="1.0" encoding="UTF-8"?>
<emulation xmlns="http://api.bonfire-project.eu/doc/schemas/occi"> 
        <name>myRubyEmu</name>
        <stopTime>180</stopTime>
        <emulationType>Mix</emulationType>
        <startTime>2013-11-22T17:22:01</startTime>
        <distributions>
                <name>CPU-ruby</name>
                <duration>60</duration>
                <granularity>6</granularity>
                <distribution name="linear" href="/distributions/linear"/>
                <startTime>5</startTime>
                <emulator-params>
                        <ncpus>0</ncpus>
                        <resourceType>CPU</resourceType>
                </emulator-params>
                <startLoad>10</startLoad>
                <stopLoad>90</stopLoad>
                <emulator name="lookbusy" href="/emulators/stressapptest"/>
        </distributions>
        <resourceType>Mix</resourceType>
</emulation>

----------------------------------SPAIN-----------------------------------

'''
from xml.dom.minidom import parseString, Node
import DistributionManager,sys,EmulationManager



def xmlReader(filename):
    
    print "This is XML Parser"
    
    
    #open the xml file for reading:
    file = open(filename,'r')
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()
    #parse the xml you got from the file
    (emulationName,emulationType,emulationLog,emulationLogFrequency, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList)=xmlParser(data)
    return emulationName,emulationType,emulationLog,emulationLogFrequency, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList

def xmlParser(xmlData):
    emulationLogFrequency = "3"
    emulationLog="0"
    
    ##new##
    dom2 = parseString(xmlData)
    distroList = []


    distributionsXml=dom2.getElementsByTagName('distributions')
    #emulationName=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emulationName')[0].firstChild.data
    emulationName=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('name')[0].firstChild.data
    
    #if <log> block is written in XML file we will find it and read it, if not we will just set default values 
    try:
        emulationLog=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('log')[0].getElementsByTagName('enable')[0].firstChild.data
        
        try:
        
            emulationLogFrequency=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('log')[0].getElementsByTagName('frequency')[0].firstChild.data
        except Exception, e:
            print "Setting emulationLogFrequency to default value of 3sec"
            
    
    except Exception, e:
        print "Logging is Off"
        
    
    emulationType=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emulationType')[0].firstChild.data
    resourceTypeEmulation=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('resourceType')[0].firstChild.data
    startTimeEmu=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('startTime')[0].firstChild.data
    stopTimeEmu=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('stopTime')[0].firstChild.data
    

    
    
    
    print "##########################"
    print "emulation name: ",emulationName
    print "emulation type: ",emulationType
    print "resource type: ",resourceTypeEmulation
    print "start time: ",startTimeEmu
    print "stop time: ",stopTimeEmu
    print "##########################"
    
    n=0
    for node in distributionsXml:
        print "n: ",n
        #Loading distribution type by module (linear, parabola, etc.)
        
        distribution = dom2.getElementsByTagName('distribution')[n]
        distrType = distribution.attributes["name"].value
        
        #getting resource type of distribution CPU,IO,MEM or NET
        resourceTypeDist = dom2.getElementsByTagName('emulator-params')[n].getElementsByTagName('resourceType')[0].firstChild.data
            
                
        try:
            moduleMethod=DistributionManager.loadDistributionArgNames(distrType)
            
            distroArgsLimitsDict=moduleMethod(resourceTypeDist)
            moduleArgs=distroArgsLimitsDict.keys()
            
            print "moduleArgs:",moduleArgs
        except IOError, e:
            print "Unable to load module name \"",distrType,"\" error:"
            print e
            sys.exit(0) 
        '''
        loading emulator args
        '''
        #emulator = dom2.getElementsByTagName('emulator')[n]
        #emulatorName = emulator.attributes["name"].value
    
        emulator = dom2.getElementsByTagName('emulator')[n]
        emulatorType = emulator.attributes["name"].value
        
        
        print "emulatorType,resourceTypeDist:",emulatorType,resourceTypeDist        
        try:
            print "trying to load emulatorType:",emulatorType
            EmulatorModuleMethod=DistributionManager.loadEmulatorArgNames(emulatorType)
            #argNames={"fileQty":{"upperBound":10,"lowerBound":0}}
            emulatorArgsLimitsDict=EmulatorModuleMethod(resourceTypeDist)
            emulatorArgs=emulatorArgsLimitsDict.keys()
            
            print "emulatorArgs:",emulatorArgs
        except IOError, e:
            print "Unable to load module name \"",emulatorType,"\" error:"
            print e
            sys.exit(0)    
        
        
        #get things inside "distributions"
        startTimeDistro = dom2.getElementsByTagName('distributions')[n].getElementsByTagName('startTime')[0].firstChild.data
        durationDistro = dom2.getElementsByTagName('duration')[n].firstChild.data
        granularity= dom2.getElementsByTagName('granularity')[n].firstChild.data
         
        distroArgs={}
        a=0
        #for things in moduleArgs:
        '''
        Getting all the arguments for distribution
        ''' 
        distroArgsNotes=[]   
        for args in moduleArgs:
            try:
               
                #arg0 = dom2.getElementsByTagName(moduleArgs[a])[n].firstChild.data
                arg0 = dom2.getElementsByTagName('distributions')[n].getElementsByTagName(moduleArgs[a])[0].firstChild.data
                print "Distro Arg",a," arg Name: ", moduleArgs[a]," arg Value: ",arg0
                
                distributionsLimitsDictValues = distroArgsLimitsDict[moduleArgs[a]]
                print "boundsCompare(arg0,distributionsLimitsDictValues):",boundsCompare(arg0,distributionsLimitsDictValues)


                checked_distroArgs,checkDistroNote = boundsCompare(arg0,distributionsLimitsDictValues)                
                distroArgsNotes.append(checkDistroNote)
                distroArgs.update({moduleArgs[a]:checked_distroArgs})                
                
                
                #distroArgs.update({moduleArgs[a]:arg0})
                a= a+1
                #print a, moduleArgs[a]
            except Exception,e:
                    print e 
                    sys.exit(0)
                    #print e, "setting value to NULL"
                    #arg0="NULL"
                    #print arg0
                    #arg.append(arg0)
                
                
                
                    arg0="NULL"
                    #arg.append(arg0)
                    a= a+1
        '''
        getting all the arguments for emulator
        '''
        emulatorArg={}
        emulatorArgNotes=[]
        a=0
        #for things in moduleArgs:
        
        for args in emulatorArgs:
            try:
                
                #arg0 = dom2.getElementsByTagName(moduleArgs[a])[n].firstChild.data
                arg0 = dom2.getElementsByTagName('distributions')[n].getElementsByTagName(emulatorArgs[a])[0].firstChild.data
                print "Emulator Arg",a," arg Name: ", emulatorArgs[a]," arg Value: ",arg0
                #emulatorArgDict={emulatorArgs[a]:arg0}
                
                emulatorLimitsDictValues = emulatorArgsLimitsDict[emulatorArgs[a]]
                print "boundsCompare(arg0,emulatorLimitsDictValues):",boundsCompare(arg0,emulatorLimitsDictValues)
                checked_emuargs,check_note = boundsCompare(arg0,emulatorLimitsDictValues)                
                emulatorArg.update({emulatorArgs[a]:checked_emuargs})
                emulatorArgNotes.append(check_note)
                
                #append(emulatorArgs[a]:arg0)
                a= a+1
                #print a, moduleArgs[a]
            except Exception, e:
                print e
                sys.exit(0)
                    #arg0="NULL"
                    #print arg0
                    #arg.append(arg0)
                
                
                
                arg0="NULL"
                emulatorArg.append(arg0)
                a= a+1
        
        print "emulatorArg:",emulatorArg
                    #a=a+1
        
        resourceTypeDist = dom2.getElementsByTagName('emulator-params')[n].getElementsByTagName('resourceType')[0].firstChild.data 
        #dom2.getElementsByTagName('resourceType')[n].firstChild.data
        ##############
        
        #get attributes

        #distributions= dom2.getElementsByTagName('distributions')[n]
        #distributionsName = distributions.attributes["name"].value
        distributionsName=dom2.getElementsByTagName('distributions')[n].getElementsByTagName('name')[0].firstChild.data
        
        emulator = dom2.getElementsByTagName('emulator')[n]
        emulatorName = emulator.attributes["name"].value
        
        ##############
        
        
        #add every emulation in the dictionary
        distroDict={"distributionsName":distributionsName,"startTimeDistro":startTimeDistro,"durationDistro":durationDistro,"granularity":granularity,"distrType":distrType,"distroArgs":distroArgs,"emulatorName":emulatorName,"emulatorArg":emulatorArg,"resourceTypeDist":resourceTypeDist,"emulatorArgNotes":emulatorArgNotes,"distroArgsNotes":distroArgsNotes}
        
       
        
        print "---->",distributionsName
        print "start time: ",startTimeDistro
        print "duration: ",durationDistro
        print "granularity: ", granularity
        print "distribution type: ",distrType
        
        #listing all available distribution parameters
        
        print "distroArgs",distroArgs
                    
        print "emulator:", emulatorName
        print "resource type: ", resourceTypeDist
        
        #atr = dom2.documentElement.getAttributeNode('name').nodeValue
        # print atr
        #emulator = dom2.getElementsByTagName('emulator')[n].firstChild.data
        distroList.append(distroDict)
        n=n+1
        # print "Distro ",n
        #print durationDistro,  startTimeDistro, distribution,emulator 
        
        #    CPU-dis-1        Mix          1              3                        Mix               now         180       [{'distroArgs': {'startLoad': u'10', 'stopLoad': u'90'}, 'emulatorName': u'lookbusy', 'distrType': u'linear', 'resourceTypeDist': u'CPU', 'startTimeDistro': u'5', 'distributionsName': u'CPU-dis-1', 'durationDistro': u'170', 'emulatorArg': {'ncpus': u'0'}, 'granularity': u'10'}] 
                                                                                                                                            
    print emulationName,emulationType,emulationLog,emulationLogFrequency, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList
    
    return emulationName,emulationType,emulationLog,emulationLogFrequency, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList


def boundsCompare(xmlValue,LimitsDictValues):
    upperBound=int(LimitsDictValues["upperBound"])
    lowerBound=int(LimitsDictValues["lowerBound"])
    xmlValue=int(xmlValue)
    
    if xmlValue >= lowerBound:
        if xmlValue <= upperBound:
            print "1 ",xmlValue,upperBound,lowerBound
            return_note ="\nOK"
            return xmlValue, return_note
            
        else:
            print "Higher than upperBound taking maximum value"
            print "2 ",xmlValue,upperBound,lowerBound
            return_note ="\nThe scpecified value "+str(xmlValue)+" was higher than the maximum limit "+str(upperBound)+" changing to the maximum limit"
            return upperBound , return_note 
    else:
        print "Lower than lowerBound taking minimum value"
        print "3 ",xmlValue,upperBound,lowerBound
        return_note ="\nThe scpecified value "+str(xmlValue)+" was lower than the minimum limit "+str(lowerBound)+" changing to the maximum limit"
        return lowerBound, return_note

    
def parse_tests(xmlStream):
    dom2 = parseString(xmlStream)

    testNameXml=dom2.getElementsByTagName('testName')[0].firstChild.data
    ##emulationName=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emulationName')[0].firstChild.data
    #emulationName=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('name')[0].firstChild.data
    print "Filename: ",testNameXml
    return testNameXml

if __name__ == '__main__':
    
    #filename = "xmldoc.xml"
    #xmlFileReader(filename)
    xmlData='''
<emulation>
  <name>Emu-CPU-RAM-IO</name>
  <emulationType>Mix</emulationType>
  <resourceType>Mix</resourceType>
  <startTime>now</startTime>
  <!--duration in seconds -->
  <stopTime>180</stopTime>
  
  <distributions> 
   <name>CPU-dis-1a</name>
     <startTime>5</startTime>
     <!--duration in seconds -->
     <duration>30</duration>
     <granularity>3</granularity>
     <distribution href="/distributions/linear" name="linear" />
    <!--cpu utilization distribution range-->
      <startLoad>10</startLoad>
      <stopLoad>90</stopLoad>
      <emulator href="/emulators/stressapptest" name="lookbusy" />
      <emulator-params>
        <!--more parameters will be added -->
        <resourceType>CPU</resourceType>
    <!--Number of CPUs to keep busy (default: autodetected)-->
    <ncpus>10</ncpus>

      </emulator-params>
  </distributions>

  <log>
      <!-- Use value "1" to enable logging(by default logging is off)  -->
      <enable>1</enable>
      <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
      <frequency>3</frequency>
  </log>
  
</emulation>

    
    
    '''
    
    
    xmlParser(xmlData)
    
    
    pass