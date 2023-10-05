Peacefair PZEM-004T V3 Energy Monitor
=====================================

.. seo::
    :description: Instructions for setting up PZEM-004T power monitors.
    :image: pzem-ac.jpg
    :keywords: PZEM-004T V3

.. note::

    This page is incomplete and could use some work. If you want to contribute, please read the
    :doc:`contributing guide </guides/contributing>`. This page is missing:

      - Images/screenshots/example configs of this device being used in action.

The ``pzemac`` sensor platform allows you to use PZEM-004T V3 energy monitors
(`website <https://innovatorsguru.com/pzem-004t-v3/>`__,
`datasheet <https://innovatorsguru.com/wp-content/uploads/2019/06/PZEM-004T-V3.0-Datasheet-User-Manual.pdf>`__)
with ESPHome.

The sensor can be connected in various configurations - please see the `manufacturer's website <https://innovatorsguru.com/pzem-004t-v3/>`__
for more information.

.. warning::

    Please note that metering chip inside of PZEM module is powered from AC side and it has to be on during startup of ESPHome device, othervise measure results won't be visible. 


.. figure:: images/pzem-ac.png
    :align: center
    :width: 80.0%

    PZEM-004T Version 3.

.. warning::

    This page refers to version V3 of the PZEM004T.
    For using the older V1 variant of this sensor please see :doc:`pzem004t <pzem004t>`.

The communication with this integration is done over a :ref:`UART bus <uart>` using :ref:`Modbus <modbus>`.
You must therefore have a ``uart:`` entry in your configuration with both the TX and RX pins set
to some pins on your board and the baud rate set to 9600.

.. code-block:: yaml

    # Example configuration entry
    uart:
      rx_pin: D1
      tx_pin: D2
      baud_rate: 9600

    modbus:

    sensor:
      - platform: pzemac
        current:
          name: "PZEM-004T V3 Current"
        voltage:
          name: "PZEM-004T V3 Voltage"
        energy:
          name: "PZEM-004T V3 Energy"
        power:
          name: "PZEM-004T V3 Power"
        frequency:
          name: "PZEM-004T V3 Frequency"
        power_factor:
          name: "PZEM-004T V3 Power Factor"
        update_interval: 60s

Configuration variables:
------------------------

- **current** (*Optional*): Use the current value of the sensor in amperes. All options from
  :ref:`Sensor <config-sensor>`.
- **energy** (*Optional*): Use the (active) energy value of the sensor in watt*hours. All options from
  :ref:`Sensor <config-sensor>`.
- **power** (*Optional*): Use the (active) power value of the sensor in watts. All options from
  :ref:`Sensor <config-sensor>`.
- **voltage** (*Optional*): Use the voltage value of the sensor in volts.
  All options from :ref:`Sensor <config-sensor>`.
- **frequency** (*Optional*): Use the frequency value of the sensor in hertz.
  All options from :ref:`Sensor <config-sensor>`.
- **power_factor** (*Optional*): Use the power factor value of the sensor.
  All options from :ref:`Sensor <config-sensor>`.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
- **address** (*Optional*, int): The address of the sensor if multiple sensors are attached to
  the same UART bus. You will need to set the address of each device manually. Defaults to ``1``.
- **modbus_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the Modbus hub.

.. _pzemac-reset_energy_action:

``pzemac.reset_energy`` Action
******************************

This action resets the total energy value of the pzemac device with the given ID when executed.

.. code-block:: yaml

    on_...:
      then:
        - pzemac.reset_energy: pzemac_1

Changing the address of a PZEM-004T:
------------------------------------

You can use the following configuration to change the address of a sensor.
You must set the ``address`` of the ``modbus_controller`` to the current address, and ``new_address`` of the ``on_boot`` lambda to the new one.

.. warning::

    This should be used only once! After changing the address, this code should be removed from the ESP before using the actual sensor code.

.. code-block:: yaml

    esphome:
      ...
      on_boot:
        ## configure controller settings at setup
        ## make sure priority is lower than setup_priority of modbus_controller
        priority: -100
        then:
          - lambda: |-
              auto new_address = 0x03;

              if(new_address < 0x01 || new_address > 0xF7) // sanity check
              {
                ESP_LOGE("ModbusLambda", "Address needs to be between 0x01 and 0xF7");
                return;
              }

              esphome::modbus_controller::ModbusController *controller = id(pzem);
              auto set_addr_cmd = esphome::modbus_controller::ModbusCommandItem::create_write_single_command(
                controller, 0x0002, new_address);

              delay(200) ;
              controller->queue_command(set_addr_cmd);
              ESP_LOGI("ModbusLambda", "PZEM Addr set");

    modbus:
      send_wait_time: 200ms
      id: mod_bus_pzem

    modbus_controller:
      - id: pzem
        # The current device address.
        address: 0x1
        # The special address 0xF8 is a broadcast address accepted by any pzem device,
        # so if you use this address, make sure there is only one pzem device connected
        # to the uart bus. 
        # address: 0xF8
        modbus_id: mod_bus_pzem
        command_throttle: 0ms
        setup_priority: -10
        update_interval: 30s

Complete example:
-----------------

A complete working example of a advanced energy monitoring node (here runnnig on a esp8266 - D1 Mini board), that can be integrated to HA, detailed comments included.
Configuration adopts internal sensors processing data from PZEM module, public sensors with pre-processed data (for HA), helper sensors with aggregated data, diagnostic sensors monitoring device status, and control buttons.

.. code-block:: yaml

    substitutions:
      name: my-powernode
      #board: esp01_1m
      board: d1_mini
    
    esphome:
      name: ${name}
      #friendly_name: 'Powernode'
      comment: 'PZEM-004T V3 Energy Meter'
    
    esp8266:
      board: ${board}
    
    # Enable logging
    logger:
    
    # Enable Home Assistant API
    api:
      encryption:
        key: "yourapikeyhere"
    
    ota:
      #password: "yourotapasswordhere"
    
    wifi:
      ssid: !secret wifi_ssid
      password: !secret wifi_password
      fast_connect: True
    
      # Enable fallback hotspot (captive portal) in case wifi connection fails
      ap:
        ssid: "Home-Powernode"
        #password: "yorufallbackpasswordhere"
    
    # fallback mechanism for when connecting to the configured WiFi fails
    # <see_esphome_web>/components/captive_portal.html
    captive_portal:
    
    # Web server to be able to consult information with a Web browser
    # <see_esphome_web>/components/web_server.html
    web_server:
      
    # We indicate the pin of the board's LED to blink according to its status
    # <see_esphome_web>/components/status_led.html
    status_led:
      pin:
        number: D4
        inverted: true
    
    # We indicate the pins where we have connected TX and RX of the device, taking into account that TX-> RX, RX-> TX must always be inverted
    uart:
      rx_pin: D2
      tx_pin: D1
      baud_rate: 9600
      # stop_bits is only necessary if indicated by the log while testing the circuit
      stop_bits: 1
    
    # enable Modbus
    modbus:
    
    # Need time for helper sensors
    # <see_esphome_web>/components/time.html
    time:
      - platform: sntp
        id: my_time
        timezone: "Europe/Bratislava" #change yours
    
    # ----- Sensors -----
    sensor:
      # --- Fast sensors (internal) for Energy calculation & local display
      # PZEM-004T V3
      # <see_esphome_web>/components/sensor/pzemac
      - platform: pzemac
        id: pzemac_1
        current:
          name: "PZEM Current"
          id: "pzem_current"
          internal: true
        voltage:
          name: "PZEM Voltage"
          id: "pzem_voltage"
          internal: true
        energy:
          name: "PZEM Energy"
          id: "pzem_energy"
          internal: true
          # convert it to kWh
          filters:
            - multiply: 0.001
          unit_of_measurement: 'kWh'
          accuracy_decimals: 3
        power:
          name: "PZEM Power"
          id: "pzem_power"
          internal: true
        frequency:
          name: "PZEM Frequency"
          id: "pzem_frequency"
          internal: true
        power_factor:
          name: "PZEM Power Factor"
          id: "pzem_power_factor"
          internal: true
        update_interval: 2s
    
      # --- Slow sensors (public) for Home Assistant
      - platform: template
        name: "Current"
        #id: "home_current"
        lambda: |-
          if (id(pzem_current).state) {
            return (id(pzem_current).state);
          } else {
            return 0;
          }
        unit_of_measurement: 'A'
        accuracy_decimals: 3
        state_class: measurement
        device_class: current
        icon: "mdi:alpha-a-circle"
        update_interval: 10s
      
      - platform: template
        name: "Voltage"
        #id: "home_voltage"
        lambda: |-
          if (id(pzem_voltage).state) {
            return (id(pzem_voltage).state);
          } else {
            return 0;
          }
        unit_of_measurement: 'V'
        accuracy_decimals: 3
        state_class: measurement
        device_class: voltage
        icon: "mdi:alpha-v-circle"
        update_interval: 10s
      
      - platform: template
        name: "Energy"
        #id: "home_energy"
        lambda: |-
          if (id(pzem_energy).state) {
            return (id(pzem_energy).state);
          } else {
            return 0;
          }
        unit_of_measurement: 'kWh' 
        accuracy_decimals: 4
        state_class: total_increasing
        device_class: energy
        icon: "mdi:counter"
        update_interval: 10s
      
      - platform: template
        name: "Power"
        #id: "home_power"
        lambda: |-
          if (id(pzem_power).state) {
            return (id(pzem_power).state);
          } else {
            return 0;
          }
        unit_of_measurement: 'W' 
        accuracy_decimals: 2
        state_class: measurement
        device_class: power
        icon: "mdi:alpha-w-circle"
        update_interval: 10s
      
      - platform: template
        name: "Frequency"
        #id: "home_frequency"
        lambda: |-
          if (id(pzem_frequency).state) {
            return (id(pzem_frequency).state);
          } else {
            return 0;
          }
        unit_of_measurement: 'Hz'
        state_class: measurement
        device_class: frequency
        icon: "mdi:alpha-f-circle"
        update_interval: 10s
    
      - platform: template
        name: "Power Factor"
        #id: "home_power_factor"
        lambda: |-
          if (id(pzem_power_factor).state) {
            return (id(pzem_power_factor).state);
          } else {
            return 0;
          }
        unit_of_measurement: '%'
        accuracy_decimals: 2
        state_class: measurement
        device_class: power_factor
        icon: "mdi:alpha-p-circle"
        update_interval: 10s
    
    # Helper sensors
      # <see_esphome_web>/components/sensor/total_daily_energy.html
      - platform: total_daily_energy
        name: "Total Daily Energy" #(sum for today)
        id: daily_energy_total
        power_id: pzem_power
        filters:
            # Multiplication factor from W to kW is 0.001
            - multiply: 0.001
        unit_of_measurement: kWh
        icon: mdi:counter
    
      # <see_esphome_web>/components/sensor/integration.html
      - platform: integration
        name: "Total Energy Running" #(sum since last restart)
        id: "running_energy_total"
        sensor: pzem_power
        time_unit: h
        filters:
         # Multiplication factor from W to kW is 0.001
          - multiply: 0.001
        unit_of_measurement: kWh
        icon: mdi:counter
    
    # General info sensors
      # Uptime sensor
      # <see_esphome_web>/components/sensor/uptime.html
      - platform: uptime
        name: "Uptime"
        id: "powernode_device_uptime"
        entity_category: "diagnostic"
    
      # WiFi Signal sensor
      # <see_esphome_web>/components/sensor/wifi_signal.html
      - platform: wifi_signal
        name: "WiFi Signal"
        id: "powernode_device_wifi_signal"
        update_interval: 60s
        entity_category: "diagnostic"
    
      - platform: copy # Reports the WiFi signal strength in %
        source_id: powernode_device_wifi_signal
        name: "WiFi Signal Percent"
        id: "powernode_device_wifi_signal_perc"
        filters:
          - lambda: return min(max(2 * (x + 100.0), 0.0), 100.0);
        unit_of_measurement: "%"
        entity_category: "diagnostic"
    
    # Status sensor
    # <see_esphome_web>/components/binary_sensor/status.html
    binary_sensor:
      - platform: status
        name: "Status"
        entity_category: "diagnostic"
    
    # ----- Buttons -----
    button:
      # restart button
      # <see_esphome_web>/components/button/restart
      - platform: restart
        name: "Device Restart"
        id: device_restart_button
    
      # restart button (safe mode)
      # <see_esphome_web>/components/button/safe_mode
      - platform: safe_mode
        name: "Device Restart (Safe Mode)"
        id: device_restart_safe_button
    
      # reset energy button
      # <see_esphome_web>/components/sensor/pzemac#pzemac-reset-energy-action
      - platform: template
        name: "Energy meter Reset"
        id: energy_reset_button
        icon: "mdi:restore"
        entity_category: "config"
        on_press:
          - pzemac.reset_energy: pzemac_1

See Also
--------

- :ref:`sensor-filters`
- :doc:`pzem004t`
- :doc:`pzemdc`
- :apiref:`pzemac/pzemac.h`
- :ghedit:`Edit`
