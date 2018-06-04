ESP8266 Software PWM Output
===========================

The ESP8266 Software PWM platform allows you to use a software PWM on
the pins GPIO0-GPIO16 on your ESP8266. As this is only a software PWM
and not a hardware PWM (like the :doc:`ESP32 LEDC PWM <ledc>`) and has a few
limitations.

- There can be a noticeable amount of flickering with increased WiFi activity.
- The output range only goes up to about 80%.
- It’s mostly fixed to a frequency of 1kHz, you can :ref:`increase this a
  bit manually <esp8266_pwm-example_usage>` in code though.

If you need a stable PWM signal, it’s definitely recommended to use the
successor of the ESP8266, the ESP32, and its :doc:`ESP32 LEDC PWM <ledc>` instead.

.. code:: yaml

    # Example configuration entry
    output:
      - platform: esp8266_pwm
        pin: D1
        id: pwm-output

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin to use PWM on.
- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- All other options from :ref:`Output <config-output>`.

See Also
^^^^^^^^

- :doc:`/esphomeyaml/components/output/index`
- :doc:`/esphomeyaml/components/output/ledc`
- :doc:`/esphomeyaml/components/light/monochromatic`
- :doc:`/esphomeyaml/components/fan/speed`
- :doc:`/esphomeyaml/components/power_supply`
- :doc:`API Reference </api/output/esp8266-pwm>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/output/esp8266_pwm.rst>`__
