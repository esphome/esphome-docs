Arlec Grid Connect Smart Plug
=============================

Arlec Grid Connect Smart Plugs are a tuya based smart plugs sold in Australia. 

.. figure:: images/arlec-grid-connect.jpg
    :align: center
    :width: 40.0%

These plugs can be flashed with a bit of work.

Flashing
--------

Prerequisites
*************

#. Before you begin you'll need:

#. Computer running Windows, Mac or Linux.
#. Serial to FTDI adapter. (Arduino can also be used.) 
#. Jumper wires.
#. Soldering iron. (can be done without but may be harder.)

Connections
***********

The Arlec Grid connect uses the TYWE2S Tuya module, which can easily be flashed with these connections.

Here is the pinout:

.. figure:: images/tywe2s.jpg
    :align: center
    :width: 50.0%

RX -- TX

TX -- RX

3.3v -- 3.3v

GND -- GND

IO0 -- GND (Only needs to be done at boot to enter flashing mode.)

If you are using an Arduino, connect the RST pin to GND to disable the microcontroller and only use as a flashing device.

More information on uploading to the TYWE2S can be found here: https://github.com/arendst/Sonoff-Tasmota/wiki/CE-Smart-Home---LA-WF3-Wifi-Plug-(TYWE2S)

Uploading
*********

Compile the firmware with the ESPHomeYAML code below. Download the Binary and use the .bin file that is downloaded when uploading.

Use any ESP8266 flashing tool. I used NodeMCU-PyFlasher.

Set the mode to DOUT as DIO and QIO will not work for the ESP8265 chip this device uses.

Make sure erase flash is on.

Configuration
-------------

.. code-block:: yaml

    esphome:
      name: arlec_grid_connect
      platform: ESP8266
      board: esp8285

    wifi:
      ssid: "SSID"
      password: "PASSWORD"

    # Enable logging
    logger:

    # Enable Home Assistant API
    api:

    ota:

    status_led:
      pin:
        number: GPIO13
        inverted: true

    binary_sensor:
      - platform: gpio
        pin:
          number: GPIO14
          mode: INPUT_PULLUP
          inverted: true
        id: button
        on_press:
          - switch.toggle: relay

    switch:
      - platform: gpio
        id: led
        pin:
          number: GPIO4
          inverted: true
      - platform: gpio
        id: relay
        name: "Arlec Grid Connect"
        pin: GPIO12
        on_turn_on:
          - switch.turn_on: led
        on_turn_off:
          - switch.turn_off: led
          
Adding to Home Assistant
------------------------

You can now add your smart plug to home assistant via the configurations page, look for 'ESPHome' under the Integrations option and click 'Configure'.

.. figure:: images/arlec-grid-connect-homeassistant.jpg
    :align: center
    :width: 50.0%

See Also
--------

- :doc:`/components/switch/index`
- :doc:`/components/binary_sensor/index`
- :doc:`/components/light/index`
- :doc:`/components/light/monochromatic`
- :doc:`/components/output/index`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/guides/automations`
- :ghedit:`Edit`
