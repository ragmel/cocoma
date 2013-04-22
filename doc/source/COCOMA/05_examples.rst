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
        <distribution href="/distributions/linear" name="linear" />
        <!--cpu utilization distribution range-->
         <startLoad>10</startLoad>
         <stopLoad>95</stopLoad>
         <emulator href="/emulators/lookbusy" name="lookbusy" />
         
         <emulator-params>
           <!--more parameters will be added -->
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
        <distribution href="/distributions/linear_incr" name="linear_incr" />
         <startLoad>1</startLoad>
         <stopLoad>10</stopLoad>
         <emulator href="/emulators/stressapptest" name="stressapptest" />
         
         <emulator-params>
           <!--more parameters will be added -->
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
        <distribution href="/distributions/trapezoidal" name="trapezoidal" />
         <startLoad>1</startLoad>
         <stopLoad>10</stopLoad>
         <emulator href="/emulators/stressapptest" name="stressapptest" />
         
         <emulator-params>
           <!--more parameters will be added -->
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
        <distribution href="/distributions/linear_incr" name="linear_incr" />
      <!--cpu utilization distribution range-->
         <startLoad>100</startLoad>
         <!-- set target bandwidth to bits per sec -->
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
----------------------

A good feature of COCOMA is the ability to combine multiple distributions within the same emulation. This allows to specify contention properties for multiple resources or create different patterns for the same resource. Distributions can overlap, meaning two distributions can run at the same time frame. If distributions for the same resource overlap and they exceed the available resources, the runs might crash.


* CPU and Memory example

.. code-block:: xml
   :linenos:
   
          <emulation>
              <emuname>CPU_and_Mem</emuname>
              <emutype>Mix</emutype>
              <emuresourceType>CPU</emuresourceType>
              <emustartTime>now</emustartTime>
              <!--duration in seconds -->
              <emustopTime>80</emustopTime>
              
              <distributions> 
               <name>CPU_distro</name>
               <startTime>0</startTime>
               <!--duration in seconds -->
               <duration>60</duration>
               <granularity>1</granularity>
               <distribution href="/distributions/linear" name="linear" />
               <!--cpu utilization distribution range-->
               <startLoad>10</startLoad>
               <stopLoad>95</stopLoad>
               <emulator href="/emulators/lookbusy" name="lookbusy" />
               <emulator-params>
                    <!--more parameters will be added -->
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
              <emuresourceType>CPU</emuresourceType>
              <emustartTime>now</emustartTime>
              <!--duration in seconds -->
              <emustopTime>80</emustopTime>
              
              <distributions> 
               <name>CPU_distro</name>
               <startTime>0</startTime>
               <!--duration in seconds -->
               <duration>60</duration>
               <granularity>1</granularity>
               <distribution href="/distributions/linear" name="linear" />
               <!--cpu utilization distribution range-->
               <startLoad>10</startLoad>
               <stopLoad>95</stopLoad>
               <emulator href="/emulators/lookbusy" name="lookbusy" />
               <emulator-params>
                    <!--more parameters will be added -->
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
                 <distribution href="/distributions/linear_incr" name="linear_incr" />
                  <startLoad>1</startLoad>
                  <stopLoad>10</stopLoad>
                  <emulator href="/emulators/lookbusy" name="lookbusy" />
                  
                  <emulator-params>
                    <!--more parameters will be added -->
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


