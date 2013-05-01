Creating Emulation via CLI
==========================
Once *Scheduler* was started and running we can now create stress emulations for the resources. We are using local XML ``emulation.xml`` file: 

.. code-block:: xml
   :linenos:
   
      <emulation>
        <emuname>CPU_Emulation</emuname>
        <emuType>Mix</emuType>
        <emuresourceType>Mix</emuresourceType>
        <emustartTime>now</emustartTime>
        <!--duration in seconds -->
        <emustopTime>180</emustopTime>
        
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
   


start with simple CLI command:

.. code-block:: bash
   
   $ ccmsh -x emulation.xml


If everything went right, you will see on the screen list of scheduled jobs:

.. code-block:: bash
   :emphasize-lines: 3,4,5,6,7,8,10
   :linenos:
   
   
   $ ccmsh -x emulation.xml 
   INFO:XML Parser:Finished running
   INFO:Distriburion Manager:Scheduler reply: 6-CPU_Emulation-7-0-Distro1-lookbusy-cpu: 90 Duration: 10.0sec.Start Time: 2013-04-10 09:43:01 End Time: 09:43:11
   INFO:Distriburion Manager:Scheduler reply: 6-CPU_Emulation-7-1-Distro1-lookbusy-cpu: 50 Duration: 10.0sec.Start Time: 2013-04-10 09:43:13 End Time: 09:43:23
   INFO:Distriburion Manager:Scheduler reply: 6-CPU_Emulation-7-2-Distro1-lookbusy-cpu: 10 Duration: 10.0sec.Start Time: 2013-04-10 09:43:25 End Time: 09:43:35
   INFO:Distriburion Manager:Scheduler reply: 6-CPU_Emulation-8-0-Distro2-lookbusy-cpu: 10 Duration: 10.0sec.Start Time: 2013-04-10 09:43:01 End Time: 09:43:11
   INFO:Distriburion Manager:Scheduler reply: 6-CPU_Emulation-8-1-Distro2-lookbusy-cpu: 50 Duration: 10.0sec.Start Time: 2013-04-10 09:43:13 End Time: 09:43:23
   INFO:Distriburion Manager:Scheduler reply: 6-CPU_Emulation-8-2-Distro2-lookbusy-cpu: 90 Duration: 10.0sec.Start Time: 2013-04-10 09:43:25 End Time: 09:43:35
   INFO:Emulation Manager:##Emulation 6-Emu-CPU-RAM-IO created
   INFO:Emulation Manager:Started logger:6-CPU_Emulation-logger interval-3sec.StartTime:2013-04-10 09:42:56
   6-Emu-CPU-RAM-IO


Each line from *3-8* shows information of a single scheduled emulation job. If we break it down, the line *3* from above as an example we have:

* **INFO:Distriburion Manager:Scheduler reply:** -just a generic logger part
* **6-CPU_Emulation** - emulation name, which is a combined string of emulation ID from the DB and ``emuname`` value in the XML file
* **7** - database ID number for distribution
* **0** - run number of this distribution
* **Distro1** - name of the distribution taken from XML file
* **lookbusy** - distribution module used to calculate each run parameters
* **cpu** - the type of the resource used by this run
* **90** - stress value applied to this run
* **Duration 10.0sec.** - how long will job run
* **Start Time: 2013-04-10 09:43:01 End Time: 09:43:11** - time gap when run will be executed 
   
We can write run name notation in this way:

``(logger reply) - (emulationID-name) - (distribution ID) - (run number} - (distribution name) - (distribution module) - (resource) - (stress value) - (run duration) - (execution time)``


Line *10* shows another job which was created for the logger.This job will appear only if *log* section is stated in XML and is optional. Logger job runs for the duration of the whole emulation 
and collects system resource usage information.
Logger job name notation can be described in this way:

``(logger reply) - (emulationID-name) - (logger mark) - {poll interval} - (start time)``
