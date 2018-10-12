FastLED Clockless Light
=======================

The ``fastled_clockless`` light platform allows you to create RGB lights
in esphomelib for a :ref:`number of supported chipsets <fastled_clockless-chipsets>`.

Clockless FastLED lights differ from the
:doc:`fastled_spi` in that they only have a single data wire to connect, and not separate data and clock wires.

.. figure:: images/fastled_clockless-ui.png
   :align: center
   :width: 60.0%

.. code:: yaml

    # Example configuration entry
    light:
      - platform: fastled_clockless
        chipset: WS2811
        pin: GPIO23
        num_leds: 60
        rgb_order: BRG
        name: "FastLED WS2811 Light"

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **chipset** (**Required**, string): Set a chipset to use.
  See :ref:`fastled_clockless-chipsets` for options.
- **pin** (**Required**, :ref:`config-pin`): The pin for the data line of the FastLED light.
- **num_leds** (**Required**, int): The number of LEDs attached.
- **rgb_order** (*Optional*, string): The order of the RGB channels. Use this if your
  light doesn't seem to map the RGB light channels correctly. For example if your light
  shows up green when you set a red color through the frontend. Valid values are ``RGB``,
  ``RBG``, ``GRB``, ``GBR``, ``BRG`` and ``BGR``. Defaults to ``RGB``.
- **max_refresh_rate** (*Optional*, :ref:`config-time`):
  A time interval used to limit the number of commands a light can handle per second. For example
  16ms will limit the light to a refresh rate of about 60Hz. Defaults to the default value for the used chipset.
- **gamma_correct** (*Optional*, float): The `gamma correction
  factor <https://en.wikipedia.org/wiki/Gamma_correction>`__ for the
  light. Defaults to ``2.8``.
- **default_transition_length** (*Optional*, :ref:`config-time`): The length of
  the transition if no transition parameter is provided by Home
  Assistant. Defaults to ``1s``.
- **power_supply** (*Optional*, :ref:`config-id`): The :doc:`/esphomeyaml/components/power_supply` to connect to
  this light. When the light is turned on, the power supply will automatically be switched on too.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`MQTT Component <config-mqtt-component>`.

.. _fastled_clockless-chipsets:

Supported Chipsets
------------------

- ``NEOPIXEL``
- ``WS2811``
- ``WS2811_400`` (``WS2811`` with a clock rate of 400kHz)
- ``WS2812B``
- ``WS2812``
- ``WS2813``
- ``WS2852``
- ``APA104``
- ``APA106``
- ``GW6205``
- ``GW6205_400`` (``GW6205`` with a clock rate of 400kHz)
- ``LPD1886``
- ``LPD1886_8BIT`` (``LPD1886`` with 8-bit color channel values)
- ``PL9823``
- ``SK6812``
- ``SK6822``
- ``TM1803``
- ``TM1804``
- ``TM1809``
- ``TM1829``
- ``UCS1903B``
- ``UCS1903``
- ``UCS1904``
- ``UCS2903``

See Also
--------

- :doc:`/esphomeyaml/components/light/index`
- :doc:`/esphomeyaml/components/light/fastled_spi`
- :doc:`/esphomeyaml/components/power_supply`
- :doc:`API Reference </api/light/fastled>`
- `Arduino FastLED library <https://github.com/FastLED/FastLED>`__
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/light/fastled_clockless.rst>`__

.. disqus::
