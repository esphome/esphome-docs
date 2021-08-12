Modbus Controller (Modbus Master)
=================================

.. seo::
    :description: Instructions for setting up the Modbus Controller component.
    :image: modbus.png

The ``modbus_controller`` component creates a RS485 connection to control a modbus device

.. warning::

    If you are using the :doc:`logger` uart logging might interfere especially on esp8266. You can disable the uart logging with the ``baud_rate: 0`` option.

.. figure:: /images/modbus.png
    :align: center
    :width: 40%

The ``modbus_controller`` component uses the modbus component



Hardware setup
--------------
I'm using a RS 485 module connected to an ESP32

.. figure:: /images/rs485.jpg

See [How is this RS485 Module Working?](https://electronics.stackexchange.com/questions/244425/how-is-this-rs485-module-working) on stackexchange for more details

The controller connects to the UART of the MCU. For ESP32  GPIO PIN 16 to TXD PIN 17 to RXD are the default ports but any other pins can be used as well . 3.3V to VCC and GND to GND.


Configuration variables:
------------------------

- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the uart hub.

- **address** (*Required*, :ref:`config-id`): The modbus address of the device device
  Specify the ID of the :ref:`Time Component <time>` which will be used.

- **ctrl_pin**  (**Optional**, :ref:`Pin Schema <config-pin_schema>`): The pin used to enable DE/RE for your rs485 controller if it is not automatically switching between receive and transmit
- **command_throttle** (*Optional*, int): minimum time in milliseconds between 2 requests to the device. Default is 0ms
  Because some modbus devices limit the rate of requests the interval between sending requests to the device can be modified.


Getting started with Home Assistant
-----------------------------------
The following code create a modbus_controller hub talking to a modbus device at address 1 with 115200 bps


Modbus sensors can be directly defined (inline) under the modbus_controller hub or as standalone components
Technically there is no difference between the "inline" and the standard definitions approach.


.. code-block:: yaml

  esphome:
    name: solarstation
    platform: ESP32
    board: esp32dev

  substitutions:
    updates: 30s

  wifi:
    ssid: !secret wifi_sid
    password: !secret wifi_password
    domain: .int.grasruck.net
    use_address: solarstation.int.grasruck.net
    reboot_timeout: 2min

  logger:
    level: INFO
    baud_rate: 0

  api:
    password: !secret api_password

  uart:
    id: mod_bus
    tx_pin: 17
    rx_pin: 16
    baud_rate: 115200
    stop_bits: 1

  modbus:
    id: modbus_epsolar


  modbus_controller:
    command_throttle: 0ms
    id: epever
    uart_id: mod_bus
    address: 0x1
    # ctrl_pin: 5    # if you need to set the driver enable (DE) pin high before transmitting data configure it here
    sensors:
      - id: array_rated_voltage
        name: "array_rated_voltage"
        address: 0x3000
        offset: 0
        unit_of_measurement: "V"
        modbus_functioncode: "read_input_registers"
        value_type: U_WORD
        accuracy_decimals: 1
        skip_updates: 60
        filters:
        - multiply: 0.01

      - id: array_rated_current
        name: "array_rated_current"
        address: 0x3000
        offset: 2
        unit_of_measurement: "V"
        modbus_functioncode: "read_input_registers"
        value_type: U_WORD
        accuracy_decimals: 2
        filters:
          - multiply: 0.01

      - id: array_rated_power
        name: "array_rated_power"
        address: 0x3000
        register_count: 2
        offset: 4
        unit_of_measurement: "W"
        modbus_functioncode: "read_input_registers"
        value_type: U_DWORD_R
        accuracy_decimals: 1
        filters:
          - multiply: 0.01

      - id: length_of_night_minutes
        address: 0x9065
        internal: true
        offset: 0
        bitmask: 0xFF
        unit_of_measurement: "m"
        name: "Length of night-mins"
        modbus_functioncode: read_holding_registers
        value_type: U_WORD

      - id: length_of_night
        address: 0x9065
        offset: 0
        bitmask: 0xFF00
        unit_of_measurement: "m"
        name: "Length of night"
        modbus_functioncode: read_holding_registers
        value_type: U_WORD
        filters:
          - lambda: return id(length_of_night_minutes).state  + ( 60 * x);

    binary_sensors:
      - id: charging_input_volt_failure
        name: "Charging Input Volt Failure"
        modbus_functioncode: read_input_registers
        address: 0x3201
        offset: 0
        bitmask: 0xC000

      - id: manual_control_load
        modbus_functioncode: read_coils
        address: 2
        offset: 0
        name: "manual control the load"
        bitmask: 1

    switches:
      - id: clear_energy_stats
        modbus_functioncode: read_coils
        address: 0x14
        offset: 0
        name: "Clear generating  electricity statistic"
        bitmask: 1

    update_interval: 30s

  switch:
    - platform: modbus_controller
      modbus_controller_id: epever
      id: reset_to_fabric_default
      name: "Reset to Factory Default"
      modbus_functioncode: write_single_coil
      address: 0x15
      bitmask: 1

  sensor:
    - platform: modbus_controller
      modbus_controller_id: epever
      name: "Battery Capacity"
      id: battery_capacity
      modbus_functioncode: read_holding_registers
      address: 0x9001
      offset: 0
      unit_of_measurement: "AH"
      value_type: U_WORD


Protocol decoding example
-------------------------

.. code-block:: yaml

  sensors:
    - id: array_rated_voltage
      name: "array_rated_voltage"
      address: 0x3000
      offset: 0
      unit_of_measurement: "V"
      modbus_functioncode: "read_input_registers"
      value_type: U_WORD
      accuracy_decimals: 1
      skip_updates: 60
      filters:
        - multiply: 0.01

    - id: array_rated_current
      name: "array_rated_current"
      address: 0x3000
      offset: 2
      unit_of_measurement: "V"
      modbus_functioncode: "read_input_registers"
      value_type: U_WORD
      accuracy_decimals: 2
      filters:
        - multiply: 0.01

    - id: array_rated_power
      name: "array_rated_power"
      address: 0x3000
      register_count: 2
      offset: 4
      unit_of_measurement: "W"
      modbus_functioncode: "read_input_registers"
      value_type: U_DWORD_R
      accuracy_decimals: 1
      filters:
        - multiply: 0.01

    - id: battery_rated_voltage
      name: "battery_rated_voltage"
      address: 0x3000
      offset: 8
      unit_of_measurement: "V"
      modbus_functioncode: "read_input_registers"
      value_type: U_WORD
      accuracy_decimals: 1
      filters:
        - multiply: 0.01

    - id: battery_rated_current
      name: "battery_rated_current"
      address: 0x3000
      offset: 10
      unit_of_measurement: "A"
      modbus_functioncode: "read_input_registers"
      value_type: U_WORD
      accuracy_decimals: 1
      filters:
        - multiply: 0.01

    - id: battery_rated_power
      name: "battery_rated_power"
      address: 0x3000
      register_count: 2
      offset: 12
      unit_of_measurement: "W"
      modbus_functioncode: "read_input_registers"
      value_type: U_DWORD_R
      accuracy_decimals: 1
      filters:
        - multiply: 0.01

    - id: charging_mode
      name: "charging_mode"
      address: 0x3000
      offset: 16
      unit_of_measurement: ""
      modbus_functioncode: "read_input_registers"
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
The code  syncs the localtime of MCU to the epever controller
The time is set by writing 12 bytes to register 0x9013. 
Then battery charge settings are sent.


.. code-block:: yaml

    esphome:
      name: solarstation-test
      platform: ESP32
      board: esp32dev

      ## send config values at startup 
      ## configure rtc clock and battery charge settings
      on_boot:
        priority: -100
        then:
          - lambda: |-
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
                traceranx->queue_command(set_rtc_command);
                ESP_LOGI("ModbusLambda", "EPSOLAR RTC set to %02d:%02d:%02d %02d.%02d.%04d", hour, minutes, seconds, day, month,
                        year + 2000);
              }
              // Battery settings
              // Note: these values are examples only and apply to my AGM Battery
              std::vector<uint16_t> battery_settings = {
                  0,       // 9000 Battery Type 0 =  User
                  0x0055,  // 9001 Battery Cap 0x55 == 85AH
                  0x012C,  // 9002 Temp compensation -3V /°C/2V
                  0x05DC,  // 9003 0x5DC == 1500 Over Voltage Disconnect Voltage 15,0
                  0x058C,  // 9004 0x58C == 1480 Charging Limit Voltage	14,8
                  0x058C,  // 9005 Over Voltage Reconnect Voltage	14,8
                  0x05B4,  // 9006 Equalize Charging Voltage	14,6
                  0x05A0,  // 9007 Boost Charging Voltage	14,4
                  0x0564,  // 9008 Float Charging Voltage	13,8
                  0x0528,  // 9009 Boost Reconnect Charging Voltage	13,2
                  0x04EC,  // 900A Low Voltage Reconnect Voltage	12,6
                  0x04C4,  // 900B Under Voltage Warning Reconnect Voltage	12,2
                  0x04BA,  // 900c Under Volt. Warning Volt	12,1
                  0x04BA,  // 900d Low Volt. Disconnect Volt.	12,1
                  0x0424   // 900E Discharging Limit Voltage	10,6
              };
              // Boost and equalization periods
              std::vector<uint16_t> battery_settings2 = {
                  0x0000,  // 906B Equalize Duration (min.)	0
                  0x0075   // 906C Boost Duration (aka absorb)	120 mins
              };


              esphome::modbus_controller::ModbusCommandItem set_battery1_command =
                  esphome::modbus_controller::ModbusCommandItem::create_write_multiple_command(controller, 0x9000, 15,
                                                                                              battery_settings);
              esphome::modbus_controller::ModbusCommandItem set_battery2_command =
                  esphome::modbus_controller::ModbusCommandItem::create_write_multiple_command(controller, 0x906B, 2,
                                                                                              battery_settings2);
              controller->queue_command(set_battery1_command);
              controller->queue_command(set_battery2_command);
              ESP_LOGI("ModbusLambda", "EPSOLAR Battery set");


    uart:
      id: mod_bus
      tx_pin: 17
      rx_pin: 16
      baud_rate: 115200
      stop_bits: 1


    modbus_controller:
      uart_id: mod_bus
      command_throttle: 0ms
      id: epever
      ## the Modbus device addr
      address: 0x1
      ctrl_pin: 5    # if you need to set the driver enable (DE) pin high before transmitting data configure it here
      setup_priority: -10
      sensors:
        - id: array_rated_voltage
          name: "array_rated_voltage"
          address: 0x3000
          offset: 0
          unit_of_measurement: "V"
          modbus_functioncode: "read_input_registers"
          value_type: U_WORD
          accuracy_decimals: 1
          skip_updates: 60
          filters:
            - multiply: 0.01



See Also
--------

- :doc:`/components/sensor/modbus_sensor`
- :doc:`/components/binary_sensor/modbus_binarysensor`
- :doc:`/components/text_sensor/modbus_textsensor`
- :doc:`/components/switch/modbus_switch`
- https://www.modbustools.com/modbus.html
- :ghedit:`Edit`
