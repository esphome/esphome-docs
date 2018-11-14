ESP32 LEDC Output
=================

.. seo::
    :description: Instructions for setting up LEDC hardware PWM outputs on the ESP32.
    :image: pwm.png

The LEDC output component exposes a `LEDC PWM
channel <https://esp-idf.readthedocs.io/en/latest/api-reference/peripherals/ledc.html>`__
of the ESP32 as an output component.

.. code:: yaml

    # Example configuration entry
    output:
      - platform: ledc
        pin: 19
        id: gpio_19

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`config-pin`): The pin to use LEDC on. Can only be GPIO0-GPIO33.
- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **frequency** (*Optional*, float): At which frequency to run the LEDC
  channel’s timer. Two LEDC channels always share the same timer and
  therefore also the same frequency. Defaults to 1000Hz.
- **bit_depth** (*Optional*, int): The bit depth to use for the LEDC channel. Defaults to 12.
- **channel** (*Optional*, int): Manually set the `LEDC
  channel <https://esp-idf.readthedocs.io/en/latest/api-reference/peripherals/ledc.html#configure-channel>`__
  to use. Two adjacent channels share the same timer. Defaults to an automatic selection.
- All other options from :ref:`Output <config-output>`.

See Also
--------

- :doc:`/esphomeyaml/components/output/index`
- :doc:`/esphomeyaml/components/output/esp8266_pwm`
- :doc:`/esphomeyaml/components/light/monochromatic`
- :doc:`/esphomeyaml/components/fan/speed`
- :doc:`/esphomeyaml/components/power_supply`
- :doc:`API Reference </api/output/ledc>`
- `esp-idf LEDC API docs <https://esp-idf.readthedocs.io/en/latest/api-reference/peripherals/ledc.html>`__
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/output/ledc.rst>`__

.. disqus::
