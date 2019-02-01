GPIO Output
===========

.. seo::
    :description: Instructions for setting up binary outputs for GPIO pins.
    :image: pin.png

The GPIO output component is quite simple: It exposes a single GPIO pin
as an output component. Note that output components are **not** switches and
will not show up in Home Assistant. See :doc:`/esphomeyaml/components/switch/gpio`.

.. code-block:: yaml

    # Example configuration entry
    output:
      - platform: gpio
        pin: D1
        id: gpio_d1

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin to use PWM on.
- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- All other options from :ref:`Output <config-output>`.

.. warning::

    This is an **output component** and will not visible from the frontend. Output components are intermediary
    components that can be attached to for example lights. To have a GPIO pin in the Home Assistant frontend, please
    see the :doc:`/esphomeyaml/components/switch/gpio`.

See Also
--------

- :doc:`/esphomeyaml/components/switch/gpio`
- :doc:`/esphomeyaml/components/output/index`
- :doc:`/esphomeyaml/components/output/esp8266_pwm`
- :doc:`/esphomeyaml/components/output/ledc`
- :doc:`/esphomeyaml/components/light/binary`
- :doc:`/esphomeyaml/components/fan/binary`
- :doc:`/esphomeyaml/components/power_supply`
- :doc:`API Reference </api/output/gpio-binary>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/output/gpio.rst>`__

.. disqus::
