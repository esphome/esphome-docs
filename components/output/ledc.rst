ESP32 LEDC Output
=================

.. seo::
    :description: Instructions for setting up LEDC hardware PWM outputs on the ESP32.
    :image: pwm.png

The LEDC (LED Controller) output component provides access to hardware PWM (Pulse Width Modulation) capabilities on the ESP32, allowing for precise control of devices such as LEDs, motor control circuits, and audio outputs like buzzers. The ESP32's LEDC hardware supports a wide range of frequencies, from 10Hz to 40MHz, although higher frequencies require a smaller bit depth which means the output is not that accurate for frequencies above ~300kHz.

On a technical level, the LEDC output component exposes a `LEDC PWM
channel <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/ledc.html>`__
of the ESP32 as an output component.

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`config-pin`): The pin to use LEDC on. Can only be GPIO0-GPIO33.
- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **frequency** (*Optional*, float): At which frequency to run the LEDC
  channel’s timer. Defaults to 1000Hz. If setting multiple outputs with custom frequencies, channel should be set. See **Note** below. 
- **channel** (*Optional*, int): Manually set the `LEDC
  channel <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/ledc.html#configure-channel>`__
  to use. Two adjacent channels share the same timer. Defaults to an automatic selection.
- All other options from :ref:`Output <config-output>`.

**Note**: When configuring custom frequencies for multiple outputs, manually specify channels 0, 2, 4, or 6 to each output. This prevents conflicts that occur because automatically assigned channels may share the same timer. See
`Issue #3114 <https://github.com/esphome/issues/issues/3114>`__ for more details. 

- **phase_angle** (*Optional*, float): Set a phase angle to the other channel of this timer.
  Range 0-360°, defaults to 0°

Note: this variable is only available for the esp-idf framework

Example Usage For a Light
*************************

.. code-block:: yaml

    # Example configuration entry
    output:
      - platform: ledc
        pin: GPIO19
        id: output_gpio_19 

    # Example usage in a light
    light:
      - platform: monochromatic
        output: output_gpio_19 # Matches id from output section
        name: "Kitchen Light"

Example Usage For a Piezo Buzzer (Passive / Externally Driven)
********************************

.. code-block:: yaml

    # Configure the output
    output:
      - platform: ledc
        # One buzzer leg connected to GPIO12, the other to GND
        pin: GPIO12
        id: buzzer

    # Example usage in an automation
    on_press:
        then:
        # Buzzer must be turned on before setting frequency & level
        - output.turn_on: buzzer
        # Set the PWM frequency, which controls the pitch of the buzzer
        - output.ledc.set_frequency:
            id: buzzer
            frequency: "1000Hz" # Higher frequency produces a higher pitch
        # Set the duty cycle (level), which controls the volume of the sound
        - output.set_level:
            id: buzzer
            level: "50%"

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
- :apiref:`ledc/ledc_output.h`
- `esp-idf LEDC API docs <https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/ledc.html>`__
- :ghedit:`Edit`
