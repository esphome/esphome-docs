Modbus Controller Switch
========================

.. seo::
    :description: Instructions for setting up a modbus_controller device sensor.

The ``modbus_controller`` sensor platform creates a sensor from a modbus_controller component
and requires :doc:`/components/modbus_controller` to be configured.


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the sensor.
- **register_type** (**Required**): type of the modbus register.
- **address** (**Required**, int): start address of the first register in a range
- **offset** (*Optional*, int): not required in most cases
  offset from start address in bytes. If more than one register is read a modbus read registers command this value is used to find the start of this datapoint relative to start address. The component calculates the size of the range based on offset and size of the value type
  The value for offset depends on the register type. For holding input registers the offset is in bytes. For coil and discrete input resisters the LSB of the first data byte contains the coil addressed in the request. The other coils follow toward the high-order end of this byte and from low order to high order in subsequent bytes. For the registers  offset is the position of the relevant bit.
  To get the value of the coil register 2 can be retrieved using address: 2 / offset: 0 or address: 0 / offset 2
- **bitmask** (*Optional*, int): Some values are packed in a response. The bitmask is used to determined if the result is true or false.
- **skip_updates** (*Optional*, int): By default all sensors of a modbus_controller are updated together. For data points that don't change very frequently updates can be skipped. A value of 5 would only update this sensor range in every 5th update cycle
- **use_write_multiple** (*Optional*, boolean): By default the modbus command ``Force Single Coil`` (function code 5) is used to send state changes to the device. If your device only supports ``Force Multiple Coils`` (function code 15) set this option to true.
- **custom_command** (*Optional*, list of bytes): raw bytes for modbus command. This allows using non-standard commands. If ``custom_command`` is used ``address`` and ``register_type`` can't be used.
  custom data must contain all required bytes including the modbus device address. The crc is automatically calculated and appended to the command.
  See :ref:`modbus_custom_command` how to use ``custom_command``
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to read the status of the switch.
- **write_lambda** (*Optional*, :ref:`lambda <config-lambda>`): Lambda called before send.
  Lambda is evaluated before the modbus write command is created.

  Parameters passed into the lambda

  - **x** (float): The float value to be sent to the modbus device
  - **payload** (``std::vector<uint8_t>&payload``): empty vector for the payload. If payload is set in the lambda it is sent as a custom command and must include all required bytes for a modbus request
    *note:* because the response contains data for all registers in the same range you have to use ``data[item->offset]`` to get the first response byte for your sensor.
  - **item** (const pointer to a Switch derived object):  The sensor object itself.

  Possible return values for the lambda:

  - ``return <true / false>;`` the new value for the sensor.
  - ``return <anything>; and fill payload with data`` if the payload is added from the lambda then these bytes will be sent.
  - ``return {};`` in the case the lambda handles the sending of the value itself.

**Example**

.. code-block:: yaml

    switch:
      - platform: modbus_controller
        modbus_controller_id: epever
        id: enable_load_test
        register_type: coil
        address: 2
        name: "enable load test mode"
        write_lambda: |-
          ESP_LOGD("main","Modbus Switch incoming state = %f",x);
          // return false ; // use this to just change the value
          payload.push_back(0x1);  // device address
          payload.push_back(0x5);  // force single coil
          payload.push_back(0x00); // high byte address of the coil
          payload.push_back(0x6);  // low byte address of the coil
          payload.push_back(0xFF); // ON = 0xFF00 OFF=0000
          payload.push_back(0x00);
          return true;



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

For holding registers the write command will be write_single_register. Because the offset for holding registers is given in bytes and the size of a register is 16 bytes the start_address is calculated as ``start_address + offset/2``

.. code-block:: yaml

    switch:
    - platform: modbus_controller
      modbus_controller_id: ventilation_system
      name: "enable turn off"
      register_type: holding
      address: 25
      bitmask: 1
      entity_category: config
      icon: "mdi:toggle-switch"


See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/sensor/modbus_controller`
- :doc:`/components/binary_sensor/modbus_controller`
- :doc:`/components/text_sensor/modbus_controller`
- https://www.modbustools.com/modbus.html
- :ghedit:`Edit`
