Modbus Sensor
=============

.. seo::
    :description: Instructions for setting up a modebus_controller device sensor.
    :image: modbus.png

The ``modbus_controller`` sensor platform creates a sensor from a modbus_controller component
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
    - "write_single_coil": Function 05 (05hex) Write Single Coil - Writes a single coil to either ON or OFF.
    - "write_single_register": Function 06 (06hex) Write Single Register - Writes a value into a single holding register.
    - "write_multiple_coils": Function 15 (0Fhex) Write Multiple Coils - Writes each coil in a sequence of coils to either ON or OFF.
    - "write_multiple_registers": Function 16 (10hex) Write Multiple Registers - Writes values into a sequence of holding registers

- **address**: (**Required**, int): start address of the first register in a range
- **offset**: (**Optional**, int): offset from start address in bytes. If more than one register is read a modbus read registers command this value is used to find the start of this datapoint relative to start address. The component calculates the size of the range based on offset and size of the value type
  For coil or discrete input registers offset is the position of the coil/register because these registers encode 8 coils in one byte.
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

- **bitmask**: (**Optional**) some values are packed in a response. The bitmask can be used to extract a value from the response.  For example, if the high byte value register 0x9013 contains the minute value of the current time. To only exctract this value use bitmask: 0xFF00.  The result will be automatically right shifted by the number of 0 before the first 1 in the bitmask.  For 0xFF00 (0b1111111100000000) the result is shifted 8 posistions.  More than one sensor can use the same address/offset if the bitmask is different.
- **skip_updates**: (**Optional**, integer): By default all sensors of of a modbus_controller are updated together. For data points that don't change very frequently updates can be skipped. A value of 5 would only update this sensor range in every 5th update cycle
  Note: The modbus_controller groups component by address ranges to reduce number of transactions. All compoents with the same address will be updated in one request. skip_updates applies for all components in the same range.
- **register_count**: (**Optional**): The number of registers this data point spans. Default is 1 

- All other options from :ref:`Sensor <config-sensor>`.


This example will send 2 modbus commands (device address 1 assumed)

0x1 0x4 0x31 0x0 0x0 0x02 x7f 0x37 ( read 2 registers starting at 0x3100)

0x1 0x3 0x90 0x1 0x0 0x1 0xf8 0xca ( read 1 holding resister from 0x9001 )

.. code-block:: yaml

  - platform: modbus_controller
    modbus_controller_id: traceran
    id: pv_input_voltage
    name: "PV array input voltage"
    address: 0x3100
    offset: 0
    unit_of_measurement: "V" ## for any other unit the value is returned in minutes
    modbus_functioncode: "read_input_registers"
    value_type: U_WORD
    accuracy_decimals: 1
    filters:
      - multiply: 0.01

  - platform: modbus_controller
    modbus_controller_id: traceran
    id: pv_input_current
    name: "PV array input current"
    address: 0x3100
    offset: 2
    unit_of_measurement: "A" ## for any other unit the value is returned in minutes
    modbus_functioncode: "read_input_registers"
    value_type: U_WORD
    accuracy_decimals: 2
    filters:
      - multiply: 0.01

  - platform: modbus_controller
    modbus_controller_id: traceran
    name: "Battery Capacity"
    id: battery_capacity
    modbus_functioncode: read_holding_registers
    address: 0x9001
    offset: 0
    unit_of_measurement: "AH"
    value_type: U_WORD    

See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/binary_sensor/modbus_binarysensor`
- :doc:`/components/text_sensor/modbus_textsensor`
- :doc:`/components/switch/modbus_switch`
- https://www.modbustools.com/modbus.html
- :ghedit:`Edit`