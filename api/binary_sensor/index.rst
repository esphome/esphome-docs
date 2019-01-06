Binary Sensor
=============

.. cpp:namespace:: binary_sensor

In esphomelib, every component that exposes a binary state, is a :cpp:class:`BinarySensor`.

To create your own binary sensor, simply subclass :cpp:class:`BinarySensor` and call
:cpp:func:`BinarySensor::publish_state` to tell the frontend that you have a new state.
Inversion is automatically done for you when publishing state and can be changed by the
user with :cpp:func:`BinarySensor::set_inverted`.

Supported Binary Sensors
------------------------

.. toctree::
    :glob:

    *

Example Usage
-------------

.. code-block:: cpp

    // Basic
    App.register_binary_sensor(custom_binary_sensor);
    // GPIO Binary Sensor
    App.make_gpio_binary_sensor("Window Open", 36);


.. cpp:namespace:: nullptr

See :cpp:func:`Application::register_binary_sensor` and :cpp:func:`Application::make_gpio_binary_sensor`.

API Reference
-------------

.. cpp:namespace:: nullptr

BinarySensor
************

.. doxygenclass:: binary_sensor::BinarySensor
    :members:
    :protected-members:
    :undoc-members:

MQTTBinarySensorComponent
*************************

.. doxygenclass:: binary_sensor::MQTTBinarySensorComponent
    :members:
    :protected-members:
    :undoc-members:

Filters
*******

.. doxygenclass:: binary_sensor::Filter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::DelayedOnFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::DelayedOffFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::HeartbeatFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::InvertFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::LambdaFilter
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::UniqueFilter
    :members:
    :protected-members:
    :undoc-members:

Triggers
********

.. doxygenclass:: binary_sensor::PressTrigger
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::ReleaseTrigger
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::ClickTrigger
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::DoubleClickTrigger
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::MultiClickTrigger
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::BinarySensorCondition
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: binary_sensor::CustomBinarySensorConstructor
    :members:
    :protected-members:
    :undoc-members:
