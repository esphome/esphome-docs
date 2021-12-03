Modbus Switch
=============

.. seo::
    :description: Instructions for setting up a modbus_controller device sensor.
    :image: modbus_controller.png

The ``modbus_controller`` sensor platform creates a sensor from a modbus_controller component
and requires :doc:`/components/modbus_controller` to be configured.


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the sensor.
- **modbus_functioncode** (**Required**): type of the modbus register.
- **address**: (**Required**, int): start address of the first register in a range
- **offset**: (*Optional*, int): not required in most cases
  offset from start address in bytes. If more than one register is read a modbus read registers command this value is used to find the start of this datapoint relative to start address. The component calculates the size of the range based on offset and size of the value type
  The value for offset depends on the register type. For holding input registers the offset is in bytes. For coil and discrete input resisters the LSB of the first data byte contains the coil addressed in the request. The other coils follow toward the high-order end of this byte and from low order to high order in subsequent bytes. For the registers  offset is the position of the relevant bit.
  To get the value of the coil register 2 can be retrived using address: 2 / offset: 0 or address: 0 / offset 2
- **bitmask** : some values are packed in a response. The bitmask is used to determined if the result is true or false
- **skip_updates**: (*Optional*, int): By default all sensors of of a modbus_controller are updated together. For data points that don't change very frequently updates can be skipped. A value of 5 would only update this sensor range in every 5th update cycle


**Example**

.. code-block:: yaml

    switch:
    - platform: modbus_controller
        modbus_controller_id: epever
        id: enable_load_test
        register_type: coil
        address: 2
        name: "enable load test mode"
        bitmask: 1

Since offset is not zero the read command is part of a range and will be parsed when the range is updated.
The write command to be constructed uses the function code to determine the write command. For a coil it is write single coil.
Because the write command only touches one register start_address and offset have to be corrected.
The final command will be write_single_coil address 5 (start_address+offset) value 1 or 0

For holding registers the write command will be write_single_register. Because the offset for holding registers is given in bytes and the size of a register is 16 bytes the start_address is calculated as start_address + offset/2

See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/sensor/modbus_controller`
- :doc:`/components/binary_sensor/modbus_controller`
- :doc:`/components/text_sensor/modbus_controller`
- https://www.modbustools.com/modbus.html
- :ghedit:`Edit`
