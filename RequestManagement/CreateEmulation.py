'''
Created on 16 Aug 2012

@author: i046533

'''

import sys, getopt
import Distribution 
import EmulationLifetime 
import Emulation
import sqlite3
import DecisionOrchestrtation.DistributionInstance

#we are getting CLI parameters to create emulation
def main(argv):
    
    
    try :
        opts, args = getopt.getopt(argv,"hn:i:t:y:d:m:e:g:p:s:x:",["emulationName=","emulationID=","emulationType=", "resourceType=", "emulationDomain=", "startTime=", "endTime=","distributionGranularity=","distributionParameters=","distributionType=","xml="])
    except getopt.GetoptError:
        print "error"
        sys.exit(2)
  
    for opt,arg in opts:
        if opt =="-h":
            print "help menu"
            sys.exit()
            
        elif opt in ("-n","--emulationName"):
            emulationName=arg
        #emulation id will be automatically generated in the future
        elif opt in ("-i","--emulationID"):
            emulationID = arg
            
        
        elif opt in ("-t","--emulationType"):
            emulationType = arg
            
        
        elif opt in ("-y","--resourceType"):
            resourceType = arg

        
        elif opt in ("-d","--emulationDomain"):
            emulationDomain = arg
            
        
        elif opt in ("-m","--startTime"):
            startTime = arg

        elif opt in ("-e","--endTime"):
            endTime = arg
            
        elif opt in ("-g","--distributionGranularity"):
            distributionGranularity = arg

        elif opt in ("-p","--distributionParameters"):
            distributionParameters = arg
            
        elif opt in ("-s","--distributionType"):
            distributionType = arg
            
        #xml file will be option in the future
        elif opt in ("-x", "--xml"):
            xml = arg
        
    
    
    
   
    print (xml)
    
    #connecting to the DB and storing parameters
    try:
        conn = sqlite3.connect('cocoma.sqlite')
        c = conn.cursor()
    
        c.execute("INSERT INTO emulation VALUES (?,?,?,?,?,?,?,?,?,?)",(emulationID , emulationName,emulationType,resourceType,emulationDomain,startTime,endTime,distributionGranularity,distributionParameters, distributionType))
        conn.commit()
    
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        print "SQL error: values might exits or"
        sys.exit(1)
        
    c.execute("SELECT * FROM emulation WHERE emulationID='"+emulationID+"'")
    print "DB entries for emulation ID", emulationID
    print c.fetchone()
        
        
    
    c.close()



#with each created instance we are giving the things to internal modules
    newEmulation = Emulation.emulation(emulationName, emulationID, emulationType, resourceType, emulationDomain)
    newEmulationLifetime = EmulationLifetime.emulationLifetime(startTime, endTime)
    newDistribution = Distribution.distribution(distributionType, distributionGranularity , distributionParameters)
    #testing purpose emulatorID should come from EmulationProcessor
    emulatorID="dummy"
    newdistributionInstance = DecisionOrchestrtation.DistributionInstance.distributionInstance(emulatorID, distributionType, distributionGranularity , distributionParameters,startTime, endTime)
    
if __name__ == "__main__":
    main(sys.argv[1:])
        