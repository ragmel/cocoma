Implementation details
======================
The Controlled Contentious and Malicious patterns (COCOMA) framework aims to provide experimenters the ability to create specific contentious and malicious payloads and workloads in a controlled fashion. The experimenter is able to use pre-defined common distributions or specify new payloads and workloads. In the table below we present the terminology introduced by COCOMA.

.. include:: glossary.rst

When a user defines an emulation, he needs to specify pairs of distribution-emulator. When specifying an emulator it is bound to a specific resource type. For more complex scenarios users can specify multiple pairs which can also overlap from the time point of view.

COCOMA is provided within a BonFIRE VM, which is interfaced with the BonFIRE aggregator as shown in the figure below:

.. _cocoma-design:

.. figure:: cocoma-design.png
                :scale: 80
                :align: center
                
                COCOMA design and components interactions
                
The different functions provided by the COCOMA components and their interactions are explained below:

        * **ccmsh**: this is the command line interface (CLI) to interact with COCOMA. Users can specify an emulation in an XML file, which is interpreted by the *XMLParser* component. Also, the CLI allows to check and control the current running emulations (list, delete, etc.) by interacting directly with the DB
        * **REST API**: COCOMA provides also a REST API to interact with the framework programmatically
        * **XMLParser**: it checks xml correct format and return interpreted values to create an emulation. It is used by both *CLI* and *API*
        * **emulationManager**: the *emulationManager* receives input from the ccmsh or the REST API to create/query/delete an emulation
        * **distributionManager**: the *distributionManager* receives input from the *emulationManager* to load the distribution(s) and apply the relative algorithm in the distribution(s). It basically calculates how many runs (individual basic emulator instances) are needed, and the parameters values of each run.  These are then passed to the *scheduler*
        * **scheduler**: it creates the runs using the values obtained from the *distributionManager* at due time
        * **DB**: it holds information about running emulations, registered emulators, distributions and some configurations
        * **Logger**: it creates 2 different log files, one with all events relative to the runs created and the other one with the resource usage

COCOMA is designed to work with different emulators. To add a new emulator a user needs to install the new emulator where COCOMA is installed, create a python wrapper for the specific parameters of the emulator and place this wrapper into the *emulators* COCOMA directory. A similar approach is for distributions. Users can specify their desired discrete functions in a python file and place it in the *distributions* directory. Emulators and distributions that are in the those directories are automatically available to be used. In the next sections we provide details of how to create both emulators and distributions.

Code structure
--------------
COCOMA code structure is shown below:

::

        /bin
        /data
        /distributions
        /doc
        /emulators
        /logs
        /rb-examples
        /scripts
        /tests
        /unitTest
        __init__.py
        LICENSE
        NEWS
        NOTICE
        README

The bin directory contains the main components presented in the :ref:`cocoma-design` figure. It also contains 3 more files

        * `Job.py`: used to create and manage the `scheduler` jobs
        * `Library.py`: contains the common functions used by various components
        * `Logger.py`: implements the logging mechanisms

The `webUI` files are also contained within the `bin` directory, specifically in a subdirectory called `webcontent`.

The `data` folder contains the SQLite database file. The `distributions` directory contains the distributions currently available, while the emulators wrappers are in the `emulators` folder. In the `rb-examples` there are `restufully` examples to create emulations using the `COCOMA API`. In the `scripts` directory there is the `rec_res_usage` script that can be used to record a real trace from a system and replayed in COCOMA. Example xml tests are in the `tests` directory, while the automated tests are in the `unitTest` folder.

Building process
----------------
COCOMA is implemented in `python`, while the `webUI` in `Javascripts`, therefore there is no need for building anything. On the other hand a deb package has been created to install the software along with some of the dependencies. A building script is provided along with the debian files (`control`, `postinst` and `postrm`). The script uses 4 specific commands in order:

        * *sdist*: this is used by python ``python setup.py sdist`` to create a python source distribution as `tar.gz` file format [#f3]_. In order to use the command, a `setup.py` is provided as well [#f4]_. To use the `setuptools` in the `setup.py`, a `distribute_setup.py` is also needed. This is provided too
        * *py2dsc*: this generates a debian source package from a Python package [#f5]_
        * *dch*: this adds a new revision at the top of the Debian changelog file [#f6]_
        * *debuild*: this buils the debian package [#f7]_

The building script pulls the cocoma source code from the `github` repository [#f8]_. It takes as argument the version of the debian package that one wants to built such as:
::

        ./build_cocoma-deb 1.7.4

The building script, along the other needed python scripts (setup.py, distribute_setup.py) and the directory structure needed can be found in the BonFIRE svn repository [#f12]_. Once the directory is checked out, the script can be run from that directory and the deb package will be created in the ``dist/deb_dist`` folder.

Dependencies and other tools
----------------------------
In order for COCOMA to work as required, a number of dependencies and tools are needed. Dependecies are:

        * **python** version is **v2.7x**. Version v3.x hasn't been tested. `python-support` and `python-dev` are also needed
        * **python modules** used by the componenents to implement various functionalities
                * **bottle**: `is a fast, simple and lightweight WSGI micro web-framework`. Latest tested version is **v0.11.6**
                * **psutil**: `is a module providing an interface for retrieving information on all running processes and system utilization (CPU, memory, disks, network)`. Latest tested version is **v1.0.1**
                * **pyro4**: `it is a library that enables you to build applications in which objects can talk to eachother over the network`. Working tested version is **v4.20** is required. Later versions give serialization problems for the scheduler. This is a known issue by the pyro developers. If fixed, later versions should work
                * **apscheduler**: `is a light but powerful in-process task scheduler that lets you schedule functions (or any other python callables) to be executed at times of your choosing`. Latest tested version is **v2.1.1**
                * **pika**: `is a pure-Python implementation of the AMQP 0-9-1 protocol`. Latest tested version is **v0.9.13**
                * **PyUnit**: `Python language version of unit testing framework JUnit`. Latest tested version is **v1.4.1**
                * **requests**: `it is a HTTP library`. Latest tested version is **v2.0.0**
                * **numpy**: `is a general-purpose array-processing package designed to efficiently manipulate large multi-dimensional arrays of arbitrary records`. Latest tested version is **v1.7.1**
        * **pip**: `A tool for installing and managing Python packages`

As tools, COCOMA uses some as emulators, such as `stressapptest` [#f9]_, `lookbusy` [#f10]_, `backfuzz` [#f1]_ [#f2]_, `iperf` [#f11]_. Other used tools are for installation, such as ``curl, bc, unzip, gcc, g++, make``.

.. rubric:: Footnotes

.. [#f1] https://github.com/localh0t/backfuzz
.. [#f2] http://www.darknet.org.uk/2012/03/backfuzz-multi-protocol-fuzzing-toolkit-supports-httpftpimap-etc/
.. [#f3] http://docs.python.org/distutils/sourcedist.html
.. [#f4] http://docs.python.org/2/distutils/setupscript.html
.. [#f5] https://pypi.python.org/pypi/stdeb
.. [#f6] http://www.debian.org/doc/manuals/maint-guide/update.en.html
.. [#f7] http://www.debian.org/doc/manuals/maint-guide/build.en.html
.. [#f8] https://github.com/cragusa/cocoma 
.. [#f9] https://code.google.com/p/stressapptest/
.. [#f10] http://devin.com/lookbusy/
.. [#f11] https://code.google.com/p/iperf/
.. [#f12] https://scm.gforge.inria.fr/svn/bonfire-dev/cocoma/build-deb/
