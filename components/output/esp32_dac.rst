ESP32 DAC
=========

.. seo::
    :description: Instructions for setting up ESP32 digital-to-analog converter.
    :image: dac.svg

The ESP32 DAC platform allows you to output arbitrary voltages using the 8-bit DAC on the ESP32. Two pins are supported: GPIO25 (Channel 1) and GPIO26 (Channel 2).

The output level is a percentage of VCC (3.3V).


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


Configuration variables:
------------------------

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin to use DAC on. Only GPIO25 and GPIO26 are supported.
- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- All other options from :ref:`Output <config-output>`.

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
