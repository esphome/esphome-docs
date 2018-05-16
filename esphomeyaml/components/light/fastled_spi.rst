FastLED SPI Light
=================

The ``fastled_spi`` light platform allows you to create RGB lights
in esphomelib for a `number of supported chipsets <#supported-chipsets>`__.

SPI FastLED lights differ from the
`FastLED Clockless lights </esphomeyaml/components/light/fastled_clockless.html>`__ in that they require
two pins to be connected, one for a data and one for a clock signal whereas the clockless lights
only need a single pin.

|image0|

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
~~~~~~~~~~~~~~~~~~~~~~~~

-  **name** (**Required**, string): The name of the light.
-  **chipset** (**Required**, string): Set a chipset to use.
   See `Supported Chipset <#supported-chipsets>`__ for options.
-  **data_pin** (**Required**, `pin </esphomeyaml/configuration-types.html#pin>`__): The pin for
   the data line of the FastLED light.
-  **clock_pin** (**Required**, `pin </esphomeyaml/configuration-types.html#pin>`__): The pin for
   the clock line of the FastLED light.
-  **num_leds** (**Required**, int): The number of LEDs attached.
-  **rgb_order** (*Optional*, string): The order of the RGB channels. Use this if your
   light doesn't seem to map the RGB light channels correctly. For example if your light
   shows up green when you set a red color through the frontend. Valid values are ``RGB``,
   ``RBG``, ``GRB``, ``GBR``, ``BRG`` and ``BGR``. Defaults to ``RGB``.
-  **max_refresh_rate** (*Optional*, `time </esphomeyaml/configuration-types.html#time>`__):
   A time interval used to limit the number of commands a light can handle per second. For example
   16ms will limit the light to a refresh rate of about 60Hz. Defaults to the default value for the used chipset.
-  **gamma_correct** (*Optional*, float): The `gamma correction
   factor <https://en.wikipedia.org/wiki/Gamma_correction>`__ for the
   light. Defaults to ``2.8``.
-  **default_transition_length** (*Optional*,
   `time </esphomeyaml/configuration-types.html#time>`__): The length of
   the transition if no transition parameter is provided by Home
   Assistant. Defaults to ``1s``.
-  **id** (*Optional*,
   `id </esphomeyaml/configuration-types.html#id>`__): Manually specify
   the ID used for code generation.
-  All other options from `MQTT
   Component </esphomeyaml/components/mqtt.html#mqtt-component-base-configuration>`__.

Supported Chipsets
~~~~~~~~~~~~~~~~~~

-  ``APA102``
-  ``DOTSTAR``
-  ``LPD8806``
-  ``P9813``
-  ``SK9822``
-  ``SM16716``
-  ``WS2801``
-  ``WS2803``

Light Effects
~~~~~~~~~~~~~

Currently, only a rainbow effect is supported. In the future, more light effects will be added
and supported out-of-the box. Creating custom effects is, however, quite easy with esphomelib.
See the `fastled example <https://github.com/OttoWinter/esphomelib/blob/master/examples/fastled.cpp>`__
in the esphomelib repository for a simple example.

|image1|

.. |image0| image:: /esphomeyaml/components/light/fastled_spi.png
    :class: align-center
    :width: 60.0%

.. |image1| image:: /esphomeyaml/components/light/fastled_effect.png
    :class: align-center
    :width: 30.0%
