Introduction
============
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

.. cmdoption:: -h, --help 
      
      Display help information of the available options

.. cmdoption:: -v, --version  

      Display installed version information of COCOMA

.. cmdoption:: -l, --list <emulation name>  

      Display list of all emulations that are scheduled or already finished. If emulation name is provided then will it will list information for that specific emulation
   
.. cmdoption:: -r, --results <emulation name>

      Display list of all emulation results that are scheduled or already finished. If emulation name is provided, then will it will list information for that specific emulation
    
.. cmdoption:: -j, --list-jobs 

      Querries scheduler for the list of jobs which is to be executed. Gives jobs names and planned execution time 
  
.. cmdoption:: -i, --dist <distribution name>

      Scans *"/usr/share/pyshared/cocoma/distributions"* folder and displays all available distribution modules.  If distribution name is provided, then it will list help information for that specific distribution 
  
.. cmdoption:: -e, --emu <emulator name>

      Scans *"/usr/share/pyshared/cocoma/emulators"* folder and displays all available emulator wrapper modules.  If emulator name is provided, then it will list help information for that specific emulator wrapper

.. cmdoption:: -x, --xml <file name>

      If you have a local XML file with emulation parameters, you can use it to create emulation.

.. cmdoption:: -n, --now (used with -x option only)

      If your local XML file emulation has set start date in past or in future, but you want to override it and start the test right now, without modifying the file, then you can add this option after the file name i.e. ``ccmsh -x <file name> -n``  

.. cmdoption:: -d, --delete <emulation name>

      Deletes specific emulation from the database, logs will remain and will be available until manualy deleted from *"/usr/share/pyshared/cocoma/logs"* folder   

.. cmdoption:: -p, --purge 

      Wipe all DB entries, removes all scheduled jobs, logs will remain and will be available until manualy deleted from *"/usr/share/pyshared/cocoma/logs"* folder 

.. cmdoption::     --start <api interface port>, <scheduler interface port>
      
      Launch Scheduler or API daemon by specifying network interface and port number i.e. ``ccmsh --start api eth0 2020`` or ``ccmsh --start scheduler eth0 3030`` . By default if interface is not specified then Scheduler daemon will run on *eth0* port *51889* and API daemon runs on *eth0* with port *5050*.
   
.. cmdoption::     --stop <api>, <scheduler> 
      
      Stop Scheduler or API daemon

.. cmdoption::     --show <api>, <scheduler>
      
      Show OS information on Scheduler or API daemon, displays PID numbers

REST API Description
--------------------
If the web API daemon has been started successfully, then COCOMA toolkit can be accessed remotely using its RESTfull API.

 * /
 * /emulations
 * /emulations/{name}
 * /distributions
 * /distributions/{name}
 * /emulators
 * /emulators/{name}
 * /results
 * /results/{name}
 * /tests
 * /tests/{name}
 * /logs
 * /logs/system
 * /logs/emulations
 * /logs/emulations/{name}
 
 


.. http:method:: GET /
   
   :title: root
   :response 200: 
   :response 404: 
 
   The **root** method returns *collection* of all the available resources. Example XML response:
   
   .. code-block:: xml

      <?xml version="1.0" ?>
      <root href="/">
        <version>0.1.1</version>
        <timestamp>1365518303.44</timestamp>
        <link href="/emulations" rel="emulations" type="application/vnd.bonfire+xml"/>
        <link href="/emulators" rel="emulators" type="application/vnd.bonfire+xml"/>
        <link href="/distributions" rel="distributions" type="application/vnd.bonfire+xml"/>
        <link href="/tests" rel="tests" type="application/vnd.bonfire+xml"/>
        <link href="/results" rel="results" type="application/vnd.bonfire+xml"/>
        <link href="/logs" rel="logs" type="application/vnd.bonfire+xml"/>
      </root> 

.. http:method:: GET /emulations
   
   :title: emulations
   :response 200: 
   :response 404: 

   The **emulations** method returns *collection* of all the available emulation resources. Example XML response:
   
   .. code-block:: xml

     <?xml version="1.0" ?>
      <collection href="/emulations" xmlns="http://127.0.0.1/cocoma">
        <items offset="0" total="3">
          <emulation href="/emulations/1-Emu-CPU-RAM-IO" id="1" name="1-Emu-CPU-RAM-IO" state="inactive"/>
          <emulation href="/emulations/2-CPU_EMU" id="2" name="2-CPU_EMU" state="inactive"/>
          <emulation href="/emulations/3-CPU_EMU" id="3" name="3-CPU_EMU" state="inactive"/>
        </items>
        <link href="/" rel="parent" type="application/vnd.bonfire+xml"/>
      </collection>


.. http:method:: GET /emulations/{name}

   :arg name: Name of emulation that you want to get more info
   :response 200: 
   :response 404: 
   
   Displays information about emulation by name. The returned *200-OK* XML is:
   
   .. code-block:: xml
   
      <?xml version="1.0" ?>
      <emulation href="/emulations/1-Emu-CPU-RAM-IO" xmlns="http://127.0.0.1/cocoma">
        <id>1</id>
        <emulationName>1-Emu-CPU-RAM-IO</emulationName>
        <emulationType>mix</emulationType>
        <resourceType>mix</resourceType>
        <emuStartTime>2013-04-09T13:00:01</emuStartTime>
        <emuStopTime>180</emuStopTime>
        <scheduledJobs>
          <jobsempty>No jobs are scheduled</jobsempty>
        </scheduledJobs>
        <distributions ID="1" name="Distro1">
          <startTime>5</startTime>
          <granularity>3</granularity>
          <duration>30</duration>
          <startload>10</startload>
          <stopload>90</stopload>
        </distributions>
        <distributions ID="2" name="Distro2">
          <startTime>5</startTime>
          <granularity>3</granularity>
          <duration>30</duration>
          <startload>10</startload>
          <stopload>90</stopload>
        </distributions>
        <link href="/" rel="parent" type="application/vnd.bonfire+xml"/>
        <link href="/emulations" rel="parent" type="application/vnd.bonfire+xml"/>
      </emulation>
     
   The returned *404 – Not Found* XML is:
   
   .. code-block:: xml
   
      <error>Emulation Name: 1-Emu-CPU-RAM-IO1 not found. Error:too many values to unpack</error>

      
.. http:method:: POST /emulations

   :param string XML: Emulation parameters defined via XML as shown in the examples section.
   :response 201: Emulation was created successfully
   :response 400:

   Create emulation.


.. http:method:: GET /emulators

   :response 200: 
   :response 404: 
   
   Displays emulators list.


.. http:method:: GET /emulators/{name}

   :arg name: Name of emulator that you want to get more info
   :response 200: 
   :response 404: 
   
   Displays information about emulator by name.


.. http:method:: GET /distributions

   :response 200: 
   :response 404: 
   
   Displays distributions list.


.. http:method:: GET /distributions/{name}

   :arg name: Name of distributions that you want to get more info
   :response 200: 
   :response 404: 
   
   Displays information about distributions by name.


.. http:method:: GET /tests

   :response 200: 
   :response 404: 
   
   Displays tests list.


.. http:method:: GET /tests/{name}

   :arg name: Name of tests that you want to get more info
   :response 200: 
   :response 404: 
   
   Displays information about tests by name.

.. http:method:: POST /tests/{name}

   :param string: name of the test that is located on COCOMA server
   :response 201: Emulation was created successfully
   :response 400:

   Create emulation from already available tests 
  
.. http:method:: GET /results

   :response 200: 
   :response 404: 
   
   Displays results list.


.. http:method:: GET /results/{name}

   :arg name: Name of tests that you want to get more info
   :response 200: 
   :response 404: 
   
   Displays information about results by name.


.. http:method:: GET /logs
   :response 200: 
   :response 404: 
   
   Displays logs list.
   
.. http:method:: GET /logs/system

   :response 200: 
   :response 404: 
   
   Return Zip file with system logs.

.. http:method:: GET /logs/emulations

   :response 200: 
   :response 404: 
   
   Displays emulations logs list.

.. http:method:: GET /logs/{name}

   :arg name: Name of emulation logs that you want to get more info
   :response 200: 
   :response 404: 
   
   Return Zip file with emulation logs.

