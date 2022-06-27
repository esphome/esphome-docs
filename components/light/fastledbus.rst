FastLED Bus Light
=================

.. seo::
    :description: Instructions for setting up FastLED as bus of light segments.
    :image: color_lens.svg

.. warning::

    FastLED Bus does **not** work as expected with Arduino 3 or newer for ESP8266.
    For now, you can either downgrade the arduino version or use :doc:`neopixelbus`.

    .. code-block:: yaml

        esp8266:
          framework:
            version: 2.7.4

    See these related issues:

    - https://github.com/FastLED/FastLED/issues/1322
    - https://github.com/FastLED/FastLED/issues/1264

.. _fastled-bus:

Bus
---

The ``fastled_bus`` light platform allows you to have a bus of e.g. P9813 or WS2811 chips.
Which could be groupd by using the standard light components like RGBCT or RGBWW or RGB into
segments. You have control over every channel and chip of the bus.

in ESPHome for a :ref:`number of supported chipsets <fastled_clockless-chipsets>`.

To use the ``fastled_bus`` you need to first define a bus. There are two bus types:

SPI:
****

Which is used for two wire chips like P9813 with DATA and CLOCK.

.. code-block:: yaml

    # SPI Bus example
    fastled_bus_spi:
        - id: spiBus
          chipset: P9813
          data_pin: D1
          clock_pin: D2
          num_chips: 2

Configuration variables:
************************

* **name** (**Required**, string): The name of the light.
* **chipset** (**Required**, string): Set a chipset to use.

* **data_pin** (**Required**, :ref:`config-pin`): The pin for the data line of the FastLED light.
* **clock_pin** (**Required**, :ref:`config-pin`): The pin for the clock line of the FastLED light.
* **num_chips** (**Required**, int): The number of Chips attached to the Bus.
* **chip_channels** (*Optional*, int, default 3): The number of channels per chip, if you use SK6812 set to four.
* **max_refresh_rate** (*Optional*, :ref:`config-time`):
  A time interval used to limit the number of commands a light can handle per second. For example
  16ms will limit the light to a refresh rate of about 60Hz. Defaults to the default value for the used chipset.
* **data_rate** (*Optional*, frequency): The data rate to use for shifting data to the light. Can help if you
  have long cables or slow level-shifters.
* **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _fastled_bus_spi-chipsets:

Supported Chipsets
******************

* ``APA102``
* ``DOTSTAR``
* ``LPD8806``
* ``P9813``
* ``SK9822``
* ``SM16716``
* ``WS2801``
* ``WS2803``

.. _fastled_bus_spi:

Clockless:
**********

Which is used for single wire chips like WS2811.

.. code-block:: yaml

    # Example configuration entry
    fastled_bus_clockless:
      - id: blaClock
        chipset: SK6812
        pin: GPIO18
        chip_channels: 4
        num_chips: 2

Configuration variables:
************************

- **name** (**Required**, string): The name of the light.
- **chipset** (**Required**, string): Set a chipset to use.
- **pin** (**Required**, :ref:`config-pin`): The pin for the data line of the FastLED light.
- **num_chips** (**Required**, int): The number of LEDs attached.
- **chip_channels** (*Optional*, int, default 3): The number of channels per chip, if you use SK6812 set to four.
- **max_refresh_rate** (*Optional*, :ref:`config-time`):
  A time interval used to limit the number of commands a light can handle per second. For example
  16ms will limit the light to a refresh rate of about 60Hz. Defaults to the default value for the used chipset.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _fastled_bus_clockless-chipsets:

Support Chipsets
****************

* ``NEOPIXEL``
* ``WS2811``
* ``WS2811_400`` (``WS2811`` with a clock rate of 400kHz)
* ``WS2812B``
* ``WS2812``
* ``WS2813``
* ``WS2852``
* ``APA104``
* ``APA106``
* ``GW6205``
* ``GW6205_400`` (``GW6205`` with a clock rate of 400kHz)
* ``LPD1886``
* ``LPD1886_8BIT`` (``LPD1886`` with 8**bit color channel values)
* ``PL9823``
* ``SK6812``
* ``SK6822``
* ``TM1803``
* ``TM1804``
* ``TM1809``
* ``TM1829``
* ``UCS1903B``
* ``UCS1903``
* ``UCS1904``
* ``UCS2903``
* ``SM16703``

.. _fastled_bus_clockless:

LightSetup
----------

To use the ``fastled_bus`` you need two more things. The Standard light Component like

- :doc:`/components/light/rgb`
- :doc:`/components/light/rgbw`
- :doc:`/components/light/rgbww`
- :doc:`/components/light/rgbct`

or every other components which maps to the :ref:`Float Output Component<output>`.

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: rgbww
        name: "Livingroom Lights"
        red: output_componentr
        green: output_componentg
        blue: output_componentb
        cold_white: output_componentc
        warm_white: output_componentw

The light component maps to the Output Component which is used to map to the ``Fastled Bus``.

The Output Mapping is Configured with ``fastled_bus`` platform:

.. code-block:: yaml

    # example Mapping to spiBus
    output:
    - platform: fastled_bus
      id: output_componentr
      bus: spiBus
      offset: 0
      num_chips: 2
      byte_offset: 0
      byte_distance: 6
    - platform: fastled_bus
      id: output_componentc
      bus: spiBus
      offset: 0
      num_chips: 2
      byte_offset: 1
      byte_distance: 6
    - platform: fastled_bus
      id: output_componentw
      bus: spiBus
      offset: 0
      num_chips: 2
      byte_offset: 2
      byte_distance: 6
    - platform: fastled_bus
      id: output_componentb
      bus: spiBus
      offset: 0
      num_chips: 2
      byte_offset: 3
      byte_distance: 6
    - platform: fastled_bus
      bus: spiBus
      id: output_componentg
      offset: 0
      num_chips: 2
      byte_offset: 5
      byte_distance: 6


The ``offset`` defines the chip offset in the bus where the mapping starts.
If you have e.g. six chips and you want to have a RGBWW light connected on
3rd and 4th chip you need to set the offset to 2. Then you need to define
on how many chips the output should applied in our case we need two chips
for one RGBWW (5channels) so we set num_chips to 2. If you use a offset and
num_chips combination which addresses more chips than defined in the bus
``bad`` things will happen(memory corruption).
You need to set the ``byte_offset`` which defines the channel in the chip.
Theses chips have typical 3 bytes (RGB). If you want to set the output to
the Blue Channel on the second chip set the offset to 5. If you have want
to replicate the state to multiple chips you set the ``byte_distance`` for
one chip to 3 or two chip configuration to 6.

Configuration variables:
************************

- **name** (**Required**, string): The name of the light.
- **bus** (**Required**, string): Define the id of the bus.
- **offset** (**Required**, int): Starting Chip in the bus.
- **num_chips** (**Required**, int): Numbers of chips in this segment of the bus.
- **channel_offset** (**Required**, int): channel offset.
- **repeat_distance** (**Optional**, int): channel distance for repeated
- All other options from :ref:`Output <output>`.

.. _fastled_bus-output:

See Also
--------

- :doc:`/components/light/rgb`
- :doc:`/components/light/rgbw`
- :doc:`/components/light/rgbww`
- :doc:`/components/light/rgbct`
- :ref:`Output <output>`
- :doc:`/components/light/index`
- :doc:`/components/power_supply`
- `Arduino FastLED library <https://github.com/FastLED/FastLED>`__
- :ghedit:`Edit`
