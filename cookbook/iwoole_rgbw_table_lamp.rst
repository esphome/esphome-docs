IWOOLE Table Lamp
===================================

.. seo::
    :description: Instructions for flashing and configuring IWOOLE Table Lamps.

The IWOOLE Table Lamp is a RGBW lamp normally configured using the Tuya Smart App.
It is available from various retailers online or directly from `iwoole.com <https://www.iwoole.com/product/category/wifi-smart-table-lamp/>`__.

.. figure:: images/iwoole_rgbw_table_lamp.png
    :align: center
    :width: 50.0%

1. Device overview
------------------
.. note::
    The following information relates to the desk model depicted above. There are free-standing and a desk version with a longer arm versions available. They are likely to share the same internals and configuration, but it is not certain. 

My device had no external markings at all.

The device is a basic 4-channel PWM RGBW light in a simple elegant housing.
The LEDs are not individually addressable.
No other sensors, outputs or status LEDs are available.

The mosfets for the different color channels are connected as follows:

- GPIO04: White
- GPIO12: Green
- GPIO13: Blue
- GPIO14: Red

1.1 Internal markings
*************************
Foto's van binnen hier

2. ESPHome configuration
------------------------
Since there is only one RGBW light to configure the .yaml file is fairly straightforward.
Alternatively, you could configure each channel as a separate light if desired.
I prefer to use the ``color_interlock`` config option along with the configuration below. 

2.1 Example configuration
*************************
.. code-block:: yaml

    esphome:
      name: "IWOOLE Table Lamp"
      #ESP type is ESP8266EX with 1MB flash
      platform: ESP8266
      board: esp01_1m


    # Standard configuration
    wifi:
      ssid: "yourwifinetwork"
      password: "iamverysecure"
      ap:
        ssid: "IWOOLE Table Lamp Fallback Hotspot"
        password: "safefallbackpassword"
    captive_portal:
    logger:
    api:
      password: "ialwaysforgetthisone"
    ota:
      password: "enteryourownpasswordhere"


    # Start of device specific configuration
    light:
      - platform: rgbw
        name: "Light"
        red: output_red
        green: output_green
        blue: output_blue
        white: output_white

    output:
      - platform: esp8266_pwm
        id: output_red
        pin: GPIO14
      - platform: esp8266_pwm
        id: output_green
        pin: GPIO12
      - platform: esp8266_pwm
        id: output_blue
        pin: GPIO13
      - platform: esp8266_pwm
        id: output_white
        pin: GPIO4

3. Flashing
-----------
There are two ways to get ESPHome onto this device.
For both ways you will need to get the binary file with ESPHome's software by compiling your configuration and then downloading the binary.

3.1 Tuya-convert
***********
.. note::
    According to `blakadder.com <https://templates.blakadder.com/iwoole_table_lamp.html>`__ if you connect the device to the tuya smart app the firmware will upgrade and the device will not be flashable via this method anymore! 

Flashing 3 times

3.2 Serial connection
*********************
.. warning::
    The circuit inside will be exposed to mains voltage. Do not connect your device to the mains when flashing. Flashing this device via a serial connection will involve precarious soldering and cutting through insulating heat-shrink tubing which will have to be replaced. If you are uncomfortable with this, or are not confident around mains voltage, do not attempt to do this! Using the Tuya-convert method is preferred.

1. Disconnect the device from mains voltage!
2. Open the device. The plastic and aluminium halves can be separated by twisting the plastic part counter-clockwise. If you're okay with a few scuffs you can also use a screwdriver to seperate the two halves.
3. Remove the two screws holding the round plate with the LEDs. It is connected to the main PCB with a little cable. Make note of the orientation of this connection to ensure you reconnect it correctly later.
4. Carefully remove the heat-shrink tubing around the two main PCBs.
5. Solder the following wires onto the PCB

See Also
--------

- :doc:`/components/light/index`
- :doc:`/components/light/rgbw`
- :doc:`/components/output/index`
- :doc:`/components/output/esp8266_pwm`
- :ghedit:`Edit`
 
