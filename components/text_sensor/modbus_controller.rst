Modbus Text Sensor
==================

.. seo::
    :description: Instructions for setting up a modbus_controller modbus text sensor.
    :image: modbus_controller.png

The ``modbus_controller`` sensor platform creates a text sensor from a modbus_controller component
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
- **address**: (**Required**, integer): start address of the first register in a range
- **bitmask**: (*Optional*) some values are packed in a response. The bitmask can be used to extract a value from the response.  For example, if the high byte value register 0x9013 contains the minute value of the current time. To only exctract this value use bitmask: 0xFF00.  The result will be automatically right shifted by the number of 0 before the first 1 in the bitmask.  For 0xFF00 (0b1111111100000000) the result is shifted 8 posistions.  More than one sensor can use the same address/offset if the bitmask is different.
- **skip_updates**: (*Optional*, integer): By default all sensors of of a modbus_controller are updated together. For data points that don't change very frequently updates can be skipped. A value of 5 would only update this sensor range in every 5th update cycle
- **register_count**: (*Optional*): The number of registers this data point spans. Default is 1
- **response_size**:  (**Required**):response number of bytes of the response
- **raw_encode**: (*Optional*, NONE , HEXBYTES, COMMA) If the response is binary it can't be published directly. Since a text sensor only publishes strings the binary data can encoded
     - HEXBYTES:  2 byte hex string. 0x2011 will be sent as "2011".
     - COMMA: Byte values as integers, delimited by a coma. 0x2011 will be sent as "32,17"
- **force_new_range**: (*Optional*, boolean): If possible sensors with sequential addresses are grouped together and requested in one range. Setting ``force_new_range: true`` enforces the start of a new range at that address.
- **custom_data** (**Optional**, list of bytes): raw bytes for modbus command. This allows using non-standard commands. If ``custom_data`` is used ``address`` and ``register_type`` can't be used. 
  custom data must contain all required bytes including the modbus device address. The crc is automatically calculated and appended to the command.
  See :ref:`modbus_custom_data` how to use ``custom_command``
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the new value of the text_sensor
- **offset**: (*Optional*, integer): not required in most cases
  offset from start address in bytes. If more than one register is read a modbus read registers command this value is used to find the start of this datapoint relative to start address. The component calculates the size of the range based on offset and size of the value type


Parameters passed into the lambda

- **x** (std:string): The parsed float value of the modbus data

- **data** (std::vector<uint8_t): vector containing the complete raw modbus response bytes for this sensor
      note: because the response contains data for all registers in the same range you have to use ``data[item->offset]`` to get the first response byte for your sensor.
- **item** (const pointer to a SensorItem derived object):  The sensor object itself.

Possible return values for the lambda:

 - ``return <FLOATING_POINT_NUMBER>;`` the new value for the sensor.
 - ``return NAN;`` if the state should be considered invalid to indicate an error (advanced).
 - ``return {};`` if you don't want to publish a new state (advanced).



**Example**


.. code-block:: yaml

    text_sensor:
    - platform: template
        name: "RTC Time Sensor"
        id: template_rtc

    - platform: modbus_controller
        modbus_controller_id: traceranx
        name: "rtc clock test"
        id: rtc_clock_test
        internal: true
        register_type: holding
        address: 0x9013
        register_count: 3
        hex_encode: true
        response_size: 6
        on_value:
            then:
            - lambda: |-
                ESP_LOGV("main", "decoding rtc hex encoded raw data: %s", x.c_str());
                uint8_t h=0,m=0,s=0,d=0,month_=0,y = 0 ;
                m = esphome::modbus_controller::byte_from_hex_str(x,0);
                s = esphome::modbus_controller::byte_from_hex_str(x,1);
                d = esphome::modbus_controller::byte_from_hex_str(x,2);
                h = esphome::modbus_controller::byte_from_hex_str(x,3);
                y = esphome::modbus_controller::byte_from_hex_str(x,4);
                month_ = esphome::modbus_controller::byte_from_hex_str(x,5);
                // Now check if the rtc time of the controller is ok and correct it
                time_t now = ::time(nullptr);
                struct tm *time_info = ::localtime(&now);
                int seconds = time_info->tm_sec;
                int minutes = time_info->tm_min;
                int hour = time_info->tm_hour;
                int day = time_info->tm_mday;
                int month = time_info->tm_mon + 1;
                int year = time_info->tm_year - 2000;
                // correct time if needed (ignore seconds)
                if (d != day || month_ != month || y != year || h != hour || m != minutes) {
                    // create the payload
                    std::vector<uint16_t> rtc_data = {uint16_t((minutes << 8) | seconds), uint16_t((day << 8) | hour),
                                                    uint16_t((year << 8) | month)};
                    // Create a modbus command item with the time information as the payload
                    esphome::modbus_controller::ModbusCommandItem set_rtc_command = esphome::modbus_controller::ModbusCommandItem::create_write_multiple_command(traceranx, 0x9013, 3, rtc_data);
                    // Submit the command to the send queue
                    traceranx->queue_command(set_rtc_command);
                    ESP_LOGI("ModbusLambda", "EPSOLAR RTC set to %02d:%02d:%02d %02d.%02d.%04d", hour, minutes, seconds, day, month, year + 2000);
                }
                char buffer[20];
                // format time as YYYY:mm:dd hh:mm:ss
                sprintf(buffer,"%04d:%02d:%02d %02d:%02d:%02d",y+2000,month_,d,h,m,s);
                id(template_rtc).publish_state(buffer);

See Also
--------
- :doc:`/components/modbus_controller`
- :doc:`/components/sensor/modbus_controller`
- :doc:`/components/binary_sensor/modbus_controller`
- :doc:`/components/switch/modbus_controller`
- https://www.modbustools.com/modbus.html
- :ghedit:`Edit`
