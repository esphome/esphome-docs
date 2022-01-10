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
    - coil: coils are also called discrete output. Coils are 1-bit registers (on/off values) that are used to control discrete outputs. Read and Write access. Modbus function code 1 (Read Coil Status) will be used
    - discrete_input: discrete input register (read only coil) are similar to coils but can only be read. Modbus function code 2 (Read Input Status) will be used.
    - holding: Holding Registers - Holding registers are the most universal 16-bit register. Read and Write access. Modbus function code 3 (Read Holding Registers) will be used.
    - read: Read Input Registers - registers are 16-bit registers used for input, and may only be read. Modbus function code 4 (Read Input Registers) will be used.
- **address**: (**Required**, int): start address of the first register in a range
- **value_type**: (**Required**): datatype of the mod_bus register data. The default data type for modbus is a 16 bit integer in big endian format (MSB first)
    - U_WORD (unsigned 16 bit integer from 1 register = 16bit)
    - S_WORD (signed 16 bit integer from 1 register = 16bit)
    - U_DWORD (unsigned 32 bit integer from 2 registers = 32bit)
    - S_DWORD (signed 32 bit integer from 2 registers = 32bit)
    - U_DWORD_R (unsigned 32 bit integer from 2 registers low word first)
    - S_DWORD_R (signed 32 bit integer from 2 registers low word first)
    - U_QWORD (unsigned 64 bit integer from 4 registers = 64bit)
    - S_QWORD (signed 64 bit integer from 4 registers = 64bit)
    - U_QWORD_R (unsigned 64 bit integer from 4 registers low word first)
    - S_QWORD_R (signed 64 bit integer from 4 registers low word first)
    - FP32 (32 bit IEEE 754 floating point from 2 registers)
    - FP32_R (32 bit IEEE 754 floating point - same as FP32 but low word first)s

- **bitmask**: (*Optional*) some values are packed in a response. The bitmask can be used to extract a value from the response.  For example, if the high byte value register 0x9013 contains the minute value of the current time. To only exctract this value use bitmask: 0xFF00.  The result will be automatically right shifted by the number of 0 before the first 1 in the bitmask.  For 0xFF00 (0b1111111100000000) the result is shifted 8 posistions.  More than one sensor can use the same address/offset if the bitmask is different.
- **skip_updates**: (*Optional*, int): By default all sensors of of a modbus_controller are updated together. For data points that don't change very frequently updates can be skipped. A value of 5 would only update this sensor range in every 5th update cycle
  Note: The modbus_controller groups component by address ranges to reduce number of transactions. All compoents with the same address will be updated in one request. skip_updates applies for all components in the same range.
- **register_count**: (*Optional*): only required for uncommon response encodings or to :ref:`optimize modbus communications<modbus_register_count>`
  The number of registers this data point spans. Overrides the defaults determined by ``value_type``.
  If no value for ``register_count`` is provided, it is calculated based on the register type.

  The default size for 1 register is 16 bits (1 Word). Some devices are not adhering to this convention and have registers larger than 16 bits.  In this case ``register_count`` and  ``response_size`` must be set. For example, if your modbus device uses 1 registers for a FP32 value instead the default of two set ``register_count: 1`` and ``response_size: 4``.
- **response_size**:  (*Optional*): Size of the response for the register in bytes. Defaults to register_count*2.
- **force_new_range**: (*Optional*, boolean): If possible sensors with sequential addresses are grouped together and requested in one range. Setting ``force_new_range: true`` enforces the start of a new range at that address.
- **custom_data** (*Optional*, list of bytes): raw bytes for modbus command. This allows using non-standard commands. If ``custom_data`` is used ``address`` and ``register_type`` can't be used. 
  custom data must contain all required bytes including the modbus device address. The crc is automatically calculated and appended to the command.
  See :ref:`modbus_custom_data` how to use ``custom_command``
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
      note: because the response contains data for all registers in the same range you have to use ``data[item->offset]`` to get the first response byte for your sensor.
- **item** (const pointer to a SensorItem derived object):  The sensor object itself.

Possible return values for the lambda:

 - ``return <FLOATING_POINT_NUMBER>;`` the new value for the sensor.
 - ``return NAN;`` if the state should be considered invalid to indicate an error (advanced).

.. _modbus_custom_data:

Using custom_data
-----------------

``custom_data`` can be used to create an arbitrary modbus command. Combined with a lambda any response can be handled. 
This example re-implements the command to read the registers 0x156 (Total active energy) and 0x158 Total (reactive energy) from a SDM-120.
SDM-120 returns the values as floats using 32 bits in 2 registers. 

    .. code-block:: yaml

        modbus:
          send_wait_time: 200ms
          uart_id: mod_uart
          id: mod_bus

        modbus_controller:
          - id: sdm
            address: 2
            modbus_id: mod_bus
            command_throttle: 100ms
            setup_priority: -10
            update_interval: 30s
        sensors:
          - platform: modbus_controller
            modbus_controller_id: sdm
            name: "Total active energy"
            id: total_energy
            #    address: 0x156
            #    register_type: "read"
            ## reimplement using custom_command
            # 0x2 : modbus device address
            # 0x4 : modbus function code
            # 0x1 : high byte of modbus register address
            # 0x56: low byte of modbus register address
            # 0x00: high byte of total number of registers requested 
            # 0x02: low byte of total number of registers requested
            custom_command: [ 0x2, 0x4, 0x1, 0x56,0x00, 0x02]
            value_type: FP32
            unit_of_measurement: kWh
            accuracy_decimals: 1

          - platform: modbus_controller
            modbus_controller_id: sdm
            name: "Total reactive energy"
            #   address: 0x158
            #   register_type: "read"
            custom_command: [0x2, 0x4, 0x1, 0x58, 0x00, 0x02]
            ## the command returns an float value using 4 bytes
            lambda: |-
              ESP_LOGD("Modbus Sensor Lambda","Got new data" );
              union {
                float float_value;
                uint32_t raw;
              } raw_to_float;
              if (data.size() < 4 ) {
                ESP_LOGE("Modbus Sensor Lambda", "invalid data size %d",data.size());
                return NAN;
              }
              raw_to_float.raw =   data[0] << 24 | data[1] << 16 | data[2] << 8 |  data[3];
              ESP_LOGD("Modbus Sensor Lambda", "FP32 = 0x%08X => %f", raw_to_float.raw, raw_to_float.float_value);
              return raw_to_float.float_value;
            unit_of_measurement: kVArh
            accuracy_decimals: 1

.. _modbus_register_count:

.. note:: **Optimize modbus communications**

    ``register_count`` can also be used to skip a register in consecutive range. 
    
    An example is a SDM meter: 
    
    .. code-block:: yaml

        - platform: modbus_controller
            name: "Voltage Phase 1"
            address: 0
            register_type: "read"
            value_type: FP32

        - platform: modbus_controller
            name: "Voltage Phase 2"
            address: 2
            register_type: "read"
            value_type: FP32

        - platform: modbus_controller
            name: "Voltage Phase 3"
            address: 4
            register_type: "read"
            value_type: FP32

          - platform: modbus_controller
            name: "Current Phase 1"
            address: 6
            register_type: "read"
            value_type: FP32
            accuracy_decimals: 1

    Maybe you don’t care about the Voltage value for Phase 2 and Phase 3 (or you have a SDM-120). 
    Of course, you can delete the sensors your don’t care about. But then you have a gap in the addresses. The configuration above will generate one modbus  command `read multiple registers from 0 to 6`. If you remove the registers at address 2 and 4 then 2 commands will be generated `read register 0` and `read register 6`.
    To avoid the generation of multiple commands and reduce the amount of uart communication ``register_count`` can be used to fill the gaps 

    .. code-block:: yaml

        - platform: modbus_controller
            name: "Voltage Phase 1"
            address: 0
            unit_of_measurement: "V"
            register_type: "read"
            value_type: FP32
            register_count: 6

          - platform: modbus_controller
            name: "Current Phase 1"
            address: 6
            register_type: "read"
            value_type: FP32

    Because `register_count: 6` is used for the first register the command “read registers from 0 to 6” can still be used but the values in between are ignored. 
    **Calculation:** FP32 is a 32 bit value and uses 2 registers. Therefore, to skip the 2 FP32 registers the size of these 2 registers must be added to the default size for the first register.
    So we have 2 for address 0, 2 for address 2 and 2 for address 4 then ``register_count`` must be 6.


See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/number/modbus_controller`
- :doc:`/components/binary_sensor/modbus_controller`
- :doc:`/components/text_sensor/modbus_controller`
- :doc:`/components/switch/modbus_controller`
- :doc:`EPEVER MPPT Solar Charge Controller Tracer-AN Series</cookbook/tracer-an>`
- :ghedit:`Edit`
