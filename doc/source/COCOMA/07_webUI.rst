The Web UI
==========
Here we explain how to use the web UI to create and manage emulations and view their results.

*Note:* For best results only use the Web UI on an up to date browser (may not function as intended on an out of date or older browser)

Opening the UI
--------------
Provided that the API is running, the web UI will be accessible at

:: 

        http://[COCOMA API IP]:[COCOMA API PORT]/index.html

The *COCOMA API IP* refers to the IP of the interface on which the API have been started. The page is compatible with Chrome, Firefox and Safari web browsers, while it is not with Internet Explorer. The page will automatically load in available emulators, distributions and resources. It will detect which distributions and resources are compatible with the given emulator so that the user needs not worry about creating XML the framework cannot process. Any emulations which already exist will also be displayed in the right hand bar.

.. figure:: webUIimages/Overall.png
        :scale: 70
        :align: center
        
        COCOMA webUI

Creating an emulation
---------------------
Each emulation requires a name and at least one distribution, although as many distributions as required can be added. Each distribution requires a name and all required fields to be filled, this data will vary as per the emulation, distribution or resource selected. Some help is provided to explain what each of the arguments are and (if relevant) what their units are. Distribution windows can be minimized for overall readability or removed entirely (not added to the emulation) by clicking the 'x' in the top right corner:


.. figure:: webUIimages/MultiDist.png
        :scale: 75
        :align: center
        
        Multi-distribution interface
        
Distribution Parameters
-----------------------
*Start time* determines how long (in seconds) after the overall emulation has begun, this particular distribution will begin. *Duration* is how long the distribution will last for. *Granularity* refers to the number of the steps taken from *startLoad* through to *stopLoad* over the course of the distributions run. For example a 60 second duration CPU stressing distribution with a granularity of 10 will move from *startLoad* to *stopLoad* in steps of 6 seconds. More information on the emulator or distribution currently selected and the specific parameters they require can be viewed by hovering over the blue question mark beside it:

.. figure:: webUIimages/ui_popup.png
        :scale: 90
        :align: center
        
        Help pop-ups

Logging and Message Queue
-------------------------
After the distributions have been created and specified, there is an option to enable or disable logging. Enabling logging give 2 more options, the *frequency* in seconds and the *level*, which dictates the amount of output the logs will contain. Below this is the option to enable or disable the message queue followed by various parameters allowing for it's setup

.. figure:: webUIimages/logsandMQ.png
        :scale: 80
        :align: center
        
        Logging and EMQ settings
        
Running the emulation
---------------------
Once all the parameters are set there are two options; run the emulation right away by clicking the *Run now* button, or schedule the emulation to begin running at a set time in the future by clicking the *Run at* button:

.. figure:: webUIimages/runAt.png
        :scale: 90
        :align: center  
        
        Set time for emulation	
	
Working with existing emulations
--------------------------------
Any existing emulations in your system will be listed on the right hand side of the screen. The UI also displays the total number of runs, how many of those failed and the current state of the emulation (*active* or *inactive*). Hovering over the emulation name will display the information on that emulation in a popup.

Clicking the small download icon to the right of each emulation will prompt the download of a zip file to your system. This zip file contains the .xml used to create the emulation as well as .csv files with the system logs and the logs for that specific emulation.

.. figure:: webUIimages/emuDisplay.png
        :scale: 90
        :align: center
        
        Emulations interface
