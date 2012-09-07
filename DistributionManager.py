#!/usr/bin/env python
'''
Created on 6 Sep 2012

@author: i046533
'''


import sys, time
from Scheduler import Daemon


class MyDaemon(Daemon):
    def run(self):
        while True:
            time.sleep(1)

daemon = MyDaemon('/tmp/ccmsh-scheduler-daemon.pid')


def distributionManager(emulationName,distributionType,resourceType,emulationType,startTime,stopTime, distributionGranularity,startLoad, stopLoad):
    print "Hello this is distributionManager"
    daemon.hello()
    daemon.checkPid()
    daemon.schedulerControl(startTime, stopTime, distributionGranularity, startLoad, stopLoad) #schedulerControl(startTime,stopTime, distributionGranularity, startLoad, stopLoad)


if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'hello' == sys.argv[1]:
            daemon.hello()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart|hello" % sys.argv[0]
        sys.exit(2)