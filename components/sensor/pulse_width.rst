Pulse Width Sensor
==================

.. seo::
    :description: Instructions for setting up pulse width sensors in ESPHome
    :image: pulse.svg

The ``pulse_width`` sensor allows you to measure how long a given digital signal
is HIGH. For example this can be used to measure PWM signals to transmit some
value over a simple protocol.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: pulse_width
        pin: D0
        name: Pulse Width Sensor

Configuration variables:
------------------------

- **pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The pin to observe for the
  pulse width.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor.
  Defaults to ``60s``.

- **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
- All other options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :ref:`sensor-filters`
- :ghsources:`esphome/components/pulse_width`
- :ghedit:`Edit`
