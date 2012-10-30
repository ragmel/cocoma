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
Created on 29 Aug 2012

<<domain type='COCOMA'>
   <emulation>   
       <emulationId>autoincrement</emulationId>
       <emulationName>mytest</emulationName>
       <emulationType>Malicious</emulationType>
       <resourceType>CPU</resourceType>
       <startTime>2012-08-30T20:03:04</startTime>
       <stopTime>2012-08-30T20:10:03</stopTime>
   </emulation>
   
   <distribution>
       <distributionGranularity>10</distributionGranularity>
       <distributionType>linear</distributionType>
       <startLoad>20</startLoad>
       <stopLoad>90</stopLoad>
   </distribution>
    
</domain>

'''
from xml.dom.minidom import parseString


def xmlReader(filename):
    print "This is XML Parser"
    
    #open the xml file for reading:
    file = open(filename,'r')
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()
    #parse the xml you got from the file
    dom = parseString(data)
    #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
    xmlTag = dom.getElementsByTagName('domain')[0].toxml()
    #strip off the tag (<tag>data</tag>  --->   data):
    xmlData=xmlTag.replace('<domain>','').replace('</domain>','')
    
    
    #Vars: "emulationType=", "resourceType=", "startTime=", "stopTime=","distributionGranularity=","distributionType=","startLoad=","stopLoad=","xml="
    #get second deep element like
    
    #<emulation>
    emulationName = dom.getElementsByTagName('emulation')[0].getElementsByTagName('emulationName')[0].firstChild.data
    #AUTOINCREMENT emulationId = dom.getElementsByTagName('emulation')[0].getElementsByTagName('emulationId')[0].firstChild.data
    emulationType = dom.getElementsByTagName('emulation')[0].getElementsByTagName('emulationType')[0].firstChild.data
    resourceType = dom.getElementsByTagName('emulation')[0].getElementsByTagName('resourceType')[0].firstChild.data
    startTime = dom.getElementsByTagName('emulation')[0].getElementsByTagName('startTime')[0].firstChild.data
    stopTime = dom.getElementsByTagName('emulation')[0].getElementsByTagName('stopTime')[0].firstChild.data
    emulator = dom.getElementsByTagName('emulation')[0].getElementsByTagName('emulator')[0].firstChild.data
    
    #<distibution>
    distributionGranularity = dom.getElementsByTagName('distribution')[0].getElementsByTagName('distributionGranularity')[0].firstChild.data
    distributionType = dom.getElementsByTagName('distribution')[0].getElementsByTagName('distributionType')[0].firstChild.data
    arg=[]
    try:
        arg.append(dom.getElementsByTagName('distribution')[0].getElementsByTagName('arg0')[0].firstChild.data)
    except:
        arg.append("NULL")

    try:
        arg.append(dom.getElementsByTagName('distribution')[0].getElementsByTagName('arg1')[0].firstChild.data)
    except:
        arg.append("NULL")
    try:
        arg.append(dom.getElementsByTagName('distribution')[0].getElementsByTagName('arg2')[0].firstChild.data)
    except:
        arg.append("NULL")
        
    try:
        arg.append(dom.getElementsByTagName('distribution')[0].getElementsByTagName('arg3')[0].firstChild.data)
    except:
        arg.append("NULL")

    try:
        arg.append(dom.getElementsByTagName('distribution')[0].getElementsByTagName('arg4')[0].firstChild.data)
    except:
        arg.append("NULL")

    try:
        arg.append(dom.getElementsByTagName('distribution')[0].getElementsByTagName('arg5')[0].firstChild.data)
    except:
        arg.append("NULL")

    try:
        arg.append(dom.getElementsByTagName('distribution')[0].getElementsByTagName('arg6')[0].firstChild.data)
    except:
        arg.append("NULL")

    try:
        arg.append(dom.getElementsByTagName('distribution')[0].getElementsByTagName('arg7')[0].firstChild.data)
    except:
        arg.append("NULL")

    try:
        arg.append(dom.getElementsByTagName('distribution')[0].getElementsByTagName('arg8')[0].firstChild.data)
    except:
        arg.append("NULL")

    try:
        arg.append(dom.getElementsByTagName('distribution')[0].getElementsByTagName('arg9')[0].firstChild.data)
    except:
        arg.append("NULL")
        
        
    
    
    
    print "Parameters taken:"
    print emulationName
    #print emulationId
    print emulationType
    print resourceType
    print startTime
    print stopTime
    print distributionGranularity
    print distributionType
    print arg
    
    
    return emulationName,distributionType,resourceType,emulationType,startTime,stopTime,emulator, distributionGranularity,arg


if __name__ == '__main__':
    
    filename = "xmldoc.xml"
    
    xmlReader(filename)
    
    
    
    pass