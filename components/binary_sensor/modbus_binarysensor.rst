Modbus Binary Sensor
====================

.. seo::
    :description: Instructions for setting up a modebus_controller device binary sensor.
    :image: modbus.png

The ``modbus_controller`` binary sensor platform creates a binary sensor from a modbus_controller component
and requires :doc:`/components/modbus_controller` to be configured.


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the sensor.
- **modbus_functioncode** (**Required**): type of the modbus register.
    - "read_coils": Function 01 (01hex) Read Coils - Reads the ON/OFF status of discrete coils in the device.
    - "read_discrete_inputs": Function 02(02hex) - Reads the ON/OFF status of discrete inputs in the device.
    - "read_holding_registers": Function 03 (03hex) Read Holding Registers - Read the binary contents of holding registers in the device.
    - "read_input_registers": Function 04 (04hex) Read Input Registers - Read the binary contents of input registers in the device.

- **address**: (**Required**, integer): start address of the first register in a range
- **offset**: (**Optional**, integer): offset from start address in bytes. If more than one register is read a modbus read registers command this value is used to find the start of this datapoint relative to start address. The component calculates the size of the range based on offset and size of the value type
  The value for offset depends on the register type. If a binary_sensor is created from an input register the offset is in bytes. For coil and discrete input resisters the LSB of the first data byte contains the coil addressed in the request. The other coils follow toward the high-order end of this byte and from low order to high order in subsequent bytes. For the registers  offset is the position of the relevant bit.
  To get the value of the coil register 2 can be retrived using address: 2 / offset: 0 or address: 0 / offset 2 
- **bitmask** : some values are packed in a response. The bitmask is used to determined if the result is true or false
- **skip_updates**: (**Optional**, integer): By default all sensors of of a modbus_controller are updated together. For data points that don't change very frequently updates can be skipped. A value of 5 would only update this sensor range in every 5th update cycle


See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/sensor/modbus_sensor`
- :doc:`/components/text_sensor/modbus_textsensor`
- :doc:`/components/switch/modbus_switch`
- https://www.modbustools.com/modbus.html
- :ghedit:`Edit`
