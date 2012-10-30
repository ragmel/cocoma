#!/usr/bin/env python
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



from bottle import route, run,response,request
import sys,os
from datetime import datetime as dt
import EmulationManager,ccmsh,DistributionManager
from json import dumps

try:
    HOMEPATH= os.environ['COCOMA']
except:
    print "no $COCOMA environmental variable set"
CONTENT = "application/vnd.cocoma+xml"


'''
#######
COCOMA ROOT
#######
'''
@route('/', method ="GET")
def get_root():
    response.content_type = CONTENT
    #curl -k -i http://10.55.164.211:8050/
    xml_content_root = '''<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/">
  <version>0.3</version>
  <timestamp>'''+str(DistributionManager.timestamp(dt.now()))[0:-2]+'''</timestamp>
  <link rel="emulations" href="/emulations" type="application/vnd.cocoma+xml"/>
  <link rel="emulators" href="/emulators" type="application/vnd.cocoma+xml"/>
  <link rel="distributions" href="/distributions" type="application/vnd.cocoma+xml"/>
</root>
    '''

    return xml_content_root    
    
    

'''
#######
GET emulation
#######
'''

@route('/emulations', method ='GET')
def get_emulations():
    response.content_type = CONTENT
    '''
    ##############
    DUMMY
    ##############
    '''
    #curl -k -i http://10.55.164.211:8050/emulations/
    xml_content_emulations=''' <?xml version="1.0" encoding="UTF-8"?>
<collection xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/emulations">
  <items offset="0" total="1">
<emulation href="/emulations/1">
  <id>1</id>
  <emulationName>myLinearEmu</emulationName>
  <emulationType>Contentious</emulationType>
  <resourceType>CPU</resourceType>
  <startTime>2012-10-23T10:30:00</startTime>
  <stopTime>2012-10-23T10:31:00</stopTime>
  <emulators>
    <emulator href="/emulations/1/stressapptest" name="stressapptest"/>
  </emulators>
  <distributions>
    <distribution href="/emulations/1/linear" name="linear"/>
  </distributions>
  <link rel="parent" href="/"/>
  <link rel="emulators" href="/emulations/1/emulators"/>
  <link rel="distributions" href="/emulations/1/distributions"/>
</emulation>
  </items>
  <link href="/" rel="parent" type="application/vnd.cocoma+xml"/>
</collection>
    '''    
    
    return xml_content_emulations  
    
    
    '''
    emulationSelect=EmulationManager.getEmulation("NULL","NULL",1,"NULL")
    print emulationSelect
    
    if emulationSelect:
            
                response.content_type = 'application/json'
                #return dumps(emulationSelect)
                return { "success" : True, "list" : dumps(emulationSelect) }

    else:
        
        #return "emulation ID: \"",emulationID,"\" does not exists"
        return {"success":False, "error": "No emulations found"}
    '''


@route('/emulations/<ID>', method='GET')
def get_emulation(ID=""):
    response.content_type = CONTENT
    #curl -k -i http://10.55.164.211:8050/emulations/1

    xml_content_emulationsID= '''<?xml version="1.0" encoding="UTF-8"?>
<emulation xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/emulations/1">
  <id>'''+ID+'''</id>
  <emulationName>myLinearEmu</emulationName>
  <emulationType>Contentious</emulationType>
  <resourceType>CPU</resourceType>
  <startTime>2012-10-23T10:30:00</startTime>
  <stopTime>2012-10-23T10:31:00</stopTime>
  <emulators>
    <emulator href="/emulations/1/stressapptest" name="stressapptest"/>
  </emulators>
  <distributions>
    <distribution href="/emulations/1/linear" name="linear"/>
  </distributions>
  <link rel="parent" href="/"/>
  <link rel="emulators" href="/emulations/1/emulators"/>
  <link rel="distributions" href="/emulations/1/distributions"/>
  <link href="/" rel="parent" type="application/vnd.cocoma+xml"/>
</emulation>
    '''
    return xml_content_emulationsID
    
    
    
    
    
    '''
    xml = request.forms.get( "xml" )
    e = request.forms.get("e")
    ret = str(e)+str(xml)+"\n"
    return  ret
    '''


@route('/emulations/<ID>/emulators', method='GET')
def get_emulators(ID=""):
    response.content_type = CONTENT
    #curl -k -i http://10.55.164.211:8050/emulations/1/emulators
    xml_content_emulators ='''<?xml version="1.0" encoding="UTF-8"?>
<collection xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/emulations/1/emulators">
  <items offset="0" total="1">
<emulator href="/emulations/1/emulators/stressapptest" name="stressapptest"/>
  </items>
  <link href="/emulations/stressaptest" rel="parent" type="application/vnd.cocoma+xml"/>
</collection>
    '''
    return xml_content_emulators




@route('/emulations/<ID>/emulators/<name>', method='GET')
def get_emulator(ID="",name=""):
    response.content_type = CONTENT
    #curl -k -i http://10.55.164.211:8050/emulations/1/emulators/stressapptest
    xml_content_emulatorName = '''<?xml version="1.0" encoding="UTF-8"?>
<emulator xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/emulations/1/emulators/stressapptest">
<name>'''+name+'''</name>
   <info>
        Stats: SAT revision 1.0.3_autoconf, 32 bit binary
        Log: buildd @ biber on Thu Jul 29 21:47:10 UTC 2010 from open source release
        Usage: ./sat(32|64) [options]
        ...
   </info>
</emulator>
    '''
    
    return xml_content_emulatorName

@route('/emulations/<ID>/distributions', method='GET')
def get_distributions(ID=""):
    response.content_type = CONTENT
    #curl -k -i http://10.55.164.211:8050/emulations/1/distributions
    xml_content_distributions ='''<?xml version="1.0" encoding="UTF-8"?>
<collection xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/emulations/1/emulators">
  <items offset="0" total="1">
<emulator href="/emulations/1/distributions/linear" name="linear"/>
  </items>
  <link href="/distributions/linear" rel="parent" type="application/vnd.cocoma+xml"/>
</collection>
    '''
    return xml_content_distributions


@route('/emulations/<ID>/distributions/<name>', method='GET')
def get_distribution(ID="", name=""):
    response.content_type = CONTENT
    #curl -k -i http://10.55.164.211:8050/emulations/1/distributions/linear
    xml_content_distributionName = '''<?xml version="1.0" encoding="UTF-8"?>
<distribution xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/emulations/1/distributions/linear">
<name>'''+name+'''</name>
   <info>
        Stats: SAT revision 1.0.3_autoconf, 32 bit binary
        Log: buildd @ biber on Thu Jul 29 21:47:10 UTC 2010 from open source release
        Usage: ./sat(32|64) [options]
        ...
   </info>
</emulator>
    '''
    return xml_content_distributionName



    
@route('/ccmsh/hello')
def api_status():
    response.status = 200
    response.headers['status'] = response.status#str(response.status_code())
    response.content_type = "application/vnd.cocoma+xml"
    return "Yes, Hello this is ccmshAPI."



'''
#######
Creating emulation
#######
'''

@route('/emulations/<ID>', method='PUT')
def create_emu(ID=""):
    xml = request.forms.get( "xml" )
    e = request.forms.get("e")
    ret = str(e)+str(xml)+"\n"
    return  ret
    





@route('/ccmsh/create', method='PUT')
def create_emulation():
        
        #checking for daemon
        if ccmsh.daemonCheck()==0:
            return "Daemon is not running or cannot be located. Please check Scheduler configuration"
        else:
            d={}
            
                                     
            emulationName = request.query.get('emulationName')
            distributionType = request.query.get('distributionType')
            resourceType = request.query.get('resourceType')
            emulationType = request.query.get('emulationType')
            startTime = request.query.get('startTime')
            stopTime = request.query.get('stopTime')
            distributionGranularity = request.query.get('distributionGranularity')
            
            #taking up to 10 custom arguments for distribution and adding them to array
            #if is empty we get array: 
            #[None, None, None, None, None, None, None, None, None, None]
            arg=[]
            arg.append(request.query.get('arg0'))
            arg.append(request.query.get('arg1'))
            arg.append(request.query.get('arg2'))
            arg.append(request.query.get('arg3'))
            arg.append(request.query.get('arg4'))
            arg.append(request.query.get('arg5'))
            arg.append(request.query.get('arg6'))
            arg.append(request.query.get('arg7'))
            arg.append(request.query.get('arg8'))
            arg.append(request.query.get('arg9'))
                        
            print arg
            try:           
                emulationID=EmulationManager.createEmulation(emulationName, distributionType, resourceType, emulationType, startTime, stopTime, distributionGranularity,arg)        
                d= {'emulationID':emulationID}
        
                print d
            
                return d
            
            except:
                return "Error: Cannot create emulation please check parameters and conflicts with already created emulations" 
        
'''
Update emulation is not in the documentation and is currently not working.
Later we have to decide how to do it correctly
'''
@route('/ccmsh/update')
def update_emulation():
        
        
        #checking for daemon
        if ccmsh.daemonCheck()==0:
            return "Daemon is not running or cannot be located. Please check Scheduler configuration"
        else:
            #setting all values to NULL
            
            emulationID = 'NULL'
            emulationName = 'NULL'
            distributionType = 'NULL'
            resourceType = 'NULL'
            emulationType = 'NULL'
            startTime = 'NULL'
            stopTime = 'NULL'
            distributionGranularity = 'NULL'
            
            
            
            d={}
            arg=[]
            
            
            
            if request.query.get('emulationID'):
                emulationID = request.query.get('emulationID')
                
                if request.query.get('emulationName'):
                    emulationName = request.query.get('emulationName')
                                
                if request.query.get('distributionType'):
                    distributionType = request.query.get('distributionType')
                
                if request.query.get('resourceType'):
                    resourceType = request.query.get('resourceType')
                
                if request.query.get('emulationType'):
                    emulationType = request.query.get('emulationType')
                    
                if request.query.get('startTime'):
                    startTime = request.query.get('startTime')
                
                if request.query.get('stopTime'):
                    stopTime = request.query.get('stopTime')
                    
                if request.query.get('distributionGranularity'):
                    distributionGranularity = request.query.get('distributionGranularity')
                    
                if request.query.get('arg0'):
                    arg.append(request.query.get('arg0'))
                    
                if request.query.get('arg1'):
                    arg.append(request.query.get('arg1'))
                
                if request.query.get('arg2'):
                    arg.append(request.query.get('arg2'))
                
                if request.query.get('arg3'):
                    arg.append(request.query.get('arg3'))
                
                if request.query.get('arg4'):
                    arg.append(request.query.get('arg4'))
                
                if request.query.get('arg5'):
                    arg.append(request.query.get('arg5'))
                
                if request.query.get('arg6'):
                    arg.append(request.query.get('arg6'))
                
                if request.query.get('arg7'):
                    arg.append(request.query.get('arg7'))
                
                if request.query.get('arg8'):
                    arg.append(request.query.get('arg8'))
                
                if request.query.get('arg9'):
                    arg.append(request.query.get('arg9'))
                    
                
                
                try:
                    EmulationManager.updateEmulation(emulationID,emulationName,distributionType,resourceType,emulationType,startTime,stopTime, distributionGranularity,arg)        
                    d= {'emulationName':emulationName, 'distributionType':distributionType, 'resourceType':resourceType, 'emulationType':emulationType, 'startTime':startTime, 'stopTime':stopTime, 'distributionGranularity':distributionGranularity,'arguments':arg}
                
                    return d
                except:
                    
                    return {'error':'Update could not be done, check your data'}
            
            else:
                
                print "No emulation ID specified"
            
                return {'error':'Update could not be done, Provide Emulation ID'} 
        

@route('/ccmsh/delete')
def emulationDelete():
    #checking for daemon
        if ccmsh.daemonCheck()==0:
            return "{'error':'Daemon is not running or cannot be located. Please check Scheduler configuration'}"
        else:
            try:
                emulationID = request.query.get('emulationID')
                EmulationManager.deleteEmulation(emulationID)
                return "EmulationID: "+emulationID+" was deleted"
            except:
                return "{error:Was not able to delete emulation, check parameters}"

def getifip(ifn):
    import socket, fcntl, struct
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(sck.fileno(),0x8915,struct.pack('256s', ifn[:15]))[20:24])


def startAPI(iface):
    if ccmsh.daemonCheck() ==0:
        sys.exit(0)
    print "Interface: ",iface
    
    run(host=getifip(iface), port=8050)
    
if __name__ == '__main__':
    try: 
        if sys.argv[1] == "-h":
            print "Use ccmshAPI <name of network interface> . Default network interface is eth0."
        else:
            startAPI(sys.argv[1])
    except:
        startAPI("eth0")
    
