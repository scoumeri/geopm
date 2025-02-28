.. role:: raw-html-m2r(raw)
   :format: html


geopm::PlatformIO(3) -- geopm platform interface
================================================






NAMESPACES
----------

The ``PlatformIO`` class, the ``IOGroup`` class, and the ``platform_io()``
singleton accessor function are members of the ``namespace geopm``\ , but
the full names, ``geopm::PlatformIO``\ , ``geopm::IOGroup`` and
``geopm::platform_io()``\ , have been abbreviated in this manual.
Similarly, the ``std::`` namespace specifier has been omitted from the
interface definitions for the following standard types:
``std::shared_ptr``\ , ``std::set``\ , ``std::string``\ , ``std::function``\ ,
``std::vector``\ , to enable better rendering of this manual.

Note that the ``PlatformIO`` class is an abstract base class that the
user interacts with.  The concrete implementation, ``PlatformIOImp``\ , is
hidden by the singleton accessor.

SYNOPSIS
--------

#include `<geopm/PlatformIO.hpp> <https://github.com/geopm/geopm/blob/dev/src/PlatformIO.hpp>`_\

Link with ``-lgeopmd``


.. code-block:: c++

    struct geopm_request_s {
        int domain;
        int domain_idx;
        char name[NAME_MAX];
    };

    namespace geopm
    {
        PlatformIO &platform_io(
            void)

        PlatformIO::PlatformIO(
            std::list<std::shared_ptr<IOGroup> > iogroup_list,
            const PlatformTopo &topo);

        void PlatformIO::register_iogroup(
            std::shared_ptr<IOGroup> iogroup);

        std::shared_ptr<IOGroup>
        PlatformIO::find_signal_iogroup(
            const std::string &signal_name) const;

        std::set<std::string>
        PlatformIO::signal_names(
            void) const;

        std::set<std::string>
        PlatformIO::control_names(
            void) const;

        int
        PlatformIO::signal_domain_type(
            const std::string &signal_name) const;

        int
        PlatformIO::control_domain_type(
            const std::string &control_name) const;

        int
        PlatformIO::push_signal(
            const std::string &signal_name,
            int domain_type,
            int domain_idx);

        int
        PlatformIO::push_signal_convert_domain(
            const std::string &signal_name,
            int domain_type,
            int domain_idx);

        int
        PlatformIO::push_combined_signal(
            const std::string &signal_name,
            int domain_type,
            int domain_idx,
            const std::vector<int> &sub_signal_idx);

        void
        PlatformIO::register_combined_signal(
            int signal_idx,
            std::vector<int> operands,
            std::unique_ptr<CombinedSignal> signal);

        int
        PlatformIO::push_control(
            const std::string &control_name,
            int domain_type,
            int domain_idx);

        int
        PlatformIO::push_control_convert_domain(
            const std::string &control_name,
            int domain_type,
            int domain_idx);

        int
        PlatformIO::num_signal_pushed(
            void) const;

        int
        PlatformIO::num_control_pushed(
            void) const;

        double
        PlatformIO::sample(
            int signal_idx);

        double
        PlatformIO::sample_combined(
            int signal_idx);

        void
        PlatformIO::adjust(
            int control_idx,
            double setting);

        void
        PlatformIO::read_batch(
            void);

        void
        PlatformIO::write_batch(
            void);

        double
        PlatformIO::read_signal(
            const std::string &signal_name,
            int domain_type,
            int domain_idx);

        double
        PlatformIO::read_signal_convert_domain(
            const std::string &signal_name,
            int domain_type,
            int domain_idx);

        void
        PlatformIO::write_control(
            const std::string &control_name,
            int domain_type,
            int domain_idx,
            double setting);

        void
        PlatformIO::write_control_convert_domain(
            const std::string &control_name,
            int domain_type,
            int domain_idx,
            double setting);

        void
        PlatformIO::save_control(
            void);

        void
        PlatformIO::restore_control(
            void);

        void
        PlatformIO::save_control(
            const std::string &save_dir);

        void PlatformIO::restore_control(
            const std::string &save_dir);

        std::function<double(const std::vector<double> &)>
        PlatformIO::agg_function(
            const std::string &signal_name) const;

        std::string
        PlatformIO::signal_description(
            const std::string &signal_name) const;

        std::string
        PlatformIO::control_description(
            const std::string &control_name) const;

        int
        PlatformIO::signal_behavior(
            const std::string &signal_name) const;

        void
        PlatformIO::start_batch_server(
            int client_pid,
            const std::vector<geopm_request_s> &signal_config,
            const std::vector<geopm_request_s> &control_config,
            int &server_pid,
            std::string &server_key);

        void
        PlatformIO::stop_batch_server(
            int server_pid);

    }


DESCRIPTION
-----------

The ``PlatformIO`` class provides a high-level interface for signals
(system monitors) and controls (system settings).  There are a large
number of built-in signals and controls.  These built-in signals and
controls include a wide range of hardware metrics, hardware settings,
and signals derived from application behavior.  Application behavior
is tracked by GEOPM's integration with MPI and OpenMP and also by
application use of the `geopm_prof_c(3) <geopm_prof_c.3.html>`_ mark-up interface. In
addition to the built-in features, ``PlatformIO`` can be extended
through the `geopm::IOGroup(3) <GEOPM_CXX_MAN_IOGroup.3.html>`_ plugin interface to provide
arbitrary signals and controls.

A domain is a discrete component within a compute node where a signal
or control is applicable.  For more information about the
``geopm_domain_e`` enum and the hierarchical platform description see
`geopm::PlatformTopo(3) <GEOPM_CXX_MAN_PlatformTopo.3.html>`_.  A signal represents any measurement in SI
units that can be sampled or any unit-free integer that can be read.
A control represents a request for a hardware domain to operate such
that a related signal measured from the hardware domain will track the
request.  For example, the user can set a ``POWER_PACKAGE_LIMIT`` in
units of watts and the related signal, ``POWER_PACKAGE``\ , will remain
below the limit.  Similarly the user can set a CPU ``FREQUENCY`` in
hertz and the related signal, ``FREQUENCY`` will show the CPU operating
at the value set.

ALIASING SIGNALS AND CONTROLS
-----------------------------

There are two classes of signals and control names: "low level" and
"high level".  All ``IOGroup``\ 's are expected to provide low level
signals and controls with names that are prefixed with the IOGroup
name and two colons, e.g. the ``MSRIOGroup`` provides the
``MSR::PKG_ENERGY_STATUS:ENERGY`` signal.  If the signal or control may
be supported on more than one platform, the implementation should be
aliased to a high level name.  This high level name enables the signal
or control to be supported by more than one ``IOGroup``\ , and different
platforms will support the loading different sets of ``IOGroups``.  The
``MSRIOGroup`` aliases the above signal to the high level
``PACKAGE_ENERGY`` signal which can be used on any platform to measure
the current package energy value.  Agents are encouraged to request
high level signals and controls to make the implementation more
portable.  The high level signals and controls supported by built-in
``IOGroup`` classes are listed below.  See `geopm::PluginFactory(3) <GEOPM_CXX_MAN_PluginFactory.3.html>`_
section on ``SEARCH AND LOAD ORDER`` for information about how the
``GEOPM_PLUGIN_PATH`` environment variable is used to select which
``IOGroup`` implementation is used in the case where more than one
provides the same high level signal or control.

Signal names that end in '#' (for example, raw MSR values) are 64-bit
integers encoded to be stored as doubles.  When accessing these
integer signals, the return value of ``read_signal``\ () or ``sample``\ ()
should not be used directly as a double precision number.  To
decode the 64-bit integer from the double use
``geopm_signal_to_field()`` described in `geopm_hash(3) <geopm_hash.3.html>`_.  The
`geopm::MSRIOGroup(3) <GEOPM_CXX_MAN_MSRIOGroup.3.html>`_ also provides raw MSR field signals that are
encoded in this way.


*
  ``TIME``\ :
  Time elapsed since the beginning of execution.

*
  ``EPOCH_COUNT``\ :
  Number of completed executions of an epoch.  Prior to the first call
  by the application to ``geopm_prof_epoch()`` the signal returns as -1.
  With each call to ``geopm_prof_epoch()`` the count increases by one.

*
  ``REGION_HASH``\ :
  The hash of the region of code (see `geopm_prof_c(3) <geopm_prof_c.3.html>`_\ ) currently being
  run by all ranks, otherwise GEOPM_REGION_HASH_UNMARKED.

*
  ``REGION_HINT``\ :
  The region hint (see `geopm_prof_c(3) <geopm_prof_c.3.html>`_\ ) associated with the currently
  running region.  For any interval when all ranks are within an MPI
  function inside of a user defined region, the hint will change from the
  hint associated with the user defined region to GEOPM_REGION_HINT_NETWORK.
  If the user defined region was defined with GEOPM_REGION_HINT_NETWORK and
  there is an interval within the region when all ranks are within an MPI
  function, GEOPM will not attribute the time spent within the MPI function as
  MPI time in the report files.  It will be instead attributed to the time
  spent in the region as a whole.

*
  ``REGION_PROGRESS``\ :
  Minimum per-rank reported progress through the current region.

*
  ``REGION_RUNTIME``\ :
  Maximum per-rank of the last recorded runtime for the current
  region.

*
  ``ENERGY_PACKAGE``\ :
  Total energy aggregated over the processor package.

*
  ``POWER_PACKAGE``\ :
  Total power aggregated over the processor package.

*
  ``FREQUENCY``\ :
  Average CPU frequency over the specified domain.

*
  ``ENERGY_DRAM``\ :
  Total energy aggregated over the DRAM DIMMs associated with a NUMA
  node.

*
  ``POWER_DRAM``\ :
  Total power aggregated over the DRAM DIMMs associated with a NUMA
  node.

*
  ``POWER_PACKAGE_MIN``\ :
  Minimum setting for package power over the given domain.

*
  ``POWER_PACKAGE_MAX``\ :
  Maximum setting for package power over the given domain.

*
  ``POWER_PACKAGE_TDP``\ :
  Maximum sustainable setting for package power over the given domain.

*
  ``CYCLES_THREAD``\ :
  Average over the domain of clock cycles executed by cores since
  the beginning of execution.

*
  ``CYCLES_REFERENCE``\ :
  Average over the domain of clock reference cycles since the
  beginning of execution.

SINGLETON ACCESSOR
------------------


* ``platform_io``\ ():
  There is only one ``PlatformIO`` object, and the only way to access
  this object is through this function.  The function returns a
  reference to the single ``PlatformIO`` object that gives access to
  all of the CLASS METHODS described below.  See ``EXAMPLE`` section
  below.

INSPECTION CLASS METHODS
------------------------


*
  ``signal_names()``\ :
  Returns the names of all available signals that can be requested.
  This includes all signals and aliases provided through ``IOGroup``
  extensions as well as signals provided by PlatformIO itself.  The
  set of strings that are returned can be passed as a _signal\ *name*
  to all ``PlatformIO`` methods that accept a signal name input
  parameter.

*
  ``control_names()``\ :
  Returns the names of all available controls.  This includes all
  controls and aliases provided by IOGroups as well as controls
  provided by PlatformIO itself.  The set of strings that are returned
  can be passed as a _control\ *name* to all ``PlatformIO`` methods that
  accept a control name input parameter.

*
  ``signal_description()``\ :
  Returns the description of the signal as defined by the IOGroup that
  provides this signal.

*
  ``control_description()``\ :
  Returns the description of the control as defined by the IOGroup that
  provides this control.

*
  ``signal_domain_type()``\ :
  Query the domain for the signal with name _signal\ *name*.  Returns
  one of the ``geopm_domain_e`` values signifying the
  granularity at which the signal is measured.  Will return
  ``GEOPM_DOMAIN_INVALID`` if the signal name is not
  supported.

*
  ``control_domain_type()``\ :
  Query the domain for the control with the name _control\ *name*.
  Returns one of the ``geopm_domain_e`` values
  signifying the granularity at which the control can be adjusted.
  Will return ``GEOPM_DOMAIN_INVALID`` if the control
  name is not supported.

*
  ``agg_function``\ ():
  Returns the function that should be used to aggregate
  _signal\ *name*.  If one was not previously specified by this class,
  the default function is select_first from `geopm::Agg(3) <GEOPM_CXX_MAN_Agg.3.html>`_.

*
  ``signal_behavior``\ ():
  Returns one of the IOGroup::signal_behavior_e values which
  describes about how a signal will change as a function of time.
  This can be used when generating reports to decide how to
  summarize a signal's value for the entire application run.

SERIAL CLASS METHODS
--------------------


*
  ``read_signal()``\ :
  Read from the platform and interpret into SI units a signal
  given its name and domain.  Does not modify values stored by
  calling ``read_batch()``.

*
  ``write_control()``\ :
  Interpret the setting and write it to the platform.  Does not
  modify the values stored by calling ``adjust()``.

*
  ``save_control()``\ :
  Save the state of all controls so that any subsequent changes
  made through PlatformIO may be reverted with a call to
  ``restore_control()``.

*
  ``restore_control()``\ :
  Restore all controls to values recorded in previous call to
  ``save_control()``.

BATCH CLASS METHODS
-------------------


*
  ``push_signal()``\ :
  Push a signal onto the stack of batch access signals.  The signal
  is defined by selecting a _signal\ *name* from the set returned by
  the ``signal_names()`` method, the _domain\ *type* from one of the
  ``geopm_domain_e`` values, and the _domain\ *idx* between
  zero to the value returned by
  ``PlatformTopo::num_domain(_domain_type_)``.  Subsequent calls to
  the ``read_batch()`` method will read the signal and update the
  internal state used to store batch signals.  The return value of
  the method can be passed to the ``sample()`` method to access
  the signal stored in the internal state from the last update.  The
  returned signal index will be repeated for each unique tuple of
  push_signal input parameters.  All signals must be pushed onto the
  stack prior to the first call to ``sample()`` or ``read_batch()``.
  Attempts to push a signal onto the stack after the first call to
  ``sample()`` or ``read_batch()`` or attempts to push a _signal\ *name*
  that is not from the set returned by ``signal_names()`` will result
  in a thrown ``geopm::Exception`` with error number
  ``GEOPM_ERROR_INVALID``.

*
  ``push_control()``\ :
  Push a control onto the stack of batch access controls.  The
  control is defined by selecting a _control\ *name* from the set
  returned by the ``control_names()`` method, the _domain\ *type* from
  one of the ``geopm_domain_e`` values, and the _domain\ *idx*
  between zero to the value returned by
  ``PlatformTopo::num_domain(_domain_type_)``.  The return value of
  the method can be passed to the ``adjust()`` method which will
  update the internal state used to store batch controls.
  Subsequent calls to the ``write_batch()`` method access the control
  values in the internal state and write the values to the hardware.
  The returned control index will be repeated for each unique tuple
  of push_control input parameters.  All controls must be pushed
  onto the stack prior to the first call to ``adjust()`` or
  ``write_batch()``.  Attempts to push a controls onto the stack after
  the first call to ``adjust()`` or ``write_batch()`` or attempts to push
  a _control\ *name* that is not from the set returned by
  ``control_names()`` will result in a thrown ``geopm::Exception`` with
  error number ``GEOPM_ERROR_INVALID``.

*
  ``sample()``\ :
  Samples cached value of a single signal that has been pushed via
  ``push_signal()`` cached value is upated at the time of call to
  ``read_batch()``.

*
  ``adjust()``\ :
  Updates cached value for single control that has been pushed via
  ``push_control()`` cached value will be written to the platform at
  time of call to ``write_batch()``.

*
  ``read_batch()``\ :
  Read all push signals from the platform so that the next call to ``sample()``
  will reflect the updated data.

*
  ``write_batch()``\ :
  Write all pushed controls so that values provided to ``adjust()``
  are written to the platform.

PLUGIN CLASS METHODS
--------------------


* ``register_iogroup()``\ :
  Registers an ``IOGroup`` with the ``PlatformIO`` so that the signals
  and controls provided by the object are available through the
  ``PlatformIO`` interface.  The *iogroup* is a shared pointer to a
  class derived from the `geopm::IOGroup(3) <GEOPM_CXX_MAN_IOGroup.3.html>`_.  This method
  provides the mechanism for extending the ``PlatformIO`` interface at
  runtime.

TYPES
-----


* ``m_request_s``\ :

EXAMPLE
-------

.. code-block::

   /* Print a signal for all CPUs on the system. */

   #include <iostream>
   #include <string>
   #include <geopm/PlatformIO.hpp>
   #include <geopm/PlatformTopo.hpp>

   int main(int argc, char **argv)
   {
       if (argc != 2) {
           std::cerr << "Usage: " << argv[0] << " SIGNAL_NAME" << std::endl;
           return -1;
       }
       std::string signal_name = argv[1];
       geopm::PlatformIO &pio = geopm::platform_io();
       geopm::PlatformTopo &topo = geopm::platform_topo();
       const int DOMAIN = pio.signal_domain_type(signal_name);
       const int NUM_DOMAIN = topo.num_domain(DOMAIN);
       std::cout << "cpu_idx    " << signal_name << std::endl;
       for (int domain_idx = 0; domain_idx != NUM_DOMAIN; ++domain_idx) {
           double signal = pio.read_signal(signal_name, DOMAIN, domain_idx);
           for (const auto &cpu_idx : topo.domain_cpus(DOMAIN, domain_idx)) {
               std::cout << cpu_idx << "    " << signal << std::endl;
           }
       }
       return 0;
   }



ERRORS
------

All functions described on this man page throw `geopm::Exception(3) <GEOPM_CXX_MAN_Exception.3.html>`_
on error.

SEE ALSO
--------

`geopm(7) <geopm.7.html>`_\ ,
`geopm_hash(3) <geopm_hash.3.html>`_\ ,
`geopm_prof_c(3) <geopm_prof_c.3.html>`_\ ,
`geopm_pio_c(3) <geopm_pio_c.3.html>`_\ ,
`geopm_topo_c(3) <geopm_topo_c.3.html>`_\ ,
`geopm::Exception(3) <GEOPM_CXX_MAN_Exception.3.html>`_\ ,
`geopm::IOGroup(3) <GEOPM_CXX_MAN_IOGroup.3.html>`_\ ,
`geopm::MSRIOGroup(3) <GEOPM_CXX_MAN_MSRIOGroup.3.html>`_\ ,
`geopm::PlatformTopo(3) <GEOPM_CXX_MAN_PlatformTopo.3.html>`_\ ,
`geopm::PluginFactory(3) <GEOPM_CXX_MAN_PluginFactory.3.html>`_
