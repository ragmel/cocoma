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

from xml.dom.minidom import parseString, Node
import xml.dom.minidom
import DistributionManager,sys,EmulationManager
import logging

def loggerSet():
    xmlLogger = logging.getLogger("")
    LOG_LEVEL=logging.INFO
    xmlLogger=EmulationManager.logToFile("XML Parser",LOG_LEVEL)
    LogLevel=EmulationManager.readLogLevel("coreloglevel")
    if LogLevel=="info":
        LOG_LEVEL=logging.INFO
    if LogLevel=="debug":
        LOG_LEVEL=logging.DEBUG
    else:
        LOG_LEVEL=logging.INFO
    
    xmlLogger=EmulationManager.logToFile("XML Parser",LOG_LEVEL)
    return xmlLogger

def xmlReader(filename):
    xmlLogger=loggerSet()
    xmlLogger.debug("This is XML Parser: xmlReader(filename)")
    
    
    
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
    xmlLogger=loggerSet()
    xmlLogger.debug("This is XML Parser: xmlParser(xmlData)")
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
            xmlLogger.debug("Setting emulationLogFrequency to default value of 3sec")
        
        try:
            emulationLogLevel=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('log')[0].getElementsByTagName('loglevel')[0].firstChild.data
            if emulationLogLevel.lower()== "debug":
                emulationLogLevel = logging.DEBUG
            else:
                emulationLogLevel = logging.INFO
                xmlLogger.debug("Setting emulationLogLevel to default value of INFO")
        except Exception, e:
            xmlLogger.debug("Setting emulationLogLevel to default value of INFO")
            emulationLogLevel = logging.INFO
            
    
    except Exception, e:
        xmlLogger.debug("XML Logging is Off")
    
    emulationType=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emutype')[0].firstChild.data
    startTimeEmu=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emustarttime')[0].firstChild.data
    resourceTypeEmulation=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emuresourcetype')[0].firstChild.data
    stopTimeEmu=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emustoptime')[0].firstChild.data
     
    
    
    xmlLogger.debug( "##########################")
    xmlLogger.debug("emulation name: "+str(emulationName))
    xmlLogger.debug("emulation type: "+str(emulationType))
    xmlLogger.debug("resource type: "+str(resourceTypeEmulation))
    xmlLogger.debug("start time: "+str(startTimeEmu))
    xmlLogger.debug("stop time: "+str(stopTimeEmu))
    xmlLogger.debug("##########################")
    
    n=0
    for node in distributionsXml:
        xmlLogger.debug("n: "+str(n))
        #Loading distribution type by module (linear, parabola, etc.)
        
        distribution = dom2.getElementsByTagName('distribution')[n]
        distrType = distribution.attributes["name"].value
        
        #getting resource type of distribution CPU,IO,MEM or NET
        resourceTypeDist = dom2.getElementsByTagName('emulator-params')[n].getElementsByTagName('resourcetype')[0].firstChild.data
            
                
        try:
            moduleMethod=DistributionManager.loadDistributionArgNames(distrType)
            
            distroArgsLimitsDict=moduleMethod(resourceTypeDist)
            moduleArgs=distroArgsLimitsDict.keys()
            
            
            xmlLogger.debug("moduleArgs:"+str(moduleArgs))
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
            
        try:
            xmlLogger.debug("trying to load emulatorType:"+str(emulatorType))
            EmulatorModuleMethod=DistributionManager.loadEmulatorArgNames(emulatorType)
            #argNames={"fileQty":{"upperBound":10,"lowerBound":0}}
            emulatorArgsLimitsDict=EmulatorModuleMethod(resourceTypeDist)
            emulatorArgs=emulatorArgsLimitsDict.keys()
            xmlLogger.debug("emulatorArgs:"+str(emulatorArgs))
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
        xmlLogger.debug("moduleArgs"+str(moduleArgs))
        
        for args in moduleArgs:
            xmlLogger.debug("Inside distribution moduleArgs loop!")
            try:
               
                
                arg0 = dom2.getElementsByTagName('distributions')[n].getElementsByTagName(moduleArgs[a].lower())[0].firstChild.data
                #print "Distro Arg",a," arg Name: ", moduleArgs[a].lower()," arg Value: ",arg0
                
                distributionsLimitsDictValues = distroArgsLimitsDict[moduleArgs[a].lower()]
                #print "boundsCompare(arg0,distributionsLimitsDictValues):",boundsCompare(arg0,distributionsLimitsDictValues)


                checked_distroArgs,checkDistroNote = boundsCompare(arg0,distributionsLimitsDictValues)         
                #print "checked_distroArgs,checkDistroNote",checked_distroArgs,checkDistroNote       
                distroArgsNotes.append(checkDistroNote)
                distroArgs.update({moduleArgs[a].lower():checked_distroArgs})                
                
                
                #distroArgs.update({moduleArgs[a]:arg0})
                a+=1
                #print a, moduleArgs[a]
            except Exception,e:
                    xmlLogger.exception("error getting distribution arguments")
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
        xmlLogger.debug("emulatorArgs"+str(emulatorArgs))
        for args in emulatorArgs:
            try:
                #print "emulatorArgs[a]",emulatorArgs[a].lower()
                arg0 = dom2.getElementsByTagName('distributions')[n].getElementsByTagName(emulatorArgs[a].lower())[0].firstChild.data
                #print "Emulator Arg",a," arg Name: ", emulatorArgs[a].lower()," arg Value: ",arg0
                #emulatorArgDict={emulatorArgs[a]:arg0}
                
                emulatorLimitsDictValues = emulatorArgsLimitsDict[emulatorArgs[a].lower()]
                #print "boundsCompare(arg0,emulatorLimitsDictValues):",boundsCompare(arg0,emulatorLimitsDictValues,emulatorArgs[a].lower())
                checked_emuargs,check_note = boundsCompare(arg0,emulatorLimitsDictValues,emulatorArgs[a].lower())                
                emulatorArg.update({emulatorArgs[a].lower():checked_emuargs})
                emulatorArgNotes.append(check_note)
                
                #append(emulatorArgs[a]:arg0)
                a+=1
                #print a, moduleArgs[a]
            except Exception, e:
                print e
                xmlLogger.exception("Not all emulator arguments are in use, setting Value of "+str(emulatorArgs[a].lower())+" to NULL")
                    #arg0="NULL"
                    #print arg0
                    #arg.append(arg0)
                arg0="NULL"
                emulatorArg.append(arg0)
                a= a+1
        
        xmlLogger.debug("emulatorArg:"+str(emulatorArg))
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
        
       
        
        #print "---->",distributionsName
        #print "start time: ",startTimeDistro
        #print "duration: ",durationDistro
        #print "granularity: ", granularity
        #print "distribution type: ",distrType
                
        distroList.append(distroDict)
        n=n+1
        
        #    CPU-dis-1        Mix          1              3                        Mix               now         180       [{'distroArgs': {'startLoad': u'10', 'stopLoad': u'90'}, 'emulatorName': u'lookbusy', 'distrType': u'linear', 'resourceTypeDist': u'CPU', 'startTimeDistro': u'5', 'distributionsName': u'CPU-dis-1', 'durationDistro': u'170', 'emulatorArg': {'ncpus': u'0'}, 'granularity': u'10'}] 
                                                                                                                                            
    xmlLogger.debug("XML Extracted Values: "+str(emulationName)+" "+str(emulationType)+" "+str(emulationLog)+" "+str(emulationLogFrequency)+" "+str(resourceTypeEmulation)+" "+str(startTimeEmu)+" "+str(stopTimeEmu)+" "+str(distroList))
    
    
    return emulationName,emulationType,emulationLog,emulationLogFrequency, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList


def boundsCompare(xmlValue,LimitsDictValues,variableName = None):
    xmlLogger=loggerSet()
    '''
    Comparing XML variables with emulator or distribution set bounds.
    NOTE: in future might be better moved to the wrapper modules
    '''
    
    if  variableName == "serverip" or variableName == "clientip" or variableName == "packettype":
        return_note ="\nOK"
        return xmlValue,return_note
    
    upperBound=int(LimitsDictValues["upperBound"])
    lowerBound=int(LimitsDictValues["lowerBound"])
    xmlValue=int(xmlValue)
    
    if xmlValue >= lowerBound:
        if xmlValue <= upperBound:
            xmlLogger.debug( "1- All OK")#,xmlValue,upperBound,lowerBound
            return_note ="\nOK"
            return xmlValue, return_note
            
        else:
            xmlLogger.debug("2- Higher than upperBound taking maximum value")#,xmlValue,upperBound,lowerBound
            return_note ="\nThe scpecified value "+str(xmlValue)+" was higher than the maximum limit "+str(upperBound)+" changing to the maximum limit"
            return upperBound , return_note 
    else:
        xmlLogger.debug("3- Lower than lowerBound taking minimum value")#,xmlValue,upperBound,lowerBound
        return_note ="\nThe scpecified value "+str(xmlValue)+" was lower than the minimum limit "+str(lowerBound)+" changing to the maximum limit"
        return lowerBound, return_note


if __name__ == '__main__':
    
    #filename = "xmldoc.xml"
    #xmlFileReader(filename)
    xmlData='''
<emulation>
  <emuname>CPU_emu</emuname>
  <emuType>Mix</emuType>
  <emuresourceType>CPU</emuresourceType>
  <emustartTime>now</emustartTime>
  <!--duration in seconds -->
  <emustopTime>60</emustopTime>
  
  <distributions> 
   <name>CPU_distro</name>
     <startTime>0</startTime>
     <!--duration in seconds -->
     <duration>10</duration>
     <granularity>1</granularity>
     <distribution href="/distributions/linear" name="linear" />
    <!--cpu utilization distribution range-->
      <startLoad>10</startLoad>
      <stopLoad>95</stopLoad>
      <emulator href="/emulators/lookbusy" name="lookbusy" />
      <emulator-params>
        <!--more parameters will be added -->
        <resourceType>CPU</resourceType>
    <!--Number of CPUs to keep busy (default: autodetected)-->
    <ncpus>0</ncpus>
      </emulator-params>
  </distributions>

  <distributions> 
   <name>CPU_distro-2</name>
     <startTime>0</startTime>
     <!--duration in seconds -->
     <duration>10</duration>
     <granularity>1</granularity>
     <distribution href="/distributions/linear" name="linear" />
    <!--cpu utilization distribution range-->
      <startLoad>10</startLoad>
      <stopLoad>95</stopLoad>
      <emulator href="/emulators/lookbusy" name="lookbusy" />
      <emulator-params>
        <!--more parameters will be added -->
        <resourceType>CPU</resourceType>
    <!--Number of CPUs to keep busy (default: autodetected)-->
    <ncpus>0</ncpus>


      </emulator-params>
  </distributions>

  <distributions> 
   <name>CPU_distro3</name>
     <startTime>50</startTime>
     <!--duration in seconds -->
     <duration>10</duration>
     <granularity>1</granularity>
     <distribution href="/distributions/linear" name="linear" />
    <!--cpu utilization distribution range-->
      <startLoad>10</startLoad>
      <stopLoad>95</stopLoad>
      <emulator href="/emulators/lookbusy" name="lookbusy" />
      <emulator-params>
        <!--more parameters will be added -->
        <resourceType>CPU</resourceType>
    <!--Number of CPUs to keep busy (default: autodetected)-->
    <ncpus>0</ncpus>
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
    
    #logging.basicConfig(level=logging.DEBUG)
    xmlParser(xmlData)
    
    
    pass