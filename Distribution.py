'''
Created on 16 Aug 2012

Linear needs these specific parameters:
startLoad
stopLoad
granularity 
runNo

returns the difference



@author: i046533
'''

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

