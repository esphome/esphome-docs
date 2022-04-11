Modbus Controller
=================

.. seo::
    :description: Instructions for setting up the Modbus Controller component.
    :image: modbus.png

The ``modbus_controller`` component creates a RS485 connection to control a modbus device

.. figure:: /images/modbus.png
    :align: center
    :width: 25%

The ``modbus_controller`` component uses the modbus component



Hardware setup
--------------
A RS 485 module connected to an ESP32, for example:

.. figure:: /images/rs485.jpg

See `How is this RS485 Module Working? <https://electronics.stackexchange.com/questions/244425/how-is-this-rs485-module-working>`__ on stackexchange for more details

The controller connects to the UART of the MCU. For ESP32  GPIO PIN 16 to TXD PIN 17 to RXD are the default ports but any other pins can be used as well. 3.3V to VCC and GND to GND.

.. note::

    If you are using an ESP8266, serial logging may cause problems reading from UART. For best results, hardware serial is recommended. Software serial may not be able to read all received data if other components spend a lot of time in the ``loop()``.

    For hardware serial only a limited set of pins can be used. Either ``tx_pin: GPIO1`` and ``rx_pin: GPIO3``  or ``tx_pin: GPIO15`` and ``rx_pin: GPIO13``.

    The disadvantage of using the hardware uart is that you can't use serial logging because the serial logs would be sent to the modbus device and cause errors.

    Serial logging can be disabled by setting ``baud_rate: 0``.

    See :doc:`logger` for more details

    .. code-block:: yaml

        logger:
            level: <level>
            baud_rate: 0



Configuration variables:
------------------------

- **modbus_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the modbus hub.

- **address** (**Required**, :ref:`config-id`): The modbus address of the device
  Specify the modbus device address of the.

- **command_throttle** (*Optional*, int): minimum time in milliseconds between 2 requests to the device. Default is 0ms
  Because some modbus devices limit the rate of requests the interval between sending requests to the device can be modified.


Example
-------
The following code create a modbus_controller hub talking to a modbus device at address 1 with 115200 bps


Modbus sensors can be directly defined (inline) under the modbus_controller hub or as standalone components
Technically there is no difference between the "inline" and the standard definitions approach.

.. code-block:: yaml

    uart:
      id: mod_bus
      tx_pin: 17
      rx_pin: 16
      baud_rate: 115200
      stop_bits: 1

    modbus:
      flow_control_pin: 5
      id: modbus1

    modbus_controller:
      - id: epever
        ## the Modbus device addr
        address: 0x1
        modbus_id: modbus1
        setup_priority: -10

    text_sensor:
      - name: "rtc_clock"
        platform: modbus_controller
        modbus_controller_id: epever
        id: rtc_clock
        internal: true
        register_type: holding
        address: 0x9013
        register_count: 3
        raw_encode: HEXBYTES
        response_size: 6

    switch:
      - platform: modbus_controller
        modbus_controller_id: epever
        id: reset_to_fabric_default
        name: "Reset to Factory Default"
        register_type: coil
        address: 0x15
        bitmask: 1

    sensor:
      - platform: modbus_controller
        modbus_controller_id: epever
        name: "Battery Capacity"
        id: battery_capacity
        register_type: holding
        address: 0x9001
        unit_of_measurement: "AH"
        value_type: U_WORD


Bitmasks
--------

Some devices use decimal values in read registers to show multiple binary states occupying only one register address. To decode them, you can use bitmasks according to the table below. The decimal value corresponding to a bit is always double of the previous one in the row. Multiple bits can be represented in a single register by making a sum of all the values corresponding to the bits.

+------------+------------------+-----------+-----------+ 
| Alarm  bit | Description      | DEC value | HEX value |
+============+==================+===========+===========+ 
| bit 0      | Binary Sensor 0  | 1         | 1         |
+------------+------------------+-----------+-----------+ 
| bit 1      | Binary Sensor 1  | 2         | 2         |
+------------+------------------+-----------+-----------+ 
| bit 2      | Binary Sensor 2  | 4         | 4         |
+------------+------------------+-----------+-----------+ 
| bit 3      | Binary Sensor 3  | 8         | 8         |
+------------+------------------+-----------+-----------+ 
| bit 4      | Binary Sensor 4  | 16        | 10        |
+------------+------------------+-----------+-----------+ 
| bit 5      | Binary Sensor 5  | 32        | 20        |
+------------+------------------+-----------+-----------+ 
| bit 6      | Binary Sensor 6  | 64        | 40        |
+------------+------------------+-----------+-----------+ 
| bit 7      | Binary Sensor 7  | 128       | 80        |
+------------+------------------+-----------+-----------+ 
| bit 8      | Binary Sensor 8  | 256       | 100       |
+------------+------------------+-----------+-----------+ 
| bit 9      | Binary Sensor 9  | 512       | 200       |
+------------+------------------+-----------+-----------+ 
| bit 10     | Binary Sensor 10 | 1024      | 400       |
+------------+------------------+-----------+-----------+ 
| bit 11     | Binary Sensor 11 | 2048      | 800       |
+------------+------------------+-----------+-----------+ 
| bit 12     | Binary Sensor 12 | 4096      | 1000      |
+------------+------------------+-----------+-----------+ 
| bit 13     | Binary Sensor 13 | 8192      | 2000      |
+------------+------------------+-----------+-----------+ 
| bit 14     | Binary Sensor 14 | 16384     | 4000      |
+------------+------------------+-----------+-----------+ 
| bit 15     | Binary Sensor 15 | 32768     | 8000      |
+------------+------------------+-----------+-----------+ 

For example, when reading register ``15``, a decimal value of ``12288`` is the sum of ``4096`` + ``8192``, meaning the corresponding bits ``12`` and ``13`` are ``1``, the other bits are ``0``. 

To gather some of these bits as binary sensors in ESPHome, use ``bitmask``:

.. code-block:: yaml

    binary_sensor:
    - platform: modbus_controller
      modbus_controller_id: ventilation_system
      name: Alarm bit0
      entity_category: diagnostic
      device_class: problem
      register_type: read
      address: 15
      bitmask: 0x1
    - platform: modbus_controller
      modbus_controller_id: ventilation_system
      name: Alarm bit1
      entity_category: diagnostic
      device_class: problem
      register_type: read
      address: 15
      bitmask: 0x2
    - platform: modbus_controller
      modbus_controller_id: ventilation_system
      name: Alarm bit10
      entity_category: diagnostic
      device_class: problem
      register_type: read
      address: 15
      bitmask: 0x400
    - platform: modbus_controller
      modbus_controller_id: ventilation_system
      name: Alarm bit15
      entity_category: diagnostic
      device_class: problem
      register_type: read
      address: 15
      bitmask: 0x8000




Protocol decoding example
-------------------------

.. code-block:: yaml

    sensors:
      - platform: modbus_controller
        modbus_controller_id: epever
        id: array_rated_voltage
        name: "array_rated_voltage"
        address: 0x3000
        unit_of_measurement: "V"
        register_type: read
        value_type: U_WORD
        accuracy_decimals: 1
        skip_updates: 60
        filters:
          - multiply: 0.01

      - platform: modbus_controller
        modbus_controller_id: epever
        id: array_rated_current
        name: "array_rated_current"
        address: 0x3001
        unit_of_measurement: "V"
        register_type: read
        value_type: U_WORD
        accuracy_decimals: 2
        filters:
          - multiply: 0.01

      - platform: modbus_controller
        modbus_controller_id: epever
        id: array_rated_power
        name: "array_rated_power"
        address: 0x3002
        unit_of_measurement: "W"
        register_type: read
        value_type: U_DWORD_R
        accuracy_decimals: 1
        filters:
          - multiply: 0.01

      -platform: modbus_controller
        modbus_controller_id: epever
        id: battery_rated_voltage
        name: "battery_rated_voltage"
        address: 0x3004
        unit_of_measurement: "V"
        register_type: read
        value_type: U_WORD
        accuracy_decimals: 1
        filters:
          - multiply: 0.01

      - platform: modbus_controller
        modbus_controller_id: epever
        id: battery_rated_current
        name: "battery_rated_current"
        address: 0x3005
        unit_of_measurement: "A"
        register_type: read
        value_type: U_WORD
        accuracy_decimals: 1
        filters:
          - multiply: 0.01

      - platform: modbus_controller
        modbus_controller_id: epever
        id: battery_rated_power
        name: "battery_rated_power"
        address: 0x3006
        unit_of_measurement: "W"
        register_type: read
        value_type: U_DWORD_R
        accuracy_decimals: 1
        filters:
          - multiply: 0.01

      - platform: modbus_controller
        modbus_controller_id: epever id: charging_mode
        name: "charging_mode"
        address: 0x3008
        unit_of_measurement: ""
        register_type: read
        value_type: U_WORD
        accuracy_decimals: 0



To minimize the required transactions all registers with the same base address are read in one request.
The response is mapped to the sensor based on register_count and offset in bytes.

**Request**

+-----------+-----------------------------------------+
| data      | description                             |
+===========+=========================================+
| 0x1  (01) | device address                          |
+-----------+-----------------------------------------+
| 0x4  (04) | function code 4 (Read Input Registers)  |
+-----------+-----------------------------------------+
| 0x30 (48) | start address high byte                 |
+-----------+-----------------------------------------+
| 0x0  (00) | start address low byte                  |
+-----------+-----------------------------------------+
| 0x0  (00) | number of registers to read high byte   |
+-----------+-----------------------------------------+
| 0x9  (09) | number of registers to read low byte    |
+-----------+-----------------------------------------+
| 0x3f (63) | crc                                     |
+-----------+-----------------------------------------+
| 0xc  (12) | crc                                     |
+-----------+-----------------------------------------+



**Response**

+--------+------------+--------------------+--------------------------------------------+
| offset | data       | value (type)       | description                                |
+========+============+====================+============================================+
|  H     | 0x1  (01)  |                    | device address                             |
+--------+------------+--------------------+--------------------------------------------+
|   H    | 0x4  (04)  |                    | function code                              |
+--------+------------+--------------------+--------------------------------------------+
|   H    | 0x12 (18)  |                    | byte count                                 |
+--------+------------+--------------------+--------------------------------------------+
|   0    | 0x27 (39)  | U_WORD             | array_rated_voltage  high byte             |
+--------+------------+--------------------+--------------------------------------------+
|   1    | 0x10 (16)  | 0x2710 (100000)    | array_rated_voltage  low byte              |
+--------+------------+--------------------+--------------------------------------------+
|   2    | 0x7  (7)   | U_WORD             | array_rated_current  high byte             |
+--------+------------+--------------------+--------------------------------------------+
|   3    | 0xd0 (208) | 0x7d0 (2000)       | array_rated_current  low byte              |
+--------+------------+--------------------+--------------------------------------------+
|   4    | 0xcb (203) | U_DWORD_R          | array_rated_power high byte of low word    |
+--------+------------+--------------------+--------------------------------------------+
|   5    | 0x20 (32)  | spans 2 register   | array_rated_power low byte of low word     |
+--------+------------+--------------------+--------------------------------------------+
|   6    | 0x0  (0)   |                    | array_rated_power high byte of high word   |
+--------+------------+--------------------+--------------------------------------------+
|   7    | 0x0  (0)   | 0x0000CB20 (52000) | array_rated_power low byte of high word    |
+--------+------------+--------------------+--------------------------------------------+
|   8    | 0x9  (09)  | U_WORD             | battery_rated_voltage high byte            |
+--------+------------+--------------------+--------------------------------------------+
|   9    | 0x60 (96)  | 0x960 (2400)       | battery_rated_voltage low byte             |
+--------+------------+--------------------+--------------------------------------------+
|   10   | 0x7  (07)  | U_WORD             | battery_rated_current high word            |
+--------+------------+--------------------+--------------------------------------------+
|   11   | 0xd0 (208) | 0x7d0 (2000)       | battery_rated_current high word            |
+--------+------------+--------------------+--------------------------------------------+
|   12   | 0xcb (203) | U_DWORD_R          | battery_rated_power high byte of low word  |
+--------+------------+--------------------+--------------------------------------------+
|   13   | 0x20 (32)  | spans 2 register   | battery_rated_power low byte of low word   |
+--------+------------+--------------------+--------------------------------------------+
|   14   | 0x0  (0)   |                    | battery_rated_power high byte of high word |
+--------+------------+--------------------+--------------------------------------------+
|   15   | 0x0  (0)   | 0x0000CB20 (52000) | battery_rated_power low byte of high word  |
+--------+------------+--------------------+--------------------------------------------+
|   16   | 0x0  (0)   | U_WORD             | charging_mode high byte                    |
+--------+------------+--------------------+--------------------------------------------+
|   17   | 0x2  (02)  | 0x2 (MPPT)         | charging_mode low  byte                    |
+--------+------------+--------------------+--------------------------------------------+
|   C    | 0x2f (47)  |                    | crc                                        |
+--------+------------+--------------------+--------------------------------------------+
|   C    | 0x31 (49)  |                    | crc                                        |
+--------+------------+--------------------+--------------------------------------------+



Note
----

Write support is only implemented for switches.
However the C++ code provides the required API to write to a modbus device.

These methods can be called from a lambda.

Here is an example how to set config values to for an EPEVER Trace AN controller.
The code synchronizes the localtime of MCU to the epever controller
The time is set by writing 12 bytes to register 0x9013.
Then battery charge settings are sent.


.. code-block:: yaml

    esphome:
      on_boot:
        ## configure controller settings at setup
        ## make sure priority is lower than setup_priority of modbus_controller
        priority: -100
        then:
          - lambda: |-
              // get local time and sync to controller
              time_t now = ::time(nullptr);
              struct tm *time_info = ::localtime(&now);
              int seconds = time_info->tm_sec;
              int minutes = time_info->tm_min;
              int hour = time_info->tm_hour;
              int day = time_info->tm_mday;
              int month = time_info->tm_mon + 1;
              int year = time_info->tm_year % 100;
              esphome::modbus_controller::ModbusController *controller = id(epever);
              // if there is no internet connection localtime returns year 70
              if (year != 70) {
                // create the payload
                std::vector<uint16_t> rtc_data = {uint16_t((minutes << 8) | seconds), uint16_t((day << 8) | hour),
                                                  uint16_t((year << 8) | month)};
                // Create a modbus command item with the time information as the payload
                esphome::modbus_controller::ModbusCommandItem set_rtc_command =
                    esphome::modbus_controller::ModbusCommandItem::create_write_multiple_command(controller, 0x9013, 3, rtc_data);
                // Submit the command to the send queue
                epever->queue_command(set_rtc_command);
                ESP_LOGI("ModbusLambda", "EPSOLAR RTC set to %02d:%02d:%02d %02d.%02d.%04d", hour, minutes, seconds, day, month,
                        year + 2000);
              }
              // Battery settings
              // Note: these values are examples only and apply my AGM Battery
              std::vector<uint16_t> battery_settings1 = {
                  0,       // 9000 Battery Type 0 =  User
                  0x0073,  // 9001 Battery Cap 0x55 == 115AH
                  0x012C,  // 9002 Temp compensation -3V /°C/2V
                  0x05DC,  // 9003 0x5DC == 1500 Over Voltage Disconnect Voltage 15,0
                  0x058C,  // 9004 0x58C == 1480 Charging Limit Voltage 14,8
                  0x058C,  // 9005 Over Voltage Reconnect Voltage 14,8
                  0x05BF,  // 9006 Equalize Charging Voltage 14,6
                  0x05BE,  // 9007 Boost Charging Voltage 14,7
                  0x0550,  // 9008 Float Charging Voltage 13,6
                  0x0528,   // 9009 Boost Reconnect Charging Voltage 13,2
                  0x04C4,  // 900A Low Voltage Reconnect Voltage 12,2
                  0x04B0,  // 900B Under Voltage Warning Reconnect Voltage 12,0
                  0x04BA,  // 900c Under Volt. Warning Volt 12,1
                  0x04BA,  // 900d Low Volt. Disconnect Volt. 11.8
                  0x04BA   // 900E Discharging Limit Voltage 11.8
              };

              // Boost and equalization periods
              std::vector<uint16_t> battery_settings2 = {
                  0x0000,  // 906B Equalize Duration (min.) 0
                  0x0075   // 906C Boost Duration (aka absorb) 117 mins
              };
              esphome::modbus_controller::ModbusCommandItem set_battery1_command =
                  esphome::modbus_controller::ModbusCommandItem::create_write_multiple_command(controller, 0x9000, battery_settings1.size() ,
                                                                                              battery_settings1);

              esphome::modbus_controller::ModbusCommandItem set_battery2_command =
                  esphome::modbus_controller::ModbusCommandItem::create_write_multiple_command(controller, 0x906B, battery_settings3.size(),
                                                                                              battery_settings2);
              delay(200) ;
              controller->queue_command(set_battery1_command);
              delay(200) ;
              controller->queue_command(set_battery2_command);
              ESP_LOGI("ModbusLambda", "EPSOLAR Battery set");

    uart:
      id: mod_bus
      tx_pin: 19
      rx_pin: 18
      baud_rate: 115200
      stop_bits: 1

    modbus:
      #flow_control_pin: 23
      send_wait_time: 200ms
      id: mod_bus_epever

    modbus_controller:
      - id: epever
        ## the Modbus device addr
        address: 0x1
        modbus_id: mod_bus_epever
        command_throttle: 0ms
        setup_priority: -10
        update_interval: ${updates}

    sensor:
      - platform: modbus_controller
        modbus_controller_id: epever
        id: array_rated_voltage
        name: "array_rated_voltage"
        address: 0x3000
        unit_of_measurement: "V"
        register_type: read
        value_type: U_WORD
        accuracy_decimals: 1
        filters:
          - multiply: 0.01

      - platform: modbus_controller
        modbus_controller_id: epever
        id: array_rated_current
        name: "array_rated_current"
        address: 0x3001
        unit_of_measurement: "A"
        register_type: read
        value_type: U_WORD
        accuracy_decimals: 2
        filters:
          - multiply: 0.01

      - platform: modbus_controller
        modbus_controller_id: epever
        id: array_rated_power
        name: "array_rated_power"
        address: 0x3002
        unit_of_measurement: "W"
        register_type: read
        value_type: U_DWORD_R
        accuracy_decimals: 1
        filters:
          - multiply: 0.01




See Also
--------

- :doc:`/components/sensor/modbus_controller`
- :doc:`/components/binary_sensor/modbus_controller`
- :doc:`/components/text_sensor/modbus_controller`
- :doc:`/components/switch/modbus_controller`
- :doc:`/components/number/modbus_controller`
- :doc:`/components/output/modbus_controller`
- :doc:`EPEVER MPPT Solar Charge Controller Tracer-AN Series</cookbook/tracer-an>`
- `Modbus RTU Protocol Description <https://www.modbustools.com/modbus.html>`__
- :ghedit:`Edit`
