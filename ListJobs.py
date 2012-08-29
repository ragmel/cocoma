'''
Created on 29 Aug 2012

We need a way to see list of the jobs that are scheduled. Somehow.

'''
from apscheduler.scheduler import Scheduler 
import CreateRun

if __name__ == '__main__':
    
    sched = Scheduler()
    sched.start()
    sched.get_jobs()
    sched.print_jobs('createRun')
    print sched.cron_schedule()
    
    
    pass