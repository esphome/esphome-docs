Pulse Counter Sensor
====================

.. seo::
    :description: Instructions for setting up pulse counter sensors.
    :image: pulse.svg

The pulse counter sensor allows you to count the number of pulses and the frequency of a signal
on any pin.

On the ESP32, this sensor is even highly accurate because it's using the hardware `pulse counter
peripheral <https://esp-idf.readthedocs.io/en/latest/api-reference/peripherals/pcnt.html>`__
on the ESP32.

.. figure:: images/pulse-counter.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    sensor:
      - platform: pulse_counter
        pin: 12
        name: "Pulse Counter"

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`config-pin`): The pin to count pulses on.
- **name** (**Required**, string): The name of the sensor.
- **count_mode** (*Optional*): Configure how the counter should behave
  on a detected rising edge/falling edge.

  - **rising_edge** (*Optional*): What to do when a rising edge is
    detected. One of ``DISABLE``, ``INCREMENT`` and ``DECREMENT``.
    Defaults to ``INCREMENT``.
  - **falling_edge** (*Optional*): What to do when a falling edge is
    detected. One of ``DISABLE``, ``INCREMENT`` and ``DECREMENT``.
    Defaults to ``DISABLE``.

- **internal_filter** (*Optional*, :ref:`config-time`): If a pulse shorter than this
  time is detected, it’s discarded and no pulse is counted. Defaults to ``13us``. On the ESP32,
  this value can not be higher than ``13us``, for the ESP8266 you can use larger intervals too.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``15s``.
  See :ref:`sensor-default_filter`.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

Converting units
----------------

The sensor defaults to measuring its values using a unit of measurement
of “pulses/min”. You can change this by using :ref:`sensor-filters`.
For example, if you’re using the pulse counter with a photodiode to
count the light pulses on a power meter, you can do the following:

.. code:: yaml

    # Example configuration entry
    sensor:
      - platform: pulse_counter
        pin: 12
        unit_of_measurement: 'kW'
        name: 'Power Meter House'
        filters:
          - multiply: 0.06

See Also
--------

- :ref:`sensor-filters`
- :doc:`rotary_encoder`
- `esp-idf Pulse Counter API <https://esp-idf.readthedocs.io/en/latest/api-reference/peripherals/pcnt.html>`__.
- :doc:`API Reference </api/sensor/pulse_counter>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/pulse_counter.rst>`__

.. disqus::
