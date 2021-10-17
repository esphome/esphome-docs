RGBWW Light
===========

.. seo::
    :description: Instructions for setting up RGBWW lights.
    :image: rgbw.png

The ``rgbww`` light platform creates an RGBWW (cold white + warm white)
light from 5 :ref:`float output components <output>` (one for each channel). The cold white
and warm white channels will be mixed using the color temperature configuration options.

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: rgbww
        name: "Livingroom Lights"
        red: output_component1
        green: output_component2
        blue: output_component3
        cold_white: output_component4
        warm_white: output_component5
        cold_white_color_temperature: 6536 K
        warm_white_color_temperature: 2000 K

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
- **cold_white** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the cold
  white channel.
- **warm_white** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the warm
  white channel.
- **cold_white_color_temperature** (**Required**, float): The color temperate (in
  `mireds <https://en.wikipedia.org/wiki/Mired>`__ or Kelvin) of the cold white channel.
- **warm_white_color_temperature** (**Required**, float): The color temperate (in
  `mireds <https://en.wikipedia.org/wiki/Mired>`__ or Kelvin) of the warm white channel.
- **constant_brightness** (*Optional*, boolean): When enabled, this will keep the overall brightness of the
  cold and warm white channels constant by limiting the combined output to 100% of a single channel. This
  reduces the possible overall brightness but is necessary for some power supplies that are not able to run
  both channels at full brightness at once. Defaults to ``false``.
- **color_interlock** (*Optional*, boolean): When enabled, this will prevent white leds being on at the same
  time as RGB leds. See :ref:`rgbw_color_interlock` for more information. Defaults to ``false``.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Light <config-light>`.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/light/index`
- :doc:`/components/light/rgb`
- :doc:`/components/light/rgbw`
- :doc:`/components/power_supply`
- :doc:`/components/output/ledc`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/output/pca9685`
- :doc:`/components/output/tlc59208f`
- :doc:`/components/output/my9231`
- :doc:`/components/output/sm16716`
- :apiref:`rgbww/rgbww_light_output.h`
- :ghedit:`Edit`
