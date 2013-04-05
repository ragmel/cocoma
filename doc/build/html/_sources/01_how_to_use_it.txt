How to use it
=============
In order to use COCOMA framework experimenter creates an emulation using XML language(see below Examples section). Emulation should contain all the neccessary information 
about duration, magnitude and required resource usage. Once XML document is received by COCOMA, the framework will automatically schedule and execute 
required workload on the chosen resource(-s) such as CPU, IO, Memory and/or Network.   

Installation
------------
The framework is designed to run on GNU/Linux and released in *.deb* package only.
Once you have downloaded latest COCOMA version install it by running:

.. code-block:: xml
   
   $ dpkg -i cocoma_X.X-X_all.deb

The application will be installed to folder *"/usr/share/pyshared/cocoma"*. All the additional required programs and libraries will be downloaded and installed on the fly if missing.
To check check if it was installed correctly run:

.. code-block:: xml
   
   $ ccmsh -v  


Starting Components
-------------------
To avail full functionality of COCOMA two daemons need to be started: 

 * Scheduler daemon (mandatory)
 * API Daemon (optional if REST API functionality is required)

**Scheduler daemon** - runs in the background and executes workload with differential parameters at the time defined in the emulation properties.
to start scheduler use command:

.. code-block:: xml

   $ ccmsh --start scheduler
   
Default network interface is *eth0*, port *51889* you can change that by adding required interface name and port number at the end:

.. code-block:: xml

   $ ccmsh --start scheduler wlan0 5180

If more detailed output information is needed *Scheduler* also can be started in *DEBUG* mode:

.. code-block:: xml

   $ ccmsh --start scheduler wlan0 5180 debug 

*Note: Scheduler needs to be running otherwise nothing will work. Always start it first!!* 

**API daemon** - represents RESTfull web API which exposes COCOMA resources for use over the network. It follows the same startup pattern as the Scheduler:

.. code-block:: xml

   $ ccmsh --start api

By default web API will try to start using *eth0* network interface on port *5050*, but it can be changed by supplying own parameters:

.. code-block:: xml

   $ ccmsh --start api wlan0 3030

The log level will be always same as the *Scheduler*.

Command Line Arguments
----------------------
   
The COCOMA :program:`ccmsh` command line interface has several options:

.. program:: ccmsh

.. cmdoption:: -h, --help show this help message and exit

.. cmdoption:: -v, --version show version information 

.. cmdoption:: -l, --list list all emulations or specific emulation by name  
   
.. cmdoption:: -r, --results list all emulations results or specific emulation results by name
    
.. cmdoption:: -j, --list-jobs list of all scheduled jobs
  
.. cmdoption:: -i, --dist lists all available distributions and gives distributiondetails by name
  
.. cmdoption:: -e, --emu lists all available emulators and gives emulator details by name

.. cmdoption:: -x, --xml provide path to XML file with emulation details

.. cmdoption:: -n, --now add to the "-x" argument to override emulation start date and execute test immediately

.. cmdoption:: -d, --delete delete emulation by name

.. cmdoption:: -p, --purge wipes all DB entries, removes all scheduled jobs and log files

.. cmdoption::     --start launch Scheduler or API daemon
   
.. cmdoption::     --stop stop Scheduler or API daemon

.. cmdoption::     --show show OS information on Scheduler or API daemon

REST API Description
--------------------


.. code-block:: xml
   :linenos:
   
   <emulation>
     <name>Emu-CPU-RAM-IO</name>
     <emulationType>Mix</emulationType>
     <resourceType>Mix</resourceType>
     <startTime>now</startTime>
     <!--duration in seconds -->
     <stopTime>180</stopTime>
     
     <distributions>
        <name>Distro1</name>
        <startTime>5</startTime>
        <!--duration in seconds -->
        <duration>30</duration>
        <granularity>3</granularity>
        <distribution href="/distributions/linear" name="linear" />
      <!--cpu utilization distribution range-->
         <startLoad>90</startLoad>
         <stopLoad>10</stopLoad>
         <emulator href="/emulators/stressapptest" name="lookbusy" />
         <emulator-params>
           <!--more parameters will be added -->
           <resourceType>CPU</resourceType>
      <!--Number of CPUs to keep busy (default: autodetected)-->
      <ncpus>0</ncpus>
   
         </emulator-params>
     </distributions>
     
      <distributions>
        <name>Distro2</name>
        <startTime>5</startTime>
        <!--duration in seconds -->
        <duration>30</duration>
        <granularity>3</granularity>
        <distribution href="/distributions/linear" name="linear" />
      <!--cpu utilization distribution range-->
         <startLoad>10</startLoad>
         <stopLoad>90</stopLoad>
         <emulator href="/emulators/stressapptest" name="lookbusy" />
         <emulator-params>
           <!--more parameters will be added -->
           <resourceType>CPU</resourceType>
      <!--Number of CPUs to keep busy (default: autodetected)-->
      <ncpus>0</ncpus>
   
         </emulator-params>
     </distributions>
   
     <log>
      <!-- Use value "1" to enable logging(by default logging is off)  -->
      <enable>1</enable>
      <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
      <frequency>3</frequency>
     </log>
   
   </emulation>
