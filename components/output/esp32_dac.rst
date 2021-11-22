ESP32 DAC
=========

.. seo::
    :description: Instructions for setting up ESP32 digital-to-analog converter.
    :image: dac.svg

The ESP32 DAC platform allows you to output analog voltages using the 8-bit digital-to-analog
converter of the ESP32. Unlike the :doc:`/components/output/ledc`, which can simulate an analog
signal by using a fast switching frequency, the hardware DAC can output a *real* analog signal with
no need for additional filtering.

The DAC spans across two pins, each on its own channel: GPIO25 (Channel 1) and GPIO26 (Channel 2).

The output level is a percentage of the board supply voltage (VDD_A) - generally this will be 3.3 V.


.. code-block:: yaml

    # Example configuration entry
    output:
      - platform: esp32_dac
        pin: GPIO25
        id: dac_output

    # Example usage
    on_...:
      then:
        - output.set_level:
            id: dac_output
            level: 50%
            
    # Use the DAC output as a light
    light:
      - platform: monochromatic
        output: dac_output
        gamma_correct: 1.4
        id: mono_light


Configuration variables:
------------------------

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin to use DAC on. Only GPIO25
  and GPIO26 are supported.
- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- All other options from :ref:`Output <config-output>`.

Use Cases
---------

- Generating a specific (and dynamic) reference voltage for an external sensor or ADC, such as the
  :doc:`/components/sensor/ads1115`
- Controlling the bias of a transistor
- Driving a bar graph or large amount of LEDs using an analog-controlled LED driver like the LM3914
  (`datasheet <https://www.ti.com/lit/ds/symlink/lm3914.pdf>`__); this can allow you to make tank
  level indicators, temperature gauges, and so on from a single output pin
- Generating 0-10 V for a dimmable light (operational amplifier required)

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/output/ledc`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/light/monochromatic`
- :doc:`/components/fan/speed`
- :doc:`/components/power_supply`
- :apiref:`esp32_dac/esp32_dac.h`
- :ghedit:`Edit`
