Known Issues
============
The interaction of the various emulators used in COCOMA can cause unexpected issues. Some of these issues are listed below (This is *not* an exhaustive list, and will be updated as new issues are discovered)

* Stressapptest uses ~100% CPU, regardless of what resource it is being ran on.

* If a Linear increase distribution is run on memory using stressapptest at the same time as Iperf is being used to load the Network, then the Network resource may not reach its target load. This problem is usually encountered when the memory usage reaches over ~80% (as shown in the graph below)

.. figure:: MEM_NET-Problem.png
    :align: center

* When running an Emulation containing an Event based distribution, then the list of jobs (seen by using the command 'ccmsh -j') may not be correct
