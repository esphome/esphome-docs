RGBWW Light
===========

.. seo::
    :description: Instructions for setting up RGBWW lights.
    :image: rgbw.png

The ``rgbww`` light platform creates an RGBWW (cold white + warm white)
light from 5 :ref:`float output components <output>` (one for each channel). The cold white
and warm white channels will be mixed using the color temperature configuration options.

.. code:: yaml

    # Example configuration entry
    light:
      - platform: rgbww
        name: "Livingroom Lights"
        red: output_component1
        green: output_component2
        blue: output_component3
        cold_white: output_component4
        warm_white: output_component5
        cold_white_color_temperature: 153 mireds
        warm_white_color_temperature: 500 mireds

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **red** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the red channel.
- **green** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the green channel.
- **blue** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the blue channel.
- **cold_white** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the cold white channel.
- **warm_white** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the warm white channel.
- **cold_white_color_temperature** (**Required**, float): The color temperate (in `mireds <https://en.wikipedia.org/wiki/Mired>`__)
  of the cold white channel.
- **warm_white_color_temperature** (**Required**, float): The color temperate (in `mireds <https://en.wikipedia.org/wiki/Mired>`__)
  of the warm white channel.
- **gamma_correct** (*Optional*, float): The `gamma correction
  factor <https://en.wikipedia.org/wiki/Gamma_correction>`__ for the light. Defaults to ``2.8``.
- **default_transition_length** (*Optional*, :ref:`config-time`): The length of
  the transition if no transition parameter is provided by Home Assistant. Defaults to ``1s``.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`MQTT Component <config-mqtt-component>`.

.. note::

    The RGBWW light platform only works with ``float`` :ref:`outputs <output>` that
    can output any light intensity percentage like the :doc:`ESP32 LEDC </esphomeyaml/components/output/ledc>` or
    :doc:`ESP8266 PWM </esphomeyaml/components/output/esp8266_pwm>` components and does **not** work with output
    platforms like the :doc:`/esphomeyaml/components/output/gpio`.

See Also
--------

- :doc:`/esphomeyaml/components/output/index`
- :doc:`/esphomeyaml/components/light/index`
- :doc:`/esphomeyaml/components/light/rgb`
- :doc:`/esphomeyaml/components/light/rgbw`
- :doc:`/esphomeyaml/components/power_supply`
- :doc:`/esphomeyaml/components/output/ledc`
- :doc:`/esphomeyaml/components/output/esp8266_pwm`
- :doc:`/esphomeyaml/components/output/pca9685`
- :doc:`/esphomeyaml/components/output/my9231`
- :doc:`API Reference </api/light/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/light/rgbww.rst>`__

.. disqus::
