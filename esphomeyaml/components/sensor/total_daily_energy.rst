Total Daily Energy Sensor
=========================

.. seo::
    :description: Instructions for setting up sensors that track the total daily energy usage per day and accumulate the power usage.
    :image: sigma.png

The ``total_daily_energy`` sensor is a helper sensor that can use the energy value of
other sensors like the :doc:`HLW8012 <hlw8012>`, :doc:`CSE7766 <cse7766>`, etc and integrate
it over time.

So this component allows you to convert readings in ``W`` or ``kW`` to readings of the total
daily energy usage in ``Wh`` or ``kWh``.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: total_daily_energy
        pin: 12
        name: "Total Daily Energy"
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
- :doc:`hlw8012`
- :doc:`cse7766`
- :doc:`/esphomeyaml/cookbook/power_meter`
- :doc:`API Reference </api/sensor/total_daily_energy>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/total_daily_energy.rst>`__

.. disqus::
