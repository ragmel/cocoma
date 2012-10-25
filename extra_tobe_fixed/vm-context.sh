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

	#if [ -f /etc/default/bonfire ]; then
	#	FELIX_HOME=/usr/local/EIS/felix-framework-4.0.2
	#	source /etc/default/bonfire

	#	zoo_ip=`echo $ZOOKEEPER`
	#	if [ "$zoo_ip" == "" ]; then
	#		zoo_ip=`ipshow`
	#	fi 
	#	sed -i "s:zookeeper.host.*:zookeeper.host=$zoo_ip:" $FELIX_HOME/load/org.apache.cxf.dosgi.discovery.zookeeper.cfg
		
	#fi

	#EIS_HOME=/usr/local/EIS

	#if [ -f $EIS_HOME/bundle/EISInstance* ]; then
	#	if [ -f $EIS_HOME/bundle/org.apache.felix.gogo.shell-0.10.0.jar ]; then
	#		mv $EIS_HOME/bundle/org.apache.felix.gogo.shell-0.10.0.jar $EIS_HOME/eis-bundles/
	#	fi
	#	if [ `ps -fe | grep "java -jar ./bin/felix.jar" | grep -v -c grep` == 0 ]; then
	#		timestamp=$(date +%Y%m%d_%H%M%S)
	#		cd $EIS_HOME/felix-framework-4.0.2/
	#		exec java -jar ./bin/felix.jar >> /var/log/felix_$timestamp.log 2>&1 &
	#	fi
	#fi

	#if [ -f $EIS_HOME/bundle/EISLoadBalancer* ]; then
        #        if [ `ps -fe | grep zookeeper | grep -v -c grep` == 0 ]; then
        #                timestamp=$(date +%Y%m%d_%H%M%S)
        #                cd /root/zookeeper-3.3.4
        #                mkdir -p /tmp/zookeeper
        #                ./bin/zkServer.sh start
        #        fi
        #fi
	
	. /etc/profile
	
	if [ `ps -fe | grep Scheduler.py | grep -v -c grep` == 0 ]; then	
		ccmsh --start scheduler >> /root/ccmsh.log 2>&1
	fi
	if [ `ps -fe | grep ccmshAPI.py | grep -v -c grep` == 0 ]; then
		ccmsh --start api >> /root/ccmsh.log 2>&1
	fi

	exit 0
}

case "$1" in
  start)
	do_start
	;;
  stop)
	#sed -i "s:ZOOKEEPER.*::g" /etc/default/bonfire
	. /etc/profile	

	ccmsh --stop scheduler >> /root/ccmsh.log 2>&1
	ccmsh --stop api >> /root/ccmsh.log 2>&1
	kill $(ps ax  | awk '/vm-context.sh/ {print $1}')
	exit 3
	;;
  *)
	echo "Usage: vm-context.sh [start|stop]" >&2
	exit 3
	;;
esac

:

