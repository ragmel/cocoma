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



<emulation>
  <emulationName>myMixEmu</emulationName>
  <emulationType>Mix</emulationType>
  <resourceType>Mix</resourceType>
  <startTime>now</startTime>
  <!--duration in seconds -->
  <stopTime>180</stopTime>
  
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
    (emulationName,emulationType, resourceTypeEmulation, startTimeEmu, stopTimeEmu, distroList)=xmlParser(data)
    return emulationName,emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList

def xmlParser(xmlData):
    
    ##new##
    dom2 = parseString(xmlData)
    distroList = []


    distributionsXml=dom2.getElementsByTagName('distributions')
    #emulationName=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('emulationName')[0].firstChild.data
    emulationName=dom2.getElementsByTagName('emulation')[0].getElementsByTagName('name')[0].firstChild.data
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
        
            
                
        try:
            moduleMethod=DistributionManager.loadDistributionArgNames(distrType)
            moduleArgs=moduleMethod()
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
        
        resourceTypeDist = dom2.getElementsByTagName('emulator-params')[n].getElementsByTagName('resourceType')[0].firstChild.data
        print "emulatorType,resourceTypeDist:",emulatorType,resourceTypeDist        
        try:
            EmulatorModuleMethod=DistributionManager.loadEmulatorArgNames(emulatorType)
            emulatorArgs=EmulatorModuleMethod(resourceTypeDist)
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
        for args in moduleArgs:
            try:
               
                #arg0 = dom2.getElementsByTagName(moduleArgs[a])[n].firstChild.data
                arg0 = dom2.getElementsByTagName('distributions')[n].getElementsByTagName(moduleArgs[a])[0].firstChild.data
                print "Distro Arg",a," arg Name: ", moduleArgs[a]," arg Value: ",arg0
                
                distroArgs.update({moduleArgs[a]:arg0})
                a= a+1
                #print a, moduleArgs[a]
            except IndexError,e:
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
        a=0
        #for things in moduleArgs:
        
        for args in emulatorArgs:
            try:
                
                #arg0 = dom2.getElementsByTagName(moduleArgs[a])[n].firstChild.data
                arg0 = dom2.getElementsByTagName('distributions')[n].getElementsByTagName(emulatorArgs[a])[0].firstChild.data
                print "Emulator Arg",a," arg Name: ", emulatorArgs[a]," arg Value: ",arg0
                emulatorArgDict={emulatorArgs[a]:arg0}
                emulatorArg.update({emulatorArgs[a]:arg0})
                #append(emulatorArgs[a]:arg0)
                a= a+1
                #print a, moduleArgs[a]
            except IndexError,e:
                    #print e, "setting value to NULL"
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
        distributionsName=dom2.getElementsByTagName('distributions')[0].getElementsByTagName('name')[0].firstChild.data
        
        emulator = dom2.getElementsByTagName('emulator')[n]
        emulatorName = emulator.attributes["name"].value
        
        ##############
        
        
        #add every emulation in the dictionary
        distroDict={"distributionsName":distributionsName,"startTimeDistro":startTimeDistro,"durationDistro":durationDistro,"granularity":granularity,"distrType":distrType,"distroArgs":distroArgs,"emulatorName":emulatorName,"emulatorArg":emulatorArg,"resourceTypeDist":resourceTypeDist}
        
       
        
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
        
    print emulationName,emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList
    
    return emulationName,emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList
    



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
  <stopTime>now</stopTime>
  
  <distributions name=" myMixEmu-dis-1">
     <startTime>0</startTime>
     <!--duration in seconds -->
     <duration>120</duration>
     <granularity>10</granularity>
     <distribution href="/distributions/linear" name="linear" />
      <startLoad>11</startLoad>
      <stopLoad>91</stopLoad>
      <emulator href="/emulators/stressapptest" name="lookbusy" />
      <emulator-params>
        <!--more parameters will be added -->
        <resourceType>CPU</resourceType>
        <!--Number of CPUs to keep busy (default: autodetected)-->
        <ncpus>0</ncpus>
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
      <emulator href="/emulators/stress" name="lookbusy" />
      <emulator-params>
        <resourceType>CPU</resourceType>
        <ncpus>3</ncpus>
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
      <emulator href="/emulators/stressapptest" name="lookbusy" />
      <emulator-params>
        <resourceType>MEM</resourceType>
        <memUtil>10GB</memUtil>
        <memSleep>100</memSleep>
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
      <emulator href="/emulators/stressapptest" name="lookbusy" />
      <emulator-params>
        <resourceType>CPU</resourceType>
        <ncpus>3</ncpus>
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
      <emulator href="/emulators/wireshark" name="lookbusy" />
      <emulator-params>
        <resourceType>IO</resourceType>
        <ioUtil>10</ioUtil>
        <ioBlockSize>20</ioBlockSize>
        <ioSleep>30</ioSleep>
      </emulator-params>
  </distributions>

  <link rel="parent" href="/"/>
  <link href="/emulations" rel="parent" type="application/vnd.cocoma+xml"/>
</emulation>
    
    
    '''
    xmlParser(xmlData)
    
    
    
    pass