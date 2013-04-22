Introduction
============
In order to use COCOMA, an experimenter defines an `emulation` which embeds all environment operational conditions as shown in the figure below. The actual operational conditions are defined in what are called `distributions`, which create specific workloads over the targeted resource of a specific resource type. For example, `distribution 1` targets the CPU creating an exponential trend over a specific time range within the whole emulation. Each distribution time is divided into multiple time-slots based on the distribution granularity then broken down into multiple runs each one injecting a different load level per time slot, which depends on the discrete function of the distribution.

	.. figure:: emulation2.png
		:align: center