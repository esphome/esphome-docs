Modbus Controller Output
========================

.. seo::
    :description: Instructions for setting up a modbus_controller device sensor.
    :image: modbus_controller.png

The ``modbus_controller`` platform creates a output from a modbus_controller.

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the sensor.
- **address**: (**Required**, int): start address of the first register in a range
- **value_type**: (**Required**): datatype of the mod_bus register data. The default data type for modbus is a 16 bit integer in big endian format (MSB first)
    - U_WORD (unsigned float from 1 register =16bit
    - S_WORD (signed float from one register)
    - U_DWORD (unsigned float from 2 registers = 32bit)
    - S_DWORD (unsigned float from 2 registers = 32bit)
    - U_DWORD_R (unsigend float from 2 registers low word first )
    - S_DWORD_R (sigend float from 2 registers low word first )
    - U_QWORD (unsigned float from 4 registers = 64bit
    - S_QWORD (signed float from 4 registers = 64bit
    - U_QWORD_R (unsigend float from 4 registers low word first )
    - S_QWORD_R (sigend float from 4 registers low word first )
- **register_count**: (*Optional*): only required for uncommon response encodings
  The number of registers this data point spans. Default is 1
- **write_lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda is evaluated before the modbus write command is created. The value is passed in as `float x` and an empty vector is passed in as `std::vector<uint16_t>&payload`
  You can directly define the payload by adding data to payload then the return value is ignored and the content of payload is used.
- **multiply** (*Optional*, float): multiply the new value with this factor before sending the requests. Ignored if lambda is defined.
- **offset**: (*Optional*, int): only required for uncommon response encodings
    offset from start address in bytes. If more than one register is read a modbus read registers command this value is used to find the start of this datapoint relative to start address. The component calculates the size of the range based on offset and size of the value type

All other options from :ref:`Output <config-output>`.


**Parameters passed into the lambda**

- **x** (float): The float value to be sent to the modbus device

- **payload** (`std::vector<uint16_t>&payload`): empty vector for the payload. The lamdba can add 16 bit raw modbus register words.
      note: because the response contains data for all registers in the same range you have to use `data[item->offset]` to get the first response byte for your sensor.
- **item** (const pointer to a SensorItem derived object):  The sensor object itself.

Possible return values for the lambda:

 - ``return <FLOATING_POINT_NUMBER>;`` the new value for the sensor.
 - ``return <anything>; and fill payload with data`` if the payload is added from the lambda then these 16 bit words will be sent
 - ``return {};`` if you don't want write the command to the device (or do it from the lambda).


**Example**

.. code-block:: yaml

    output:
        - platform: modbus_controller
            modbus_controller_id: epever
            id: battery_capacity_output
            lambda: |-
              ESP_LOGD("main","Modbus Output incoming value = %f",x);
              uint16_t b_capacity = x ;
              payload.push_back(b_capacity);
              return x * 1.0 ;
            address: 0x9001
            value_type: U_WORD




See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/sensor/modbus_sensor`
- :doc:`/components/binary_sensor/modbus_binarysensor`
- :doc:`/components/switch/modbus_switch`
- :doc:`/components/text_sensor/modbus_textsensor`
- :doc:`/components/number/modbus_number`
- https://www.modbustools.com/modbus.html
- :ghedit:`Edit`
