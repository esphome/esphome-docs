Sensor
======

The `sensor` namespace contains all sensors.

.. cpp:namespace:: nullptr

See :cpp:func:`Application::register_sensor`.

.. toctree::
    :glob:

    *


API Reference
-------------

.. cpp:namespace:: nullptr

Sensor
******

.. doxygenclass:: sensor::Sensor
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::PollingSensorComponent
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::EmptySensor
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::EmptyPollingParentSensor
    :members:
    :protected-members:
    :undoc-members:

.. doxygenvariable:: sensor::ICON_EMPTY
.. doxygenvariable:: sensor::ICON_WATER_PERCENT
.. doxygenvariable:: sensor::ICON_GAUGE
.. doxygenvariable:: sensor::ICON_FLASH
.. doxygenvariable:: sensor::ICON_SCREEN_ROTATION
.. doxygenvariable:: sensor::ICON_BRIEFCASE_DOWNLOAD

.. doxygenvariable:: sensor::UNIT_C
.. doxygenvariable:: sensor::UNIT_PERCENT
.. doxygenvariable:: sensor::UNIT_HPA
.. doxygenvariable:: sensor::UNIT_V
.. doxygenvariable:: sensor::UNIT_DEGREES_PER_SECOND
.. doxygenvariable:: sensor::UNIT_M_PER_S_SQUARED


Filter
******

.. doxygenclass:: sensor::Filter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::SlidingWindowMovingAverageFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::ExponentialMovingAverageFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygentypedef:: sensor::lambda_filter_t

.. doxygenclass:: sensor::LambdaFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::OffsetFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::MultiplyFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::FilterOutValueFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::FilterOutNANFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::ThrottleFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::HeartbeatFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::DebounceFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::DeltaFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::OrFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::UniqueFilter
    :members:
    :protected-members:
    :undoc-members:

MQTTSensorComponent
*******************

.. doxygenclass:: sensor::MQTTSensorComponent
    :members:
    :protected-members:
    :undoc-members:
