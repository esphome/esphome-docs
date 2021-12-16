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

- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **period** (**Required**, :ref:`config-time`): The duration of each cycle. (i.e. a 10s
  period at 50% duty would result in the pin being turned on for 5s, then off for 5s)
- **pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The pin to pulse.
- **toggle_action**  (*Optional*, :ref:`Automation <automation>`): An automation to perform when the load is toggled. If a `lambda` is used the ``bool state`` parameter holds the new status.
- **turn_on_action**  (*Optional*, :ref:`Automation <automation>`): An automation to perform when the load is turned_on. Can be used to controll for example a switch or output component.
- **turn_off_action** (*Optional*, :ref:`Automation <automation>`): An automation to perform when the load is turned_off. ``turn_on_action`` and ``turn_off_action`` must be configured together

- All other options from :ref:`Output <config-output>`.


.. note::

    - If ``pin`` is defined the gpio pin state is writen before any action is executed.
    - ``toggle_action`` and ``turn_on/off_action`` can be used togther. ``toggle_action`` is called before ``turn_on/off_action``. It's recommended to use either ``toggle_action`` or ``turn_on/off_action`` to change the state of an output. Using both automations together is only recommended for montitoring


Example:
--------



.. code-block:: yaml

    esphome:
      name: testing
      on_boot:
        priority: -100
        then:
          output.set_level:
            id: my_slow_pwm
            level: 25%
              
    output:
      - platform: template
        id: output1
        type: binary
        write_action:
          - then:
              - lambda: ESP_LOGD("Template Output","set state to %d",state);

      - platform: slow_pwm
        id: my_slow_pwm
        period: 15s
        # pin: 5
        # toggle_action:
        #  - lambda: |-
        #      ESP_LOGD("SLOW PWM","toggle to state %d",state);
        #      auto *out1 = id(output1);
        #      if (state)
        #        out1->turn_on();
        #      else
        #        out1->turn_off();

        turn_on_action:
          - lambda: |-
              auto *out1 = id(output1);
              out1->turn_on();
        turn_off_action:
          - output.turn_off: output1



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
