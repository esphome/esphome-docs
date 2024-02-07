RP2040 PIO LED Strip
====================

.. seo::
    :description: Instructions for setting up addressable lights like NEOPIXEL on an RP2040 using the PIO peripheral.
    :image: color_lens.svg

This is a component using the RP2040 PIO peripheral to drive most addressable LED strips.

.. code-block:: yaml

    light:
      - platform: rp2040_pio_led_strip
        name: led_strip
        id: led_strip
        pin: GPIO13
        num_leds: 10
        pio: 0
        rgb_order: GRB
        chipset: WS2812B

Configuration variables
-----------------------

- **pin** (**Required**, :ref:`config-pin`): The pin for the data line of the light.
- **num_leds** (**Required**, int): The number of LEDs in the strip.
- **pio** (**Required**, int): The PIO peripheral to use. If using multiple strips, you can use up to 4 strips per PIO. Must be one of ``0`` or ``1``.

- **chipset** (**Required**, enum): The chipset to apply known timings from.
    - ``WS2812``
    - ``WS2812B``
    - ``SK6812``
    - ``SM16703``

- **rgb_order** (**Required**, string): The RGB order of the strip.
    - ``RGB``
    - ``RBG``
    - ``GRB``
    - ``GBR``
    - ``BGR``
    - ``BRG``

- **is_rgbw** (*Optional*, boolean): Set to ``true`` if the strip is RGBW. Defaults to ``false``.

- All other options from :ref:`Light <config-light>`.


Manual Timings
**************

These can be used if you know the timings and your chipset is not set above. If you have a new specific chipset,
please consider adding support to the codebase and add it to the list above.

- **bit0_high** (*Optional*, :ref:`config-time`): The time to hold the data line high for a ``0`` bit.
- **bit0_low** (*Optional*, :ref:`config-time`): The time to hold the data line low for a ``0`` bit.
- **bit1_high** (*Optional*, :ref:`config-time`): The time to hold the data line high for a ``1`` bit.
- **bit1_low** (*Optional*, :ref:`config-time`): The time to hold the data line low for a ``1`` bit.

See Also
--------

- :doc:`/components/light/index`
- :doc:`/components/power_supply`
- :ghedit:`Edit`
