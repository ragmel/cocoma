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
    #response.content_type = CONTENT
    #response.headers['Content-Type'] = 'application/vnd.cocoma+xml'
    '''
    ######################
    HEADER
    ######################
    '''
    
    
    
    
    response.set_header('Allow', 'GET,OPTIONS,HEAD')
    response.set_header('Cache-Control', 'public,max-age=120')
    response.content_type = 'application/vnd.bonfire+xml; charset=utf-8'
    # have no idea if we need these
    #response.set_header('ETag', '1039483f4e6f724fa5cc5d0e8019b404')
    #response.set_header('X-UA-Compatible', 'IE=Edge,chrome=1')
    #response.set_header('X-Runtime', '0.004356')
    #response.set_header('Vary', 'Authorization,Accept')
    response.set_header('Connection', 'close')
    response.set_header('Transfer-Encoding', 'chunked')
    
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
    #curl -k -i http://10.55.164.211:8050/emulations
    xml_content_emulations='''<?xml version="1.0" encoding="UTF-8"?>
<collection xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/emulations">
  <items offset="0" total="2">
    <emulator href="/emulations/1" name="Emu1"/>
    <emulator href="/emulations/2" name="Emu2"/>
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
  <distributions name=" myMixEmu-dis-2">
     <startTime>60</startTime>
     <!--duration in seconds -->
     <duration>60</duration>
     <distribution href="/distributions/poisson" name="poisson" />
      <emulator href="/emulators/stress" name="stress" />
      <emulator-params>
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
  <distributions name=" myMixEmu-dis-4">
     <startTime>120</startTime>
     <!--duration in seconds -->
     <duration>60</duration>
     <distribution href="/distributions/poisson" name="poisson" />
      <emulator href="/emulators/stressapptest" name="stressapptest" />
      <emulator-params>
        <resourceType>CPU</resourceType>
      </emulator-params>
  </distributions>
  <distributions name=" myMixEmu-dis-5">
     <startTime>120</startTime>
     <!--duration in seconds -->
     <duration>60</duration>
     <distribution href="/distributions/geometric" name="geometric" />
      <emulator href="/emulators/wireshark" name="wireshark" />
      <emulator-params>
        <resourceType>net</resourceType>
      </emulator-params>
  </distributions>
  <link rel="parent" href="/"/>
  <link href="/emulations" rel="parent" type="application/vnd.cocoma+xml"/>
</emulation>'''
    return xml_content_emulationsID
    
    
    
    
    
    '''
    xml = request.forms.get( "xml" )
    e = request.forms.get("e")
    ret = str(e)+str(xml)+"\n"
    return  ret
    '''


@route('/emulators', method='GET')
def get_emulators(ID=""):
    response.content_type = CONTENT
    #curl -k -i http://10.55.164.211:8050/emulations/1/emulators
    xml_content_emulators ='''<?xml version="1.0" encoding="UTF-8"?>
<collection xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/emulators">
  <items offset="0" total="2">
    <emulator href="/emulators/stressapptest" name="stressapptest"/>
    <emulator href="/emulators/stress" name="stress"/>
  </items>
  <link href="/" rel="parent" type="application/vnd.cocoma+xml"/>
</collection>
    '''
    return xml_content_emulators




@route('/emulators/<name>', method='GET')
def get_emulator(name=""):
    response.content_type = CONTENT
    #curl -k -i http://10.55.164.211:8050/emulations/1/emulators/stressapptest
    xml_content_emulatorName = '''<?xml version="1.0" encoding="UTF-8"?>
<emulator xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/emulators/stressapptest">
   <name>'''+name+'''</name>
   <info>
        Stats: SAT revision 1.0.3_autoconf, 32 bit binary
        Log: buildd @ biber on Thu Jul 29 21:47:10 UTC 2010 from open source release
        Usage: ./sat(32|64) [options]
         -M mbytes        megabytes of ram to test
         -H mbytes        minimum megabytes of hugepages to require
         -s seconds       number of seconds to run
         -m threads       number of memory copy threads to run
         -i threads       number of memory invert threads to run
         -C threads       number of memory CPU stress threads to run
         --findfiles      find locations to do disk IO automatically
         -d device        add a direct write disk thread with block device (or file) 'device'
         -f filename      add a disk thread with tempfile 'filename'
         -l logfile       log output to file 'logfile'
         --max_errors n   exit early after finding 'n' errors
         -v level         verbosity (0-20), default is 8
         -W               Use more CPU-stressful memory copy
         -A               run in degraded mode on incompatible systems
         -p pagesize      size in bytes of memory chunks
         --filesize size  size of disk IO tempfiles
         -n ipaddr        add a network thread connecting to system at 'ipaddr'
         --listen         run a thread to listen for and respond to network threads.
         --no_errors      run without checking for ECC or other errors
         --force_errors   inject false errors to test error handling
         --force_errors_like_crazy   inject a lot of false errors to test error handling
         -F               don't result check each transaction
         --stop_on_errors  Stop after finding the first error.
         --read-block-size     size of block for reading (-d)
         --write-block-size    size of block for writing (-d). If not defined, the size of block for writing will be defined as the size of block for reading
         --segment-size   size of segments to split disk into (-d)
         --cache-size     size of disk cache (-d)
         --blocks-per-segment  number of blocks to read/write per segment per iteration (-d)
         --read-threshold      maximum time (in us) a block read should take (-d)
         --write-threshold     maximum time (in us) a block write should take (-d)
         --random-threads      number of random threads for each disk write thread (-d)
         --destructive    write/wipe disk partition (-d)
         --monitor_mode   only do ECC error polling, no stress load.
         --cc_test        do the cache coherency testing
         --cc_inc_count   number of times to increment the cacheline's member
         --cc_line_count  number of cache line sized datastructures to allocate for the cache coherency threads to operate
         --paddr_base     allocate memory starting from this address
         --pause_delay    delay (in seconds) between power spikes
         --pause_duration duration (in seconds) of each pause
         --local_numa : choose memory regions associated with each CPU to be tested by that CPU
         --remote_numa : choose memory regions not associated with each CPU to be tested by that CPU
   </info>
</emulator>
    '''
    
    return xml_content_emulatorName

@route('/distributions', method='GET')
def get_distributions(ID=""):
    response.content_type = CONTENT
    #curl -k -i http://10.55.164.211:8050/emulations/1/distributions
    xml_content_distributions ='''<?xml version="1.0" encoding="UTF-8"?>
<collection xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/distributions">
  <items offset="0" total="2">
    <distribution href="/distributions/linear" name="linear"/>
    <distribution href="/distributions/poisson" name="poisson"/>
  </items>
  <link href="/" rel="parent" type="application/vnd.cocoma+xml"/>
</collection>
    '''
    return xml_content_distributions


@route('/distributions/<dtype>', method='GET')
def get_distribution(dtype=""):
    response.content_type = CONTENT
    #curl -k -i http://10.55.164.211:8050/emulations/1/distributions/linear
    xml_content_distributionName = '''<?xml version="1.0" encoding="UTF-8"?>
<distribution xmlns="http://api.bonfire-project.eu/doc/schemas/cocoma" href="/distributions/linear">
   <distributionType>'''+dtype+'''</distributionType>
   <info>
        --g        granularity
        --st    startTime
        --d        duration
        --sl    startLoad
        --stl    stopLoad
        ...
   </info>
</distribution>
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
    
