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


import math

def linearCalculate(startLoad, stopLoad, distributionGranularity,runNo):
    linearStep=((int(startLoad)-int(stopLoad))/int(distributionGranularity))
    linearStep=math.fabs((int(linearStep)))
    print "LINEAR STEP SHOULD BE THE SAME"
    print linearStep
    linearStress= ((linearStep*int(runNo)))+int(startLoad)
    #make sure we return integer
    linearStress=int(linearStress)
    print "LINEAR STRESS SHOULD CHANGE"
    print linearStress
    return linearStress

