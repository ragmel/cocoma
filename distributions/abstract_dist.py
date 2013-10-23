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