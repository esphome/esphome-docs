Color Temperature Light
=======================

.. seo::
    :description: Instructions for setting up Color Temperature lights.
    :image: brightness-medium.svg

The ``color_temperature`` light platform creates a Color Temperature
light from 2 :ref:`float output components <output>`. One channel controls the LED temperature,
and the other channel controls the brightness.

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: color_temperature
        name: "Livingroom Lights"
        color_temperature: output_component1
        brightness: output_component2
        cold_white_color_temperature: 6536 K
        warm_white_color_temperature: 2000 K

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **color_temperature** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the color temperature.
- **brightness** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the brightness.
- **cold_white_color_temperature** (**Required**, float): The coldest color temperature supported by this light. This
  is the lowest value when expressed in `mireds <https://en.wikipedia.org/wiki/Mired>`__, or the highest value when
  expressed in Kelvin.
- **warm_white_color_temperature** (**Required**, float): The warmest color temperature supported by this light. This
  is the highest value when expressed in `mireds <https://en.wikipedia.org/wiki/Mired>`__, or the lowest value when
  expressed in Kelvin.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Light <config-light>`.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/light/index`
- :doc:`/components/light/cwww`
- :doc:`/components/light/rgb`
- :doc:`/components/light/rgbw`
- :doc:`/components/light/rgbww`
- :doc:`/components/light/rgbct`
- :doc:`/components/power_supply`
- :doc:`/components/output/ledc`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/output/pca9685`
- :doc:`/components/output/tlc59208f`
- :apiref:`color_temperature/ct_light_output.h`
- :ghedit:`Edit`
