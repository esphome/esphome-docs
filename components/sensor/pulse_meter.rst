Pulse Meter Sensor
==================

.. seo::
    :description: Instructions for setting up pulse meter sensors.
    :image: pulse.png

The pulse meter sensor allows you to count the number and frequency of pulses on any pin. It is intended to be a drop-in replacement
for :doc:`integration sensor </components/sensor/pulse_counter>`, but offering better resolution.
It measures the time between rising edges on a pin, for each pulse it outputs the frequency in pulses/min.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: pulse_meter
        pin: 12
        name: "Pulse Meter"

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`config-pin`): The pin to count pulses on.
- **name** (**Required**, string): The name of the sensor.

- **internal_filter** (*Optional*, :ref:`config-time`): If a pulse shorter than this
  time is detected, it’s discarded and no pulse is counted. Defaults to ``13us``. For S0 pulse meters that are used to meter power consumption 50-100 ms is a reasonable value.

- **timeout** (*Optional*, :ref:`config-time`): If we don't see a pulse for this length of time, we assume 0 pulses/sec. Defaults to ``5 min``.
- **total** (*Optional*, :ref:`Sensor <config-sensor>`): An additional sensor that outputs the total number of pulses counted.
- All other options from :ref:`Sensor <config-sensor>`.

Converting units
----------------

The sensor defaults to units of “pulses/min”. You can change this by using :ref:`sensor-filters`.
For example, if you’re using the pulse meter with a photodiode to
count the light pulses on a power meter that outputs 1000 pulses per kWh,
you can use the following to output instantaneous usage in kW:

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: pulse_meter
        pin: 12
        unit_of_measurement: 'kW'
        name: 'Electricity Usage'
        filters:
          - multiply: 0.06

Counting total pulses
---------------------

When the total sensor is configured, pulse_meter also reports the total
number of pulses measured. When used on a power meter, this can be used to
measure the total consumed energy in kWh.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: pulse_meter
        pin: 12
        unit_of_measurement: 'kW'
        name: 'Electricity Usage'
        internal_filter: 100ms
        accuracy_decimals: 3
        filters:
          - multiply: 0.06
        total:
          name: "Electricity Total"
          unit_of_measurement: "kWh"
          accuracy_decimals: 5
          filters:
            - multiply: 0.001

(Re)Setting the total pulse count
---------------------------------

Using this action, you are able to reset/set the total pulse count. This can be useful
if you would like the ``total`` sensor to match what you see on your meter you are
trying to match.

.. code-block:: yaml

    on_...:
      then:
        - pulse_meter.set_total_pulses:
            id: pulse_meter_id
            value: 12345

.. note::

    This value is the raw count of pulses, and not the value you see after the filters
    are applied.


See Also
--------

- :ref:`sensor-filters`
- :doc:`/components/sensor/pulse_counter`
- :apiref:`pulse_meter/pulse_meter_sensor.h`
- :ghedit:`Edit`
