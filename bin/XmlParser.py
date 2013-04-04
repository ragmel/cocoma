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
import __builtin__
from xml.dom.minidom import parseString, Node
import xml.dom.minidom,psutil
import DistributionManager,sys,EmulationManager
import logging

#declare global variable for reference 
xmlLogger = None

def xmlReader(filename):
    
    fileObj = open(filename,'r')
    #convert to string:
    data = fileObj.read()
    #close file because we don't need it anymore:
    fileObj.close()
    #parse the xml you got from the file
    (emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData)=xmlParser(data)
    return emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData

def xmlParser(xmlData):
    #general log creator
    global xmlLogger
    if xmlLogger is None:
        #initialize logger
        levelStr=str(EmulationManager.readLogLevel("coreloglevel"))
        if levelStr=="info":
            level=logging.INFO
        if levelStr=="debug":
            level=logging.DEBUG
        #xmlLogger=EmulationManager.logToFile("XML Parser",level)
        xmlLogger=EmulationManager.loggerSet("XML Parser")

    xmlLogger.debug("###This is XML Parser: xmlParser(xmlData)")
    emulationLogFrequency = "3"
    emulationLog="0"

    #normal values
    try:
        dom1 = parseString(xmlData)
        
        #lower case values
        dom2 = parseString(xmlData.lower())
    except Exception,e:
        xmlLogger.exception("XML input Error:"+str(e))
        return "<error>XML input Error:"+str(e)+"</error>"
        
        
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
            if int(emulationLog)==1:
                xmlLogger.debug("Log frequency not set in XML setting to 3s")
        
        try:
            emulationLogLevel=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('log')[0].getElementsByTagName('loglevel')[0].firstChild.data
            if emulationLogLevel.lower()!= "debug":
                emulationLogLevel = "info"
        except Exception, e:
            emulationLogLevel = "info"

    except Exception, e:
        emulationLogLevel = "info"
        xmlLogger.debug("Setting logging to INFO")
    
    try:
        emulationType=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emutype')[0].firstChild.data
        startTimeEmu=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emustarttime')[0].firstChild.data
        resourceTypeEmulation=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emuresourcetype')[0].firstChild.data
        stopTimeEmu=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emustoptime')[0].firstChild.data
    except Exception,e:
        xmlLogger.exception("XML input Error:"+str(e))
        return "<error>XML input Error:"+str(e)+"</error>"
     
    
    
    xmlLogger.debug( "##########################")
    xmlLogger.debug("emulation name: "+str(emulationName))
    xmlLogger.debug("emulation type: "+str(emulationType))
    xmlLogger.debug("resource type: "+str(resourceTypeEmulation))
    xmlLogger.debug("start time: "+str(startTimeEmu))
    xmlLogger.debug("stop time: "+str(stopTimeEmu))
    xmlLogger.debug("##########################")
    
    n=0
    for node in distributionsXml:
        distribution = dom2.getElementsByTagName('distribution')[n]
        distrType = distribution.attributes["name"].value
        
        #getting resource type of distribution CPU,IO,MEM or NET
        try:
            resourceTypeDist = dom2.getElementsByTagName('emulator-params')[n].getElementsByTagName('resourcetype')[0].firstChild.data
        except Exception,e:
            xmlLogger.exception("XML input Error:"+str(e))
            return "<error>XML input Error:"+str(e)+"</error>"

        try:
            moduleMethod=DistributionManager.loadDistributionArgNames(distrType)
            
            distroArgsLimitsDict=moduleMethod(resourceTypeDist)
            moduleArgs=distroArgsLimitsDict.keys()
        except IOError, e:
            print "Unable to load module name \"",distrType,"\" error:"
            print e
            sys.exit(0) 
        '''
        loading emulator args
        '''
        
        emulator = dom2.getElementsByTagName('emulator')[n]
        emulatorType = emulator.attributes["name"].value
            
        try:
            EmulatorModuleMethod=DistributionManager.loadEmulatorArgNames(emulatorType)
            #argNames={"fileQty":{"upperBound":10,"lowerBound":0}}
            emulatorArgsLimitsDict=EmulatorModuleMethod(resourceTypeDist)
            emulatorArgs=emulatorArgsLimitsDict.keys()
        except IOError, e:
            print "Unable to load module name \"",emulatorType,"\" error:"
            print e
            sys.exit(0)    
        
        
        #get things inside "distributions"
        try:
            startTimeDistro = dom2.getElementsByTagName('distributions')[n].getElementsByTagName('starttime')[0].firstChild.data
            durationDistro = dom2.getElementsByTagName('duration')[n].firstChild.data
            granularity= dom2.getElementsByTagName('granularity')[n].firstChild.data
        except Exception,e:
            xmlLogger.exception("XML input Error:"+str(e))
            return "<error>XML input Error:"+str(e)+"</error>"
         
        distroArgs={}
        a=0
        #for things in moduleArgs:
        '''
        Getting all the arguments for distribution
        ''' 
        distroArgsNotes=[]
        for args in moduleArgs:
            
            try:    
                arg0 = dom2.getElementsByTagName('distributions')[n].getElementsByTagName(moduleArgs[a].lower())[0].firstChild.data
                
                #if data given in percentage for memory converting it to real values
                if resourceTypeDist.lower()=="mem":
                    if str(arg0[-1])=="%":
                        memReading=psutil.phymem_usage()
                        allMemoryPc =(memReading.total/1048576.00)/100.00
                        arg0=int(str(arg0[:-1]))*allMemoryPc
                        
                distributionsLimitsDictValues = distroArgsLimitsDict[moduleArgs[a].lower()]
                checked_distroArgs,checkDistroNote = boundsCompare(arg0,distributionsLimitsDictValues)               
                distroArgsNotes.append(checkDistroNote)
                distroArgs.update({moduleArgs[a].lower():checked_distroArgs})                
                a+=1
               
            except Exception,e:
                    xmlLogger.exception("Distribution argument specified in XML does not exist in distribution module \""+str(resourceTypeDist)+"\" section: "+str(e))
                    return "<error>Distribution argument specified in XML does not exist in distribution module \""+str(resourceTypeDist)+"\" section: "+str(e)+"</error>"
        '''
        getting all the arguments for emulator
        '''
        emulatorArg={}
        emulatorArgNotes=[]
        a=0
        #for things in moduleArgs:
        for args in emulatorArgs:
            try:
                
                arg0 = dom2.getElementsByTagName('distributions')[n].getElementsByTagName(emulatorArgs[a].lower())[0].firstChild.data
                emulatorLimitsDictValues = emulatorArgsLimitsDict[emulatorArgs[a].lower()]
                checked_emuargs,check_note = boundsCompare(arg0,emulatorLimitsDictValues,emulatorArgs[a].lower())                
                emulatorArg.update({emulatorArgs[a].lower():checked_emuargs})
                emulatorArgNotes.append(check_note)
                a+=1
                
            except Exception, e:
                    xmlLogger.exception("Emulator argument specified in XML does not exist in emulator module \""+str(resourceTypeDist)+"\" section: "+str(e))
                    return "<error>Emulator argument specified in XML does not exist in emulator module \""+str(resourceTypeDist)+"\" section: "+str(e)+"</error>"
        
        try:
            resourceTypeDist = dom2.getElementsByTagName('emulator-params')[n].getElementsByTagName('resourcetype')[0].firstChild.data 
            distributionsName=dom1.getElementsByTagName('distributions')[n].getElementsByTagName('name')[0].firstChild.data     
            emulator = dom1.getElementsByTagName('emulator')[n]
            emulatorName = emulator.attributes["name"].value
        except Exception,e:
            xmlLogger.exception("XML input Error:"+str(e))
            return "<error>XML input Error:"+str(e)+"</error>"
        
        #add every emulation in the dictionary
        distroDict={"distributionsName":distributionsName,"startTimeDistro":startTimeDistro,"durationDistro":durationDistro,"granularity":granularity,"distrType":distrType,"distroArgs":distroArgs,"emulatorName":emulatorName,"emulatorArg":emulatorArg,"resourceTypeDist":resourceTypeDist,"emulatorArgNotes":emulatorArgNotes,"distroArgsNotes":distroArgsNotes}
        distroList.append(distroDict)
        n=n+1
        
        #    CPU-dis-1        Mix          1              3                        Mix               now         180       [{'distroArgs': {'startLoad': u'10', 'stopLoad': u'90'}, 'emulatorName': u'lookbusy', 'distrType': u'linear', 'resourceTypeDist': u'CPU', 'startTimeDistro': u'5', 'distributionsName': u'CPU-dis-1', 'durationDistro': u'170', 'emulatorArg': {'ncpus': u'0'}, 'granularity': u'10'}] 
                                                                                                                                            
    xmlLogger.debug("XML Extracted Values: "+str(emulationName)+" "+str(emulationType)+" "+str(emulationLog)+" "+str(emulationLogFrequency)+" "+str(resourceTypeEmulation)+" "+str(startTimeEmu)+" "+str(stopTimeEmu)+" "+str(distroList))
    xmlLogger.info("Finished running")
    
    return emulationName,emulationType,emulationLog,emulationLogFrequency,emulationLogLevel, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList,xmlData


def boundsCompare(xmlValue,LimitsDictValues,variableName = None):
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
            return_note ="\nOK"
            return xmlValue, return_note
            
        else:
            return_note ="\nThe specified value "+str(xmlValue)+" was higher than the maximum limit "+str(upperBound)+" changing to the maximum limit"
            return upperBound , return_note 
    else:
        return_note ="\nThe specified value "+str(xmlValue)+" was lower than the minimum limit "+str(lowerBound)+" changing to the maximum limit"
        return lowerBound, return_note


if __name__ == '__main__':
    """
    Testing information
    """
    xmlData='''
<emulation>
  <emuname>MEM_EMU</emuname>
  <emuType>Mix</emuType>
  <emuresourceType>MEM</emuresourceType>
  <!--date format: 2014-10-10T10:10:10 -->
  <emustartTime>now</emustartTime>
  <!--duration in seconds -->
  <emustopTime>60</emustopTime>
  
  <distributions >
     <name>MEM_Distro</name>
     <startTime>0</startTime>
     <!--duration in seconds -->
     <duration>60</duration>
     <granularity>5</granularity>
     <distribution href="/distributions/linear_incr" name="linear_incr" />
     <!--Megabytes for memory -->
      <startLoad>100</startLoad>
      <stopLoad>1000</stopLoad>
      <emulator href="/emulators/lookbusy" name="lookbusy" />
      <emulator-params>
        <resourceType>MEM</resourceType>
        <!--time between iterations in usec (default 1000)-->    
        <memSleep>0</memSleep>
      </emulator-params>
  </distributions>

  <log>
      <!-- Use value "1" to enable logging(by default logging is off)  -->
      <enable>0</enable>
      <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
      <frequency>3</frequency>
      <logLevel>debug</logLevel>
  </log>

</emulation>

    
    
    '''
    
    xmlParser(xmlData)
    
    pass