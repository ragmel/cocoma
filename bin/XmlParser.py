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
<emulation>
  <emulationName>myMixEmu</emulationName>
  <emulationType>Mix</emulationType>
  <resourceType>Mix</resourceType>
  <startTime>now</startTime>
  <!--duration in seconds -->
  <stopTime>now+180</stopTime>
  
  <distributions name=" myMixEmu-dis-1">
     <startTime>0</startTime>
     <!--duration in seconds -->
     <duration>60</duration>
     <distribution href="/distributions/linear" name="linear" />
      <startLoad>10</startLoad>
      <stopLoad>90</stopLoad>
      <emulator href="/emulators/stressapptest" name="stressapptest" />
      <emulator-params>
        <!--more parameters will be added -->
        <resourceType>CPU</resourceType>
      </emulator-params>
  </distributions>

  <distributions name=" myMixEmu-dis-3">
     <startTime>now+60</startTime>
     <!--duration in seconds -->
     <duration>60</duration>
     <distribution href="/distributions/linear" name="linear" />
      <emulator href="/emulators/stressapptest" name="stressapptest" />
      <emulator-params>
        <resourceType>NET</resourceType>
      </emulator-params>
  </distributions>


</emulation>
'''
from xml.dom.minidom import parseString, Node


def xmlReader(filename):
    
    print "This is XML Parser"
    
    
    #open the xml file for reading:
    file = open(filename,'r')
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()
    #parse the xml you got from the file
    xmlParser(data)

def xmlParser(xmlData):
    
    ##new##
    dom2 = parseString(xmlData)
    distroList = []


    distributionsXml=dom2.getElementsByTagName('distributions')

    emulationName=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emulationName')[0].firstChild.data
    emulationType=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emulationType')[0].firstChild.data
    resourceTypeEmulation=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('resourceType')[0].firstChild.data
    startTimeEmu=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('startTime')[0].firstChild.data
    
    print "##########################"
    print "emulation name: ",emulationName
    print "emulation type: ",emulationType
    print "resource type: ",resourceTypeEmulation
    print "start time: ",startTimeEmu
    print "##########################"
    
    n=0
    for node in distributionsXml:
        #get things inside "distributions"
        startTimeDistro = dom2.getElementsByTagName('startTime')[n].firstChild.data
        durationDistro = dom2.getElementsByTagName('duration')[n].firstChild.data
        granularity= dom2.getElementsByTagName('granularity')[n].firstChild.data
         
        
        try:
        #arg.append(dom.getElementsByTagName('distribution')[0].getElementsByTagName('arg9')[0].firstChild.data)
            arg0 = dom2.getElementsByTagName('startLoad')[n].firstChild.data
        except:
        #arg.append("NULL")
            arg0="NULL"
        
    
        try:
       
            arg1 = dom2.getElementsByTagName('stopLoad')[n].firstChild.data
        except:
       
            arg1="NULL"
       
        #arg2
        #arg3
        #arg4
        #arg5
        #arg6
        #arg7
        #arg8
        #arg9
        
        resourceTypeEmu = dom2.getElementsByTagName('emulator-params')[0].getElementsByTagName('resourceType')[0].firstChild.data 
        #dom2.getElementsByTagName('resourceType')[n].firstChild.data
        ##############
        
        #get attributes
        distribution = dom2.getElementsByTagName('distribution')[n]
        distrType = distribution.attributes["name"].value
        
        distributions= dom2.getElementsByTagName('distributions')[n]
        distrinutionsName = distributions.attributes["name"].value
        
        emulator = dom2.getElementsByTagName('emulator')[n]
        emuName = emulator.attributes["name"].value
        ##############
        
        
        #add every emulation in the dictionary
        distroDict={"distrinutionsName":distrinutionsName,"startTimeDistro":startTimeDistro,"durationDistro":durationDistro,"granularity":granularity,"distrType":distrType,"arg0":arg0,"arg1":arg1,"emuName":emuName,"resourceTypeEmu":resourceTypeEmu}
        
       
        
        print "---->",distrinutionsName
        print "start time: ",startTimeDistro
        print "duration: ",durationDistro
        print "granularity: ", granularity
        print "distribution type: ",distrType
        print "startLoad: ",arg0
        print "stopLoad: ",arg1
        print "emulator:", emuName
        print "resource type: ", resourceTypeEmu
        #atr = dom2.documentElement.getAttributeNode('name').nodeValue
        # print atr


        
        
        #emulator = dom2.getElementsByTagName('emulator')[n].firstChild.data
        distroList.append(distroDict)
        n=n+1
        # print "Distro ",n
        #print durationDistro,  startTimeDistro, distribution,emulator 
    print distroList
    return emulationName, emulationType, resourceTypeEmulation, startTimeEmu, distroList
    



if __name__ == '__main__':
    
    #filename = "xmldoc.xml"
    #xmlFileReader(filename)
    xmlData='''<?xml version="1.0" encoding="UTF-8"?>
<emulation>
  <emulationName>myMixEmu</emulationName>
  <emulationType>Mix</emulationType>
  <resourceType>Mix</resourceType>
  <startTime>now</startTime>
  <!--duration in seconds -->
  <stopTime>now+180</stopTime>
  
  <distributions name=" myMixEmu-dis-1">
     <startTime>0</startTime>
     <!--duration in seconds -->
     <duration>1</duration>
     <granularity>10</granularity>
     <distribution href="/distributions/linear" name="linear" />
      <startLoad>10</startLoad>
      <stopLoad>90</stopLoad>
      <emulator href="/emulators/stressapptest" name="stressapptest" />
      <emulator-params>
        <!--more parameters will be added -->
        <resourceType>CPU</resourceType>
      </emulator-params>
  </distributions>
  
  <distributions name=" myMixEmu-dis-2">
     <startTime>60</startTime>
     <!--duration in seconds -->
     <duration>2</duration>
     <granularity>10</granularity>
     <distribution href="/distributions/poisson" name="poisson" />
      <emulator href="/emulators/stress" name="stress" />
      <emulator-params>
        <resourceType>CPU</resourceType>
      </emulator-params>
  </distributions>

  <distributions name=" myMixEmu-dis-3">
     <startTime>now+60</startTime>
     <!--duration in seconds -->
     <duration>3</duration>
     <granularity>10</granularity>
     <distribution href="/distributions/linear" name="linear" />
      <emulator href="/emulators/stressapptest" name="stressapptest" />
      <emulator-params>
        <resourceType>NET</resourceType>
      </emulator-params>
  </distributions>

  <distributions name=" myMixEmu-dis-4">
     <startTime>120</startTime>
     <!--duration in seconds -->
     <duration>4</duration>
     <granularity>10</granularity>
     <distribution href="/distributions/poisson" name="poisson" />
      <emulator href="/emulators/stressapptest" name="stressapptest" />
      <emulator-params>
        <resourceType>CPU</resourceType>
      </emulator-params>
  </distributions>

  <distributions name=" myMixEmu-dis-5">
     <startTime>120</startTime>
     <!--duration in seconds -->
     <duration>5</duration>
     <granularity>10</granularity>
     <distribution href="/distributions/geometric" name="geometric" />
      <emulator href="/emulators/wireshark" name="wireshark" />
      <emulator-params>
        <resourceType>net</resourceType>
      </emulator-params>
  </distributions>

  <link rel="parent" href="/"/>
  <link href="/emulations" rel="parent" type="application/vnd.cocoma+xml"/>
</emulation>
    
    
    '''
    xmlParser(xmlData)
    
    
    
    pass