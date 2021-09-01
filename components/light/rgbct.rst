RGBCT Light
===========

.. seo::
    :description: Instructions for setting up RGBCT lights.
    :image: rgbw.png

The ``rgbct`` light platform creates an RGBWT (color temperature + white brightness)
light from 5 :ref:`float output components <output>` (one for each channel).

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: rgbct
        name: "Livingroom Lights"
        red: output_component1
        green: output_component2
        blue: output_component3
        color_temperature: output_component4
        white_brightness: output_component5
        cold_white_color_temperature: 153 mireds
        warm_white_color_temperature: 500 mireds

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **red** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the red channel.
- **green** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the green channel.
- **blue** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the blue channel.
- **color_temperature** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the
  color temperature channel.
- **white_brightness** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the brightness
  of the white leds.
- **cold_white_color_temperature** (**Required**, float): The coldest color temperature supported by this light. This
  is the lowest value when expressed in `mireds <https://en.wikipedia.org/wiki/Mired>`__, or the highest value when
  expressed in Kelvin.
- **warm_white_color_temperature** (**Required**, float): The warmest color temperature supported by this light. This
  is the highest value when expressed in `mireds <https://en.wikipedia.org/wiki/Mired>`__, or the lowest value when
  expressed in Kelvin.
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
- :doc:`/components/light/rgbww`
- :doc:`/components/power_supply`
- :doc:`/components/output/ledc`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/output/pca9685`
- :doc:`/components/output/tlc59208f`
- :doc:`/components/output/my9231`
- :doc:`/components/output/sm16716`
- :apiref:`rgbct/rgbct_light_output.h`
- :ghedit:`Edit`
