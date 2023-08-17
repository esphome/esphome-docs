Mitsubishi Climate
==================

.. seo::
    :description: Instructions for setting up Mitsubishi Heat Pump Devices
    :image: air-conditioner.svg

The ``climate_mitsubishi`` climate platform interfaces with Mitsubishi mini-split heat pump units equipped with the RedLINK
communication interface(also known as CN105).

.. code-block:: yaml

    # Sample configuration entry
    uart:
      tx_pin: 1
      rx_pin: 3
      baud_rate: 2400 #9600 on some units
      parity: EVEN
      id: uart_0
    climate:
      - platform: climate_mitsubishi
        uart_id: uart_0
        name: Heat Pump
        compressor_frequency:
          name: Compressor Frequency
        fan_velocity:
          name: Fan Velocity
        conflicted:
          name: Conflict
        preheat:
          name: Preheat
        inject_enable:
          name: Inject Enable
        control_temperature:
          name: Control Temperature
        remote_temperature:
          name: Remote Temperature
        temperature_offset:
          name: Temperature Offset
        vertical_airflow:
          name: Vertical Airflow

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **uart_id** (*Optional*, :ref:`config-id`): ID of the UART port to communicate with the HP.
- **name** (*Optional*, string): The name of the climate device.
- **compressor_frequency** (*Optional*): Reported VFD frequency of the compressor in the outdoor unit.
  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional* , :ref: `config-id`): ID of the sensor, can be used for code generation
- **fan_velocity** (*Optional*): Reported fan speed of the indoor unit.
  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional* , :ref: `config-id`): ID of the sensor, can be used for code generation
- **conflicted** (*Optional*): Binary sensor that indicates when the indoor unit is waiting for the outdoor unit to switch to the direction of the system to the direction that the indoor unit is calling for.
  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional* , :ref: `config-id`): ID of the sensor, can be used for code generation
- **preheat** (*Optional*): Binary sensor that indicates when the unit is waiting for the indoor coils to heat up to resume heating operation.
  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional* , :ref: `config-id`): ID of the sensor, can be used for code generation
- **inject_enable** (*Optional*): Switch that enables the injection of external temperatures into the unit(via remote_temperature).
  - **name** (**Required**, string): The name of the switch.
  - **id** (*Optional* , :ref: `config-id`): ID of the switch, can be used for code generation
- **remote_temperature** (*Optional*): Number that is used to set a remote room temperature for the unit(see inject_enable).
  - **name** (**Required**, string): The name of the number.
  - **id** (*Optional* , :ref: `config-id`): ID of the number, can be used for code generation
- **temperature_offset** (*Optional*): Number that sets the offset applied before the remote temperature is sent into the unit.
  - **name** (**Required**, string): The name of the number.
  - **id** (*Optional* , :ref: `config-id`): ID of the number, can be used for code generation
- **control_temperature** (*Optional*): Sensor that reports the room temperature as reported by the unit(useful when using temperature injection with an offset).
  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional* , :ref: `config-id`): ID of the sensor, can be used for code generation
- **vertical_airflow** (*Optional*): Select that sets the vertical airflow direction(vertical vane).
  - **name** (**Required**, string): The name of the select.
  - **id** (*Optional* , :ref: `config-id`): ID of the select, can be used for code generation

See Also
--------

- :doc:`/components/climate/index`
- `HeatPump <https://github.com/SwiCago/HeatPump>`__
