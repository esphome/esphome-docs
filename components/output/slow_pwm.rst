Slow PWM Output
===============

.. seo::
    :description: Instructions for setting up slow pwm outputs for GPIO pins.
    :image: pwm.png

Similar to PWM, the Slow PWM Output platform allows you to control GPIO pins by
pulsing them on/off over a longer time period. It could be used to control a
heating element through a relay where a fast PWM update cycle would not be appropriate.

.. note::

    This is for **slow** PWM output. For fast-switching PWM outputs (for example,
    lights), see these outputs:

    - ESP32: :doc:`ledc`
    - ESP8266: :doc:`esp8266_pwm`

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
- **period** (**Required**, :ref:`config-time`): The duration of each cycle. (i.e. a 10s
  period at 50% duty would result in the pin being turned on for 5s, then off for 5s)
- **restart_cycle_on_state_change** (*Optional*, boolean): Restart a timer of a cycle
  when new state is set. Defaults to ``false``.
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
