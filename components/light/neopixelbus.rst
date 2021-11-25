NeoPixelBus Light
=================

.. seo::
    :description: Instructions for setting up Neopixel addressable lights.
    :image: color_lens.png

The ``neopixelbus`` light platform allows you to create RGB lights
in ESPHome for an individually addressable lights like NeoPixel or WS2812.

It is very similar to the :doc:`fastled` platform.
In fact, most addressable lights are supported through both light platforms. The
difference is that they use different libraries: While the fastled platform uses
the `FastLED <https://github.com/FastLED/FastLED>`__ library, this integration uses
the `NeoPixelBus <https://github.com/Makuna/NeoPixelBus/>`__ library internally.

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: neopixelbus
        type: GRB
        variant: 800KBPS
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
- **variant** (**Required**, string): The chipset variant. You can read more about these
  `here <https://github.com/Makuna/NeoPixelBus/wiki/NeoPixelBus-object#neo-methods>`__.
  One of these values:

  - ``800KBPS`` (recommended, unless the chip you're using is listed below)
  - ``400KBPS``
  - ``DotStar``
  - ``APA106``
  - ``LC8812``
  - ``LPD8806``
  - ``LPD6803``
  - ``P9813``
  - ``SK6812``
  - ``TM1814``
  - ``TM1829``
  - ``TM1914``
  - ``WS2801``
  - ``WS2811``
  - ``WS2812``
  - ``WS2812X``
  - ``WS2813``

- **method** (*Optional*, string): The method used to transmit the data.

  - **type** (*Optional*, string): One of ``bit_bang``, ``spi``, ``esp8266_uart``, ``esp8266_dma``, ``esp32_rmt`` or ``esp32_i2s``. By default a method suitable for your ESP, chip and used pins is chosen. You can read more about these methods for the `ESP32 <https://github.com/Makuna/NeoPixelBus/wiki/ESP32-NeoMethods>`__ and  `ESP8266 <https://github.com/Makuna/NeoPixelBus/wiki/ESP8266-NeoMethods>`__.
  
    - ``bit_bang``: Use bit-banging. This is slow and can cause flicker, but is always available.
    - ``spi``: Use the SPI bus. Only compatible with two-wire chips. On the ESP8266, must use pin GPIO13 (data) and GPIO14 (clock).
    - ``esp8266_uart``: Use the hardware UART on the ESP8266. Only compatible with one-wire chips. Must use either pin GPIO1 (bus 0) or GPIO2 (bus 1).
    - ``esp8266_dma``: Use the I2S DMA functionality on the ESP8266. Only compatible with one-wire chips. Must use pin GPIO3.
    - ``esp32_rmt``: Use the RMT module on the ESP32. Only compatible with one-wire chips. 
    - ``esp32_i2s``: Use the I2S module on the ESP32. Only compatible with one-wire chips. 
    
  Additional options for ``spi``:
    
    - **bus** (*Optional*, string): One of ``vspi`` or ``hspi``. Only on ESP32, defaults to ``vspi``.
    - **speed** (*Optional*, float): The frequency to use for the SPI bus. One of 500 kHz, 1 MHz, 2 MHz, 5 MHz, 10 MHz, 20 MHz or 40 MHz. Defaults to 10 MHz.
    
  Additional options for ``esp8266_uart``:
  
    - **bus** (*Optional*, integer): Bus to use, either 0 or 1. Defaults to 1.
    - **async** (*Optional*, boolean): Whether to send data asynchronously. Defaults to false.
    
  Additional options for ``esp32_rmt``:
  
    - **channel** (*Optional*, integer): RMT channel to use.
    
  Additional options for ``esp32_i2s``:
  
    - **bus** (*Optional*, integer): I2C bus number to use.
     
  Additionally, the following short-hand values are accepted for historic reasons:
  
    - ``BIT_BANG`` (for ``bit_bang``)
    - ``SPI`` (for ``spi`` on bus ``vspi``)
    - ``ESP8266_DMA`` (for ``esp8266_dma``)
    - ``ESP8266_UART0`` (for ``esp8266_uart`` on bus 0)
    - ``ESP8266_UART1`` (for ``esp8266_uart`` on bus 1)
    - ``ESP8266_ASYNC_UART0`` (for ``esp8266_uart`` on bus 0 with async enabled)
    - ``ESP8266_ASYNC_UART1`` (for ``esp8266_uart`` on bus 1 with async enabled)
    - ``ESP32_I2S_0`` (for ``esp32_i2s`` on bus 0)
    - ``ESP32_I2S_1`` (for ``esp32_i2s`` on bus 1)
    - ``ESP32_RMT_0`` (for ``esp32_rmt`` on channel 0)
    - ``ESP32_RMT_1`` (for ``esp32_rmt`` on channel 1)
    - ``ESP32_RMT_2`` (for ``esp32_rmt`` on channel 2)
    - ``ESP32_RMT_3`` (for ``esp32_rmt`` on channel 3)
    - ``ESP32_RMT_4`` (for ``esp32_rmt`` on channel 4)
    - ``ESP32_RMT_5`` (for ``esp32_rmt`` on channel 5)
    - ``ESP32_RMT_6`` (for ``esp32_rmt`` on channel 6)
    - ``ESP32_RMT_7`` (for ``esp32_rmt`` on channel 7)

- **num_leds** (**Required**, int): The number of LEDs attached.
- **invert** (*Optional*, boolean): Invert data output, for use with n-type transistor. Defaults to ``no``.  

**Pin Options:** Some chipsets have two data pins to connect, others only have one.
If you have one line, only specify ``pin``, otherwise specify both ``clock_pin`` and ``data_pin``.

- **pin** (**Required**, :ref:`config-pin`): The pin for the data line of the light.
- **clock_pin** (**Required**, :ref:`config-pin`): The pin for the clock line of the light, for two-pin lights.
- **data_pin** (**Required**, :ref:`config-pin`): The pin for the data line of the light, for two-pin lights.

**Advanced Options:**

- All other options from :ref:`Light <config-light>`.

See Also
--------

- :doc:`/components/light/index`
- :doc:`/components/light/fastled`
- :doc:`/components/power_supply`
- :apiref:`neopixelbus/neopixelbus_light.h`
- `NeoPixelBus library <https://github.com/Makuna/NeoPixelBus/wiki/ESP8266-NeoMethods>`__
- :ghedit:`Edit`
