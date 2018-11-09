Total Daily Energy Sensor
=========================

The ``total_daily_energy`` sensor is a helper sensor that can use the energy value of
other sensors like the :doc:`HLW8012 <hlw8012>`, :doc:`CSE7766 <cse776>`, etc and integrate
it over time.

So this component allows you to convert readings in ``W`` or ``kW`` to readings of the total
daily energy usage in ``Wh`` or ``kWh``.

.. figure:: images/total-daily-energy-ui.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    sensor:
      - platform: total_daily_energy
        pin: 12
        name: "Pulse Counter"
        power_id: my_power

      # The power sensor to convert, can be any power sensor
      - platform: hlw8012
        # ...
        power:
          id: my_power

    # Enable time component to reset energy at midnight
    time:
      - platform: sntp
        id: my_time

Configuration variables:
------------------------

- **power_id** (**Required**, :ref:`config-id`): The ID of the power sensor
  to integrate over time.
- **name** (**Required**, string): The name of the sensor.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

Converting from W to kW
-----------------------

Some sensors such as the :doc:`HLW8012 <hlw8012>` expose their power sensor with a unit of measurement of
``W``. To have your readings in ``kW``, use a filter:

.. code::

    sensor:
      # The power sensor to convert, can be any power sensor
      - platform: hlw8012
        # ...
        power:
          id: my_power
          filters:
            # Multiplication factor from W to kW is 0.001
            - multiply: 0.001
          unit_of_measurement: kW

See Also
--------

- :ref:`sensor-filters`
- :doc:`rotary_encoder`
- `esp-idf Pulse Counter API <https://esp-idf.readthedocs.io/en/latest/api-reference/peripherals/pcnt.html>`__.
- :doc:`API Reference </api/sensor/pulse_counter>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/pulse_counter.rst>`__

.. disqus::
