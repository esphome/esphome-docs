Using With Sonoff Basic
=======================

.. seo::
    :description: Instructions for putting Sonoff basic devices into flash mode and installing esphomelib on them.
    :image: sonoff_basic.jpg

esphomeyaml can be used with Sonoff Basic. These devices are basically just
an ESP8266 chip with a relay to control the connection, a small button on the
front and a green LED light. 

.. figure:: images/sonoff_basic-full.jpg
    :align: center
    :width: 75.0%

    Sonoff Basic

This guide will not guide you through setting up your Sonoff Basic step-by-step. It just provide
a sample configuration. For detailed instructions, see :doc:`sonoff_s20`, as those devices are
pretty similar.

.. note::

    If you've previously installed Sonoff-Tasmota or ESPurna on your Sonoff Basic, you're in luck 😀
    esphomeyaml can generate a firmware binary which you can then upload via the
    web interface.

Sample configuration
--------------------

The Sonoff Basic is based on the ``ESP8266`` platform and is a subtype of the ``esp01_1m`` board.
With this information, you can also step through the esphomeyaml wizard (``esphomeyaml sonoff_basic.yaml wizard``)
if you don't want to use the sample configuration file from below.

If you go through the wizard, please make sure you manually set ``board_flash_mode`` to ``dout``
as seen below. The version of the uploader used by esphomeyaml should automatically detect that
the Sonoff Basic uses the ``dout`` SPI flash chip mode. But, as some users of other firmwares have
said that other flash modes can brick the device, it's always good to specify it explicitly.

Below you will find a table of all usable GPIO pins of the Sonoff Basic and a configuration file that
exposes all of the basic functions.

.. table::
    :class: no-center

    ================================================== ==================================================
    ``GPIO0``                                          Button (inverted)
    -------------------------------------------------- --------------------------------------------------
    ``GPIO1``                                          ``RX`` pin (C1 Pin 2)
    -------------------------------------------------- --------------------------------------------------
    ``GPIO3``                                          ``TX`` pin (C1 Pin 3)
    -------------------------------------------------- --------------------------------------------------
    ``GPIO12``                                         Relay
    -------------------------------------------------- --------------------------------------------------
    ``GPIO13``                                         Green LED (inverted)
    -------------------------------------------------- --------------------------------------------------
    ``GPIO14``                                         Optional Sensor (C1 Pin 5)
    ================================================== ==================================================

.. code-block:: yaml

    esphomeyaml:
      name: <NAME_OF_NODE>
      platform: ESP8266
      board: esp01_1m
      board_flash_mode: dout

    wifi:
      ssid: <YOUR_SSID>
      password: <YOUR_PASSWORD>

    mqtt:
      broker: <YOUR_MQTT_BROKER>
      username: <YOUR_USERNAME>
      password: <YOUR_PASSWORD>

    logger:

    ota:

    binary_sensor:
      - platform: gpio
        pin:
          number: GPIO0
          mode: INPUT_PULLUP
          inverted: True
        name: "Sonoff Basic Button"
      - platform: status
        name: "Sonoff Basic Status"

    switch:
      - platform: gpio
        name: "Sonoff Basic Relay"
        pin: GPIO12

    output:
      - platform: esp8266_pwm
        id: basic_green_led
        pin: 
          number: GPIO13
          inverted: True

    light:
      - platform: monochromatic
        name: "Sonoff Basic Green LED"
        output: basic_green_led

Now run ``esphomeyaml sonoff_basic.yaml compile`` to validate the configuration and
pre-compile the firmware.

.. note::

    After this step, you will be able to find the compiled binary under
    ``<NAME_OF_NODE>/.pioenvs/<NAME_OF_NODE>/firmware.bin``. If you're having trouble with
    uploading, you can also try uploading this file directly with other tools.

Or run the upload command if your device is connected to the serial interface:

.. code-block:: bash

    esphomeyaml sonoff_basic.yaml run

See Also
--------

- :doc:`sonoff`
- :doc:`sonoff_4ch`
- :doc:`sonoff_s20`
- `GPIO locations <https://github.com/arendst/Sonoff-Tasmota/wiki/GPIO-Locations>`__
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/devices/sonoff_basic.rst>`__

.. disqus::
