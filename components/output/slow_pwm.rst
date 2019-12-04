Slow PWM Output
===============

.. seo::
    :description: Instructions for setting up slow pwm outputs for GPIO pins.
    :image: pwm.png

Similar to PWM, The Slow PWM Output platform allows you to control GPIO pins by
pulsing them on/off over a longer time period. It could be used to control a
heating element through a relay where a fast PWM update cycle would not be appropriate.

.. code-block:: yaml

    # Example configuration entry
    output:
      - platform: slow_pwm
        pin: D1
        id: my_slow_pwm
        period: 15s


Configuration variables:
------------------------

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin to pulse.
- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **period** (**Required**, frequency): The duration of each cycle. (i.e. a 10s
  period at 50% duty would result in the pin being turned on for 5s, then off for 5s)
- All other options from :ref:`Output <config-output>`.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/output/ledc`
- :doc:`/components/light/monochromatic`
- :doc:`/components/fan/speed`
- :doc:`/components/power_supply`
- :apiref:`slow_pwm/slow_pwm_output.h`
- :ghedit:`Edit`
