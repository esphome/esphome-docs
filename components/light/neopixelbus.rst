NeoPixelBus Light
=================

.. seo::
    :description: Instructions for setting up Neopixel addressable lights.
    :image: color_lens.png

The ``neopixelbus`` light platform allows you to create RGB lights
in ESPHome for an individually addressable lights like NeoPixel or WS2812.

It is very similar to the :doc:`fastled` platform.
in fact most addressable lights are supported through both light platforms. The
difference is that they use different libraries: While the fastled platform uses
the `FastLED <https://github.com/FastLED/FastLED>`__ library, this integration uses
the `NeoPixelBus <https://github.com/Makuna/NeoPixelBus/>`__ library internally.

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: neopixelbus
        type: GRB
        variant: WS2811
        pin: GPIO23
        num_leds: 60
        name: "NeoPixel Light"

Configuration variables:
------------------------

**Base Options:**

- **name** (**Required**, string): The name of the light.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.

**Type Options:**

- **type** (*Optional*, string): The type of light. This is used to specify
  if it is an RGBW or RGB light and in which order the colors are. Defaults to
  ``GRB``. Change this if you have lights with white value and/or the colors are in the wrong order.
- **variant** (**Required**, string): The chipset of the light.
  
  The following chipsets are supported:

  - ``ws2811``
  - ``ws2812``
  - ``ws2812x``
  - ``ws2813``
  - ``sk6812``
  - ``tm1814``
  - ``tm1829``
  - ``tm1914``
  - ``apa106``
  - ``lc8812``

  Additionally the following two-wire (set ``data_pin`` and ``clock_pin``) 
  chipsets are supported:

  - ``ws2801``
  - ``dotstar``
  - ``lpd6803``
  - ``lpd8806``
  - ``p9813``

- **method** (*Optional*, string): The method used to transmit the data. By default, ESPHome will try to use the best method 
  available for this chipset, ESP platform, and the given pin. See `methods <neopixelbus-methods>` for more information.

- **num_leds** (**Required**, int): The number of LEDs attached.
- **invert** (*Optional*, boolean): Invert data output, for use with n-type transistor. Defaults to ``no``.  

**Pin Options:** Some chipsets have two data pins to connect, others only have one.
If you have one line, only specify ``pin``, otherwise specify both ``clock_pin`` and ``data_pin``.

- **pin** (**Required**, :ref:`config-pin`): The pin for the data line of the light.
- **clock_pin** (**Required**, :ref:`config-pin`): The pin for the clock line of the light, for two-pin lights.
- **data_pin** (**Required**, :ref:`config-pin`): The pin for the data line of the light, for two-pin lights.

**Advanced Options:**

- All other options from :ref:`Light <config-light>`.

.. warning::

    On ESP8266 it's highly recommended to connect the light strip to pin
    GPIO3 to reduce flickering.

.. _neopixelbus-method:

Methods
-------

NeoPixelBus supports different methods to transmit the pixel data to the light strip depending
on the chipset, ESP platform and pin.

Each of these has their own advantages/disadvantages regarding stability & speed. So by default
ESPHome will choose the best one that is available on the device. However, you can override this
by manually supplying the method option.

.. code-block:: yaml

    light:
      - platform: neopixelbus
        # ...
        method:
          type: esp8266_uart
          bus: 0
          async: false

Use the ``type`` configuration variable to select the method used. The additional configuration
settings vary by method:

- **bit_bang**: The simplest method and available on all platforms. However it can produce quite a bit of flickering,
  and so is not recommended for use. On ESP8266, supports pins GPIO0-GPIO15, on ESP32 pins GPIO0-GPIO31.

- **esp8266_dma**: The recommended method for ESP8266s. Only available on pin GPIO3.

- **esp8266_uart**: An alternative method for ESP8266s that uses the UART peripheral to send data.
  Available on pin GPIO1 for bus 0, and GPIO2 for bus 1. Additional options:

  - **bus** (*Optional*, int): The UART bus to use. If 0, the logger ``baud_rate`` option must 
    be set to 0 and logs over USB/Serial won't work.
  - **async** (*Optional*, boolean): Use an asynchronous transfer. Defaults to ``false``. If enabled,
    the logger must be disabled even bus 1 is used.

- **esp32_i2s**: The recommended method for ESP32. Available on all output pins. Additional options:

  - **bus** (*Optional*): The i2s bus to use. ESP32 have bus 0 or 1 available, but ESP32S2 only bus 0.
    One of ``0``, ``1``, ``dynamic``.

- **esp32_rmt**: An alternative method for ESP32 that uses the RMT peripheral to send data.
  Available on all output pins. Additional options:

  - **channel** (*Optional*): The RMT channel to use. ESP32 have channels 0-7, ESP32S2 0-3 and ESP32C3 0-1.
    Defaults to 6 on ESP32, and 1 on other ESP32 variants.

The following method is available for two-wire chips (``data_pin`` and ``clock_pin``):

- **spi**: Uses the hardware SPI interface to transmit the data. Available on both ESP platforms.
  Additional options:

  - **bus** (*Optional*, string): On ESP32s the SPI bus to be used can be selected. One of ``vspi`` and ``hspi``.
  - **speed** (*Optional*, int): The frequency to send data with. Defaults to ``10MHz``. One of
    ``40MHz``, ``20MHz``, ``10MHz``, ``5MHz``, ``2MHz``, ``1MHz``, ``500KHz``.
  
  On ESP8266 only GPIO13 can be used for ``data_pin`` and only GPIO14 can be used for ``clock_pin``.

See Also
--------

- :doc:`/components/light/index`
- :doc:`/components/light/fastled`
- :doc:`/components/power_supply`
- :apiref:`neopixelbus/neopixelbus_light.h`
- `NeoPixelBus library <https://github.com/Makuna/NeoPixelBus/wiki/ESP8266-NeoMethods>`__
- :ghedit:`Edit`
