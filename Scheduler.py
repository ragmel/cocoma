'''
Created on 6 Sep 2012

@author: i046533
'''

#!/usr/bin/env python

import sys, os, time, atexit
from signal import SIGTERM 

from datetime import datetime
from apscheduler.scheduler import Scheduler 
import datetime as dt
import Distribution,Run

class Daemon:
    """
    A generic daemon class.
    
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
    
    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit first parent
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
    
        # decouple from parent environment
        os.chdir("/") 
        os.setsid() 
        os.umask(0) 
    
        # do second fork
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit from second parent
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1) 
    
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
    
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        
        # Start the daemon
        self.daemonize()
        self.run()
    
    def checkPid(self):
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
        else:
            # Start the daemon
            self.daemonize()
            self.run()
            print "Daemon Started"
            
        
        

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process    
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def hello(self):
        print "Hello this is Scheduler Daemon, whosagoodboy?"
                  
    
    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
    def  schedulerControl(self,startTime,stopTime, distributionGranularity,startLoad, stopLoad):   
            print "this is schedulerControl"
            
                
            
            
            startTime= self.timeConv(startTime)
            stopTime = self.timeConv(stopTime)
        
            #make sure it is integer
            distributionGranularity = int(distributionGranularity)
        
            #make copy for counting(qty can also be used)
            distributionGranularity_count = distributionGranularity
            # Start the scheduler
            sched = Scheduler()
            sched.start()
                
            qty=int(0)
        
        
        
            duration = (self.timestamp(stopTime) - self.timestamp(startTime))/distributionGranularity
        
            print "Duration is seconds:"
            print duration
  
            while(distributionGranularity_count>=0):
            
                print "Run No: "
                print qty
            
            
                #This needs to be changed
            
                runStartTime=self.timestamp(startTime)+duration*qty
                print "This run start time: "
                print runStartTime
                print "This is time passed to scheduler:"
                print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime))
            
                
                stressValue= Distribution.linearCalculate(startLoad, stopLoad, distributionGranularity,qty)
                print "This run stress Value: "
                print stressValue
            
                #job=sched.add_date_job(createRun, exec_date, [duration,stressValue])
                job=sched.add_date_job(Run.createRun, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(runStartTime)), [duration,stressValue])
            
                #increasing to next run            
                qty=int(qty)+1
                print "list of jobs:"
                sched.print_jobs()
            
                print "distributionGranularity_count:"
                distributionGranularity_count= int(distributionGranularity_count)-1
                print distributionGranularity_count

                #we can return single values, seconds and proper python date            
    def timeConv(self,dbtimestamp):
        print "this is timeConv!!!"
        Year = int(dbtimestamp[0:4])
        Month = int(dbtimestamp[4+1:7])
        Day = int(dbtimestamp[7+1:10])
        Hour =int(dbtimestamp[11:13])
        Min =int(dbtimestamp[14:16])
        Sec =int(dbtimestamp[17:19])

        #convert date from DB to python date
        pytime=dt.datetime(Year,Month,Day,Hour,Min,Sec)
        
        return pytime
        
    
                #convert date to seconds
    def timestamp(self,date):
        print"This is timestamp"
        print date
        return time.mktime(date.timetuple())

                   
