Pulse Meter Sensor
==================

.. seo::
    :description: Instructions for setting up pulse meter sensors.
    :image: pulse.svg

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

- **internal_filter_mode** (*Optional*, string): Determines how the internal filter is applied.
  One of ``EDGE`` and ``PULSE``. Defaults to ``EDGE``. In ``EDGE`` mode subsequent rising edges are compared and if they fall into an interval lesser than the internal filter value, the last one is discarded. In ``PULSE`` mode the rising edge is discarded if any further interrupts are detected before the internal_filter time has passed. In other words, a high pulse must be at least internal_filter long to be counted. This is useful if you are detecting long pulses that may bounces before and/or after the main pulse.

- **timeout** (*Optional*, :ref:`config-time`): If we don't see a pulse for this length of time, we assume 0 pulses/min. Defaults to ``5 min``.
- **total** (*Optional*, :ref:`config-id`): An additional sensor that outputs the total number of pulses counted.
- **fade** (*Optional*, boolean): If ``true``, the sensor will output fake pulses to fade towards zero when no pulses are detected. Defaults to ``false``.
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
          accuracy_decimals: 3
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

Fading to zero
--------------

When the fade option is enabled, the pulse meter will generate fading simulated values in cases where the sensor doesn't detect any pulses.
Use this feature when you need to trigger automations when something turning off, as it ensures events are triggered even when pulses stop.

With the fade option turned on, the sensor gradually generates simulated values that fade toward zero.
These simulated values fire when the time since the last detected pulse is double the last reported pulse width value.

Enabling the fade option introduces a slight change in understanding the sensor's behavior.
When a simulated pulse occurs, it indicates that no real pulse has been detected for at least double the currently reported pulse width.
Consequently, the true value will consistently be the same as or lower than the simulated value.
To show this consider the following two cases:
If a real pulse coincided with the generation of the simulated value, it will result in the same output value.
If a real pulse occurred after the simulated value it will always produce a lower value than the simulated output.

When using the fade option do not integrate the sensor's output.
Doing so will result in an overestimation of the total due to the simulated values.
Instead, rely on the total sensor output to accurately count the pulses.
The total count remains unaffected by the fade option.

See Also
--------

- :ref:`sensor-filters`
- :doc:`/components/sensor/pulse_counter`
- :apiref:`pulse_meter/pulse_meter_sensor.h`
- :ghedit:`Edit`
