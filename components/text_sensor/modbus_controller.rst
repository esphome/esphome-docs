Modbus Controller Text Sensor
=============================

.. seo::
    :description: Instructions for setting up a modbus_controller modbus text sensor.

The ``modbus_controller`` sensor platform creates a text sensor from a modbus_controller component
and requires :doc:`/components/modbus_controller` to be configured.


Configuration variables:
------------------------
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the sensor.
- **register_type** (**Required**): type of the modbus register.

    - ``coil``: coils are also called discrete outout. Coils are 1-bit registers (on/off values) that are used to control discrete outputs. Read and Write access
    - ``discrete_input``: discrete input register (read only coil) are similar to coils but can only be read.
    - ``holding``: Holding Registers - Holding registers are the most universal 16-bit register. Read and Write access
    - ``read``: Read Input Registers - registers are 16-bit registers used for input, and may only be read

- **address** (**Required**, int): start address of the first register in a range
- **skip_updates** (*Optional*, int): By default all sensors of a modbus_controller are updated together. For data points that don't change very frequently updates can be skipped. A value of 5 would only update this sensor range in every 5th update cycle
- **register_count** (*Optional*): The number of registers this data point spans. Default is 1
- **response_size** (**Required**): Number of bytes of the response
- **raw_encode** (*Optional*, enum): If the response is binary it can't be published directly. Since a text sensor only publishes strings the binary data can be encoded

     - ``NONE``: Don't encode data.
     - ``HEXBYTES``:  2 byte hex string. 0x2011 will be sent as "2011".
     - ``COMMA``: Byte values as integers, delimited by a coma. 0x2011 will be sent as "32,17"

- **force_new_range** (*Optional*, boolean): If possible sensors with sequential addresses are grouped together and requested in one range. Setting ``force_new_range: true`` enforces the start of a new range at that address.
- **custom_command** (*Optional*, list of bytes): raw bytes for modbus command. This allows using non-standard commands. If ``custom_command`` is used ``address`` and ``register_type`` can't be used.
  custom command must contain all required bytes including the modbus device address. The crc is automatically calculated and appended to the command.
  See :ref:`modbus_custom_command` how to use ``custom_command``
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the new value of the sensor. It is called after the encoding according to **raw_encode**.

  Parameters passed into the lambda

  - **x** (std:string): The parsed value of the modbus data according to **raw_encode**
  - **data** (std::vector<uint8_t): vector containing the complete raw modbus response bytes for this sensor
    *note:* because the response contains data for all registers in the same range you have to use ``data[item->offset]`` to get the first response byte for your sensor.
  - **item** (const pointer to a SensorItem derived object):  The sensor object itself.

  Possible return values for the lambda:

  - ``return <std::string>;`` the new value for the sensor.
  - ``return {};`` uses the parsed value for the state (same as ``return x;``).

- **offset** (*Optional*, int): not required in most cases
  offset from start address in bytes. If more than one register is read a modbus read registers command this value is used to find the start of this datapoint relative to start address. The component calculates the size of the range based on offset and size of the value type
- All options from :ref:`Text Sensor <config-text_sensor>`.

**Example**


.. code-block:: yaml

    text_sensor:
      - platform: modbus_controller
        modbus_controller_id: modbus_device
        id: reg_1002_text
        bitmask: 0
        register_type: holding
        address: 1002
        raw_encode: HEXBYTES
        name: Register 1002 (Text)
        lambda: |-
          uint16_t value = modbus_controller::word_from_hex_str(x, 0);
          switch (value) {
            case 1: return std::string("ready");
            case 2: return std::string("EV is present");
            case 3: return std::string("charging");
            case 4: return std::string("charging with ventilation");
            default: return std::string("Unknown");
          }
          return x;

See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/sensor/modbus_controller`
- :doc:`/components/binary_sensor/modbus_controller`
- :doc:`/components/switch/modbus_controller`
- https://www.modbustools.com/modbus.html
- :ghedit:`Edit`
