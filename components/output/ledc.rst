ESP32 LEDC Output
=================

.. seo::
    :description: Instructions for setting up LEDC hardware PWM outputs on the ESP32.
    :image: pwm.png

The LEDC output component exposes a `LEDC PWM
channel <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/ledc.html>`__
of the ESP32 as an output component.

The frequency range of LEDC is from 10Hz to 40MHz - however, higher frequencies require a smaller
bit_depth which means the output is not that accurate for frequencies above ~300kHz.

.. code-block:: yaml

    # Example configuration entry
    output:
      - platform: ledc
        pin: GPIO19
        id: gpio_19

    # Example usage in a light
    light:
      - platform: monochromatic
        output: gpio_19
        name: "Kitchen Light"

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`config-pin`): The pin to use LEDC on. Can only be GPIO0-GPIO33.
- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **frequency** (*Optional*, float): At which frequency to run the LEDC
  channel’s timer. Defaults to 1000Hz.
- **bit_depth** (*Optional*, int): The bit depth to use for the LEDC channel. Defaults to the
  highest possible for the configured frequency.
- All other options from :ref:`Output <config-output>`.

Advanced options:

- **channel** (*Optional*, int): Manually set the `LEDC
  channel <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/ledc.html#configure-channel>`__
  to use. Two adjacent channels share the same timer. Defaults to an automatic selection.

.. _output-ledc-set_frequency_action:

``output.ledc.set_frequency`` Action
------------------------------------

This :ref:`Action <config-action>` allows you to manually change the frequency of an LEDC
channel at runtime. Use cases include controlling a passive buzzer (for pitch control).

.. code-block:: yaml

    on_...:
      - output.ledc.set_frequency:
          id: ledc_output
          frequency: 100Hz

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the LEDC output to change.
- **frequency** (**Required**, :ref:`templatable <config-templatable>`, float): The frequency
  to set in hertz.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/light/monochromatic`
- :doc:`/components/fan/speed`
- :doc:`/components/power_supply`
- :apiref:`ledc/ledc_output.h`
- `esp-idf LEDC API docs <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/ledc.html>`__
- :ghedit:`Edit`
