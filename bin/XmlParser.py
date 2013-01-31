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

from xml.dom.minidom import parseString, Node
import xml.dom.minidom
import DistributionManager,sys,EmulationManager
import logging
logging.basicConfig(level=logging.DEBUG)

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
    #normal values
    dom1 = parseString(xmlData)
    #lower case values
    dom2 = parseString(xmlData.lower())
    domNode=dom2.documentElement
    
    distroList = []


    distributionsXml=dom2.getElementsByTagName('distributions')
    #emulationName=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emulationName')[0].firstChild.data
    emulationName=dom1.getElementsByTagName('emulation')[0].getElementsByTagName('emuname')[0].firstChild.data
    
    #if <log> block is written in XML file we will find it and read it, if not we will just set default values 
    try:
        emulationLog=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('log')[0].getElementsByTagName('enable')[0].firstChild.data
        
        try:
        
            emulationLogFrequency=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('log')[0].getElementsByTagName('frequency')[0].firstChild.data
        except Exception, e:
            print "Setting emulationLogFrequency to default value of 3sec"
            
    
    except Exception, e:
        print "Logging is Off"
    
    emulationType=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emutype')[0].firstChild.data
    startTimeEmu=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emustarttime')[0].firstChild.data
    resourceTypeEmulation=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emuresourcetype')[0].firstChild.data
    stopTimeEmu=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emustoptime')[0].firstChild.data
     
    
    
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
        resourceTypeDist = dom2.getElementsByTagName('emulator-params')[n].getElementsByTagName('resourcetype')[0].firstChild.data
            
                
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
        startTimeDistro = dom2.getElementsByTagName('distributions')[n].getElementsByTagName('starttime')[0].firstChild.data
        durationDistro = dom2.getElementsByTagName('duration')[n].firstChild.data
        granularity= dom2.getElementsByTagName('granularity')[n].firstChild.data
         
        distroArgs={}
        a=0
        #for things in moduleArgs:
        '''
        Getting all the arguments for distribution
        ''' 
        distroArgsNotes=[]
        print "moduleArgs",moduleArgs
        
        for args in moduleArgs:
            logging.debug("Inside distribution moduleArgs loop!")
            try:
               
                
                arg0 = dom2.getElementsByTagName('distributions')[n].getElementsByTagName(moduleArgs[a].lower())[0].firstChild.data
                print "Distro Arg",a," arg Name: ", moduleArgs[a].lower()," arg Value: ",arg0
                
                distributionsLimitsDictValues = distroArgsLimitsDict[moduleArgs[a].lower()]
                
                #checking for percentage sign
                if arg0[-1]=="%":
                    #get total amount of memory devide by 100(to get mb per single percent) and multiply on the percentage in the document 
                    print "Value is in %",distroArgsLimitsDict[moduleArgs[a].lower()]
                    import psutil
                    memReading=psutil.phymem_usage()
                    percentageInMegabytes=((memReading.total/100)*int(arg0[:-1]))/1048576 
                    print percentageInMegabytes
                    checked_distroArgs,checkDistroNote = boundsCompare(percentageInMegabytes,distributionsLimitsDictValues)
                

                else:
                    checked_distroArgs,checkDistroNote = boundsCompare(arg0,distributionsLimitsDictValues)         
                    print "checked_distroArgs,checkDistroNote",checked_distroArgs,checkDistroNote       
                
                distroArgsNotes.append(checkDistroNote)
                distroArgs.update({moduleArgs[a].lower():checked_distroArgs})                
                
                
                #distroArgs.update({moduleArgs[a]:arg0})
                a+=1
                #print a, moduleArgs[a]
            except Exception,e:
                    logging.exception("Error getting distribution arguments. Check stress values of "+"\""+str(moduleArgs[a].lower())+"\"")
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
        print "emulatorArgs",emulatorArgs
        for args in emulatorArgs:
            logging.debug("Inside emulatorArgs loop!")
            try:
                print "emulatorArgs[a]",emulatorArgs[a].lower()
                arg0 = dom2.getElementsByTagName('distributions')[n].getElementsByTagName(emulatorArgs[a].lower())[0].firstChild.data
                print "Emulator Arg",a," arg Name: ", emulatorArgs[a].lower()," arg Value: ",arg0
                #emulatorArgDict={emulatorArgs[a]:arg0}
                
                emulatorLimitsDictValues = emulatorArgsLimitsDict[emulatorArgs[a].lower()]
                checked_emuargs,check_note = boundsCompare(arg0,emulatorLimitsDictValues,emulatorArgs[a].lower())                
                emulatorArg.update({emulatorArgs[a].lower():checked_emuargs})
                emulatorArgNotes.append(check_note)
                
                #append(emulatorArgs[a]:arg0)
                a+=1
                #print a, moduleArgs[a]
            except Exception, e:
                print e
                logging.exception("Not all emulator arguments are in use, setting Value of "+str(emulatorArgs[a].lower())+" to NULL")
                    #arg0="NULL"
                    #print arg0
                    #arg.append(arg0)
                arg0="NULL"
                emulatorArg.append(arg0)
                a= a+1
        
        print "emulatorArg:",emulatorArg
                    #a=a+1
        
        resourceTypeDist = dom2.getElementsByTagName('emulator-params')[n].getElementsByTagName('resourcetype')[0].firstChild.data 
        #dom2.getElementsByTagName('resourceType')[n].firstChild.data
        ##############
        
        #get attributes

        #distributions= dom2.getElementsByTagName('distributions')[n]
        #distributionsName = distributions.attributes["name"].value
        distributionsName=dom1.getElementsByTagName('distributions')[n].getElementsByTagName('name')[0].firstChild.data
        
        emulator = dom1.getElementsByTagName('emulator')[n]
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


def boundsCompare(xmlValue,LimitsDictValues,variableName = None):
    #ignoring IP address(variableName=emulatorArgs[a])
    if  variableName == "remoteip":
        return_note ="\nOK"
        return xmlValue,return_note
    
    
    upperBound=int(LimitsDictValues["upperBound"])
    lowerBound=int(LimitsDictValues["lowerBound"])
    xmlValue=int(xmlValue)
    
    
    if xmlValue >= lowerBound:
        if xmlValue <= upperBound:
            print "\n1)Xml value",xmlValue,"is within the bounds"
            return_note ="\nOK"
            return xmlValue, return_note
            
        else:
            print "\n2)Xml value",xmlValue,"Higher than upperBound taking maximum value",upperBound
            return_note ="\nThe scpecified value "+str(xmlValue)+" was higher than the maximum limit "+str(upperBound)+" changing to the maximum limit"
            return upperBound , return_note 
    else:
        print "\n3)Xml value",xmlValue,"lover than lowerBound taking maximum value",lowerBound
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
  <emuname>NETworkCLIent</emuname>
  <emuType>Mix</emuType>
  <emuResourceType>NET</emuResourceType>
  <emuStartTime>now</emuStartTime>
  <!--duration in seconds -->
  <emuStopTime>25</emuStopTime>
  
    <distributions>
     <name>Distro1</name>
     <startTime>5</startTime>
     <!--duration in seconds -->
     <duration>30</duration>
     <granularity>3</granularity>
     <distribution href="/distributions/linear" name="linear" />
     <!--Megabytes for memory -->
      <startLoad>10%</startLoad>
      <stopLoad>1000</stopLoad>
      <emulator href="/emulators/stressapptest" name="lookbusy" />
      <emulator-params>
        <resourceType>MEM</resourceType>
    <!--time between iterations in usec (default 1000)-->
    <memSleep>0</memSleep>
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