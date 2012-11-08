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
import DistributionManager,sys


def xmlReader(filename):
    
    print "This is XML Parser"
    
    
    #open the xml file for reading:
    file = open(filename,'r')
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()
    #parse the xml you got from the file
    (emulationName,emulationType, resourceTypeEmulation, startTimeEmu, distroList)=xmlParser(data)
    return emulationName,emulationType, resourceTypeEmulation, startTimeEmu, distroList

def xmlParser(xmlData):
    
    ##new##
    dom2 = parseString(xmlData)
    distroList = []
    
    emulationName=""
    emulationType=""
    resourceTypeEmulation=""
    startTimeEmu=""


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
        print "n: ",n
        #Loading distribution type by module (linear, parabola, etc.)
        distribution = dom2.getElementsByTagName('distribution')[n]
        distrType = distribution.attributes["name"].value        
        try:
            moduleMethod=DistributionManager.loadDistributionArgNames(distrType)
            moduleArgs=moduleMethod()
            print "moduleArgs:",moduleArgs
        except IOError, e:
            print "Unable to load module name \"",distrType,"\" error:"
            print e
            sys.exit(0) 
        
        
        
        #get things inside "distributions"
        startTimeDistro = dom2.getElementsByTagName('distributions')[n].getElementsByTagName('startTime')[0].firstChild.data
        durationDistro = dom2.getElementsByTagName('duration')[n].firstChild.data
        granularity= dom2.getElementsByTagName('granularity')[n].firstChild.data
         
        arg=[]
        a=0
        #for things in moduleArgs:
            
        while a<10:
            try:
                
                #arg0 = dom2.getElementsByTagName(moduleArgs[a])[n].firstChild.data
                arg0 = dom2.getElementsByTagName('distributions')[n].getElementsByTagName(moduleArgs[a])[0].firstChild.data
                print "Arg",a," arg Name: ", moduleArgs[a]," arg Value: ",arg0
                arg.append(arg0)
                a= a+1
                #print a, moduleArgs[a]
            except IndexError,e:
                    #print e, "setting value to NULL"
                    #arg0="NULL"
                    #print arg0
                    #arg.append(arg0)
                
                
                
                arg0="NULL"
                arg.append(arg0)
                a= a+1
                    #a=a+1
        
        resourceTypeEmu = dom2.getElementsByTagName('emulator-params')[n].getElementsByTagName('resourceType')[0].firstChild.data 
        #dom2.getElementsByTagName('resourceType')[n].firstChild.data
        ##############
        
        #get attributes

        distributions= dom2.getElementsByTagName('distributions')[n]
        distributionsName = distributions.attributes["name"].value
        
        emulator = dom2.getElementsByTagName('emulator')[n]
        emulatorName = emulator.attributes["name"].value
        
        ##############
        
        
        #add every emulation in the dictionary
        distroDict={"distributionsName":distributionsName,"startTimeDistro":startTimeDistro,"durationDistro":durationDistro,"granularity":granularity,"distrType":distrType,"arg":arg,"emulatorName":emulatorName,"resourceTypeEmu":resourceTypeEmu}
        
       
        
        print "---->",distributionsName
        print "start time: ",startTimeDistro
        print "duration: ",durationDistro
        print "granularity: ", granularity
        print "distribution type: ",distrType
        
        #listing all available distribution parameters
        m=0
        for names in moduleArgs:
            print moduleArgs[m],arg[m]
            m=m+1
            
        print "emulator:", emulatorName
        print "resource type: ", resourceTypeEmu
        
        #atr = dom2.documentElement.getAttributeNode('name').nodeValue
        # print atr
        #emulator = dom2.getElementsByTagName('emulator')[n].firstChild.data
        distroList.append(distroDict)
        n=n+1
        # print "Distro ",n
        #print durationDistro,  startTimeDistro, distribution,emulator 
        
    print emulationName,emulationType, resourceTypeEmulation, startTimeEmu, distroList
    return (emulationName,emulationType, resourceTypeEmulation, startTimeEmu, distroList)
    



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
     <duration>120</duration>
     <granularity>10</granularity>
     <distribution href="/distributions/linear" name="linear" />
      <startLoad>11</startLoad>
      <stopLoad>91</stopLoad>
      <emulator href="/emulators/stressapptest" name="stressapptest" />
      <emulator-params>
        <!--more parameters will be added -->
        <resourceType>CPU</resourceType>
      </emulator-params>
  </distributions>
  
  <distributions name=" myMixEmu-dis-2">
     <startTime>60</startTime>
     <!--duration in seconds -->
     <duration>200</duration>
     <granularity>10</granularity>
     <distribution href="/distributions/poisson" name="linear" />
    <startLoad>12</startLoad>
      <stopLoad>92</stopLoad>  
      <emulator href="/emulators/stress" name="stress" />
      <emulator-params>
        <resourceType>CPU</resourceType>
      </emulator-params>
  </distributions>

  <distributions name=" myMixEmu-dis-3">
     <startTime>50</startTime>
     <!--duration in seconds -->
     <duration>3</duration>
     <granularity>10</granularity>
     <distribution href="/distributions/linear" name="linear" />
    <startLoad>13</startLoad>
      <stopLoad>93</stopLoad>  
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
     <distribution href="/distributions/poisson" name="parabola" />
      <curve>14</curve>
      <sphere>34</sphere>
      <bend>94</bend>     
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
     <distribution href="/distributions/geometric" name="linear" />
      <startLoad>15</startLoad>
      <stopLoad>95</stopLoad>     
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