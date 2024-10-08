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
      - platform: ...
        id: output_component1
        max_power: 80%

.. note::

    Remember that ``gamma_correct`` is enabled by default (``γ=2.8``), and you may want take it into account for the calibration. For instance if you command a light to *50%* brightness and want it to be the new maximum: ``max_PWM_power = max_light_power^2.8 = 0.5^2.8 = 0.144``, then you would set ``max_power`` to *14.4%*.

.. _rgbw_color_interlock:

Color Interlock
---------------

With some LED bulbs, it is not possible to enable the RGB leds at the same time as the white leds, or setting
the RGB channels to maximum whilst wanting a white light will have an undesired hue effect. For these cases a
configuration variable is available that prevents the RGB leds and white leds from being turned on at the same
time: ``color_interlock``.

Setting this option to ``true`` will result in the light having two color modes available, ``RGB`` and ``WHITE``.
When the ``RGB`` color mode is active, the white leds are turned off, and when the ``WHITE`` color mode is active,
the RGB leds are turned off. Switching between these modes can be done from the Home Assistant interface, or by using
the ``color_mode`` option of the :ref:`light control actions <light-turn_on_action>`.

Configuration variables:
------------------------

- **red** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the red channel.
- **green** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the green channel.
- **blue** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the blue channel.
- **white** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the white channel.
- **color_interlock** (*Optional*, boolean): When enabled, this will prevent white leds being on at the same
  time as RGB leds. See :ref:`rgbw_color_interlock` for more information. Defaults to ``false``.
- All other options from :ref:`Light <config-light>`.

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
