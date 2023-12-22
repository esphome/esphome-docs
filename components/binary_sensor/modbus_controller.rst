Modbus Controller Binary Sensor
===============================

.. seo::
    :description: Instructions for setting up a modbus_controller device binary sensor.
    :image: modbus.png

The ``modbus_controller`` binary sensor platform creates a binary sensor from a modbus_controller component
and requires :doc:`/components/modbus_controller` to be configured.


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the sensor.
- **register_type** (**Required**): type of the modbus register.

    - ``coil``: Read Coils - Reads the ON/OFF status of discrete coils in the device with *Function Code 1 (01hex)*.
    - ``discrete_input``: Reads the ON/OFF status of discrete inputs in the device with *Function 02(02hex)*.
    - ``holding``: Read Holding Registers - Read the binary contents of holding registers in the device with *Function 03 (03hex)*.
    - ``read``: Read Input Registers - Read the binary contents of input registers in the device with *Function 04 (04hex)*

- **address** (**Required**, int): start address of the first register in a range (can be decimal or hexadecimal).
- **bitmask** (*Optional*, int): sometimes multiple values are packed in a single register's response. The bitmask is used to determined if the result is true or false. See :ref:`bitmasks`.
- **skip_updates** (*Optional*, int): By default all sensors of a modbus_controller are updated together. For data points that don't change very frequently updates can be skipped. A value of 5 would only update this sensor range in every 5th update cycle. Note: The modbus_controller groups components by address ranges to reduce number of transactions. All components with the starting same address will be updated in one request. ``skip_updates`` applies for *all* components in the same range.
- **register_count** (*Optional*, int): Number of consecutive registers  this data point spans or to skip in a single read command. Default is 1. See :ref:`modbus_register_count` for more details.
- **response_size** (*Optional*, int): Size of the response for the register in bytes. Defaults to register_count*2.
- **force_new_range** (*Optional*, boolean): If possible sensors with sequential addresses are grouped together and requested in one range. Setting ``force_new_range: true`` enforces the start of a new range at that address.
- **custom_command** (*Optional*, list of bytes): raw bytes for modbus command. This allows using non-standard commands. If ``custom_command`` is used ``address`` and ``register_type`` can't be used.
  custom data must contain all required bytes including the modbus device address. The crc is automatically calculated and appended to the command.
  See :ref:`modbus_custom_command` how to use ``custom_command``.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the new value of the sensor. Parameters:

  - **x** (bool): The parsed float value of the modbus data
  - **data** (std::vector<uint8_t): vector containing the complete raw modbus response bytes for this sensor
  - **item** (const pointer to a ModbusBinarySensor object):  The sensor object itself.

  Possible return values for the lambda:

  - ``return true/false;`` the new value for the sensor.


 - **offset** (*Optional*, int): Offset from start address in bytes (only required for uncommon response encodings). If more than one register is written in a command this value is used to find the start of this datapoint relative to start address. The component calculates the size of the range based on offset and size of the value type. The value for offset depends on the register type. If a binary_sensor is created from an input register the offset is in bytes. For coil and discrete input resisters the LSB of the first data byte contains the coil addressed in the request. The other coils follow toward the high-order end of this byte and from low order to high order in subsequent bytes. For the registers  offset is the position of the relevant bit. To get the value of the coil register 2 can be retrieved using address: 2 / offset: 0 or address: 0 / offset 2

- All other options from :ref:`Binary Sensor <config-binary_sensor>`.

Example:
--------

.. code-block:: yaml

    binary_sensor:
    - platform: modbus_controller
      modbus_controller_id: modbus1
      name: "Error status"
      register_type: read
      address: 0x3200
      bitmask: 0x80 #(bit 8)


See Also
--------
- :doc:`/components/modbus`
- :doc:`/components/modbus_controller`
- :doc:`/components/sensor/modbus_controller`
- :doc:`/components/output/modbus_controller`
- :doc:`/components/switch/modbus_controller`
- :doc:`/components/number/modbus_controller`
- :doc:`/components/select/modbus_controller`
- :doc:`/components/text_sensor/modbus_controller`
- https://www.modbustools.com/modbus.html
- :apiclass:`:modbus_controller::ModbusBinarySensor`
- :ghedit:`Edit`
