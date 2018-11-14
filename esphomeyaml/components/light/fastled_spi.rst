FastLED SPI Light
=================

.. seo::
    :description: Instructions for setting up other FastLED addressable lights.
    :image: color_lens.svg

The ``fastled_spi`` light platform allows you to create RGB lights
in esphomelib for a :ref:`number of supported chipsets <fastled_spi-chipsets>`.

SPI FastLED lights differ from the
:doc:`fastled_clockless` in that they require two pins to be connected, one for a data and one for a clock signal
whereas the clockless lights only need a single pin.

.. figure:: images/fastled_spi-ui.png
    :align: center
    :width: 60.0%

.. code:: yaml

    # Example configuration entry
    light:
      - platform: fastled_spi
        chipset: WS2801
        data_pin: GPIO23
        clock_pin: GPIO22
        num_leds: 60
        rgb_order: BRG
        name: "FastLED SPI Light"

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **chipset** (**Required**, string): Set a chipset to use. See :ref:`fastled_spi-chipsets` for options.
- **data_pin** (**Required**, :ref:`config-pin`): The pin for the data line of the FastLED light.
- **clock_pin** (**Required**, :ref:`config-pin`): The pin for the clock line of the FastLED light.
- **num_leds** (**Required**, int): The number of LEDs attached.
- **rgb_order** (*Optional*, string): The order of the RGB channels. Use this if your
  light doesn't seem to map the RGB light channels correctly. For example if your light
  shows up green when you set a red color through the frontend. Valid values are ``RGB``,
  ``RBG``, ``GRB``, ``GBR``, ``BRG`` and ``BGR``. Defaults to ``RGB``.
- **max_refresh_rate** (*Optional*, :ref:`config-time`):
  A time interval used to limit the number of commands a light can handle per second. For example
  16ms will limit the light to a refresh rate of about 60Hz. Defaults to the default value for the used chipset.
- **gamma_correct** (*Optional*, float): The `gamma correction
  factor <https://en.wikipedia.org/wiki/Gamma_correction>`__ for the light. Defaults to ``2.8``.
- **color_correct** (*Optional*, list of percentages): The color correction for each channel. This denotes
  the maximum brightness of the red, green and blue channel. Defaults to ``color_correct: [100%, 100%, 100%]``.
- **default_transition_length** (*Optional*, :ref:`config-time`): The length of
  the transition if no transition parameter is provided by Home Assistant. Defaults to ``1s``.
- **power_supply** (*Optional*, :ref:`config-id`): The :doc:`/esphomeyaml/components/power_supply` to connect to
  this light. When the light is turned on, the power supply will automatically be switched on too.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`MQTT Component <config-mqtt-component>`.

.. _fastled_spi-chipsets:

Supported Chipsets
------------------

- ``APA102``
- ``DOTSTAR``
- ``LPD8806``
- ``P9813``
- ``SK9822``
- ``SM16716``
- ``WS2801``
- ``WS2803``

See Also
--------

- :doc:`/esphomeyaml/components/light/index`
- :doc:`/esphomeyaml/components/light/fastled_clockless`
- :doc:`/esphomeyaml/components/power_supply`
- :doc:`API Reference </api/light/fastled>`
- `Arduino FastLED library <https://github.com/FastLED/FastLED>`__
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/light/fastled_spi.rst>`__

.. disqus::
