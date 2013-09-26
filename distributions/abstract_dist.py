import abc
from abc import ABCMeta

class abstract_dist(object):
    
    __metaclass__ = ABCMeta
    
@abc.abstractmethod
def distHelp():
    """
    Used for displaying help about a distribution (eg, what Resources types it can use)
    """
    raise NotImplementedError ("'distHelp' method not Implemented in Distribution Class")

@abc.abstractmethod
def functionCount (emulationID,emulationName,emulationLifetimeID,startTimesec,duration, distributionGranularity,distributionArg,resType,HOMEPATH):
    """
    Used for getting values for: stressValues, runStartTimeList, runDurations
    """
    raise NotImplementedError ("'functionCount' method not Implemented in Distribution Class")

@abc.abstractmethod
def argNames(Rtype=None):
    """
    Used for returning the names of the arguments that a given resource takes
    """
    raise NotImplementedError ("'argNames' method not Implemented in Distribution Class")