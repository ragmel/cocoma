XML Examples
============
This section provides XML payload examples for creating different emulations over various resources.

CPU
---
Emulation XML for CPU contention:

.. code-block:: xml
   :linenos:
   
   <emulation>
     <emuname>CPU_EMU</emuname>
     <emuType>Mix</emuType>
     <emuresourceType>CPU</emuresourceType>
     <!--date format: 2014-10-10T10:10:10 -->
     <emustartTime>now</emustartTime>
     <!--duration in seconds -->
     <emustopTime>120</emustopTime>
     
     <distributions>  
      <name>CPU_Distro</name>
        <startTime>0</startTime>
        <!--duration in seconds -->
        <duration>120</duration>
        <granularity>24</granularity>
        <minJobTime>2</minJobTime>
        <distribution href="/distributions/linear" name="linear" />
        <!--cpu utilization distribution range-->
         <startLoad>10</startLoad>
         <stopLoad>95</stopLoad>
         <emulator href="/emulators/lookbusy" name="lookbusy" />
         
         <emulator-params>
           <resourceType>CPU</resourceType>
          <!--Number of CPUs to keep busy (default: autodetected)-->
          <ncpus>1</ncpus>
         </emulator-params>     
     </distributions>
   
     <log>
      <!-- Use value "1" to enable logging(by default logging is off)  -->
      <enable>1</enable>
      <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
      <frequency>1</frequency>
      <logLevel>debug</logLevel>
     </log>
     
   </emulation>


I/O
---

Emulation XML for I/O contention:

.. code-block:: xml
   :linenos:

   <emulation>
     <emuname>IO_EMU</emuname>
     <emuType>Mix</emuType>
     <emuresourceType>IO</emuresourceType>
     <!--date format: 2014-10-10T10:10:10 -->
     <emustartTime>now</emustartTime>
     <!--duration in seconds -->
     <emustopTime>60</emustopTime>
     
     <distributions>
      
      <name>IO_Distro</name>
        <startTime>0</startTime>
        <!--duration in seconds -->
        <duration>60</duration>
        <granularity>5</granularity>
        <minJobTime>2</minJobTime>
        <distribution href="/distributions/linear_incr" name="linear_incr" />
        <startLoad>1</startLoad>
        <stopLoad>10</stopLoad>
        <emulator href="/emulators/stressapptest" name="stressapptest" />
         
         <emulator-params>
           <resourceType>IO</resourceType>
           <!--Size of mem in MB used-->
           <memsize>1000</memsize>
           <!--Number of threads-->
           <memThreads>10</memThreads>
         </emulator-params>
         
     </distributions>
   
     <log>
      <!-- Use value "1" to enable logging(by default logging is off)  -->
      <enable>1</enable>
      <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
      <frequency>3</frequency>
      <logLevel>debug</logLevel>
     </log>
     
   </emulation>

In this example we use a different distribution called *trapezoidal*:

.. code-block:: xml
   :linenos:

   <emulation>
     <emuname>IO_EMU</emuname>
     <emuType>Mix</emuType>
     <emuresourceType>IO</emuresourceType>
     <!--date format: 2014-10-10T10:10:10 -->
     <emustartTime>now</emustartTime>
     <!--duration in seconds -->
     <emustopTime>60</emustopTime>
     
     <distributions>
      
      <name>IO_Distro</name>
        <startTime>0</startTime>
        <!--duration in seconds -->
        <duration>60</duration>
        <granularity>5</granularity>
        <minJobTime>2</minJobTime>
        <distribution href="/distributions/trapezoidal" name="trapezoidal" />
        <startLoad>1</startLoad>
        <stopLoad>10</stopLoad>
        <emulator href="/emulators/stressapptest" name="stressapptest" />
         
         <emulator-params>
           <resourceType>IO</resourceType>
           <!--Size of mem in MB used-->
           <memsize>1000</memsize>
           <!--Number of threads-->
           <memThreads>10</memThreads>
         </emulator-params>
         
     </distributions>
   
     <log>
      <!-- Use value "1" to enable logging(by default logging is off)  -->
      <enable>1</enable>
      <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
      <frequency>3</frequency>
      <logLevel>debug</logLevel>
     </log>
     
   </emulation>


Memory
------
Emulation XML for memory contention:

.. code-block:: xml
   :linenos:

   <emulation>
     <emuname>MEM_EMU</emuname>
     <emuType>Mix</emuType>
     <emuresourceType>MEM</emuresourceType>
     <!--date format: 2014-10-10T10:10:10 -->
     <emustartTime>now</emustartTime>
     <!--duration in seconds -->
     <emustopTime>60</emustopTime>
     
     <distributions >
        <name>MEM_Distro</name>
        <startTime>0</startTime>
        <!--duration in seconds -->
        <duration>60</duration>
        <granularity>5</granularity>
        <minJobTime>2</minJobTime>
        <distribution href="/distributions/linear_incr" name="linear_incr" />
        <!--Memory usage (Megabytes) -->
        <startLoad>100</startLoad>
        <stopLoad>1000</stopLoad>
        <malloclimit>4095</malloclimit>
        <emulator href="/emulators/stressapptest" name="stressapptest" />
        <emulator-params>
            <resourceType>MEM</resourceType>
            <memThreads>0</memThreads>
        </emulator-params>
     </distributions>
   
     <log>
      <!-- Use value "1" to enable logging(by default logging is off)  -->
      <enable>1</enable>
      <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
      <frequency>3</frequency>
      <logLevel>debug</logLevel>
     </log>
   
   </emulation>

Example for memory emulation using *trapezoidal* distribution:

.. code-block:: xml
   :linenos:

   <emulation>
     <emuname>MEM_EMU</emuname>
     <emuType>Mix</emuType>
     <emuresourceType>MEM</emuresourceType>
     <!--date format: 2014-10-10T10:10:10 -->
     <emustartTime>now</emustartTime>
     <!--duration in seconds -->
     <emustopTime>60</emustopTime>
     
     <distributions >
        <name>MEM_Distro</name>
        <startTime>0</startTime>
        <!--duration in seconds -->
        <duration>60</duration>
        <granularity>5</granularity>
        <minJobTime>2</minJobTime>
        <distribution href="/distributions/trapezoidal" name="trapezoidal" />
        <!--Megabytes for memory -->
        <startLoad>100</startLoad>
        <stopLoad>1000</stopLoad>
        <malloclimit>4095</malloclimit>
        <emulator href="/emulators/stressapptest" name="stressapptest" />
        <emulator-params>
            <resourceType>MEM</resourceType>  
            <memThreads>0</memThreads>
        </emulator-params>
     </distributions>
   
     <log>
      <!-- Use value "1" to enable logging(by default logging is off)  -->
      <enable>0</enable>
      <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
      <frequency>3</frequency>
      <logLevel>debug</logLevel>
     </log>
   
   </emulation>




Network
-------

The newtork emulation needs two COCOMA VM's, one that acts as a client and the other as a server. Normally those two VMs are placed in different nodes. The SuT should be composed of at least two VMs placed on the same two nodes of COCOMA. The emulation XML for network contention looks like:

.. code-block:: xml
   :linenos:

   <emulation>
     <emuname>NET_emu</emuname>
     <emuType>Mix</emuType>
     <emuresourceType>NET</emuresourceType>
     <!--2014-02-02T10:10:10-->
     <emustartTime>now</emustartTime>
     <!--duration in seconds -->
     <emustopTime>155</emustopTime>
     
     <distributions> 
        <name>NET_distro</name>
        <startTime>0</startTime>
        <!--duration in seconds -->
        <duration>150</duration>
        <granularity>10</granularity>
        <minJobTime>2</minJobTime>
        <distribution href="/distributions/linear_incr" name="linear_incr" />
        <!--set target bandwidth to bits per sec-->
        <startLoad>100</startLoad>
        <stopLoad>1000</stopLoad>
        <emulator href="/emulators/iperf" name="iperf" />
        <emulator-params>
           <resourceType>NET</resourceType>
           <serverip>172.18.254.234</serverip>
           <!--Leave "0" for default 5001 port -->
           <serverport>5001</serverport>
           <clientip>172.18.254.236</clientip>
           <clientport>5001</clientport>
           <packettype>UDP</packettype>
           </emulator-params>
     </distributions>
   
     <log>
      <!-- Use value "1" to enable logging(by default logging is off)  -->
      <enable>0</enable>
      <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
      <frequency>3</frequency>
     </log>
     
   </emulation>


Multiple distributions emulation
--------------------------------

An important feature of COCOMA is the ability to combine multiple distributions within the same emulation. This allows to specify contention properties for multiple resources or create different patterns for the same resource. Distributions can overlap, meaning two distributions can run at the same time frame. If distributions for the same resource overlap and they exceed the available resources, the runs might crash.


* CPU and Memory example

.. code-block:: xml
   :linenos:
   
    <emulation>
        <emuname>CPU_and_Mem</emuname>
        <emutype>Mix</emutype>
        <emuresourceType>MIX</emuresourceType>
        <emustartTime>now</emustartTime>
        <!--duration in seconds -->
        <emustopTime>80</emustopTime>
        
        <distributions> 
           <name>CPU_distro</name>
           <startTime>0</startTime>
           <!--duration in seconds -->
           <duration>60</duration>
           <granularity>1</granularity>
           <minJobTime>2</minJobTime>
           <distribution href="/distributions/linear" name="linear" />
           <!--cpu utilization distribution range-->
           <startLoad>10</startLoad>
           <stopLoad>95</stopLoad>
           <emulator href="/emulators/lookbusy" name="lookbusy" />
           <emulator-params>
                <resourceType>CPU</resourceType>
                <!--Number of CPUs to keep busy (default: autodetected)-->
                <ncpus>0</ncpus>
           </emulator-params>
        </distributions>
             
        <distributions>
            <name>MEM_Distro</name>
            <startTime>20</startTime>
            <!--duration in seconds -->
            <duration>60</duration>
            <granularity>5</granularity>
            <minJobTime>2</minJobTime>
            <distribution href="/distributions/linear_incr" name="linear_incr" />
            <!--Megabytes for memory -->
            <startLoad>100</startLoad>
            <stopLoad>1000</stopLoad>
            <malloclimit>4095</malloclimit>
            <emulator href="/emulators/stressapptest" name="stressapptest" />
            <emulator-params>
              <resourceType>MEM</resourceType>
              <memThreads>0</memThreads>
            </emulator-params>
        </distributions>

        <log>
           <!-- Use value "1" to enable logging(by default logging is off)  -->
           <enable>1</enable>
           <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
           <frequency>3</frequency>
        </log>
    </emulation>


* CPU, MEM and IO example

.. code-block:: xml
   :linenos:
   
    <emulation>
        <emuname>CPU_and_Mem</emuname>
        <emutype>Mix</emutype>
        <emuresourceType>MIX</emuresourceType>
        <emustartTime>now</emustartTime>
        <!--duration in seconds -->
        <emustopTime>80</emustopTime>
        
        <distributions> 
            <name>CPU_distro</name>
            <startTime>0</startTime>
            <!--duration in seconds -->
            <duration>60</duration>
            <granularity>1</granularity>
            <minJobTime>2</minJobTime>
            <distribution href="/distributions/linear" name="linear" />
            <!--cpu utilization distribution range-->
            <startLoad>10</startLoad>
            <stopLoad>95</stopLoad>
            <emulator href="/emulators/lookbusy" name="lookbusy" />
            <emulator-params>
                 <resourceType>CPU</resourceType>
                 <!--Number of CPUs to keep busy (default: autodetected)-->
                 <ncpus>0</ncpus>
            </emulator-params>
         </distributions>
             
         <distributions >
            <name>MEM_Distro</name>
            <startTime>20</startTime>
            <!--duration in seconds -->
            <duration>60</duration>
            <granularity>5</granularity>
            <minJobTime>2</minJobTime>
            <distribution href="/distributions/linear_incr" name="linear_incr" />
            <!--Megabytes for memory -->
            <startLoad>100</startLoad>
            <stopLoad>1000</stopLoad>
            <malloclimit>4095</malloclimit>
            <emulator href="/emulators/stressapptest" name="stressapptest" />
            <emulator-params>
               <resourceType>MEM</resourceType>
               <memThreads>0</memThreads>
            </emulator-params>
         </distributions>
        
        <distributions>
            <name>IO_Distro</name>
            <startTime>0</startTime>
            <!--duration in seconds -->
            <duration>60</duration>
            <granularity>5</granularity>
            <minJobTime>2</minJobTime>
            <distribution href="/distributions/linear_incr" name="linear_incr" />
            <startLoad>1</startLoad>
            <stopLoad>10</stopLoad>
            <emulator href="/emulators/lookbusy" name="lookbusy" />
            <emulator-params>
                <resourceType>IO</resourceType>
                <!--Size of blocks to use for I/O, in MB-->
                <ioBlockSize>10</ioBlockSize>
                <!--Time to sleep between iterations, in msec-->
               <ioSleep>100</ioSleep>
           </emulator-params>   
       </distributions>

       <log>
          <!-- Use value "1" to enable logging(by default logging is off)  -->
          <enable>1</enable>
          <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
          <frequency>3</frequency>
       </log>
    </emulation>

Event Based Scheduling
----------------------
In addition to the regular, time based, scheduling there is Event based scheduling. In Event based scheduling the order of jobs ioin the xml is used to determine which order jobs will run in. Below is a short explanation of how jobs are scheduled when using events:

* Run time based jobs as normal (if there are any) until an Event is reached
* Stop scheduling any further jobs unitl the Event finishes
* Resume Scheduling jobs, using their start time as a delay after the event finishes. (A job with a start time of 5 would start 5 secounds after the event finishes)
* Repeat until all distribuitons are scheduled or emuStopTime expires (at whcih point all running jobs will be killed, and scheduling will stop)

Event Based Emulation example:

.. code-block:: xml
   :linenos:

    <emulation>
      <emuname>MAL_EMU</emuname>
      <emuType>MIX</emuType>
      <emuresourceType>MIX</emuresourceType>
      <!--date format: 2014-10-10T10:10:10 -->
      <emustartTime>now</emustartTime>
      <!--duration in seconds -->
      <emustopTime>35</emustopTime>
    
      <distributions>
         <name>MAL_Distro1</name>
         <startTime>0</startTime>
         <minJobTime>2</minJobTime>
         <distribution href="/distributions/event" name="event" />
          <emulator href="/emulators/backfuzz" name="backfuzz" />
          <emulator-params>
            <resourceType>NET</resourceType>
            <min>100</min>
            <fuzzRange>900</fuzzRange>
            <serverip>10.55.168.142</serverip>
            <serverport>5050</serverport>
            <packettype>TCP</packettype>
            <timedelay>1</timedelay>
            <salt>100</salt>
         </emulator-params>
      </distributions>
    
      <distributions>
       <name>CPU_Distro</name>
         <startTime>5</startTime>
         <!--duration in seconds -->
         <duration>10</duration>
         <granularity>2</granularity>
         <minJobTime>2</minJobTime>
         <distribution href="/distributions/linear" name="linear" />
         <startLoad>10</startLoad>
         <stopLoad>50</stopLoad>
         <emulator href="/emulators/lookbusy" name="lookbusy" />
         <emulator-params>
           <resourceType>CPU</resourceType>
           <ncpus>0</ncpus>
         </emulator-params>
       </distributions>
    
      <log>
            <!-- Use value "1" to enable logging(by default logging is off)  -->
            <enable>0</enable>
            <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
            <frequency>3</frequency>
            <logLevel>debug</logLevel>
      </log>
    
    </emulation>


Known Issues
------------
The interaction of the various emulators used in COCOMA can cause unexpected issues. Some of these issues are listed below (This is *not* an exhaustive list, and will be updated as new issues are discovered)

* Stressapptest uses ~100% CPU, regardless of what resource it is being ran on.

* If a Linear increase distribution is run on memory using stressapptest at the same time as Iperf is being used to load the Network, then the Network resource may not reach its target load. This problem is usually encountered when the memory usage reaches over ~80% (as shown in the graph below)

.. figure:: MEM_NET-Problem.png
    :align: center

* When running an Emulation containing an Event based distribution, then the list of jobs (seen by using the command 'ccmsh -j') may not be correct