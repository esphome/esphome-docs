Free Heap Sensor
================

.. seo::
    :description: Instructions for setting up a sensor that tracks the free heap memory of the MCU.
    :image: memory.svg

The ``heapmon`` sensor allows you to track the free heap memory space of the MCU.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: heapmon
        name: Free Heap

Configuration variables:
------------------------

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``60s``.

- **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
- All other options from :ref:`Sensor <config-sensor>`.


See Also
--------

- :ref:`sensor-filters`
- :ghedit:`Edit`
