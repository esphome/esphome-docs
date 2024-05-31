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
        pin: GPIOXX
        id: my_slow_pwm
        period: 15s


Configuration variables:
------------------------

- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **period** (**Required**, :ref:`config-time`): The duration of each cycle. (i.e. a 10s
  period at 50% duty would result in the pin being turned on for 5s, then off for 5s)
- **pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The pin to pulse.
- **state_change_action** (*Optional*, :ref:`Automation <automation>`): An automation to perform when the load is switched. If a lambda is used the boolean ``state`` parameter holds the new status.
- **turn_on_action** (*Optional*, :ref:`Automation <automation>`): An automation to perform when the load is turned on. Can be used to control for example a switch or output component.
- **turn_off_action** (*Optional*, :ref:`Automation <automation>`): An automation to perform when the load is turned off. ``turn_on_action`` and ``turn_off_action`` must be configured together.
- **restart_cycle_on_state_change** (*Optional*, boolean): Restart a timer of a cycle
  when new state is set. Defaults to ``false``.

- All other options from :ref:`Output <config-output>`.


.. note::

    - If ``pin`` is defined the GPIO pin state is writen before any action is executed.
    - ``state_change_action`` and ``turn_on_action``/``turn_off_action`` can be used togther. ``state_change_action`` is called before ``turn_on_action``/``turn_off_action``. It's recommended to use either ``state_change_action`` or ``turn_on_action``/``turn_off_action`` to change the state of an output. Using both automations together is only recommended for monitoring.


Example:
--------

.. code-block:: yaml


    output:
      - platform: slow_pwm
        id: my_slow_pwm
        period: 15s
        turn_on_action:
          - lambda: |-
              auto *out1 = id(output1);
              out1->turn_on();
        turn_off_action:
          - output.turn_off: output1


.. note::

    If the duty cycle is not constrained to a maximum value, the
    :doc:`/components/output/sigma_delta_output` component offers faster updates and
    greater control over the switching frequency. This is better for loads that
    need some time to fully change between on and off, like eletric thermal
    actuator heads or fans.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/output/ledc`
- :doc:`/components/output/sigma_delta_output`
- :doc:`/components/light/monochromatic`
- :doc:`/components/fan/speed`
- :doc:`/components/power_supply`
- :apiref:`slow_pwm/slow_pwm_output.h`
- :ghedit:`Edit`
