Adding a new emulator
=====================
In order to add a new emulator, a new wrapper has to be implemented. This needs to inherit from the relative abstract class, which can be found in the same *emulators* directory. The class needs 3 different methods:

        * **__init__**: Used to accept the emulators parameters and pass them to whatever methods are used to load the desired resource
        * **emulatorHelp**: Used for displaying help about an emulator (eg. what parameters it needs)
        * **emulatorArgNames**: Used for returning the names of the arguments that a given emulator takes. If any of the arguments aren't numerical then they must have their name added to the `textBasedArgs` list in the `boundsCompare` method contained in `bin/Library.py`

As well as the following code:

::

    sys.path.insert(0, getHomepath() + '/emulators/')
    from abstract_emu import *
    
    class run_yourEmulatorName(abstract_emu):
   pass

Specific methods to execute the wanted emulator instance with the relative needed parameters will have to be added. Checking the existing emulator wrappers should give a clear view on how the wrapping process can be carried out.

`Note`: The zombieBuster method (from the abstract class) **must** be called at some point in the emulator wrapper (passing in the PID and name of the emulator being ran). One of the purposes of this method is to terminate any remaining processes after the emulation time expires; If it is not used then jobs may be created after the emulation finishes, or jobs created during the emulation may not terminate properly.

Adding a new distribution
=========================
In order to add a new distribution, it needs to inherit from the relative abstract class, which can be found in the same *distributions* directory. The class needs 3 different methods:

        * **distHelp**: Used for displaying help about a distribution (eg. what Resources types it can use)
        * **functionCount**: Used for getting values for: stressValues, runStartTimeList, runDurations. The actual algorithm (which calculates those values) goes in this function
        * **argNames**: Used for returning the names of the arguments that a given resource takes. If any of the arguments aren't numerical then they must have their name added to the `textBasedArgs` list in the `boundsCompare` method contained in `bin/Library.py`

As well as the following code:

::

    sys.path.insert(0, getHomepath() + '/distributions/')
    from abstract_dist import *

   class dist_yourDistributionName(abstract_dist):
   pass