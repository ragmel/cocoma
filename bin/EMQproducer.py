#!/usr/bin/env python
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

import logging
from logging import handlers
import pika, time, datetime, sys, os
import sqlite3 as sqlite
import json
import Library
#from EmulationManager import *

global HOMEPATH
#HOMEPATH = Library.getHomepath()
try:
    HOMEPATH= os.environ['COCOMA']
except:
    print "no $COCOMA environmental variable set"

logging.getLogger('pika').setLevel(logging.DEBUG)


class Producer():
  
    def __init__(self):
        self.init()

    def init(self):
        
        try:
            mqconfig = MQconfigLoad()
            self.enabled = mqconfig[0][0]
            self.vhost = mqconfig[0][1]
            self.exchange = mqconfig[0][2]
            self.user = mqconfig[0][3]
            self.password = mqconfig[0][4]
            self.host = mqconfig[0][5]
            self.topic = mqconfig[0][6]
            
        except:
            self.enabled = "no"
            self.vhost = ""
            self.exchange = ""
            self.user = ""
            self.password = ""
            self.host = ""
            self.topic = ""            
            pass
    
	#print "In Producer 1: "+ vhost + " " + exchange + " " + user + " " + password + " " + host + " " + topic

    def sendmsg(self,loggingName,message):
        if self.enabled == "yes":
            frtmsg = self.formatmsg(self.topic,loggingName,message)
            #print "In Producer 3, frtmsg: "+frtmsg
            credentials = pika.PlainCredentials(self.user, self.password)
            #print "In Producer 2 "+ self.vhost + " " + self.exchange + " " + self.user + " " + self.password + " " + self.host + " " + self.topic
            #self.vhost = "bonfire"
            #self.exchange = "experiments"
            #self.user = "eventreader"
            #self.password = "reader1348"
            #self.host = "mq.bonfire-project.eu"
            #self.topic = "f47aa8ce21c2273d077b"
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, virtual_host=self.vhost, credentials=credentials))
            #print "In Producer 4"
            channel = connection.channel()
            channel.basic_publish(exchange=self.exchange, routing_key=self.topic,body=json.dumps(frtmsg))
            #print " [x] Sent %s:%s" % (self.topic, frtmsg)
            print " [x] Sent: "+ json.dumps(frtmsg)
            connection.close()

    def formatmsg(self, topic, name, message):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #newmsg = st+';'+name+';'+message
	#print "scheduler.getUniqueID: "+self.scheduler.getUniqueID()
        data = {"Timestamp":ts, "From":name, "Message":message}
        #data2 = unicode(data, 'latin-1')
        return data

class BroadcastLogHandler(logging.Handler):
    def __init__(self,loggingName,producer):
        self.broadcaster = producer
        #print "In BroadcastLogHandler 1"
        self.level = 0
        self.filters = []
        self.lock = 0
	self.loggingname = loggingName
        #self.machine = os.uname()[1]

    def emit(self,record):
        # Send the log message to the broadcast queue
	#print "Who calls Producer.emit: "+sys._getframe(1).f_code.co_name
        message = "%s" % (record.msg)
        self.broadcaster.sendmsg(self.loggingname,message)
        #print "In BroadcastLogHandler 2"

def StreamAndBroadcastHandler(loggingName,producer,level=logging.DEBUG):
    "Factory function for a logging.StreamHandler instance connected to your namespace."
    logger = logging.getLogger(loggingName)
    logger.setLevel(level)
    handler_messages = BroadcastLogHandler(loggingName,producer)
    logger.addHandler(handler_messages)
    #print "In StreamAndBroadcastHandler"

def MQconfig(arguments):
     try:
        if len(arguments)==7:
            #print "got 7 arguments"
                if (arguments["emulationMQenable"]=="yes") or (arguments["emulationMQenable"]=="no") :
                        if HOMEPATH:
                            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')

                        c = conn.cursor()
                        #print "In producer MQconfig: "+str(arguments.values())
                        c.execute('DELETE from MQconfig')
                        c.execute('INSERT INTO MQconfig (enabled,vhost,exchange,user,password,host,topic) VALUES (?, ?, ?, ?, ?, ?, ?)',[arguments["emulationMQenable"],arguments["emulationMQvhost"],arguments["emulationMQexchange"],arguments["emulationMQuser"],arguments["emulationMQpassword"],arguments["emulationMQhost"],arguments["emulationMQtopic"]])
                        conn.commit()
                        c.close()
                        #print "In producer MQconfig 2: "+str(arguments.values())
                else:
                        print "Enabled parameter accepts either 'yes' or 'no'"
        else:
            print "MQproducer Not all arguments supplied, check help: "+ str(len(arguments))
     except sqlite.Error, e:
        print "MQconfig(arguments) SQL Error %s:" % e.args[0]
        print e
        return "<error>str(e)</error>"
        sys.exit(1)

def MQconfigDelete():
     try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')

        c = conn.cursor()
        #print "In producer MQconfig: "+enabled+" "+vhost+" "+exchange+" "+user+" "+password+" "+host+" "+topic
        c.execute('DELETE from MQconfig')
        conn.commit()
        c.close()

     except sqlite.Error, e:
        print "MQconfigDelete() SQL Error %s:" % e.args[0]
        print e
        return "<error>str(e)</error>"
        sys.exit(1)

def MQconfigEnable(enabled):
     try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')

        c = conn.cursor()
        #print "In producer MQconfig: "+enabled+" "+vhost+" "+exchange+" "+user+" "+password+" "+host+" "+topic
        c.execute('UPDATE MQconfig SET enabled = (?)',[enabled])
        conn.commit()
        c.close()

     except sqlite.Error, e:
        print "MQconfigEnable() SQL Error %s:" % e.args[0]
        print e
        return "<error>str(e)</error>"
        sys.exit(1)

def MQconfigLoad():
     try:
        if HOMEPATH:
            conn = sqlite.connect(HOMEPATH+'/data/cocoma.sqlite')

        c = conn.cursor()
        #print "In producer MQconfig: "+enabled+" "+vhost+" "+exchange+" "+user+" "+password+" "+host+" "+topic
        c.execute('SELECT * from MQconfig')
        mqconfig = c.fetchall()
        #for par in mqconfig:
            #for i in range(0,6):
        #    print "enabled: "+str(par[0])+", vhost: "+par[1]+", exchange: "+par[2]+", user: "+par[3]+", password: "+par[4]+", host: "+par[5]+", topic: "+par[6]
        
        conn.commit()
        return mqconfig
        c.close()

     except sqlite.Error, e:
        print "MQconfigLoad() SQL Error %s:" % e.args[0]
        print e
        return "<error>str(e)</error>"
        sys.exit(1)

     

def MQconfigShow():
        mqconfig=MQconfigLoad()
        for par in mqconfig:
            #for i in range(0,6):
            print "enabled: "+str(par[0])+", vhost: "+par[1]+", exchange: "+par[2]+", user: "+par[3]+", password: "+par[4]+", host: "+par[5]+", topic: "+par[6]
