.. tabularcolumns:: |p{4.5cm}|p{8.5cm}|
.. list-table::
        :widths: 20 80
        :header-rows: 1
   
        * - Term
          - Description
        * - Emulation
          - Process that imitates a specific behaviour specified in the emulation type, over a resource type, using one or more distributions during the emulation lifetime
        * - Emulation type
          - An emulation can be of the following types:
          
                - Contentiousness
                - Maliciousness
                - Faultiness (not yet implemented)
                - Mixed (a combination of the above types)
        * - Resource type
          - A resource can be of the following types:
          
                - CPU
                - RAM
                - I/O
                - Network
        * - Emulator
          - Specific mechanism/tool that is used to create an emulation type. For example load generators, stress generators, fault generators and malicious payload creation.
        * - Distribution
          - In the case of contention, it is a discrete function of a specific resource type over a specific time within the emulation lifetime. The distribution time is divided into multiple timeslots (t0, .. , tn) based on the distribution granularity. A distribution is broken down into multiple runs each one injecting a different load level per time slot depending on the discrete function of the distribution. In the case of malicious, it is a straight mapping to the emulator
        * - Distribution granularity
          - Number of runs for the distribution
        * - Emulation lifetime
          - Duration of the emulation
        * - Run
          - Basic emulator instantiation
