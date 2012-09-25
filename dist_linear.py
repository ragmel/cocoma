'''
Created on 25 Sep 2012

@author: i046533
'''
import math


class dist_linear(object):
    
    def __init__(self,startLoad, stopLoad, distributionGranularity,runNo):
    
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

    def hello(self):
        print "This is Python Linear Distribution Module. Input parameters : startLoad, stopLoad, distributionGranularity,runNo "
    
        return ["startLoad", "stopLoad", "distributionGranularity","runNo"]
    

if __name__ == '__main__':
    
    pass