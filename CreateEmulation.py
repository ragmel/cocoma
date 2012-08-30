'''
Created on 16 Aug 2012

@author: i046533

'''

import sys, getopt
import sqlite3
import SchedulerControl 
import XmlParser


def main(argv):
    
    
    try :
        opts, args = getopt.getopt(argv,"hi:y:s:t:g:p:l:o:x:",["emulationType=", "resourceType=", "startTime=", "stopTime=","distributionGranularity=","distributionType=","startLoad=","stopLoad=","xml="])
    except getopt.GetoptError:
        print "error in parameters"
        sys.exit(2)
  
    for opt,arg in opts:
        if opt =="-h":
            print "help menu"
            sys.exit()
            
        elif opt in ("-i","--emulationType"):
            emulationType=arg
            print (emulationType)
        
        elif opt in ("-y","--resourceType"):
            resourceType = arg
            print resourceType
                
        elif opt in ("-s","--startTime"):
            startTime = arg
            print startTime

        elif opt in ("-t","--stopTime"):
            stopTime = arg
            print stopTime
            
        elif opt in ("-g","--distributionGranularity"):
            distributionGranularity = arg
            print distributionGranularity
        
            
        elif opt in ("-p","--distributionType"):
            distributionType = arg
            print distributionType
            
        #we will separate depending on the distributionType above    
        elif opt in ("-l","--startLoad"):
            startLoad = arg
            print startLoad
            
        elif opt in ("-o","--stopLoad"):
            stopLoad = arg
            print (stopLoad)
        
        #xml file will be option in the future
        elif opt in ("-x", "--xml"):
            xml = arg    
            print "filename is taken as:"
            print (xml)
            #getting parsed variables from xml
            (startTime,stopTime, distributionGranularity,startLoad, stopLoad) = XmlParser.xmlReader(xml)
            
            
    
    
    newScheduler =SchedulerControl.schedulerControl(startTime,stopTime, distributionGranularity,startLoad, stopLoad)
 
if __name__ == "__main__":
    main(sys.argv[1:])
   
#skip DB for now
''' 
    #connecting to the DB and storing parameters
    try:
        conn = sqlite3.connect('cocoma.sqlite')
        c = conn.cursor()
    
        c.execute("INSERT INTO emulation VALUES (?,?,?,?,?,?,?,?,?,?)",(emulationID , emulationName,emulationType,resourceType,emulationDomain,startTime,stopTime,distributionGranularity,distributionParameters, distributionType))
        conn.commit()
    
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        print "SQL error: values might exits or"
        sys.exit(1)
        
    c.execute("SELECT * FROM emulation WHERE emulationID='"+emulationID+"'")
    print "DB entries for emulation ID", emulationID
    print c.fetchone()
        
        
    
    c.close()

'''


        