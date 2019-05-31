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

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **red** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the red channel.
- **green** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the green channel.
- **blue** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the blue channel.
- **white** (**Required**, :ref:`config-id`): The id of the float :ref:`output` to use for the white channel.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Light <config-light>`.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/light/index`
- :doc:`/components/light/rgb`
- :doc:`/components/power_supply`
- :doc:`/components/output/ledc`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/output/pca9685`
- :doc:`/components/output/my9231`
- :doc:`/components/output/sm16716`
- :apiref:`rgbw/rgb_light_output.h`
- :ghedit:`Edit`
