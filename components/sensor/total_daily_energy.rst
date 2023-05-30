Total Daily Energy Sensor
=========================

.. seo::
    :description: Instructions for setting up sensors that track the total daily energy usage per day and accumulate the power usage.
    :image: sigma.svg

The ``total_daily_energy`` sensor is a helper sensor that can use the power value of
other sensors like the :doc:`HLW8012 <hlw8012>`, :doc:`CSE7766 <cse7766>`, :doc:`ATM90E32 <atm90e32>`, etc and integrate
it over time.

So this component allows you to convert readings in ``W`` or ``kW`` to readings of the total
daily energy usage in ``Wh`` or ``kWh``.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: total_daily_energy
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
- **restore** (*Optional*, boolean): Whether to store the intermediate result on the device so
  that the value can be restored upon power cycle or reboot.
  Defaults to ``true``.
- **method** (*Optional*, string): The method to use for calculating the total daily energy. One of
  ``trapezoid``, ``left`` or ``right``. Defaults to ``right``.
- All other options from :ref:`Sensor <config-sensor>`.

Converting from W to kW
-----------------------

Some sensors such as the :doc:`HLW8012 <hlw8012>` expose their power sensor with a unit of measurement of
``W``. To have your readings in ``kW``, use a filter:

.. code-block:: yaml

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
- :doc:`/cookbook/power_meter`
- :apiref:`total_daily_energy/total_daily_energy.h`
- :ghedit:`Edit`
