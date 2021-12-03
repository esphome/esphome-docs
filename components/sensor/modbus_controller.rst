Modbus Sensor
=============

.. seo::
    :description: Instructions for setting up a modbus_controller device sensor.
    :image: modbus.png

The ``modbus_controller`` sensor platform creates a sensor from a modbus_controller component
and requires :doc:`/components/modbus_controller` to be configured.


Configuration variables:
------------------------
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the sensor.
- **register_type** (**Required**): type of the modbus register.
    - coil: coils are also called discrete outout. Coils are 1-bit registers (on/off values) that are used to control discrete outputs. Read and Write access
    - discrete_input: discrete input register (read only coil) are similar to coils but can only be read.
    - holding: Holding Registers - Holding registers are the most universal 16-bit register. Read and Write access
    - read: Read Input Registers - registers are 16-bit registers used for input, and may only be read
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

- **bitmask**: (*Optional*) some values are packed in a response. The bitmask can be used to extract a value from the response.  For example, if the high byte value register 0x9013 contains the minute value of the current time. To only exctract this value use bitmask: 0xFF00.  The result will be automatically right shifted by the number of 0 before the first 1 in the bitmask.  For 0xFF00 (0b1111111100000000) the result is shifted 8 posistions.  More than one sensor can use the same address/offset if the bitmask is different.
- **skip_updates**: (*Optional*, int): By default all sensors of of a modbus_controller are updated together. For data points that don't change very frequently updates can be skipped. A value of 5 would only update this sensor range in every 5th update cycle
  Note: The modbus_controller groups component by address ranges to reduce number of transactions. All compoents with the same address will be updated in one request. skip_updates applies for all components in the same range.
- **register_count**: (*Optional*): only required for uncommon response encodings
  The number of registers this data point spans. Default is 1
- **force_new_range**: (*Optional*, boolean): If possible sensors with sequential addresses are grouped together and requested in one range. Setting `foce_new_range: true` enforces the start of a new range at that address.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the new value of the sensor.
- **offset**: (*Optional*, int): only required for uncommon response encodings
    offset from start address in bytes. If more than one register is read a modbus read registers command this value is used to find the start of this datapoint relative to start address. The component calculates the size of the range based on offset and size of the value type
    For coil or discrete input registers offset is the position of the coil/register because these registers encode 8 coils in one byte.

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
      unit_of_measurement: "V" ## for any other unit the value is returned in minutes
      register_type: read
      value_type: U_WORD
      accuracy_decimals: 1
      filters:
        - multiply: 0.01

    - platform: modbus_controller
      modbus_controller_id: traceran
      id: pv_input_current
      name: "PV array input current"
      address: 0x3101
      unit_of_measurement: "A" ## for any other unit the value is returned in minutes
      register_type: read
      value_type: U_WORD
      accuracy_decimals: 2
      filters:
        - multiply: 0.01

    - platform: modbus_controller
      modbus_controller_id: traceran
      name: "Battery Capacity"
      id: battery_capacity
      register_type: holding
      address: 0x9001
      unit_of_measurement: "AH"
      value_type: U_WORD


The ``modbus`` sensor platform allows you use a lambda that gets called before data is published
using :ref:`lambdas <config-lambda>`.

This example logs the value as parsed and the raw modbus bytes received for this register range

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: modbus_controller
          modbus_controller_id: epever
          id: battery_capacity
          address: 0x9001
          name: "Battery Capacity"
          register_type: holding
          value_type: U_WORD
          lambda: |-
            ESP_LOGI("","Lambda incoming value=%f - data array size is %d",x,data.size());
            ESP_LOGI("","Sensor properties: adress = 0x%X, offset = 0x%X value type=%d",item->start_address,item->offset,item->sensor_value_type);
            int i=0 ;
            for (auto val : data) {
              ESP_LOGI("","data[%d]=0x%02X (%d)",i++ ,data[i],data[i]);
            }
            return x ;


Parameters passed into the lambda

- **x** (float): The parsed float value of the modbus data

- **data** (std::vector<uint8_t): vector containing the complete raw modbus response bytes for this sensor
      note: because the response contains data for all registers in the same range you have to use `data[item->offset]` to get the first response byte for your sensor.
- **item** (const pointer to a SensorItem derived object):  The sensor object itself.

Possible return values for the lambda:

 - ``return <FLOATING_POINT_NUMBER>;`` the new value for the sensor.
 - ``return NAN;`` if the state should be considered invalid to indicate an error (advanced).

See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/number/modbus_controller`
- :doc:`/components/binary_sensor/modbus_controller`
- :doc:`/components/text_sensor/modbus_controller`
- :doc:`/components/switch/modbus_controller`
- :doc:`EPEVER MPPT Solar Charge Controller Tracer-AN Series</cookbook/tracer-an>`
- :ghedit:`Edit`
