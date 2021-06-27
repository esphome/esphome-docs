Servo Component
===============

.. seo::
    :description: Instructions for setting up servos in ESPHome
    :image: servo.png

The ``servo`` component allows you to use servo motors with ESPHome. Servos are
motor controllers that contain all the electronics necessary for driving the motor and provide
a simple PWM interface to control the motor.

This integration works with both continuous-rotation and absolute servos and has a similar
interface to the Arduino Servo library.

First, create an :ref:`output component <output>` (here ``esp8266_pwm``) for the pin the
servo is connected to. Then connect that output to the servo component by assigning an ID.
Please note the frequency of the output must be around 50Hz, as most servo controllers
only operate in this frequency range.

.. note::

    This component will not show up in the Home Assistant front-end automatically because
    Home Assistant doesn't have support for servos. Please see :ref:`servo-ha-config`.

.. code-block:: yaml

    # Example configuration entry
    servo:
      - id: my_servo
        output: pwm_output

    # Example output platform
    # On ESP32, use ledc output
    output:
      - platform: esp8266_pwm
        id: pwm_output
        pin: D1
        frequency: 50 Hz

Configuration variables:
------------------------

- **output** (**Required**, :ref:`config-id`): The ID of the :doc:`output component </components/output/index>`
  to use for this servo.
- **id** (**Required**, :ref:`config-id`): The ID of this servo so that it can be controlled.

Advanced Options:

- **min_level** (*Optional*, percentage): The PWM duty cycle the minimum value (-100%) will map
  to. Defaults to ``3%``.
- **idle_level** (*Optional*, percentage): The PWM duty cycle the idle value (0%) will map
  to. This is also the state of the servo at startup. Defaults to ``7.5%``.
- **max_level** (*Optional*, percentage): The PWM duty cycle the maximum value (100%) will map
  to. Defaults to ``12.0%``.
- **restore** (*Optional*, boolean): Whether to restore the state of the servo motor at startup.
  This is useful if you have an absolute servo motor and it goes back to its 0 position at startup.
  Defaults to ``false``.
- **auto_detach_time** (*Optional*, :ref:`config-time`): The time after reaching the target value when the servo will be detached`, if set to zero, servo will not be detached. Defaults to ``0s``.
- **transition_length** (*Optional*, :ref:`config-time`): The time needed for a full movement (-1.0 to 1.0). This will effectively limit the speed of the servo, the larger the value, the slowest the servo will move. Defaults to `` 0s``
  This can slow down the servo to avoid loud noises or just make the movement not jerking.

.. note::

    Some servos support a larger range for the level. For continuous rotation servos
    this can speed them up a bit and for absolute servos this can extend their angle range.
    You can configure the ``min_level`` and ``max_level`` options to adjust the level range
    to match your servo (Experiment with these values).

.. _servo-write_action:

``servo.write`` Action
----------------------

To use your servo motor in :ref:`automations <automation>` or templates, you can use this action to set the
target level of the servo from -100% to 100%.

- -100% (= -1.0) is the minimum value of the servo. For continuous-rotation servos this will
  rotate the servo backward.
- 0% (= 0.0) is the idle level of the servo. For continuous-rotation servos this will
  stop the servo.
- 100% (= 1.0) is the maximum value of the servo. For continuous-rotation servos this will
  rotate the servo forward.

.. code-block:: yaml

    on_...:
      then:
      - servo.write:
          id: my_servo
          level: -100.0%

      # Templated
      - servo.write:
          id: my_servo
          # For template values, range is [-1; 1]
          level: !lambda |-
            if (id(my_binary_sensor).state) {
              return 1.0;
            } else {
              return -1.0;
            }

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the servo.
- **level** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The target level.
  Range is from -100% to 100% (-1.0 to 1.0).

.. note::

    This action can also be expressed as a :ref:`lambda <config-lambda>`:

    .. code-block:: cpp

        id(my_servo).write(1.0);

.. _servo-detach_action:

``servo.detach`` Action
-----------------------

This :ref:`Action <config-action>` allows you to disable the output on a servo motor -
this will make the servo motor stop immediately and disable its active control.

.. code-block:: yaml

    on_...:
      then:
      - servo.detach: my_servo

.. note::

    This action can also be expressed as a :ref:`lambda <config-lambda>`:

    .. code-block:: cpp

        id(my_servo).detach();

.. _servo-ha-config:

Home Assistant Configuration
----------------------------

This component will not show up in the Home Assistant frontend automatically because Home Assistant
does not support servos natively (raise this issue in Home Assistant forums to make this a
higher priority for Home Assistant). You can add this to your Home Assistant configuration to
be able to control the servo from the frontend.

.. code-block:: yaml

    # Home Assistant configuration
    input_number:
      servo_control:
        name: Servo Control
        initial: 0
        min: -100
        max: 100
        step: 1
        mode: slider

    automation:
      - alias: Write Servo Value to ESP
        trigger:
          platform: state
          entity_id: input_number.servo_control
        action:
          # Replace livingroom with the name you gave the ESP
          - service: esphome.livingroom_control_servo
            data_template:
              level: '{{ trigger.to_state.state | int }}'

.. code-block:: yaml

    # ESPHome configuration
    api:
      services:
        - service: control_servo
          variables:
            level: float
          then:
            - servo.write:
                id: my_servo
                level: !lambda 'return level / 100.0;'

    servo:
      - platform: ...
        # [...] servo config
        id: my_servo


See Also
--------

- :apiref:`servo/servo.h`
- :ghedit:`Edit`
