Single Distribution: REST Examples
==================================
blah   

CPU
---
blah



I/O
---
Words can have *emphasis in italics* or be **bold** and you can
define code samples with back quotes, like when you talk about a 
command: ``sudo`` gives you super user powers! 



Memory
------
blah

blah

Network
-------
blah





This is an example on how to link images:


.. code-block:: xml
   :linenos:
   
            <emulation>
              <emuname>CPU_emu</emuname>
              <emuType>Mix</emuType>
              <emuresourceType>CPU</emuresourceType>
              <emustartTime>now</emustartTime>
              <!--duration in seconds -->
              <emustopTime>15</emustopTime>
              
              <distributions> 
               <name>CPU_distro</name>
               <startTime>0</startTime>
               <!--duration in seconds -->
               <duration>10</duration>
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
            
             <log>
               <!-- Use value "1" to enable logging(by default logging is off)  -->
               <enable>1</enable>
               <!-- Use seconds for setting probe intervals(if logging is enabled default is 3sec)  -->
               <frequency>3</frequency>
             </log>              
            </emulation>
