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
import optparse,sys,Pyro4,itertools
#import argparse - new version of optparse
import EmulationManager,XmlParser,ccmsh
from json import dumps

@route('/hello/:id')
def hello(id):
    #return "Hello World!"
    return "MyID: "+id

@route('/ccmsh/list')
def get_emulation():
    emulationID = request.query.get('emulationID')
    if emulationID=="all":
        emulationSelect=EmulationManager.getEmulation("NULL","NULL",1,0)
    else:
        emulationSelect=EmulationManager.getEmulation("NULL",emulationID,0,0)
    
    
    
    if emulationSelect:
            
                response.content_type = 'application/json'
                return dumps(emulationSelect)

    else:
        
        return "emulation ID: \"",emulationID,"\" does not exists"
    
@route('/ccmsh/hello')
def api_status():
    return "Yes, Hello this is ccmshAPI."


@route('/ccmsh/create')
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
            EmulationManager.createEmulation(emulationName, distributionType, resourceType, emulationType, startTime, stopTime, distributionGranularity,arg)        
            d= {'emulationName':emulationName, 'distributionType':distributionType, 'resourceType':resourceType, 'emulationType':emulationType, 'startTime':startTime, 'stopTime':stopTime, 'distributionGranularity':distributionGranularity,'arg1':arg[0], 'arg2':arg[1]}
        
            print d
            
            return d 
        

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
            startLoad = 'NULL'
            stopLoad = 'NULL'
            
            d={}
            
            
            
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
                    
                if request.query.get('startLoad'):
                    startLoad = request.query.get('startLoad')
                
                if request.query.get('stopLoad'):
                    stopLoad = request.query.get('stopLoad')
        
                EmulationManager.updateEmulation(emulationID,emulationName,distributionType,resourceType,emulationType,startTime,stopTime, distributionGranularity,startLoad, stopLoad)        
                d= {'emulationName':emulationName, 'distributionType':distributionType, 'resourceType':resourceType, 'emulationType':emulationType, 'startTime':startTime, 'stopTime':stopTime, 'distributionGranularity':distributionGranularity,'startLoad':startLoad, 'stopLoad':stopLoad}
                
                return d
            
            else:
                
                print "No emulation ID specified"
            
                return "Error: Provide Emulation ID" 
        

@route('/ccmsh/delete')
def emulationDelete():
    #checking for daemon
        if ccmsh.daemonCheck()==0:
            return "Daemon is not running or cannot be located. Please check Scheduler configuration"
        else:
            emulationID = request.query.get('emulationID')
            EmulationManager.deleteEmulation(emulationID)
            return "EmulationID: "+emulationID+" was deleted"

def startAPI():
    run(host='10.55.164.240', port=8050)
    
if __name__ == '__main__':
    startAPI()