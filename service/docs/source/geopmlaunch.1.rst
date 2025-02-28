.. role:: raw-html-m2r(raw)
   :format: html


geopmlaunch(1) -- application launch wrapper
============================================






SYNOPSIS
--------

``geopmlaunch`` *launcher* [_launcher\ *opt*\ ] [_geopm\ *opt*\ ] ``--`` *executable* [_executable\ *opt*\ ]

DESCRIPTION
-----------

The ``geopmlaunch`` application enables execution of the GEOPM runtime
along with a distributed parallel compute application, *executable*\ ,
using the command line interface for the underlying application
scheduler, *launcher*\ , deployed on the HPC system.  The ``geopmlaunch``
command line interface is designed to support many application
schedulers including SLURM ``srun``\ , ALPS ``aprun``\ , and Intel / MPICH
``mpiexec``.  The ``geopmlaunch`` command line interface has been designed
to wrap the underlying application scheduler while reinterpreting the
command line options, _launcher\ *opt*\ , specified for it.  In this way,
the user can easily modify an existing job launch command to enable
the GEOPM runtime by prefixing the command with ``geopmlaunch`` and
extending the existing scheduler options with the the options for the
GEOPM runtime, _geopm\ *opt*.  The GEOPM runtime options control the
behavior of the GEOPM runtime and are detailed in the ``GEOPM OPTIONS``
section below.

All command line options accepted by the underlying job scheduler
(e.g. ``srun`` or ``aprun``\ ) can be passed to the ``geopmlaunch`` wrapper
with the exception of CPU affinity related options.  The wrapper
script reinterprets the command line to pass modified options and set
environment variables for the underlying application scheduler.  The
GEOPM options, _geopm\ *opt*\ , are translated into environment variables
to be interpreted by the GEOPM runtime (see the ENVIRONMENT section of
`geopm(7) <geopm.7.html>`_\ ).  The reinterpreted command line, including the
environment modification, is printed to standard output by the script
before execution.  The command that is printed can be executed in the
``bash`` shell to replicate the execution without using ``geopmlaunch``
directly.  The command is modified to support the GEOPM control thread
by setting CPU affinity for each process and increasing the number of
processes per node or CPUs per process.

Note: the primary compute *executable* and its options,
_executable\ *opt*\ , must appear at the end of the command line and be
preceded by two dashes: ``--``. The GEOPM launcher will not parse
arguments to the right of the first ``--`` sequence and will pass the
arguments that follow unaltered while removing the first ``--`` from the
command line.  Refer to the EXAMPLES section below.

SUPPORTED LAUNCHERS
-------------------

The launcher is selected by specifying the *launcher* as the first
command line parameter.  Available *launcher* values are
listed below.


* 
  *srun*\ , *SrunLauncher*\ :
  Wrapper for the SLURM resource manager's ``srun`` job launcher.  The
  ``--cpu_bind`` and ``--cpu-bind`` options are reserved for use by GEOPM;
  do not specify when using ``geopmlaunch``.

* 
  *aprun*\ , *AlpsLauncher*\ :
  Wrapper for the Cray ALPS ``aprun`` job launcher.  The ``-cc`` and
  ``--cpu-binding`` options are reserserved for use by GEOPM; do not
  specify these when using ``geopmlaunch``.

* 
  *impi*\ , *IMPIExecLauncher*\ :
  Wrapper for the Intel MPI ``mpiexec`` job launcher.  The
  ``KMP_AFFINITY`` ``I_MPI_PIN_DOMAIN``\ , and ``MV2_ENABLE_AFFINITY``
  environment variables reserved for use by GEOPM and are overwritten
  when using ``geopmlaunch``.

* 
  *ompi*\ , *OMPIExecLauncher*\ :
  Wrapper for the Open MPI ``mpiexec`` job launcher.  The
  ``-rf`` and ``--rank-file`` as well as explictly specifying number of
  processes with ``-H`` and ``--host`` options are reserved for use by GEOPM;
  do not specify when using ``geopmlaunch``.

* 
  *SrunTOSSLauncher*\ :
  Wrapper for ``srun`` when used with the Trilab Operating System
  Software stack.  This special launcher was developed to support
  special affinity plugins for SLURM that were deployed at LLNL's
  computing center.  The ``--cpu_bind`` and ``--cpu-bind`` options are
  reserved for use by GEOPM; do not specify when using ``geopmlaunch``.

GEOPM OPTIONS
-------------


* 
  ``--geopm-report`` path:
  Specifies the path to the GEOPM report output file that is generated
  at the conclusion of the run if this option is provided.  If the
  option is not provided, a report named "geopm.report" will be
  created.  The GEOPM report contains a summary of the profiling
  information collected by GEOPM throughout the application execution.
  Refer to `geopm_report(7) <geopm_report.7.html>`_ for a description of the information
  contained in the report.  This option is used by the launcher to set
  the ``GEOPM_REPORT`` environment variable.  The command line option
  will override any value currently set in the environment.  See the
  ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-report-signals`` signals:
  Used to insert additional measurements into the report beyond the
  default values.  This feature requires that the requested signals
  are increasing monotonically with time.  Each time a region is
  entered or exited the value of the signals is measured.  When the
  region is exited the value of the signal upon entry is subtracted
  from the value of the signal upon exit.  The total given in the
  report for the signal associated with the region is the cumulative
  sum of the differences for each occurrence of the region.  The value
  must be formatted as a comma-separated list of valid signal names.
  The signals available and their descriptions are documented in the
  **PlatformIO(3)** man page.

  By default the signals in the report will be aggregated to the board
  domain.  A domain other than board can be specified by appending the
  signal name with an "@" character and then specifying one of the
  domains.  For example, the following will extend the region and
  application totals sections of the report with package energy for
  each package and DRAM energy summed over the all DIMMs:

  ``--geopm-report-signals=ENERGY_PACKAGE@package,ENERGY_DRAM``

  The `geopmread(1) <geopmread.1.html>`_ executable enables discovery of signals and
  domains available on your system.  The signal names and domain names
  given for this parameter are specified as in the `geopmread(1) <geopmread.1.html>`_
  command line interface.

* 
  ``--geopm-trace`` path:
  The base name and path of the trace file(s) generated if this option
  is specified.  One trace file is generated for each compute node
  used by the application containing a pipe-delimited ASCII table
  describing a time series of measurements made by the GEOPM runtime.
  The path is extended with the host name of the node for each created
  file.  The trace files will be written to the file system path
  specified or current directory if only a file name is given.  This
  feature is primarily a debugging tool, and may not scale to large
  node counts due to file system issues.  This option is used by the
  launcher to set the GEOPM_TRACE environment variable.  The command
  line option will override any value currently set in the
  environment.  See the ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-trace-signals`` signals:
  Used to insert additional columns into the trace beyond the default
  columns and the columns added by the Agent.  This option has no
  effect unless tracing is enabled with ``--geopm-trace``.  The value
  must be formatted as a comma-separated list of valid signal names.
  When not specified all custom signals added to the trace will be
  sampled and aggregated for the entire node unless the domain is
  specified by appending "@domain_type" to the signal name.  For
  example, the following will add total DRAM energy and power as
  columns in the trace:

  ``--geopm-trace-signals=ENERGY_DRAM,POWER_DRAM``

  The signals available and their descriptions are documented in the
  **PlatformIO(3)** man page.  "TIME", "REGION_HASH", "REGION_HINT",
  "REGION_PROGRESS", "REGION_RUNTIME", "ENERGY_PACKAGE",
  "POWER_PACKAGE", and "FREQUENCY" are included in the trace by
  default.  A domain other than board can be specified by appending
  the signal name with an "@" character and then specifying one of the
  domains, e.g:

  ``--geopm-trace-signals=POWER_PACKAGE@package,ENERGY_PACKAGE@package``

  will trace the package power and energy for each package on the
  system.  The `geopmread(1) <geopmread.1.html>`_ executable enables discovery of
  signals and domains available on your system.  The signal names and
  domain names given for this parameter are specified as in the
  `geopmread(1) <geopmread.1.html>`_ command line interface.  This option is used by the
  launcher to set the GEOPM_TRACE_SIGNALS environment variable.  The
  command line option will override any value currently set in the
  environment.  See the ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-trace-profile`` path:
  The base name and path of the profile trace file(s) generated if
  this option is specified.  One trace file is generated for each
  compute node used by the application containing a pipe-delimited
  ASCII table describing a log of each call to the ``geopm_prof_*()``
  APIs.  The path is extended with the host name of the node for each
  created file.  The profile trace files will be written to the file
  system path specified or current directory if only a file name is
  given.  This feature is primarily a debugging tool, and may not
  scale to large node counts due to file system issues.  This option
  is used by the launcher to set the GEOPM_TRACE_PROFILE environment
  variable.  The command line option will override any value currently
  set in the environment.  See the ENVIRONMENT section of
  `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-trace-endpoint-policy`` path:
  The path to the endpoint policy trace file generated if this option
  is specified.  This file tracks only policies sent through the
  endpoint at the root controller, not all policies within the
  controller tree.  If ``--geopm-endpoint`` is not provided, or if the
  agent does not have any policy values, this file will not be
  created.  This option is used by the launcher to set the
  GEOPM_TRACE_ENDPOINT_POLICY environment variable.  The command line
  option will override any value currently set in the environment.
  See the ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-profile`` name:
  The name of the profile which is printed in the report and trace
  files.  This name can be used to index the data in post-processing.
  For example, when running a sweep of experiments with multiple power
  caps, the profile could contain the power setting for one run.  The
  default profile name is the name of the compute application
  executable.  This option is used by the launcher to set the
  GEOPM_PROFILE environment variable.  The command line option will
  override any value currently set in the environment.  See the
  ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-ctl`` *process*\ |\ *pthread*\ |\ *application*\ :
  Use GEOPM runtime and launch GEOPM with one of three methods:
  *process*\ , *pthread* or *application*.  The *process* method
  allocates one extra MPI process per node for the GEOPM controller,
  and this is the default method if the ``--geopm-ctl`` option is not
  provided.  The *pthread* method spawns a thread from one MPI process
  per node to run the GEOPM controller.  The *application* method
  launches the `geopmctl(1) <geopmctl.1.html>`_ application in the background which
  connects to the primary compute application.  The *process* method
  can be used in the widest variety of cases, but some systems require
  that each MPI process be assigned the same number of CPUs which may
  waste resources by assigning more than one CPU to the GEOPM
  controller process.  The *pthread* option requires support for
  MPI_THREAD_MULTIPLE, which is not enabled at many sites.  The
  *application* method of launch is not compatible with ``aprun``\ ; with
  ``srun``\ , the call must be made inside of an existing allocation made
  with salloc or sbatch and the command must request all of the
  compute nodes assigned to the allocation.  This option is used by
  the launcher to set the GEOPM_CTL environment variable.  The command
  line option will override any value currently set in the
  environment.  See the ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-agent`` agent:
  Specify the Agent type.  The Agent defines the control algorithm
  used by the GEOPM runtime.  Available agents are: "monitor" (default
  if option not specified; enables profiling features only),
  "power_balancer" (optimizes runtime under a power cap),
  "power_governor" (enforces a uniform power cap), "frequency_map"
  (runs each region at a specifed frequency), and "energy_efficient"
  (saves energy).  See `geopm_agent_monitor(7) <geopm_agent_monitor.7.html>`_\ ,
  `geopm_agent_power_balancer(7) <geopm_agent_power_balancer.7.html>`_\ ,
  `geopm_agent_power_governor(7) <geopm_agent_power_governor.7.html>`_\ , `geopm_agent_frequency_map(7) <geopm_agent_frequency_map.7.html>`_
  and `geopm_agent_energy_efficient(7) <geopm_agent_energy_efficient.7.html>`_ for descriptions of each
  agent.  For more details on the responsibilities of the Agent, see
  `geopm::Agent(3) <GEOPM_CXX_MAN_Agent.3.html>`_.  This option is used by the launcher to set the
  GEOPM_AGENT environment variable.  The command line option will
  override any value currently set in the environment.  See the
  ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-policy`` policy:
  GEOPM policy JSON file used to configure the Agent plugin.  If the
  policy is provided through this file, it will only be read once and
  cannot be changed dynamically.  In this mode, samples will not be
  provided to the resource manager.  See `geopmagent(1) <geopmagent.1.html>`_ and
  `geopm_agent_c(3) <geopm_agent_c.3.html>`_ for more information about how to create this
  input file.  This option is used by the launcher to set the
  GEOPM_POLICY environment variable.  The command line option will
  override any value currently set in the environment.  See the
  ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-affinity-disable``\ :
  Enable direct user control of all application CPU affinity settings.
  When specified, the launcher will not emit command line arguments or
  environment variables related to affinity settings for the
  underlying launcher.  The user is free to provide whatever affinity
  settings are best for their application.  It is recommended that at
  least one core is left free for the GEOPM controller thread, and if
  there is a free core, the controller will automatically affinitize
  itself to a CPU on that core when it connects with the application.
  When this option is specified the user is responsible for providing
  settings that affinitize MPI ranks to distinct CPUs.  Note: this
  requirement is satisfied by the default behavior for some launchers
  like Intel MPI.

* 
  ``--geopm-endpoint`` endpoint:
  Prefix for shared memory keys used by the endpoint.  The endpoint
  will be used to receive policies dynamically from the resource
  manager.  The shared memory for the endpoint does not use the
  ``--geopm-shmkey`` prefix.  Refer to `geopm_endpoint_c(3) <geopm_endpoint_c.3.html>`_ for more
  detail.  If this option is provided, the GEOPM controller will also
  send samples to the endpoint at runtime, depending on the Agent
  selected.  This option overrides the use of ``--geopm-policy`` to
  receive policy values.  This option is used by the launcher to set
  the GEOPM_ENDPOINT environment variable.  The command line option
  will override any value currently set in the environment.  See the
  ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-shmkey`` key:
  Specify a special prefix to be used with all of the shared memory
  keys generated by the GEOPM runtime for communication with the
  application.  It is not used for the endpoint.  This is useful for
  avoiding collisions with keys that were not properly cleaned up.
  The default key prefix is "geopm-shm".  A shared memory key must
  have no occurrences of the '/' character.  The base key is used as
  the prefix for each shared memory region used by the runtime.  If
  the keys are left behind, a simple command to clean up after an
  aborted job is:

    ``$ test -n "$GEOPM_SHMKEY" && rm -f /dev/shm${GEOPM_SHMKEY}* || rm -f /dev/shm/geopm-shm*``

  This option is used by the launcher to set the GEOPM_SHMKEY
  environment variable.  The command line option will override any
  value currently set in the environment.  See the ENVIRONMENT section
  of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-timeout`` sec:
  Time in seconds that the application should wait for the GEOPM
  controller to connect over shared memory.  The default value is 30
  seconds.  This option is used by the launcher to set the
  GEOPM_TIMEOUT environment variable.  The command line option will
  override any value currently set in the environment.  See the
  ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-plugin-path`` path:
  The search path for GEOPM plugins. It is a colon-separated list of
  directories used by GEOPM to search for shared objects which contain
  GEOPM plugins.  In order to be available to the GEOPM runtime,
  plugins should register themselves with the appropriate factory.
  See `geopm::PluginFactory(3) <GEOPM_CXX_MAN_PluginFactory.3.html>`_ for information about the GEOPM
  plugin interface.  A zero-length directory name indicates the
  current working directory; this can be specified by a leading or
  trailing colon, or two adjacent colons.  The default search location
  is always loaded first and is determined at library configuration
  time and by way of the 'pkglib' variable (typically
  /usr/lib64/geopm/).  This option is used by the launcher to set the
  GEOPM_PLUGIN_PATH environment variable.  The command line option
  will override any value currently set in the environment.  See the
  ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-record-filter`` filter:
  Applies the user specified filter to the application record data
  feed.  The filters currently supported are "proxy_epoch" and
  "edit_distance".  These filters can be used to infer the application
  outer loop (epoch) without modifying the application by inserting
  calls to ``geopm_prof_epoch()`` (see `geopm_prof_c(3) <geopm_prof_c.3.html>`_\ ).  Region
  entry and exit may be captured automatically through runtimes such
  as MPI and OpenMP.

  The "proxy_epoch" filter looks for entries into a specific region
  that serves as a proxy for epoch events.  The filter is specified as
  a comma-separated list.  The first value selects the filter by name:
  "proxy_epoch". The second value in the comma-separated list
  specifies a region that will be used as a proxy for calls to
  geopm_prof_epoch().  If the value can be interpreted as an integer,
  it will be used as the numerical region hash of the region name,
  otherwise, the value is interpreted as the region name.  The third
  value that can be provided in the comma-separated list is optional.
  If provided, it specifies the number of region entries into the
  proxy region that are expected per outer loop.  By default this is
  assumed to be 1.  The fourth optional parameter that can be
  specified in the comma-separated list is the number of region
  entries into the proxy region that are expected prior to the outer
  loop beginning.  By default this is assumed to be 0.  In the
  following example, the MPI_Barrier region entry is used as a proxy
  for the epoch event:

  .. code-block::

     --geopm-record-filter=proxy_epoch,MPI_Barrier


  In the next example the MPI_Barrier region is specified as a hash
  and the calls per outer loop is given as 6:

  .. code-block::

     --geopm-record-filter=proxy_epoch,0x7b561f45,6


  In the last example the calls prior to startup is specified as 10:

  .. code-block::

     --geopm-record-filter=proxy_epoch,MPI_Barrier,6,10


  Note: you must specify the calls per outer loop in order to specify
  the calls prior to startup.

  The "edit_distance" filter will attempt to infer the epoch based on
  patterns in the region entry events using an edit distance
  algorithm.  The filter is specified as string beginning with the
  name "edit_distance"; if optional parameters are specified, they are
  provided as a comma-separated list following the name.  The first
  parameter is the buffer size; the default if not provided is 100.
  The second parameter is the minimum stable period length in number
  of records.  The third parameter is the stable period hysteresis
  factor.  The fourth parameter is the unstable period hysteresis
  factor.  In the following example, the "edit_distance" filter will
  be used with all optional parameters provided:

  .. code-block::

     --geopm-record-filter=edit_distance,200,8,2.0,3.0

* 
  ``--geopm-debug-attach`` rank:
  Enables a serial debugger such as gdb to attach to a job when the
  GEOPM PMPI wrappers are enabled.  If set to a numerical value, the
  associated rank will wait in MPI_Init() until a debugger is attached
  and the local variable "cont" is set to a non-zero value.  If set,
  but not to a numerical value then all ranks will wait.  The runtime
  will print a message explaining the hostname and process ID that the
  debugger should attach to.  This option is used by the launcher to
  set the GEOPM_DEBUG_ATTACH environment variable.  The command line
  option will override any value currently set in the environment.
  See the ENVIRONMENT section of `geopm(7) <geopm.7.html>`_.

* 
  ``--geopm-hyperthreads-disable``\ :
  Prevent the launcher from trying to use hyperthreads for pinning
  purposes when attempting to satisfy the MPI ranks / OMP threads
  configuration specified.  This is done for both the controller and
  the application.  An error is raised if the launcher cannot satisfy
  the current request without hyperthreads.

* 
  ``--geopm-ctl-disable``\ :
  Used to allow passing the command through to the underlying launcher.
  By default, ``geopmlaunch`` will launch the GEOPM runtime in process mode.
  When this option is specified, the GEOPM runtime will not be launched.

* 
  ``--geopm-ompt-disable``\ :
  Disable OMPT detection of OpenMP regions.  See the INTEGRATION WITH OMPT
  section of `geopm(7) <geopm.7.html>`_ for more information about OpenMP region detection.

EXAMPLES
--------

Use geopmlaunch to queue a job using geopmbench on a SLURM managed system
requesting two nodes using 32 application MPI process each with four threads:

.. code-block::

   geopmlaunch srun -N 2 -n 32 -c 4 \
                    --geopm-ctl=process \
                    --geopm-report=tutorial6.report \
                    -- ./geopmbench tutorial6_config.json


Use geopmlaunch to launch the miniFE executable with the same configuration,
but on an ALPS managed system:

.. code-block::

   geopmlaunch aprun -N 2 -n 64 --cpus-per-pe 4 \
                     --geopm-ctl process \
                     --geopm-report miniFE.report \
                     -- ./miniFE.x -nx 256 -ny 256 -nz 256


ENVIRONMENT
-----------

Every command line option to the launcher can also be specified as an
environment variable if desired (with the exception of ``--geopm-ctl``\ ).
For example, instead of specifying ``--geopm-trace=geopm.trace`` one can
instead set in the environment ``GEOPM_TRACE=geopm.trace`` prior to
invoking the launcher script.  The environment variables are named the
same as the command line option but have the hyphens replaced with
underscores, and are all uppercase.  The command line options take
precedence over the environment variables.

The usage of ``--geopm-ctl`` here is slightly different than how the
controller handles the ``GEOPM_CTL`` environment variable.  In the
case of the launcher, one can specify *process*\ , *pthread*\ , or
*application* to the command line argument.  In the case of
``GEOPM_CTL`` one can ONLY specify ``process`` or ``pthread``\ , as
launching the controller as a separate application is handled through
the ``geopmctl`` binary.

The interpretation of the environment is affected if either of the
GEOPM configuration files exist:

.. code-block::

   /etc/geopm/environment-default.json
   /etc/geopm/environment-override.json


These files may specify system default and override settings for all
of the GEOPM environment variables.  The ``environment-default.json``
file contains a JSON object mapping GEOPM environment variable strings
to strings that define default values for any unspecified GEOPM
environment variable or unspecified ``geopmlaunch`` command line
options.  The ``environment-override.json`` contains a JSON object that
defines values for GEOPM environment variables that take precedence
over any settings provided by the user either through the environment
or through the ``geopmlaunch`` command line options.  The order of
precedence for each GEOPM variable is: override configuration file,
``geopmlaunch`` command line option, environment setting, the default
configuration file, and finally there are some preset default values
that are coded into GEOPM which have the lowest precedence.

The ``KMP_WARNINGS`` environment variable is set to 'FALSE', thus
disabling the Intel OpenMP warnings.  This avoids warnings emitted
because the launcher configures the ``OMP_PROC_BIND`` environment
variable to support applications compiled with a non-Intel
implementation of OpenMP.

SEE ALSO
--------

`geopm(7) <geopm.7.html>`_\ ,
`geopmpy(7) <geopmpy.7.html>`_\ ,
`geopm_agent_energy_efficient(7) <geopm_agent_energy_efficient.7.html>`_\ ,
`geopm_agent_monitor(7) <geopm_agent_monitor.7.html>`_\ ,
`geopm_agent_power_balancer(7) <geopm_agent_power_balancer.7.html>`_\ ,
`geopm_agent_power_governor(7) <geopm_agent_power_governor.7.html>`_\ ,
`geopm_report(7) <geopm_report.7.html>`_\ ,
`geopm_error(3) <geopm_error.3.html>`_\ ,
`geopmctl(1) <geopmctl.1.html>`_
