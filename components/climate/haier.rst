Haier Climate
=============

.. seo::
    :description: Instructions for setting up a Haier climate devices.
    :image: air-conditioner.svg

The `haier` climate platform creates a Haier climate device.
The component can be used to create replacement for original Hair AC WiFi modules KZW-W001, KZW-W002, ESP32-for-haier or to create new ESPHome based firmware for ESP32-for-haier module. This component implements two different protocols smartAir2 and hOn. If your AC is using KZW-W001 or KZW-W002 module you should select smarAir2 protocol, if your AC is using ESP32-for-haier - use hOn protocol.

This component requires a :ref:`uart` to be setup.

.. code-block:: yaml

  uart:
    baud_rate: 9600
    tx_pin: 17
    rx_pin: 16
    id: haier_ac_uart

  climate:
    - platform: haier
      id: haier_ac_climate
      protocol: hOn               # Required, should be hOn or smartAir2 (not all features supported by smartAir2)
      name: ${device_name} 
      uart_id: haier_ac_uart
      wifi_signal: true           # Optional, not supported by smartAir2, enables WiFI signal transmission from ESP to AC
      beeper: true                # Optional, not supported by smartAir2, disables beep on commands from ESP
      outdoor_temperature:        # Optional, not supported by smartAir2, outdoor temperature sensor
        name: ${device_name} outdoor temperature
      visual:                     # Optional, can be used to limit min and max temperatures in UI (not working for remote!)
        min_temperature: 16 °C
        max_temperature: 30 °C
        temperature_step: 1 °C
      supported_modes:            # Optional, can be used to disable some modes
      - 'OFF'                     # always available
      - AUTO                      # always available
      - COOL
      - HEAT
      - DRY
      - FAN_ONLY
      supported_swing_modes:      # Optional, can be used to disable some swing modes if your AC does not support it
      - 'OFF'                     # always available
      - VERTICAL                  # always available
      - HORIZONTAL
      - BOTH

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation
- **uart_id** (*Optional*, :ref:`config-id`): ID of the UART port to communicate with AC
- **protocol** (**Required**, string): Defines protocol of communication with AC. Possible values: hon or smartair2
- **name** (**Required**, string): The name of the climate device
- **wifi_signal** (*Optional*, boolean): If true - send wifi signal level to AC (not supported by smartAir2 protocol)
- **beeper** (*Optional*, boolean): Can be used to disable beeping on commands from AC (not supported by smartAir2 protocol)
- **outdoor_temperature** (*Optional*): Temperature sensor for outdoor temperature (not supported by smartAir2 protocol)
  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional*, :ref:`config-id`): ID of the sensor, can be used for code generation
  - All other options from :ref:`Sensor <config-sensor>`.
- **supported_modes** (*Optional*, list): Can be used to disable some AC modes. Possible values: 'OFF', AUTO, COOL, HEAT, DRY, FAN_ONLY (first 2 always available)
- **supported_swing_modes** (*Optional*, list): Can be used to disable some swing modes if AC does not support it. Possible values: 'OFF', VERTICAL, HORIZONTAL, BOTH (first 2 always available)
- All other options from :ref:`Climate <config-climate>`.

Automations
-----------

``climate.haier.display_on`` Action
***********************************

This action turns the AC display on

.. code-block:: yaml

    on_...:
      then:
        climate.haier.display_on: device_id

``climate.haier.display_off`` Action
************************************

This action turns the AC display off

.. code-block:: yaml

    on_...:
      then:
        climate.haier.display_off: device_id

``climate.haier.beeper_on`` Action
**********************************

This action enables beep feedback on every command sent to AC

.. code-block:: yaml

    on_...:
      then:
        climate.haier.beeper_on: device_id


``climate.haier.beeper_off`` Action
***********************************

This action disables beep feedback on every command sent to AC (keep in mind that this will not work for IR remote commands)

.. code-block:: yaml

    on_...:
      then:
        climate.haier.beeper_off: device_id


``climate.haier.set_vertical_airflow`` Action
*********************************************

Set direction for vertical airflow if the vertical swing is disabled. Possible values: Up, Center, Down.

.. code-block:: yaml

    on_value:
      then:
        - climate.haier.set_vertical_airflow:
          id: device_id
          vertical_airflow: Up


``climate.haier.set_horizontal_airflow`` Action
***********************************************

Set direction for horizontal airflow if the horizontal swing is disabled. Possible values: Left, Center, Right.

.. code-block:: yaml

    on_value:
      then:
        - climate.haier.set_horizontal_airflow:
          id: device_id
          vertical_airflow: Right


Hardware setup for smartAir2 ACs
--------------------------------

Most units will have a dedicated USB-A port for Haier WiFi module.
The physical USB port is in fact UART and does not "speak" USB protocol.
It uses four USB pins as 5V, GND, RX, TX. 
You can use spare male USB cable to connect esphome device directly to the climate appliance.

Other units will not have USB ports, but will still probably have UART exposed somewhere on the main board. 

.. list-table:: Haier UART pinout
    :header-rows: 1

    * - Board
      - USB
      - Wire color
      - ESP8266
    * - 5V
      - VCC
      - red
      - 5V
    * - GND
      - GND
      - black
      - GND
    * - TX
      - DATA+
      - green
      - RX
    * - RX
      - DATA-
      - white
      - TX

.. figure:: images/usb_pinout.png
    :align: center
    :width: 70.0%

    USB Pinout

Hardware setup for hOn ACs
--------------------------

To flash the firmware you will need to use a USB to TTL converter and solder wires to access UART0 on board (or use some Pogo Pin Probe Clip)

**UART0 pinout:**
.. figure:: images/haier_pinout.png
    :align: center
    :width: 70.0%

To put the device in the flash mode you will need to shortcut GPIO0 to the ground before powering the device.

Once the device is in flash mode you can make a full backup of the original firmware in case you would like to return the module to its factory state. To make a backup you can use [esptool](https://github.com/espressif/esptool). Command to make a full flash backup: 

**python esptool.py -b 115200 --port <port_name> read_flash 0x00000 0x400000 flash_4M.bin**

After this, you can flash firmware using ESPHome tools (dashboard, website, esphome command, etc)

See Also
--------

- `esphaier <https://github.com/MiguelAngelLV/esphaier>`__
- `ESP32-S0WD-Haier <https://github.com/paveldn/ESP32-S0WD-Haier>`__
- :doc:`/components/climate/index`
- :ghedit:`Edit`
