Pulse Meter Sensor
==================

.. seo::
    :description: Instructions for setting up pulse meter sensors.
    :image: pulse.svg

The pulse meter sensor allows you to count the number and frequency of pulses on any pin. It is intended to be a drop-in replacement
for :doc:`integration sensor </components/sensor/pulse_counter>`.
It measures the time between rising edges on a pin, for each pulse it outputs the frequency in pulses/min, as opposed to the pulse counter sensor which outputs the number of pulses in a time interval.

This leads to a higher resolution, especially for low pulse rates, as the pulse counter sensor is limited by the number of pulses within a time interval. The difference between 1 pulse/min and 2 pulse/min is much higher than 2000 pulses/min and 2001 pulses/min. The pulse_meter is only limited by its accuracy to measure the time between pulses, which leads to an inverse relationship between pulse rate and accuracy. The lower the pulse rate, the higher the accuracy. Lower accuracy with very high pulse rates is less likely to be a problem, as the ESP32 can measure time intervals with a resolution of 1us.

Here's a comparison of the two sensors; both are set to an update interval of 10 seconds (using the ``update_interval`` and the ``throttle_average`` option respectively):

.. figure:: /images/pulse-counter_vs_pulse-meter.png
    :align: center
    :width: 50.0%

Example code:

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
  time is detected, it’s discarded and no pulse is counted. Defaults to ``13us``. 
  
  The minimum pulse width threshold is determined by considering the upper limit of the *load* the meter is designed to handle, as well as the meter's *impulse constant* (``x pulses / kWh``). Here's the calculation involved:

  **Load Limit in Watts**: Establish the *upper load limit* that the meter is designed to measure. For example, if the limit is 16 kW (16,000 Watts), this becomes a reference point.

  **Pulse Rate Calculation**: Determine the pulse rate corresponding to this load limit. For this we need to know the impulse constant. In our example, the power meter has an impulse constant of ``10000 Pulses / kWh``. Dividing both sides by 60s gives us ``166.67 Pulses/s = 60 kWs``. This means that 60 kW corresponds to 1,000 impulses per 6 seconds, or 166.67 impulses per second. Scaling this down to 16 kW, we get 16 kW = 444.44  impulses per second (or 400 pulses per 9 seconds). This is the upper bound of the pulse rate we expect to see.

  **Minimum Pulse Width Calculation**: Use the pulse rate to calculate the minimum pulse width threshold. Employ the formula: ``Minimum Pulse Width (seconds) = Time Period / Number of Pulses``. In our example, with a time period of 9 seconds and 400 pulses, the minimum pulse width is approximately 22.5 milliseconds. This means you don't want to increase the internal filter time above 22.5ms, or you will start to miss pulses within the expected load range.

- **internal_filter_mode** (*Optional*, string): Determines how the internal filter is applied.
  One of ``EDGE`` and ``PULSE``. Defaults to ``EDGE``. In ``EDGE`` mode subsequent rising edges are compared and if they fall into an interval lesser than the internal filter value, the last one is discarded. In ``PULSE`` mode the rising edge is discarded if any further interrupts are detected before the internal_filter time has passed. In other words, a high pulse must be at least internal_filter long to be counted. This is useful if you are detecting long pulses that may bounces before and/or after the main pulse.  

- **timeout** (*Optional*, :ref:`config-time`): If we don't see a pulse for this length of time, we assume 0 pulses/sec. Defaults to ``5 min``.
- **total** (*Optional*, :ref:`config-id`): An additional sensor that outputs the total number of pulses counted.
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


See Also
--------

- :ref:`sensor-filters`
- :doc:`/components/sensor/pulse_counter`
- :doc:`/components/sensor/total_daily_energy`
- :doc:`/cookbook/power_meter`
- :apiref:`pulse_meter/pulse_meter_sensor.h`
- :ghedit:`Edit`
