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

import xml.dom.minidom
import sys
from xml.dom.minidom import parseString
import Library

xmlLogger = None
runOverloaded = False

def xmlFileParser (xmlFileName, runIfOverloaded):
    global xmlLogger
    xmlLogger = Library.loggerSet("XML Parser")
    xmlStr = getXMLFile(xmlFileName)
    if xmlStr.lstrip()[:1] == "<":  #Does if XML File Exists
#        xmlStr = getXMLString(fileName)
        xmlData = getXMLString(xmlStr)
        return xmlReader(xmlStr, runIfOverloaded)
    else:
        raise Exception ("Cannot parse XML, see documentation for required sections \n Printing xmlData: \n" + xmlStr)

def xmlReader(xmlParam, runIfOverloaded):
    global runOverloaded
    runOverloaded = runIfOverloaded
    setLoggerDetails(xmlParam)
    xmlStr = getXMLString(xmlParam)
#    
#    xmlData = getXMLFile(fileName)
#    if xmlData.lstrip()[:1] == "<":  #Does if XML File Exists
#        xmlStr = getXMLString(fileName)
#    else:
#        raise Exception ("Cannot parse XML, see documentation for required sections \n Printing xmlData: \n" + xmlData)
    
    emuPresent = sectionCheck(xmlStr, "emulation")
    distroPresent = sectionCheck(xmlStr, "distributions")
    if not (emuPresent) or not (distroPresent):    #If either section is absent, fail 
        errorStr = "XML not well formed, 'Emulation' or 'Distributions' sections(s) missing"
        xmlLogger.error(errorStr)
        raise Exception (errorStr)

    xmlStr = xmlStr.getElementsByTagName('emulation')[0] #Set to emulation (main) tree
    
    (emulationName, emulationType, resourceTypeEmulation, startTimeEmu, stopTimeEmu) = getEmulationDetails(xmlStr)
    emulationName = emulationName.upper()

#    distroList = getDistributionDetails(xmlStr)
#    if not (type(distroList) == list):
#        return (emulationName, emulationType, emulationLog, emulationLogFrequency, emulationLogLevel, resourceTypeEmulation, startTimeEmu, stopTimeEmu, distroList, xmlParam, MQproducerValues)

    if sectionCheck(xmlStr, "log"):
        (emulationLog, emulationLogFrequency, emulationLogLevel) = getLoggerDetails(xmlStr.getElementsByTagName('log')[0])
    else:
        (emulationLog, emulationLogFrequency, emulationLogLevel) = getLoggerDetails("")

    MQproducerValues = {}
    if sectionCheck(xmlStr, "mq"):
        MQproducerValues = getMQDetails(xmlStr.getElementsByTagName('mq')[0])

    distroList = getDistributionDetails(xmlStr)
    if (type(distroList) == unicode):
        return (emulationName, emulationType, emulationLog, emulationLogFrequency, emulationLogLevel, resourceTypeEmulation, startTimeEmu, stopTimeEmu, distroList, xmlParam, MQproducerValues)

    xmlLogger.info("##########################")
    xmlLogger.info("emulation name: " + str(emulationName))
    xmlLogger.info("emulation type: " + str(emulationType))
    xmlLogger.info("resource type: " + str(resourceTypeEmulation))
    xmlLogger.info("start time: " + str(startTimeEmu))
    xmlLogger.info("stop time: " + str(stopTimeEmu))
    xmlLogger.info("##########################")

    xmlLogger.info("XML Extracted Values: " + str(emulationName) + " " + str(emulationType) + " " + 
                    str(emulationLog) + " " + str(emulationLogFrequency) + " " + str(resourceTypeEmulation) + 
                    " " + str(startTimeEmu) + " " + str(stopTimeEmu) + " " + str(distroList) + " " + str(MQproducerValues.values()))

    # Check distroResType match emuResType
    resTypeCheck(resourceTypeEmulation, distroList)

    xmlLogger.info("XML parsing done")


    return (emulationName, emulationType, emulationLog, emulationLogFrequency, emulationLogLevel,
            resourceTypeEmulation, startTimeEmu, stopTimeEmu, distroList, xmlParam, MQproducerValues)

def getXMLFile(fileName):
    xmlData = None

    try:
        fileObj = open(fileName, 'r')
        #convert to string:
        xmlData = fileObj.read()
        #close file because we don't need it anymore
        fileObj.close()
    except Exception, e:
        xmlLogger.error('File "' + str(fileName) + '" could not be loaded. Check if it exists. Error:' + str(e))
        return 'File "' + str(fileName) + '" could not be loaded. Check if it exists'

    return xmlData

def getXMLString(xmlData):
    xmlStr = ""
#    xmlData = getXMLFile(fileName)
    try:
        xmlStr = parseString(xmlData.lower())
    except Exception, e:
        xmlLogger.error("XML input Error:" + str(e))
        return "XML is not well formed Error: " + str(e)

    return xmlStr

def getXMLData (xmlData, xmlTagName, secondXMLTagName): #Accepts up-to 2 xmlTageName's
    tagData = ""
    if sectionCheck(xmlData, xmlTagName):
        if (secondXMLTagName == ""): #if second value is empty ignore it
            tagData = xmlData.getElementsByTagName(xmlTagName)[0].firstChild.data
        else:
            if sectionCheck(xmlData, secondXMLTagName):
                tagData = xmlData.getElementsByTagName(xmlTagName)[0].getElementsByTagName(secondXMLTagName)[0].firstChild.data
                xmlTagName = secondXMLTagName #For Exception Handling below
            else:
                raise Exception ("XML input Error: " + secondXMLTagName + " section not found")
    else:
        raise Exception ("XML input Error: " + xmlTagName + " section not found")

    return tagData

def getXMLValue(xmlStr, xmlTagName, xmlValueName):    #Used for getting values contained within a tag
    tagValue = ""
    if sectionCheck(xmlStr, xmlTagName):
        try:
            tagValue = xmlStr.getElementsByTagName(xmlTagName)[0].attributes[xmlValueName].value
        except Exception, e:
            xmlLogger.error('XML input Error: ' + xmlValueName + ' not found in section ' + xmlTagName + str(e))
            return 'XML input Error: ' + xmlValueName + ' not found in section ' + xmlTagName
    else:
        raise Exception ("XML input Error: " + xmlTagName + " section not found")
    return tagValue

def getModuleArgs (moduleType, moduleName, resourceType):
    moduleArgs = []
    argsLimitsDict = None

    try:
        moduleMethod = getArgsModule(moduleName, moduleType)
        argsLimitsDict = moduleMethod(resourceType)

        try:
            moduleArgs = argsLimitsDict.keys()
        except Exception, e:
            xmlLogger.error(moduleType + ' "' + str(moduleName) + '" does not support resource type "' + str(resourceType) + '"')
            return moduleType + ' "' + str(moduleName) + '" does not support resource type "' + str(resourceType) + '"'

    except Exception, e:
        error = "Error: " + str(e) + "\nUnable to find " + moduleType + " module name: " + str(moduleName)
        xmlLogger.error(error)
        return error

    return moduleArgs

def getArgsModule(moduleName, moduleType):
    if moduleType == "Distribution":
        moduleMethod = Library.loadDistributionArgNames(moduleName)
    elif moduleType == "Emulation":
        moduleMethod = Library.loadEmulatorArgNames(moduleName)
    return moduleMethod

def getArgs (xmlStr, moduleType, moduleName, resourceType):
    moduleArgsDict = {}
    moduleArgsNotes = []
    checkNote = "\nOK"

    moduleArgs = getModuleArgs(moduleType, moduleName, resourceType)
    
    moduleMethod = getArgsModule(moduleName, moduleType)
    if (type(moduleMethod) is str):
        print moduleMethod
        sys.exit(0)
    else:
        if type(moduleArgs) is list: #If the list is returned
            
            for arg in moduleArgs:
                arg = arg.lower()
    #            xmlArg = getXMLData(xmlStr, "distributions", arg)
                xmlArg = getXMLData(xmlStr, arg, "")
    
                #Convert stress values mem to real values (if given in %)
                if ((moduleType.lower() == "distribution") and (resourceType == "mem") and (str(xmlArg[-1]) == "%")):
                    sysMemory = Library.getTotalMem()
                    xmlArg = (int(str(xmlArg[:-1])) * sysMemory)/100
        
                moduleArgsNotes.append(checkNote)
                moduleArgsNotes.append(xmlArg)
        
                moduleArgsDict.update({arg:xmlArg})
    
        else:
            errorStr = moduleArgs + "\nXML Error: Cannot get " + moduleType + " arguments, check if 'href' and 'name' exist in XML"
            xmlLogger.error(errorStr)
            raise Exception (errorStr)
    return (moduleArgsDict, moduleArgsNotes)

def getDistributionDetails(xmlStr):
    distroList = []
    xmlDistroList = []

    numDistributions = len(xmlStr.getElementsByTagName('distributions'))
    for i in xrange(numDistributions):
        xmlDistroList.append(xmlStr.getElementsByTagName('distributions')[i])

    for xmlDistro in xmlDistroList:
        distributionsName = getXMLData(xmlDistro, "name", "")
        startTimeDistro = getXMLData(xmlDistro, "starttime", "")
        distrType = getXMLValue(xmlDistro, "distribution", "name")
        emulatorName = getXMLValue(xmlDistro, "emulator", "name")
        resourceType = getXMLData(xmlDistro, "emulator-params", "resourcetype")

        (distroArgs, distroArgsNotes) = getArgs (xmlDistro, "Distribution", distrType, resourceType)
        (emulatorArg, emulatorArgNotes) = getArgs (xmlDistro, "Emulation", emulatorName, resourceType)

        def removeFromDict(dictionary, key):
            itemValue = 0
            if dictionary.has_key(key):
                itemValue = dictionary[key]
                del dictionary[key]
            return dictionary, itemValue
        
        distroArgs, granularity = removeFromDict(distroArgs, "granularity")
        distroArgs, durationDistro = removeFromDict(distroArgs, "duration")

        if not runOverloaded:
            overloadedResource = checkLoadValues (resourceType, distroArgs)
            if (type(overloadedResource) == unicode):
                return overloadedResource

        distroDict = {"distributionsName":distributionsName, "startTimeDistro":startTimeDistro, "durationDistro":durationDistro,
                    "granularity":granularity, "distrType":distrType, "distroArgs":distroArgs,
                    "emulatorName":emulatorName, "emulatorArg":emulatorArg, "resourceTypeDist":resourceType,
                    "emulatorArgNotes":emulatorArgNotes, "distroArgsNotes":distroArgsNotes}
        distroList.append(distroDict)
    return distroList

def sectionCheck(xmlStr, sectionName):
    sectionFound = False
    try:
        section = xmlStr.getElementsByTagName(sectionName)
        if len(section) > 0:
            sectionFound = True
    except Exception, e:
        xmlLogger.error("XML input Error:" + str(e))
        return 'XML input Error: ' + sectionName + ' section not found'

    return sectionFound

def resTypeCheck(emulationResType, distroList):
    for distro in distroList:
        if not (emulationResType.lower() == distro["resourceTypeDist"].lower()) and not emulationResType.lower() == "mix":
            raise Exception ("Emulation should only contain distributions of type: " + emulationResType.upper())

def setLoggerDetails(fileName):
    global xmlLogger
    if xmlLogger is None:
        xmlLogger = Library.loggerSet("XML Parser")
    xmlLogger.info("###This is XML Parser for : " + fileName)

def getLoggerDetails(xmlStr):
    #Set logger details to Default values
    emulationLog = "0"    
    emulationLogFrequency = "3"
    emulationLogLevel = "info"

    try:
        emulationLog = xmlStr.getElementsByTagName('enable')[0].firstChild.data
    
        try:
            emulationLogFrequency = xmlStr.getElementsByTagName('frequency')[0].firstChild.data
        except Exception, e:
            if int(emulationLog) == 1:
                xmlLogger.info("Log frequency not set in XML setting to 3s")

        try:
            newEmulationLogLevel = xmlStr.getElementsByTagName('loglevel')[0].firstChild.data
            if newEmulationLogLevel == "debug":
                emulationLogLevel = newEmulationLogLevel
        except Exception, e:
            xmlLogger.info("Setting logging to INFO")

    except Exception, e:
            xmlLogger.info("enable Log not set, setting to 0")
    return (emulationLog, emulationLogFrequency, emulationLogLevel)

def getEmulationDetails(xmlStr):
    emuName = getXMLData(xmlStr, "emuname", "")
    emuType = getXMLData(xmlStr, "emutype", "")
    emuResourceType = getXMLData(xmlStr, "emuresourcetype", "")
    emuStartTime = getXMLData(xmlStr, "emustarttime", "")
    emuStopTime = getXMLData(xmlStr, "emustoptime", "")

    return (emuName, emuType, emuResourceType, emuStartTime, emuStopTime)

def getMQDetails(xmlStr):
    MQproducerValues = {}

    MQproducerValues["emulationMQenable"] = getXMLData(xmlStr, "enable", "")
    MQproducerValues["emulationMQvhost"] = getXMLData(xmlStr, "vhost", "")
    MQproducerValues["emulationMQexchange"] = getXMLData(xmlStr, "exchange", "")
    MQproducerValues["emulationMQuser"] = getXMLData(xmlStr, "user", "")
    MQproducerValues["emulationMQpassword"] = getXMLData(xmlStr, "password", "")
    MQproducerValues["emulationMQhost"] = getXMLData(xmlStr, "host", "")
    MQproducerValues["emulationMQtopic"] = getXMLData(xmlStr, "topic", "")

    return MQproducerValues

def checkLoadValues(resourceType, distArgs):
    maxResourceLoad = Library.getResourceLimit(resourceType)
    loads = []
    if distArgs.has_key("startload"):
        loads.append(int(distArgs["startload"]))
    if distArgs.has_key("stopload"):
        loads.append(int(distArgs["stopload"]))
    
    #Subtracts current MEM usage from maximum system MEM
    if (resourceType.upper() == "MEM"):
        maxResourceLoad -= Library.getMemUsed();
        
    for load in loads:
        if (load > (maxResourceLoad * 0.9)):
            errorStr = resourceType.upper() + " close to maximum value. Re-send with force ('-f') to run"
            print errorStr
            return errorStr
    return False

if __name__ == '__main__': #For testing purposes
    print xmlFileParser("/home/jordan/git/cocoma/tests/CPU-Linear-Lookbusy_10-95.xml", False)
#    xmlReader("/home/jordan/Desktop/XMLfail.xml")  #REMOVE
    pass
