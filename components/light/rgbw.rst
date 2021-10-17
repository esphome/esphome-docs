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

.. note::

    Remember that ``gamma_correct`` is enabled by default (``γ=2.8``), and you may want take it into account for the calibration. For instance if you command a light to *50%* brightness and want it to be the new maximum: ``max_PWM_power = max_light_power^2.8 = 0.5^2.8 = 0.144``, then you would set ``max_power`` to *14.4%*.

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

With some LED bulbs, setting the RGB channels to maximum whilst wanting a white light will have an undesired
hue affect. Additionally, the brightness command may not work as expected depending upon configuration,
leaving users to adjust the white component level separately. For these cases a new configration variable
has been added: color_interlock.

Setting this variable to True will turn off RGB leds when white value is above 0 (or if they are to 255,255,255)
and turn off white leds if color is not set to 255,255,255. This also allows the brightness parameter to
control the intensity of the white leds.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/light/index`
- :doc:`/components/light/rgb`
- :doc:`/components/power_supply`
- :doc:`/components/output/ledc`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/output/pca9685`
- :doc:`/components/output/tlc59208f`
- :doc:`/components/output/my9231`
- :doc:`/components/output/sm16716`
- :apiref:`rgbw/rgb_light_output.h`
- :ghedit:`Edit`
