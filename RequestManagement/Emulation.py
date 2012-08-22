class emulation(object):
    def __init__(self, emulationName, emulationID, emulationType, resourceType, emulationDomain):
        self.emulationID = emulationID
        self.emulationType = emulationType 
        self.resourceType = resourceType
        
        #Possible addition
        self.emulationName = emulationName 
        self.emulationDomain = emulationDomain
        
        print (emulationName)
        print (emulationID)
        print (emulationType)
        print (resourceType)
        print (emulationDomain)       