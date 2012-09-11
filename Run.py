'''
Created on 28 Aug 2012
This will be executed as single run from SchedulerControl
@author: ltenru
'''
import os,sys,time,thread
import sqlite3 as sqlite

#timer for the job, has to be set to the run interval
    
def createRun(emulationID,emulationLifetimeID,duration, stressValue,runNo):
    
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
        
        #Connect to DB and write info into runs table
        
        try:
            conn = sqlite.connect('cocoma.sqlite')
            c = conn.cursor()
            #check if this is the last run in batch and update emulation table
            if runNo == 0:
                c.execute('UPDATE emulation SET executed=? , active =? WHERE emulationID =?',["1","NULL",emulationID])
            
            c.execute('Update runLog SET executed=? WHERE emulationLifetimeID=? and runNo=?', ["1",emulationLifetimeID,runNo])
            conn.commit()
        
        except sqlite.Error, e:
            print "Error %s:" % e.args[0]
            print e
            sys.exit(1)
    
        c.close()
        
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