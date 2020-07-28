Accumulator Sensor
==================

.. seo::
    :description: Instructions for setting up sensors that Accumulates values.
    :image: sigma.png

The ``accumulator`` sensor is a helper sensor that can accumulate values from other sensors.
This can for example be useful to keep track of the total amount of consumed energy or water, even
over a power cycle or reboot.

The last reported value of this sensor is continuously stored on the device. After a reboot this value is added 
to value of the source sensor and reported as the value of the accumulator.


.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: accumulator
        name: "Total Energy"
        sensor: my_energy_meter

      # The sensor to accumulate, can be any sensor
      - platform: pulse_counter
        # ...
        total:
          id: my_energy_meter
          # ...

Configuration variables:
------------------------

- **sensor** (**Required**, :ref:`config-id`): The ID of the sensor to monitor.
- **name** (**Required**, string): The name of the accumulator sensor.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

- **reset_value** (*Optional*, float): If set, the stored value will be reset to this value when the device starts.

- **save_on_value_delta** (*Optional*, float): The maximum amount the value is allowed to change 
  before it is saved after at least ``save_min_interval``
- **save_min_interval** (*Optional*): The minimum time between two saves
- **save_max_interval** (*Optional*): The maximum time between saves

- All other options from :ref:`Sensor <config-sensor>`.

.. _sensor-accumulator-reset_action:


Throttle saving to flash
------------------------

To prevent the flash memory from wearing out too fast, the accumulator can be configured to limit
the amount of writes to the flash memory.

.. code-block:: yaml

    - platform: accumulator
      name: "Total Energy"
      sensor: my_energy_meter
      save_on_value_delta: 100
      save_min_interval: 30s
      save_max_interval: 20min


In the example above, the current value is saved to the flash memory when it has changed by at least 
100 since the last save AND at least 30 seconds have passed. It will also be saved at least every 
20 minutes (if changed).


``sensor.accumulator.reset`` Action
-----------------------------------

This :ref:`Action <config-action>` allows you to reset the value of the accumulator sensor
to zero. For example this can be used to reset the accumulator sensor to zero at midnight with
a time-based automation.

.. code-block:: yaml

    on_...:
      - sensor.accumulator.reset:  my_accumulator_sensor

See Also
--------

- :ref:`sensor-filters`
- :apiref:`accumulator/accumulator_sensor.h`
- :ghedit:`Edit`
