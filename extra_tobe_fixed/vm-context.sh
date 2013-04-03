#!/bin/bash

### BEGIN INIT INFO
# Provides:          vm-context
# Required-Start:    $all
# Required-Stop:
# Should-Start:      $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Contextualize the VM based on /etc/default/bonfire
# Description:       Read the zookeeper IP from /etc/default/bonfire, and
#                    update the felix zookeeper IP with this value. It waits
#                    until the /etc/default/bonfire is there and the zookeeper
#                    IP is there too.
### END INIT INFO


do_start () {
	
	while true
	do
		[ -f /etc/default/bonfire ] && break
		sleep 1
	done

	until [ `grep -c AGGREGATOR_IP /etc/default/bonfire` == 1 ]
	do
		sleep 1
	done

	. /etc/profile
	
	if [ `ps -fe | grep Scheduler.py | grep -v -c grep` == 0 ]; then	
		ccmsh --start scheduler >> /var/log/ccmsh.log 2>&1
	fi
	if [ `ps -fe | grep ccmshAPI.py | grep -v -c grep` == 0 ]; then
		ccmsh --start api >> /var/log/ccmsh.log 2>&1
	fi

	exit 0
}

case "$1" in
  start)
	do_start
	;;
  stop)
	. /etc/profile	

	ccmsh --stop scheduler >> /var/log/ccmsh.log 2>&1
	ccmsh --stop api >> /var/log/ccmsh.log 2>&1
	kill $(ps ax  | awk '/vm-context.sh/ {print $1}')
	exit 3
	;;
  *)
	echo "Usage: vm-context.sh [start|stop]" >&2
	exit 3
	;;
esac

:

