Modbus Controller Output
========================

.. seo::
    :description: Instructions for setting up a modbus_controller device sensor.

The ``modbus_controller`` platform creates a output from a modbus_controller.

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the sensor.
- **address**: (**Required**, int): start address of the first register in a range
- **value_type**: (**Required**): datatype of the mod_bus register data. The default data type for modbus is a 16 bit integer in big endian format (MSB first)
    - U_WORD (unsigned 16 bit integer from 1 register = 16bit)
    - S_WORD (signed 16 bit integer from 1 register = 16bit)
    - U_DWORD (unsigned 32 bit integer from 2 registers = 32bit)
    - S_DWORD (signed 32 bit integer from 2 registers = 32bit)
    - U_DWORD_R (unsigned 32 bit integer from 2 registers low word first)
    - S_DWORD_R (signed 32 bit integer from 2 registers low word first)
    - U_QWORD (unsigned 64 bit integer from 4 registers = 64bit)
    - S_QWORD (unsigned 64 bit integer from 4 registers = 64bit)
    - U_QWORD_R (unsigned 64 bit integer from 4 registers low word first)
    - U_QWORD_R signed 64 bit integer from 4 registers low word first)
    - FP32 (32 bit IEEE 754 floating point from 2 registers)
    - FP32_R (32 bit IEEE 754 floating point - same as FP32 but low word first)
- **register_count**: (*Optional*): only required for uncommon response encodings
  The number of registers this data point spans. Default is 1
- **write_lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda is evaluated before the modbus write command is created. The value is passed in as ``float x`` and an empty vector is passed in as ``std::vector<uint16_t>&payload``.
  You can directly define the payload by adding data to payload then the return value is ignored and the content of payload is used.
- **register_type** (*Optional*): ``coil`` to create a binary outout or ``holding`` to create a float output.
- **multiply** (*Optional*, float): multiply the new value with this factor before sending the requests. Ignored if lambda is defined. Only valid for ``register_type: holding``.
- **offset**: (*Optional*, int): only required for uncommon response encodings
    offset from start address in bytes. If more than one register is read a modbus read registers command this value is used to find the start of this datapoint relative to start address. The component calculates the size of the range based on offset and size of the value type
- **use_write_multiple**: (*Optional*, boolean): By default the modbus command ``Preset Single Registers`` (function code 6) is used for setting the holding register if only 1 register is set. If your device only supports ``Preset Multiple Registers`` (function code 16) set this option to true.

All other options from :ref:`Output <config-output>`.


**Parameters passed into the lambda**

- **x** (float): The float value to be sent to the modbus device for ``register_type: holding``
- **x** (bool): The boolean value to be sent to the modbus device for ``register_type: coil``

- **payload** (`std::vector<uint16_t>&payload`): 

  - for ``register_type: holding``: empty vector for the payload. The lamdba can add 16 bit raw modbus register words.
  - for ``register_type: coil``: empty vector for the payload. If payload is set in the lambda it is sent as a custom command and must include all required bytes for a modbus request
    note: because the response contains data for all registers in the same range you have to use ``data[item->offset]`` to get the first response byte for your sensor.

- **item** (const pointer to a SensorItem derived object):  The sensor object itself.

Possible return values for the lambda:

 - ``return <FLOATING_POINT_NUMBER / BOOL>;`` the new value for the sensor.
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
- :doc:`/components/sensor/modbus_controller`
- :doc:`/components/binary_sensor/modbus_controller`
- :doc:`/components/switch/modbus_controller`
- :doc:`/components/text_sensor/modbus_controller`
- :doc:`/components/number/modbus_controller`
- https://www.modbustools.com/modbus.html
- :ghedit:`Edit`
