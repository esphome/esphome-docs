ESP32 SPI LED Strip
===================

.. seo::
    :description: Instructions for setting up addressable lights like FASTLED on an ESP32 using the SPI bus.
    :image: color_lens.svg

This is a component using the ESP32 SPI bus to drive some addressable LED strips.

.. code-block:: yaml

    light:
      - platform: esp32_spi_led_strip
        name: "My Light"
        data_pin: GPIO40
        clock_pin: GPIO39
        num_leds: 1
        rgb_order: RGB
        max_refresh_rate: 50us

Configuration variables
-----------------------

- **data_pin** (**Required**, :ref:`config-pin`): The pin for the data line of the light.
- **clock_pin** (**Required**, :ref:`config-pin`): The pin for the clock line of the light.
- **num_leds** (**Required**, int): The number of LEDs in the strip.
- **rgb_order** (**Optional**, string): The RGB order of the strip. Default: RGB
    - ``RGB``
    - ``RBG``
    - ``GRB``
    - ``GBR``
    - ``BGR``
    - ``BRG``
- **max_refresh_rate** (*Optional*, :ref:`config-time`):
  A time interval used to limit the number of commands a light can handle per second. For example
  16ms will limit the light to a refresh rate of about 60Hz. Defaults to sending commands as quickly as
  changes are made to the lights.


Supported Chipsets
******************

- ``APA102``
- ``SK9822``

See Also
--------

- :doc:`/components/light/index`
- :doc:`/components/power_supply`
- :apiref:`esp32_spi_led_strip/led_strip.h`
- :ghedit:`Edit`
