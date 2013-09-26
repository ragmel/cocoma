Additional Features
===================
In this section the additional features of COCOMA will be discussed

Testing
-------

COCOMA has two main sets of tests supplied with it; **API Tests** and **Command Line Interface (CLI) Tests**. Both of which are implemented using python's unit testing framework (pyUnit)

The test files (**TestAPI** and **TestCLI**) are located in *"/usr/share/pyshared/cocoma/unitTest"*

To run a set of tests on the API or CLI, navigate to the *unitTest* folder and use on of the commands:

.. code-block:: bash

    $ python -m unittest -v TestAPI
    $ python -m unittest -v TestCLI

The *-v* argument gives more verbose output, and may be omitted if required

Individual test results are output to the terminal in the format ``test_Emulators (TestAPI.TestAPI) ... ok`` if the test was successful
An unsuccessful test will produce the same outoput, with *ERROR* or *FAIL* instead of *ok*

Once all the tests in the  file have run, a summary of the results will be printed. This will indicate which (if any) tests were unsuccessful, and attempt to give a reason why the test failed

CLI Testing
...........
Individual tests can be run on the CLI using the syntax

.. code-block:: bash

    $ python -m unittest TestCLI.TestCLI.test_Name
    
Where ``test_Name`` is replaced by one of the following:

::

	test_EMU_CPU
	test_EMU_IO
	test_EMU_IOTrap
	test_EMU_MEM
	test_EMU_MEMTrap
	test_EMU_MULTI1
	test_EMU_MULTI2
	test_EMU_NETWORK
	test_EMU_NowOperator

	test_Scheduler_Start
	test_Scheduler_Show
	test_Scheduler_Stop

	test_API_Start
	test_API_Show
	test_API_Stop

	test_Help
	test_Version
	test_List
	test_Result
	test_Distributions
	test_Emulators
	test_Purge
	test_Jobs

This will produce output similar to running the entire set of tests

API Testing
...........

Individual tests can be run on the API using the syntax

.. code-block:: bash

    $ python -m unittest TestAPI.TestAPI.test_Name

Where ``test_Name`` is replaced by one of the following:

::

	test_List_Emulation
        test_List_Emulator
        test_List_Distributions
        test_List_Results
        test_List_Logs
        test_List_SysLogs
        test_List_EmuLogs
        test_List_Tests

	test_EMU_Logs
	test_EMUcr_IO
        test_EMUcr_IOtrap
        test_EMUcr_MEM
        test_EMUcr_MEMtrap
        test_EMUcr_NETWORK
        test_EMUcr_MULTI1
        test_EMUcr_MULTI2

This will produce output similar to running the entire set of tests

Resource Overloading
--------------------

In order to prevent resources from becoming Overloaded (using more than 100% of a resource at a point in time,) the system calculates the resource usage before any Emulation is run.

If an Emulation would cause any of the resources to become overloaded, then that emulation will not run and an exception will be raised with the format:

::

    Unable to create distribution:
    CPU resource will become Overloaded: Stopping execution
    
Abstract Classes
----------------

When adding a new Emulator or Distribution class they should extend their respective abstract class. This requires the new class to contain the following code:

* For Emulators

::
    sys.path.insert(0, getHomepath() + '/emulators/')
    from abstract_emu import *
    
    class run_yourEmulatorName(abstract_emu):
        pass

* For Distributions

::
    sys.path.insert(0, getHomepath() + '/distributions/')
    from abstract_dist import *
    
    class dist_yourDistributionName(abstract_dist):
        pass

This feature was added to minimize problems caused by adding new emulators or distributions