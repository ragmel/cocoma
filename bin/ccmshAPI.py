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
import sys,os, time
from datetime import datetime as dt
import EmulationManager,ccmsh,DistributionManager
from json import dumps
from xml.etree import ElementTree
from xml.dom import minidom
import xml.etree.ElementTree as ET




def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    
    
    rough_string = ET.tostring(elem, encoding="utf-8", method='xml')
    
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")



try:
    HOMEPATH= os.environ['COCOMA']
except:
    print "no $COCOMA environmental variable set"
CONTENT = "application/vnd.bonfire+xml"


'''
#######
COCOMA ROOT
#######
'''
@route('/', method ="GET")
def get_root():
    #curl -k -i http://10.55.164.232:8050/
    response.set_header('Content-Type', 'application/vnd.bonfire+xml')
    ET.register_namespace("test", "http://127.0.0.1/cocoma")
    
    root = ET.Element('root', { 'href':'/'})
    ver = ET.SubElement(root, 'version')
    ver.text = '0.1.1'
    ts = ET.SubElement(root, 'timestamp')
    ts.text = str(time.time())
    lk = ET.SubElement(root, 'link', {'rel':'emulations', 'href':'/emulations', 'type':'application/vnd.bonfire+xml'})
    lk = ET.SubElement(root, 'link', {'rel':'emulationshistory', 'href':'/emulationshistory', 'type':'application/vnd.bonfire+xml'})
    lk = ET.SubElement(root, 'link', {'rel':'emulators', 'href':'/emulators', 'type':'application/vnd.bonfire+xml'})
    lk = ET.SubElement(root, 'link', {'rel':'distributions', 'href':'/distributions', 'type':'application/vnd.bonfire+xml'})
    

    return prettify(root)
    

'''
#######
GET emulation
#######
'''
@route('/emulationshistory/', method ='GET')
@route('/emulationshistory', method ='GET')
def get_emulationsHistory():
    
    emuList=EmulationManager.getAllEmulationList()
    
    response.set_header('Content-Type', 'application/vnd.bonfire+xml')
    
    '''
    XML namespaces are used for providing uniquely named elements and attributes in an XML document.
    '''
    
    ET.register_namespace("test", "http://127.0.0.1/cocoma")
    
    #building the XML we will return
    emulations = ET.Element('collection', { 'xmlns':'http://127.0.0.1/cocoma','href':'/emulationshistory'})
    #<items offset="0" total="2">
    items =ET.SubElement(emulations,'items', { 'offset':'0','total':str(len(emuList))})
    
    #<emulator href="/emulations/1" name="Emu1"/>
    
    for elem in emuList :
        emulator = ET.SubElement(items,'emulator', { 'href':'/emulationshistory/'+str(elem[0]),'name':str(elem[1])})
        
    
    #<link href="/" rel="parent" type="application/vnd.cocoma+xml"/>
    lk = ET.SubElement(emulations, 'link', {'rel':'parent', 'href':'/', 'type':'application/vnd.bonfire+xml'})
    
    

    return prettify(emulations)    

   
    
    '''
    ##############
    DUMMY
    ##############
    '''
    #curl -k -i http://10.55.164.211:8050/emulations
    #xml_content_emulations=
    '''
    <?xml version="1.0" encoding="UTF-8"?>
    <collection xmlns="file:///home/melo/cocoma" href="/emulations">
      <items offset="0" total="2">
        <emulator href="/emulations/1" name="Emu1"/>
        <emulator href="/emulations/2" name="Emu2"/>
      </items>
      <link href="/" rel="parent" type="application/vnd.cocoma+xml"/>
    </collection>
    '''    
    
    #return xml_content_emulations  
    
    
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
@route('/emulations/', method ='GET')
@route('/emulations', method ='GET')
def get_emulations():
    
    emuList=EmulationManager.getActiveEmulationList()
    
    response.set_header('Content-Type', 'application/vnd.bonfire+xml')
    
    '''
    XML namespaces are used for providing uniquely named elements and attributes in an XML document.
    '''
    
    ET.register_namespace("test", "http://127.0.0.1/cocoma")
    
    #building the XML we will return
    emulations = ET.Element('collection', { 'xmlns':'http://127.0.0.1/cocoma','href':'/emulations'})
    #<items offset="0" total="2">
    items =ET.SubElement(emulations,'items', { 'offset':'0','total':str(len(emuList))})
    
    #<emulator href="/emulations/1" name="Emu1"/>
    
    for elem in emuList :
        emulator = ET.SubElement(items,'emulator', { 'href':'/emulations/'+str(elem[0]),'name':str(elem[1])})
        
    
    #<link href="/" rel="parent" type="application/vnd.cocoma+xml"/>
    lk = ET.SubElement(emulations, 'link', {'rel':'parent', 'href':'/', 'type':'application/vnd.bonfire+xml'})
    
    

    return prettify(emulations)


@route('/emulations/<ID>/', method='GET')
@route('/emulations/<ID>', method='GET')
def get_emulation(ID=""):
    
    #curl -k -i http:///10.55.164.232:8050/emulations/1
    
    response.set_header('Content-Type', 'application/vnd.bonfire+xml')
    
    try:
        (emulationID,emulationName,emulationType, resourceTypeEmulation, startTimeEmu,stopTimeEmu, distroList)=EmulationManager.getEmulation(ID)
    except:
        return "<error>Wrong ID</error>"

    ET.register_namespace("test", "http://127.0.0.1/cocoma")
    
    #building the XML we will return
    emulation = ET.Element('emulation', { 'xmlns':'http://127.0.0.1/cocoma','href':'/emulations/'+str(ID)})
    #<id>1</id>
    idXml =ET.SubElement(emulation,'id')
    idXml.text = str(emulationID)
    #<emulationName>myMixEmu</emulationName>
    emulationNameXml =ET.SubElement(emulation,'emulationName')
    emulationNameXml.text = emulationName
    
    #<emulationType>Mix</emulationType>
    emulationTypeXml =ET.SubElement(emulation,'emulationType')
    emulationTypeXml.text = emulationType
    
    #<resourceType>Mix</resourceType>
    resourceTypeXml =ET.SubElement(emulation,'resourceType')
    resourceTypeXml.text = resourceTypeEmulation
        
    #<startTime>now</startTime>
    startTimeEmuXml =ET.SubElement(emulation,'startTime')
    startTimeEmuXml.text = startTimeEmu    
    
    #<stopTime>now+180</stopTime>
    stopTimeEmuXml =ET.SubElement(emulation,'stopTime')
    stopTimeEmuXml.text = str(stopTimeEmu)
    
    #create distributions list
    for distro in distroList :
        #<distributions ID="1" name="myMixEmu-dis-1" >
        distributionsXml = ET.SubElement(emulation,'distributions', { 'ID':str(distro['distributionsID']),'name':distro['distributionsName']})
        
        startTimeDistroXml=ET.SubElement(distributionsXml,'startTime')
        startTimeDistroXml.text = str(distro['startTimeDistro'])
        
        durationDistroXml=ET.SubElement(distributionsXml,'duration')
        durationDistroXml.text = str(distro['durationDistro'])
        
        distroArgs = distro['distroArgs']
        for distroArg in distroArgs:
            distroArgXml =ET.SubElement(distributionsXml,distroArg) 
            distroArgXml.text = str(distroArgs[distroArg])
        
        
        #<distribution href="/distributions/geometric" name="geometric" />
        distributionXml = ET.SubElement(distributionsXml,'distribution', { 'href':'/distributions/'+ str(distro['distrType']),'name':str(distro['distrType'])})
        
        #<emulator href="/emulators/wireshark" name="wireshark" />
        emulatorXml = ET.SubElement(distributionsXml,'emulator', { 'href':'/emulators/'+ str(distro['emulatorName']),'name':str(distro['emulatorName'])})
        
        emulatorParamsXml = ET.SubElement(distributionsXml,'emulator-params')

        resourceTypeXml=ET.SubElement(emulatorParamsXml,'resourceType')
        resourceTypeXml.text = str(distro['resourceTypeDist'])
        
        
        emulatorArg = distro['emulatorArg']
        for emuArg in emulatorArg:
            emuArgXml =ET.SubElement(emulatorParamsXml,emuArg) 
            emuArgXml.text = str(emulatorArg[emuArg])

    
    #<link href="/" rel="parent" type="application/vnd.cocoma+xml"/>
    lk0 = ET.SubElement(emulation, 'link', {'rel':'parent', 'href':'/', 'type':'application/vnd.bonfire+xml'})
    #<link href="/emulations" rel="parent" type="application/vnd.cocoma+xml"/>
    lk0 = ET.SubElement(emulation, 'link', {'rel':'parent', 'href':'/emulations', 'type':'application/vnd.bonfire+xml'})
    lk0 = ET.SubElement(emulation, 'link', {'rel':'parent', 'href':'/emulationshistory', 'type':'application/vnd.bonfire+xml'})
    
    

    return prettify(emulation)    

@route('/emulators/', method='GET')
@route('/emulators', method='GET')
def get_emulators():
    
    ET.register_namespace("test", "http://127.0.0.1/cocoma")
    response.set_header('Content-Type', 'application/vnd.bonfire+xml')
    
    
    emuList=DistributionManager.listEmulations()
    print "emulist",emuList
    '''
    XML namespaces are used for providing uniquely named elements and attributes in an XML document.
    '''
    
    
    
    #building the XML we will return
    emulators = ET.Element('collection', { 'xmlns':'http://127.0.0.1/cocoma','href':'/emulators'})
    #<items offset="0" total="2">
    items =ET.SubElement(emulators,'items', { 'offset':'0','total':str(len(emuList))})
    
    #<emulator href="/emulations/1" name="Emu1"/>
    
    for elem in emuList :
        emulator = ET.SubElement(items,'emulator', { 'href':'/emulators/'+str(elem),'name':str(elem)})
        
        
    
    #<link href="/" rel="parent" type="application/vnd.cocoma+xml"/>
    lk = ET.SubElement(emulators, 'link', {'rel':'parent', 'href':'/', 'type':'application/vnd.bonfire+xml'})
    
    

    return prettify(emulators)




@route('/emulators/<name>/', method='GET')
@route('/emulators/<name>', method='GET')
def get_emulator(name=""):
    
    ET.register_namespace("test", "http://127.0.0.1/cocoma")
    response.set_header('Content-Type', 'application/vnd.bonfire+xml')
    
    helpMod=DistributionManager.loadEmulatorHelp(name)
    
    
    emulatorXml = ET.Element('emulator', { 'xmlns':'http://127.0.0.1/cocoma','href':'/emulator/'+str(name)})
    
    emulatorHelpXml=ET.SubElement(emulatorXml,'info')
    emulatorHelpXml.text = str(helpMod())    
    
    #distroArgXml=ET.SubElement(distributionXml,'arguments')
    #distroArgXml.text = str(argMod())    
    
    lk0 = ET.SubElement(emulatorXml, 'link', {'rel':'parent', 'href':'/', 'type':'application/vnd.bonfire+xml'})
    #<link href="/emulations" rel="parent" type="application/vnd.cocoma+xml"/>
    lk0 = ET.SubElement(emulatorXml, 'link', {'rel':'parent', 'href':'/emulators', 'type':'application/vnd.bonfire+xml'})
    
    
    return prettify(emulatorXml)    
    
    
    #curl -k -i http://10.55.164.211:8050/emulations/1/emulators/stressapptest
 
@route('/distributions/', method='GET')
@route('/distributions', method='GET')
def get_distributions():
    
    ET.register_namespace("test", "http://127.0.0.1/cocoma")
    response.set_header('Content-Type', 'application/vnd.bonfire+xml')
    
    
    distroList=DistributionManager.listDistributions()
    print "distroList",distroList
    '''
    XML namespaces are used for providing uniquely named elements and attributes in an XML document.
    '''
    
    
    
    #building the XML we will return
    distributions = ET.Element('collection', { 'xmlns':'http://127.0.0.1/cocoma','href':'/distributions'})
    #<items offset="0" total="2">
    items =ET.SubElement(distributions,'items', { 'offset':'0','total':str(len(distroList))})
    
    #<distribution href="/emulations/1" name="Emu1"/>
    
    for elem in distroList :
        distribution = ET.SubElement(items,'distribution', { 'href':'/distributions/'+str(elem),'name':str(elem)})
        
        
    
    #<link href="/" rel="parent" type="application/vnd.cocoma+xml"/>
    lk = ET.SubElement(distributions, 'link', {'rel':'parent', 'href':'/', 'type':'application/vnd.bonfire+xml'})
    
    

    return prettify(distributions)

@route('/distributions/<name>/', method='GET')
@route('/distributions/<name>', method='GET')
def get_distribution(name=""):
    #curl -k -i http://10.55.164.232:8050/distributions/linear
    
    ET.register_namespace("test", "http://127.0.0.1/cocoma")
    response.set_header('Content-Type', 'application/vnd.bonfire+xml')
    
    helpMod=DistributionManager.loadDistributionHelp(name)
    argMod=DistributionManager.loadDistributionArgNames(name)
    
    distributionXml = ET.Element('distribution', { 'xmlns':'http://127.0.0.1/cocoma','href':'/distributions/'+str(name)})
    
    distroHelpXml=ET.SubElement(distributionXml,'info')
    distroHelpXml.text = str(helpMod())    
    
    distroArgXml=ET.SubElement(distributionXml,'arguments')
    distroArgXml.text = str(argMod())    
    
    lk0 = ET.SubElement(distributionXml, 'link', {'rel':'parent', 'href':'/', 'type':'application/vnd.bonfire+xml'})
    #<link href="/emulations" rel="parent" type="application/vnd.cocoma+xml"/>
    lk0 = ET.SubElement(distributionXml, 'link', {'rel':'parent', 'href':'/distributions', 'type':'application/vnd.bonfire+xml'})
    
    
    return prettify(distributionXml)
 



    
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
    