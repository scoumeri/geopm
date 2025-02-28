.. role:: raw-html-m2r(raw)
   :format: html


geopm::CircularBuffer(3) -- generic circular buffer
===================================================






NAMESPACES
----------

The ``CircularBuffer`` class is a member of the ``namespace geopm``,
but the full name, ``geopm::CircularBuffer``, has been abbreviated in this manual.
Similarly, the ``std::`` namespace specifier has been omitted from the
interface definitions for the following standard types: ``std::vector``\ ,
``std::pair``\ , ``std::string``\ , ``std::map``\ , and ``std::function``\ , to enable
better rendering of this manual.

SYNOPSIS
--------

#include `<geopm/CircularBuffer.hpp> <https://github.com/geopm/geopm/blob/dev/src/CircularBuffer.hpp>`_\ 


.. code-block:: c++

       void CircularBuffer::set_capacity(const unsigned int size);

       void CircularBuffer::clear(void);

       int CircularBuffer::size(void) const;

       int CircularBuffer::capacity(void) const;

       void CircularBuffer::insert(const T value);

       const T& CircularBuffer::value(const unsigned int index) const;

       vector<T> CircularBuffer::make_vector(void) const;

       vector<T> CircularBuffer::make_vector(const unsigned int start, const unsigned int end) const;

DESCRIPTION
-----------

The CircularBuffer container implements a fixed-size buffer. Once at
capacity, any new insertions cause the oldest entry to be dropped.

CLASS METHODS
-------------


* 
  ``set_capacity()``:
  Resets the capacity of the circular buffer to *size* without
  modifying its current contents.

* 
  ``clear()``:
  Clears all entries from the buffer.  The size becomes ``0``, but the
  capacity is unchanged.

* 
  ``size()``:
  Returns the number of items in the buffer.  This value will be less
  than or equal to the current capacity of the buffer.

* 
  ``capacity()``:
  Returns the current size of the circular buffer at the time of the
  call.

* 
  ``insert()``:
  Inserts *value* into the buffer.  If the buffer is not full, the new
  value is simply added to the buffer. It the buffer is at capacity,
  The head of the buffer is **dropped** and moved to the next oldest entry
  and the new value is then inserted at the end of the buffer.

* 
  ``value()``:
  Accesses the contents of the circular buffer at *index*. Valid
  indices range from ``0`` to ``[size-1]``, where *size* is the number of valid
  entries in the buffer.  An attempt to retrieve a value for an out of
  bound index will throw a `geopm::Exception(3) <GEOPM_CXX_MAN_Exception.3.html>`_ with an
  ``error_value()`` of ``GEOPM_ERROR_INVALID``.

* 
  ``make_vector()``:
  Create a vector from the entire circular buffer contents.
  Or create a vector slice from the circular buffer contents,
  delimited by the *Start* index **(inclusive)** and *End* index **(exclusive)**
  such as ``[start, end)``. 
  If the range presented by these two indexes is invalid
  it will throw a `geopm::Exception(3) <GEOPM_CXX_MAN_Exception.3.html>`_

SEE ALSO
--------

`geopm(7) <geopm.7.html>`_\ ,
`geopm::Exception(3) <GEOPM_CXX_MAN_Exception.3.html>`_
