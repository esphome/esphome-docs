Uptime Sensor
=============

.. seo::
    :description: Instructions for setting up a sensor that tracks the uptime of the ESP.
    :image: timer.svg

The ``uptime`` sensor allows you to track the time the ESP has stayed up for in seconds.
Time rollovers are automatically handled.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: uptime
        name: Uptime Sensor

Configuration variables:
------------------------

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``60s``.

- **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
- All other options from :ref:`Sensor <config-sensor>`.


See Also
--------

- :ref:`sensor-filters`
- :apiref:`uptime/uptime_sensor.h`
- :ghedit:`Edit`
