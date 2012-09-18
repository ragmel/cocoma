'''
Media type: application/json
we will try to return JSON object 
{
    "firstName": "John",
    "lastName": "Smith",
    "age": 25,
    "address": {
        "streetAddress": "21 2nd Street",
        "city": "New York",
        "state": "NY",
        "postalCode": "10021"
    },
    "phoneNumber": [
        {
            "type": "home",
            "number": "212 555-1234"
        },
        {
            "type": "fax",
            "number": "646 555-4567"
        }
    ]
}


'''


from bottle import route, run,response,request
import optparse,sys,Pyro4
#import argparse - new version of optparse
import EmulationManager,XmlParser
from json import dumps

@route('/hello/:id')
def hello(id):
    #return "Hello World!"
    return "MyID: "+id

@route('/emulation/:listAll')
def get_emulation(listAll):
    
    if listAll=="all":
        emulationSelect=EmulationManager.getEmulation("NULL","NULL",1,0)
    else:
        emulationSelect=EmulationManager.getEmulation("NULL",listAll,0,0)
    
    
    
    if emulationSelect:
            
                #response.content_type = 'application/json'
                response.content_type = 'application/json'
                return dumps(emulationSelect)

            
    else:
        return "myrows2"
        #return "emulation ID: \"",listAll,"\" does not exists"
    
@route('/api/status')
def api_status():
    return {'status':'online', 'servertime':'noon'}

    

    #return "your ID: "+id
#http://10.55.164.240:8050/forum?filters=2
#getall

@route('/forum')
def display_forum():
    terms = unicode (request.query.get('filters','','aa',''), "utf-8")
    print terms


    forum_id = request.query.id
    page = request.query.page or '1'
    return 'Forum ID: %s (page %s)' % (terms, page)

def startAPI():
    run(host='10.55.164.240', port=8050)
    
if __name__ == '__main__':
    startAPI()