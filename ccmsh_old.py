'''
Created on 16 Aug 2012

@author: i046533

'''

import sys, getopt
import sqlite3
import XmlParser
import EmulationManager
import Daemon
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
            (emulationName,distributionType,resourceType,emulationType,startTime,stopTime, distributionGranularity,startLoad, stopLoad) = XmlParser.xmlReader(xml)
            
            
    
    
    newGetEmu=EmulationManager.getEmulation("NULL","NULL",0,1)
    
    #newEmulationManager =EmulationManager.createEmulation(emulationName, emulationType, resourceType, startTime, stopTime, distributionGranularity, distributionType, startLoad, stopLoad)
 
if __name__ == "__main__":
    main(sys.argv[1:])
   



        