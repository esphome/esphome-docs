Neopixelbus Light
=================

.. seo::
    :description: Instructions for setting up Neopixel addressable lights.
    :image: color_lens.png

The ``neopixelbus`` light platform allows you to create RGB lights
in esphomelib for a individually addressable lights like NeoPixel or WS2812.

It is very similar to the :doc:`fastled_clockless` and :doc:`fastled_spi` platforms;
in fact most addressable lights are supported through both light platforms. The
difference is that they use different libraries: While the fastled platforms use
the `FastLED <https://github.com/FastLED/FastLED>`__ library, this integration uses
the `NeoPixelBus <https://github.com/Makuna/NeoPixelBus/>`__ library internally.

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: neopixelbus
        type: GRB
        pin: GPIO23
        num_leds: 60
        name: "NeoPixel Light"

Configuration variables:
------------------------

**Base Options:**

- **name** (**Required**, string): The name of the light.
- **gamma_correct** (*Optional*, float): The `gamma correction
  factor <https://en.wikipedia.org/wiki/Gamma_correction>`__ for the
  light. Defaults to ``2.8``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **color_correct** (*Optional*, list of percentages): The color correction for each channel. This denotes
  the maximum brightness of the red, green, blue[, white] channel. Defaults to ``color_correct: [100%, 100%, 100%]``.
- **default_transition_length** (*Optional*, :ref:`config-time`): The length of
  the transition if no transition parameter is provided by Home
  Assistant. Defaults to ``1s``.
- **power_supply** (*Optional*, :ref:`config-id`): The :doc:`/esphomeyaml/components/power_supply` to connect to
  this light. When the light is turned on, the power supply will automatically be switched on too.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.
- All other options from :ref:`MQTT Component <config-mqtt-component>`.

**Type Options:**

- **type** (*Optional*, string): The type of light. This is used to specify
  if it is an RGBW or RGB light and in which order the colors are. Defaults to
  ``GRB``. Change this if you have lights with white value and/or the colors are in the wrong order.
- **variant** (*Optional*, string): The chipset variant. You can read more about these
  `here <https://github.com/Makuna/NeoPixelBus/wiki/NeoPixelBus-object#neopixel-led-model-specific-methods>`__
  (some of the info on that page is not entirely correct).
  One of these values:

  - ``800KBPS`` (default)
  - ``400KBPS``
  - ``WS2812X``
  - ``SK6812``
  - ``WS2813`` (same as ``WS2812X``)
  - ``WS2812`` (same as ``800KBPS``)
  - ``LC8812`` (same as ``SK6812``)

- **method** (*Optional*, string): The method to transmit the data with. You can read
  more about these here: `ESP32 <https://github.com/Makuna/NeoPixelBus/wiki/ESP32-NeoMethods>`__,
  `ESP8266 <https://github.com/Makuna/NeoPixelBus/wiki/ESP8266-NeoMethods>`__

  - ``ESP8266_DMA`` (default for ESP8266)
  - ``ESP8266_UART0``
  - ``ESP8266_UART1``
  - ``ESP8266_ASYNC_UART0``
  - ``ESP8266_ASYNC_UART1``
  - ``ESP32_I2S_0``
  - ``ESP32_I2S_1`` (default for ESP32)
  - ``BIT_BANG``

- **num_leds** (**Required**, int): The number of LEDs attached.

**Pin Options:** Some chipsets have two data pins to connect, others only have one.
If you have one line, only specify ``pin``, otherwise specify both ``clock_pin`` and ``data_pin``.

- **pin** (**Required**, :ref:`config-pin`): The pin for the data line of the light.
- **clock_pin** (**Required**, :ref:`config-pin`): The pin for the clock line of the light, for two-pin lights.
- **data_pin** (**Required**, :ref:`config-pin`): The pin for the data line of the light, for two-pin lights.

See Also
--------

- :doc:`/esphomeyaml/components/light/index`
- :doc:`/esphomeyaml/components/light/fastled_clockless`
- :doc:`/esphomeyaml/components/power_supply`
- :doc:`API Reference </api/light/neopixelbus>`
- `NeoPixelBus library <https://github.com/Makuna/NeoPixelBus/wiki/ESP8266-NeoMethods>`__
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/light/neopixelbus.rst>`__

.. disqus::
