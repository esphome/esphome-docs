EPEVER® MPPT Solar Charge Controller Tracer-AN Series
=====================================================
.. seo::
    :description: ESPHome configuration for EPEVER® MPPT Solar Charge Controller Tracer-AN Series
    :image: images/mages/tracer-an.jpg
    :keywords: EPEVER Tracer

.. figure:: images/tracer-an.jpg
    :align: center
    :width: 50.0%

.. warning::

    Enabling all modbus registers will probably cause a stack overflow in main


Tested with Tracer-AN Series 10A/20A/30A/40A and XTRA Series 10A/20A/30A/40A.
Probably works for other EPEver MPPT controllers as well.


Below is the ESPHome configuration file that will get you up and running. This assumes you have a ``secret.yaml`` with ssid, password, api_password and ota_password keys.

.. code-block:: yaml

    substitutions:
      updates: 60s
      unique_id: solarstation

    esphome:
      name: ${unique_id}
      platform: ESP32
      board: esp32dev
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
              std::vector<uint16_t> battery_settings3 = {
                  0x0000,  // 906B Equalize Duration (min.) 0
                  0x0075   // 906C Boost Duration (aka absorb) 117 mins
              };
              esphome::modbus_controller::ModbusCommandItem set_battery1_command =
                  esphome::modbus_controller::ModbusCommandItem::create_write_multiple_command(controller, 0x9000, battery_settings1.size() ,
                                                                                              battery_settings1);
              //   esphome::modbus_controller::ModbusCommandItem set_battery2_command =
              //   esphome::modbus_controller::ModbusCommandItem::create_write_multiple_command(controller, 0x900A, battery_settings2.size() ,
              //                                                                              battery_settings2);

              esphome::modbus_controller::ModbusCommandItem set_battery3_command =
                  esphome::modbus_controller::ModbusCommandItem::create_write_multiple_command(controller, 0x906B, battery_settings3.size(),
                                                                                              battery_settings3);
              delay(200) ;
              controller->queue_command(set_battery1_command);
              delay(200) ;
              // controller->queue_command(set_battery2_command);
              // delay(200) ;
              controller->queue_command(set_battery3_command);
              ESP_LOGI("ModbusLambda", "EPSOLAR Battery set");

    wifi:
      ssid: !secret wifi_sid
      password: !secret wifi_password

    time:
      - platform: sntp
        id: sntp_time
        timezone: "CET-1CEST,M3.5.0,M10.5.0/3"
        servers: "pool.ntp.org"

    # Enable logging
    logger:
      level: DEBUG

    # Enable Home Assistant API
    api:
      password: !secret api_password
      reboot_timeout: 0s

    ota:
      password: !secret ota_password

    uart:
      id: mod_bus_uart
      tx_pin: 17
      rx_pin: 16
      baud_rate: 115200
      stop_bits: 1

    modbus:
      id: mod_bus1

    modbus_controller:
      - id: epever
        ## the Modbus device addr
        address: 0x1
        modbus_id: mod_bus1
        command_throttle: 0ms
        # ctrl_pin: 5    # if you need to set the driver enable (DE) pin high before transmitting data configure it here
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

          - id: rated_current_of_load
            name: "rated_current_of_load"
            address: 0x300E
            offset: 0
            unit_of_measurement: "A"
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            filters:
              - multiply: 0.01

          - id: pv_input_voltage
            name: "PV array input voltage"
            address: 0x3100
            offset: 0
            unit_of_measurement: "V" ## for any other unit the value is returned in minutes
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            filters:
              - multiply: 0.01

          - id: pv_input_current
            name: "PV array input current"
            address: 0x3100
            offset: 2
            unit_of_measurement: "A" ## for any other unit the value is returned in minutes
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 2
            filters:
              - multiply: 0.01

          - id: pv_input_power
            name: "PV array input power"
            address: 0x3100
            offset: 4
            unit_of_measurement: "W" ## for any other unit the value is returned in minutes
            modbus_functioncode: "read_input_registers"
            value_type: U_DWORD_R
            accuracy_decimals: 1
            register_count: 2
            filters:
              - multiply: 0.01

          - id: charging_voltage
            name: "Charging voltage"
            address: 0x3100
            offset: 8
            unit_of_measurement: "V" ## for any other unit the value is returned in minutes
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            register_count: 1
            filters:
              - multiply: 0.01

          - id: charging_current
            name: "Charging current"
            address: 0x3100
            offset: 10
            unit_of_measurement: "A" ## for any other unit the value is returned in minutes
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            register_count: 1
            filters:
              - multiply: 0.01

          - id: charging_power
            name: "Charging power"
            address: 0x3100
            offset: 12
            unit_of_measurement: "W" ## for any other unit the value is returned in minutes
            modbus_functioncode: "read_input_registers"
            value_type: U_DWORD_R
            accuracy_decimals: 1
            register_count: 2
            filters:
              - multiply: 0.01

          - id: load_voltage
            name: "Load voltage"
            address: 0x310C
            offset: 0x0
            unit_of_measurement: "V" ## for any other unit the value is returned in minutes
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            filters:
              - multiply: 0.01

          - id: load_current
            name: "Load Current"
            address: 0x310C
            offset: 0x2
            unit_of_measurement: "A" ## for any other unit the value is returned in minutes
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 2
            filters:
              - multiply: 0.01

          - id: load_power
            name: "Load power"
            address: 0x310C
            offset: 0x04
            unit_of_measurement: "W" ## for any other components
            address: 0x310C
            offset: 0xA
            unit_of_measurement: °C ## for any other unit the value is returned in minutes
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            filters:
              - multiply: 0.01

          - id: battery_soc
            name: "Battery SOC"
            address: 0x311A
            offset: 0
            unit_of_measurement: "%" ## for any other unit the value is returned in minutes
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 0

          - id: battery_volt_settings
            name: "Remote real voltage"
            address: 0x311D
            offset: 0
            unit_of_measurement: "°C" ## for any other unit the value is returned in minutes
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            filters:
              - multiply: 0.01

          - id: max_pv_voltage_today
            name: "Maximum PV voltage today"
            address: 0x3300
            offset: 0
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            unit_of_measurement: "V"
            filters:
              - multiply: 0.01

          - id: min_pv_voltage_today
            name: "Minimum PV voltage today"
            address: 0x3300
            offset: 2
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            unit_of_measurement: "V"
            filters:
              - multiply: 0.01

          - id: max_battery_voltage_today
            name: "Maximum battery voltage today"
            address: 0x3300
            offset: 4
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            unit_of_measurement: "V"
            filters:
              - multiply: 0.01

          - id: min_battery_today
            name: "Minimum battery voltage today"
            address: 0x3300
            offset: 6
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            unit_of_measurement: "V"
            filters:
              - multiply: 0.01

          - id: consumed_energy_today
            name: "Consumed energy today"
            address: 0x3300
            offset: 8
            register_count: 2
            modbus_functioncode: "read_input_registers"
            value_type: U_DWORD_R
            accuracy_decimals: 0
            unit_of_measurement: "Wh"
            filters:
              - multiply: 10.0

          - id: consumed_energy_month
            name: "Consumed Energy Month"
            address: 0x3300
            offset: 12
            register_count: 2
            modbus_functioncode: "read_input_registers"
            value_type: U_DWORD_R
            accuracy_decimals: 0
            unit_of_measurement: "Wh"
            filters:
              - multiply: 10.0

          - id: consumed_energy_year
            name: "Consumed energy year"
            address: 0x3300
            offset: 16
            register_count: 2
            modbus_functioncode: "read_input_registers"
            value_type: U_DWORD_R
            accuracy_decimals: 1
            unit_of_measurement: "kWh"
            filters:
              - multiply: 0.01

          - id: consumed_energy_total
            name: "Consumed energy total"
            address: 0x3300
            offset: 20
            register_count: 2
            modbus_functioncode: "read_input_registers"
            value_type: U_DWORD_R
            accuracy_decimals: 1
            unit_of_measurement: "kWh"
            filters:
              - multiply: 0.01

          - id: generated_energy_today
            name: "Generated energy today"
            address: 0x3300
            offset: 24
            register_count: 2
            modbus_functioncode: "read_input_registers"
            value_type: U_DWORD_R
            accuracy_decimals: 0
            unit_of_measurement: "Wh"
            on_value:
              then:
                - sensor.template.publish:
                    id: generated_charge_today
                    state: !lambda 'return x/12.0;'
            filters:
              - multiply: 10.0

          - id: generated_energy_month
            name: "Generated energy month"
            address: 0x3300
            offset: 28
            register_count: 2
            modbus_functioncode: "read_input_registers"
            value_type: U_DWORD_R
            accuracy_decimals: 0
            unit_of_measurement: "Wh"
            filters:
              - multiply: 10.0

          - id: generated_energy_year
            name: "Generated energy year"
            address: 0x3300
            offset: 32
            register_count: 2
            modbus_functioncode: "read_input_registers"
            value_type: U_DWORD_R
            accuracy_decimals: 1
            unit_of_measurement: "kWh"
            filters:
              - multiply: 0.01

          - id: generated_energy_total
            name: "Generated energy total"
            address: 0x3300
            offset: 36
            register_count: 2
            modbus_functioncode: "read_input_registers"
            value_type: U_DWORD_R
            accuracy_decimals: 1
            filters:
              - multiply: 0.01

          - id: co2_reduction
            name: "CO2 reduction"
            address: 0x3300
            offset: 40
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            unit_of_measurement: "kg"
            filters:
              - multiply: 1.0

          - id: battery_voltage
            name: "Battery voltage"
            address: 0x331A
            offset: 0
            modbus_functioncode: "read_input_registers"
            value_type: U_WORD
            accuracy_decimals: 1
            unit_of_measurement: "V"
            filters:
              - multiply: 0.01

          - id: battery_current
            name: "Battery current"
            address: 0x331A
            offset: 2
            modbus_functioncode: "read_input_registers"
            value_type: S_DWORD_R
            register_count: 2
            accuracy_decimals: 2
            unit_of_measurement: "A"
            filters:
              - multiply: 0.01
          #- id: battery_type
          #  address: 0x9000
          #  offset: 0
          #  name: "Battery Type"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD

          #- id: temperature_compensation_coefficient
          #  address: 0x9000
          #  offset: 4
          #  name: "Temperature compensation coefficient"
          #  unit_of_measurement: "mV/°C/2V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: high_voltage_disconnect
          #  address: 0x9000
          #  offset: 6
          #  name: "High Voltage disconnect"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: charging_limit_voltage
          #  address: 0x9000
          #  offset: 6
          #  name: "Charging limit voltage"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: over_voltage_reconnect
          #  address: 0x9000
          #  offset: 8
          #  name: "Over voltage reconnect"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: equalization_voltage
          #  address: 0x9000
          #  offset: 10
          #  name: "Equalization voltage"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: boost_voltage
          #  address: 0x9000
          #  offset: 12
          #  name: "Boost voltage"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: float_voltage
          #  address: 0x9000
          #  offset: 14
          #  name: "Float voltage"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: boost_reconnect_voltage
          #  address: 0x9000
          #  offset: 16
          #  name: "Boost reconnect voltage"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: low_voltage_reconnect
          #  address: 0x9000
          #  offset: 18
          #  name: "Low voltage reconnect"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: under_voltage_recover
          #  address: 0x9000
          #  offset: 20
          #  name: "Under voltage recover"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: under_voltage_reconect
          #  address: 0x9000
          #  offset: 22
          #  name: "Under voltage reconnect"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: under_voltage_waring
          #  address: 0x9000
          #  offset: 24
          #  name: "Under voltage warning"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: low_voltage_disconnect
          #  address: 0x9000
          #  offset: 26
          #  name: "Low voltage disconnect"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: discharging_limit_voltage
          #  address: 0x9000
          #  offset: 28
          #  name: "Discharging limit voltage"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: battery_temperature_warning_lower_limit
          #  address: 0x9018
          #  offset: 0
          #  name: "Battery temperature warning lower limit"
          #  unit_of_measurement: "°C"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: controller_inner_temperature_upper_limit
          #  address: 0x9018
          #  offset: 2
          #  name: "Controller inner temperature upper limit"
          #  unit_of_measurement: "°C"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: controller_inner_temperature_upper_limit
          #  address: 0x9018
          #  offset: 2
          #  name: "Controller inner temperature upper limit"
          #  unit_of_measurement: "°C"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: controller_inner_temperature_upper_limit_recover
          #  address: 0x9018
          #  offset: 4
          #  name: "Controller inner temperature upper limit recover"
          #  unit_of_measurement: "°C"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: dttv
          #  address: 0x901E
          #  offset: 0
          #  name: "Day Time Threshold Voltage"
          #  unit_of_measurement: "V"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: light_signal_startup_delay_time
          #  address: 0x901E
          #  offset: 2
          #  name: "Light signal startup delay time"
          #  unit_of_measurement: "mins"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: nttv
          #  address: 0x901E
          #  offset: 4
          #  name: "Light Time Threshold Voltage"
          #  unit_of_measurement: "mins"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: light_signal_close_delay_time
          #  address: 0x901E
          #  offset: 6
          #  name: "Light signal close delay time"
          #  unit_of_measurement: "mins"
          #  modbus_functioncode: read_holding_registers
          #  value_type: U_WORD
          #  filters:
          #    - multiply: 0.01

          #- id: load_controlling_modes
          #    # 0000H Manual Control
          #    # 0001H Light ON/OFF
          #    # 0002H Light ON+ Timer/
          #    # 0003H Time Control
          #  address: 0x903D
          #  offset: 0
          #  name: "Light Time Threshold Voltage"
          #  modbus_functioncode: read_holding_registers
          #  accuracy_decimals: 0
          #  value_type: U_WORD

          #- id: working_time_length_1
          #    # The length of load output timer1,
          #    # D15-D8,hour, D7-D0, minute
          #  address: 0x903D
          #  offset: 2
          #  name: "Working_time length 1"
          #  modbus_functioncode: read_holding_registers
          #  accuracy_decimals: 0
          #  value_type: U_WORD

          #- id: working_time_length_2
          #  address: 0x903D
          #  offset: 4
          #  name: "Working_time length 1"
          #  modbus_functioncode: read_holding_registers
          #  accuracy_decimals: 0
          #  value_type: U_WORD

          #- id: backlight_time
          #  address: 0x9063
          #  offset: 0
          #  name: "Backlight time"
          #  modbus_functioncode: read_holding_registers
          #  accuracy_decimals: 0
          #  unit_of_measurement: "s"
          #  value_type: U_WORD

          - id: length_of_night_minutes
            address: 0x9065
            internal: true
            offset: 0
            bitmask: 0xFF
            unit_of_measurement: "m" ## for any other unit the value is returned in minutes
            name: "Length of night-mins"
            modbus_functioncode: read_holding_registers
            value_type: U_WORD

          - id: length_of_night
            address: 0x9065
            offset: 0
            bitmask: 0xFF00
            unit_of_measurement: "m" ## for any other unit the value is returned in minutes
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

        switches:
          - id: manual_control_load
            modbus_functioncode: read_coils
            address: 2
            offset: 0
            name: "manual control the load"
            bitmask: 1

          - id: default_control_the_load
            modbus_functioncode: read_coils
            address: 2
            offset: 1
            name: "default control the load"
            bitmask: 1

          - id: enable_load_test
            modbus_functioncode: read_coils
            address: 2
            offset: 3
            name: "enable load test mode"
            bitmask: 1

          - id: force_load
            modbus_functioncode: read_coils
            address: 2
            offset: 4
            name: "Force Load on/off"
            bitmask: 1

          - id: clear_energy_stats
            modbus_functioncode: write_single_coil
            address: 0x14
            offset: 0
            name: "Clear generating  electricity statistic"
            bitmask: 1

        text_sensors:
          - name: "rtc_clock"
            id: rtc_clock
            internal: true
            modbus_functioncode: read_holding_registers
            address: 0x9013
            offset: 0
            register_count: 3
            raw_encode: HEXBYTES
            response_size: 6
            #                /*
            #                E20 Real time clock 9013 D7-0 Sec, D15-8 Min
            #                E21 Real time clock 9014 D7-0componentst16_t((minutes << 8) | seconds), uint16_t((day << 8) | hour),
                                                        uint16_t((year << 8) | month)};
                      // Create a modbus command item with the time information as the payload
                      esphome::modbus_controller::ModbusCommandItem set_rtc_command = esphome::modbus_controller::ModbusCommandItem::create_write_multiple_command(epever, 0x9013, 3, rtc_data);
                      // Submit the command to the send queue
                      epever->queue_command(set_rtc_command);
                      ESP_LOGI("ModbusLambda", "EPSOLAR RTC set to %02d:%02d:%02d %02d.%02d.%04d", hour, minutes, seconds, day, month, year + 2000);
                    }
                    char buffer[20];
                    // format time as YYYY-mm-dd hh:mm:ss
                    sprintf(buffer,"%04d-%02d-%02d %02d:%02d:%02d",y+2000,month_,d,h,m,s);
                    id(template_rtc).publish_state(buffer);

        update_interval: ${updates}

    text_sensor:
      - platform: template
        name: "RTC Time Sensor"
        id: template_rtc


    switch:
      - platform: modbus_controller
        modbus_controller_id: epever
        id: reset_to_fabric_default
        name: "Reset to Factory Default"
        modbus_functioncode: write_single_coil
        address: 0x15
        bitmask: 1

    sensor:
      - platform: wifi_signal
        name: "WiFi Signal"
        update_interval: ${updates}
    web_server:
      port: 80




See Also
--------

- :doc:`/components/modbus_controller`
- :ghedit:`Edit`
