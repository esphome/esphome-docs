ESP32 LEDC Output
=================

.. seo::
    :description: Instructions for setting up LEDC hardware PWM outputs on the ESP32.
    :image: pwm.png

The LEDC output component exposes a `LEDC PWM
channel <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/ledc.html>`__
of the ESP32 as an output component.

The frequency range of LEDC is from 10Hz to 40MHz - however, higher frequencies require a smaller
bit depth which means the output is not that accurate for frequencies above ~300kHz.

Example Usage For a Light
*************************

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

Example Usage For a Piezo Buzzer
********************************

.. code-block:: yaml

    # Configure the output
    output:
      - platform: ledc
        ######################################################
        # One buzzer leg connected to GPIO12, the other to GND
        ######################################################
        pin: GPIO12
        id: buzzer

    # Example usage in an automation
    on_press:
        then:
        ######################################################
        # Must be turned on before setting frequency & level
        ######################################################
        - output.turn_on: buzzer
        ######################################################
        # Frequency sets the wave size
        ######################################################
        - output.ledc.set_frequency:
            id: buzzer
            frequency: "1000Hz"
        ######################################################
        # level sets the %age time the PWM is on
        ######################################################
        - output.set_level:
            id: buzzer
            level: "50%"

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`config-pin`): The pin to use LEDC on. Can only be GPIO0-GPIO33.
- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **frequency** (*Optional*, float): At which frequency to run the LEDC
  channel’s timer. Defaults to 1000Hz.
- All other options from :ref:`Output <config-output>`.

Advanced options:

- **channel** (*Optional*, int): Manually set the `LEDC
  channel <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/ledc.html#configure-channel>`__
  to use. Two adjacent channels share the same timer. Defaults to an automatic selection.

Recommended frequencies
-----------------------

To get the highest available frequency while still getting the same bit depth it is
recommended to pick one of the following frequencies.

Higher bit depth means that the light has more steps available to change from one
value to another. This is especially noticeable when the light is below 10% and takes
a long transition, e.g. turning slowly off.

================================== =================================== ===================================
**Frequency**                      **Bit depth**                       **Available steps for transitions**
---------------------------------- ----------------------------------- -----------------------------------
1220Hz                             16                                  65536
---------------------------------- ----------------------------------- -----------------------------------
2441Hz                             15                                  32768
---------------------------------- ----------------------------------- -----------------------------------
4882Hz                             14                                  16384
---------------------------------- ----------------------------------- -----------------------------------
9765Hz                             13                                  8192
---------------------------------- ----------------------------------- -----------------------------------
19531Hz                            12                                  4096
================================== =================================== ===================================

The ESP8266 for instance has *usually* a frequency of 1000Hz with a resolution of 10 bits.
This means that there are only 4 steps between each value.

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
- :ghsources:`esphome/components/ledc`
- `esp-idf LEDC API docs <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/ledc.html>`__
- :ghedit:`Edit`
