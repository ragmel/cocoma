'''
Created on 28 Aug 2012
This will be executed as single run from SchedulerControl
@author: ltenru
'''
import os,sys,time,thread

#timer for the job, has to be set to the run interval
    
def createRun(duration, stressValue):
    
        duration=str(duration)
        stressValue = str(stressValue)
        print duration
        print stressValue
                
        #for testing reasons commands are commented  and replaced with echo
        #os.system("cpulimit -e stressapptest -l "+stressValue+"&")
        os.system("echo cpulimit -e stressapptest -l "+stressValue+"&")
        print "cpu limit executed"
        #os.system("stressapptest -s "+duration)
        os.system("echo stressapptest -s "+duration)
        
        print"stressapp test executed"
        #and second thread runs this
        #while duration >0:
        #    time.sleep(1)
         #   print(duration)
          #  duration = duration-1
    
    #shut down scheduler emergency
    #sched.shutdown(wait=False)
    
        #sys.exit()
    
if __name__ == '__main__':
    print "main"
    
    duration = 10
    stressValue = 50
    createRun(duration,stressValue)