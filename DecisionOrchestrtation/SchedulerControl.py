'''
Created on 21 Aug 2012

@author: i046533

1. Get from DB every 5sec unscheduled runs
2. Mark DB that the job is queued  
3. Create job with corresponding name
3. Mark DB that job was scheduled
4. Execute job when time comes(done by external scheduler)
5. When job is done mark DB as executed probably we need to enter this code in the run itself


DB tables for now:

 emulationID       emulatorID      runID    runStartDate    runEndDate    queued      scheduled     executed

 emulation12       stress_md5        1        13135410      13135419         N            N            N
 emulation12       stress_md5        2        13135510      13135519         N            N            N
 emulation12       stress_md5        3        13135610      13135619         N            N            N

New possibly better Alternative:

1. DistributionInstance.py sends runs info directly to SchedulerControl.py
2. Create DB table entries
3. Send Runs directly to scheduler
3a. We can query scheduler directly to see info of the jobs
4. When job is done mark DB as executed probably we need to enter this code in the run itself(optionally)

DB tables for now:

 emulationID       emulatorID      runID    runStartDate    runEndDate    executed

 emulation12       stress_md5        1        13135410      13135419         N
 emulation12       stress_md5        2        13135510      13135519         N
 emulation12       stress_md5        3        13135610      13135619         N



Future challenges:
Update runs
Lost runs problem


'''


from datetime import datetime
import time
from apscheduler.scheduler import Scheduler 
import threading

# Start the scheduler
sched = Scheduler()
sched.start()


'''
Creating Job function here which will be executed by scheduler
'''

#timer for the job, has to be set to the run interval
    
class stressRun(object):
    def __init__(self, emulatorID, distributionType, distributionGranularity , distributionParameters,startTime, endTime, runTime):
        self.distributionType = distributionType, 
        self.distributionGranularity = distributionGranularity
        self.distributionParameters  = distributionParameters
        self.emulatorID =emulatorID
        self.runTime =runTime
        #getting already converted values in seconds
        self.endTime = endTime 
        self.startTime = startTime
        
        while runTime >0:
            time.sleep(1)
            #print(boom)
            runTime -=1
        
    def threadstone(self):
        t1_stop= threading.Event()
        t1 = threading.Thread(target=thread1, args=(1, t1_stop))

        t2_stop = threading.Event()
        t2 = threading.Thread(target=thread2,  args=(2, t2_stop))

        time.sleep(1)
        #stop the thread2
        t2_stop.set()

        def thread1(arg1, stop_event):
            while(not stop_event.is_set()):
                #equivalent to time.sleep()
                stop_event.wait(time)
                pass


        def thread2(arg1, stop_event):
            while(not stop_event.is_set()):
                stop_event.wait(time)
                pass













def job_function():
    print "Hello World"

# Schedule job_function to be called every two hours
sched.add_interval_job(job_function, hours=2)

# The same as before, but start after a certain time point
sched.add_interval_job(job_function, hours=2, start_date='2010-10-10 09:30')





















