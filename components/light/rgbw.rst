RGBW Light
==========

.. seo::
    :description: Instructions for setting up RGB + White-Channel lights.
    :image: rgbw.png

The ``rgbw`` light platform creates an RGBW light from 4 :ref:`float output components <output>` (one for each channel).

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: rgbw
        name: "Livingroom Lights"
        red: output_component1
        green: output_component2
        blue: output_component3
        white: output_component4

Color Correction
----------------

It is often favourable to calibrate/correct the color produced by an LED strip light as the
perceived intensity of different colors will generally vary. This can be done by using
:ref:`max_power <config-output>` on individual output channels:

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: rgbw
        name: "Livingroom Lights"
        red: output_component1
        green: output_component2
        blue: output_component3
        white: output_component4

    # Example output entry
    output:
      - platform: esp8266_pwm
        id: output_component1
        pin: D1
        max_power: 80%

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **red** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the red channel.
- **green** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the green channel.
- **blue** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the blue channel.
- **white** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the white channel.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.
- **color_interlock** (*Optional*, boolean): When enabled, this will prevent white leds being on at the same
  time as RGB leds. See :ref:`rgbw_color_interlock` for more information. Defaults to ``false``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Light <config-light>`.

.. _rgbw_color_interlock:

Color Interlock
***************

With some LED bulbs, it is not possible to enable the RGB leds at the same time as the white leds, or setting
the RGB channels to maximum whilst wanting a white light will have an undesired hue effect. For these cases a
configuration variable is available that prevents the RGB leds and white leds from being turned on at the same
time: ``color_interlock``.

Setting this variable to ``true`` will automatically turn off the RGB leds when the white value is non-zero, or
when the color is set to white (equal values for red, green and blue). When a different color is set, or the
color brightness is raised above 0%, the white leds are automatically turned off.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/light/index`
- :doc:`/components/light/cwww`
- :doc:`/components/light/color_temperature`
- :doc:`/components/light/rgb`
- :doc:`/components/light/rgbww`
- :doc:`/components/light/rgbct`
- :doc:`/components/power_supply`
- :doc:`/components/output/ledc`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/output/pca9685`
- :doc:`/components/output/tlc59208f`
- :doc:`/components/output/my9231`
- :doc:`/components/output/sm16716`
- :apiref:`rgbw/rgb_light_output.h`
- :ghedit:`Edit`
