NeoPixelBus Light
=================

.. seo::
    :description: Instructions for setting up Neopixel addressable lights.
    :image: color_lens.svg

.. warning::

    NeoPixelBus does **not** work with ESP-IDF.

    For clockless lights, you can use :doc:`esp32_rmt_led_strip`, and for SPI LEDs see :doc:`spi_led_strip`.


The ``neopixelbus`` light platform allows you to create RGB lights
in ESPHome for individually addressable lights like NeoPixel or WS2812.

It is very similar to the :doc:`fastled` platform.
In fact, most addressable lights are supported through both light platforms. The
difference is that they use different libraries: while the fastled platform uses
the `FastLED <https://github.com/FastLED/FastLED>`__ library, this component uses
the `NeoPixelBus <https://github.com/Makuna/NeoPixelBus/>`__ library internally.

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: neopixelbus
        type: GRB
        variant: WS2811
        pin: GPIOXX
        num_leds: 60
        name: "NeoPixel Light"

Configuration variables:
------------------------

**Base Options:**

- **num_leds** (**Required**, int): The number of LEDs attached.

**Type Options:**

- **type** (*Optional*, string): The type of light. This is used to specify
  if it is an RGBW or RGB light and in which order the colors are. Defaults to
  ``GRB``. Change this if you have lights with white channel and/or the colors are in the wrong order.
- **variant** (**Required**, string): The chipset of the light.

  The following options are supported:

  - ``800KBPS`` (generic option, recommended for chipsets without explicit support)
  - ``400KBPS``
  - ``WS2811``
  - ``WS2812``
  - ``WS2812X``
  - ``WS2813``
  - ``SK6812``
  - ``TM1814``
  - ``TM1829``
  - ``TM1914``
  - ``APA106``
  - ``LC8812``

  Additionally the following two-wire chipsets (set ``data_pin`` and ``clock_pin``)
  are supported:

  - ``WS2801``
  - ``DotStar``
  - ``LPD6803``
  - ``LPD8806``
  - ``P9813``

- **method** (*Optional*, string): The method used to transmit the data. By default, ESPHome will try to use the best method
  available for this chipset, ESP platform, and the given pin. See :ref:`methods <neopixelbus-methods>` for more information.

- **invert** (*Optional*, boolean): Invert data output, for use with n-type transistors. Defaults to ``no``.

**Pin Options:**

Some chipsets have two data pins to connect, others only have one.
If you have one line, only specify ``pin``, otherwise specify both ``clock_pin`` and ``data_pin``.

- **pin** (**Required**, :ref:`config-pin`): The pin for the data line of the light.
- **clock_pin** (**Required**, :ref:`config-pin`): The pin for the clock line of the light, for two-wire lights.
- **data_pin** (**Required**, :ref:`config-pin`): The pin for the data line of the light, for two-wire lights.

- All other options from :ref:`Light <config-light>`.

.. warning::

    On ESP8266 it's highly recommended to connect the light strip to pin
    GPIO3 to reduce flickering.

.. _neopixelbus-methods:

Methods
-------

NeoPixelBus supports different methods to transmit the pixel data to the light strip depending
on the chipset, ESP platform and pin.

Each of these has their own advantages/disadvantages regarding stability and speed. By default
ESPHome will choose the best one that is available on the device. However, you can override this
by manually supplying the ``method`` option.

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

- **bit_bang**: The simplest method and available on all platforms. However, it can produce quite a bit of flickering,
  and so is not recommended for use. On ESP8266, supports pins GPIO0-GPIO15, on ESP32 pins GPIO0-GPIO31.

- **esp8266_dma**: The recommended method for ESP8266s. Only available on pin GPIO3.

- **esp8266_uart**: An alternative method for ESP8266s that uses the UART peripheral to send data.
  Available on pin GPIO1 for bus 0, and GPIO2 for bus 1. Additional options:

  - **bus** (*Optional*, int): The UART bus to use. If 0, the logger ``baud_rate`` option must
    be set to 0 and logs over USB/serial won't work.
  - **async** (*Optional*, boolean): Use an asynchronous transfer. Defaults to ``false``. If enabled,
    the logger must be disabled even if bus 1 is used.

- **esp32_i2s**: The recommended method for ESP32, but not available on the ESP32-S3 or ESP32-C3.
  Available on all output pins. Additional options:

  - **bus** (*Optional*): The I2S bus to use. The ESP32 has bus 0 or 1 available, but the ESP32-S2 only bus 0.
    One of ``0``, ``1``, ``dynamic``.

- **esp32_rmt**: An alternative method for ESP32 that uses the RMT peripheral to send data.
  Available on all output pins. Additional options:

  - **channel** (*Optional*): The RMT channel to use. The ESP32 has channels 0-7, ESP32-S2 0-3, ESP32-S3 0-3, and ESP32-C3 0-1.
    Defaults to 6 on ESP32, and 1 on other ESP32 variants.

The following method is available only for two-wire chips (specify ``data_pin`` and ``clock_pin``):

- **spi**: Uses the hardware SPI interface to transmit the data. Available on both ESP platforms.
  Additional options:

  - **bus** (*Optional*, string): On ESP32s the SPI bus to be used can be selected. One of ``vspi`` and ``hspi``.
  - **speed** (*Optional*, int): The frequency to send data with. Defaults to ``10MHz``. One of
    ``40MHz``, ``20MHz``, ``10MHz``, ``5MHz``, ``2MHz``, ``1MHz``, ``500KHz``.

  On ESP8266 only GPIO13 can be used for ``data_pin`` and only GPIO14 can be used for ``clock_pin``.

The ``method`` key also accepts a short-hand syntax consisting of a single value for historic reasons. Usage of
this method is no longer recommended, but documented here for reference purposes. Possible values were:

- ``ESP8266_DMA`` (for ``esp8266_dma``)
- ``ESP8266_UART0`` (for ``esp8266_uart`` on bus 0)
- ``ESP8266_UART1`` (for ``esp8266_uart`` on bus 1)
- ``ESP8266_ASYNC_UART0`` (for ``esp8266_uart`` on bus 0 with async enabled)
- ``ESP8266_ASYNC_UART1`` (for ``esp8266_uart`` on bus 1 with async enabled)
- ``ESP32_I2S_0`` (for ``esp32_i2s`` on bus 0)
- ``ESP32_I2S_1`` (for ``esp32_i2s`` on bus 1)
- ``BIT_BANG`` (for ``bit_bang``)

See Also
--------

- :doc:`/components/light/index`
- :doc:`/components/light/fastled`
- :doc:`/components/power_supply`
- :apiref:`neopixelbus/neopixelbus_light.h`
- `NeoPixelBus library <https://github.com/Makuna/NeoPixelBus/wiki/ESP8266-NeoMethods>`__
- :ghedit:`Edit`
