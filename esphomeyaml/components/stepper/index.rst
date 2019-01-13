Stepper Component
=================

.. seo::
    :description: Instructions for setting up stepper motor drivers in esphomelib
    :image: folder-open.png
    :keywords: stepper motor, stepper driver, a4988

The ``stepper`` component allows you to use stepper motors with esphomelib.
Currently only the A4988 stepper driver
(`datasheet <https://www.pololu.com/file/0J450/a4988_DMOS_microstepping_driver_with_translator.pdf>`__)
and ULN2003 (`datasheet <http://www.ti.com/lit/ds/symlink/uln2003a.pdf>`__) are supported.

A4988 Configuration
-------------------

.. code-block:: yaml

    # Example configuration entry
    stepper:
      - platform: a4988
        id: my_stepper
        step_pin: D0
        dir_pin: D1
        max_speed: 250 steps/s

        # Optional:
        sleep_pin: D2
        acceleration: inf
        deceleration: inf


Configuration variables:

- **id** (**Required**, :ref:`config-id`): Specify the ID of the stepper so that you can control it.
- **step_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The ``STEP`` pin of the A4988
  stepper driver.
- **dir_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The ``DIRECTION`` pin of the A4988
  stepper driver.
- **max_speed** (**Required**, float): The maximum speed in ``steps/s`` (steps per seconds) to drive the
  stepper at. Note most steppers can't step properly with speeds higher than 250 steps/s.
- **sleep_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): Optionally also use the ``SLEEP`` pin
  of the A4988 stepper driver. If specified, the driver will be put into sleep mode as soon as the stepper
  reaches the target steps.
- **acceleration** (*Optional*, float): The acceleration in ``steps/s^2`` (steps per seconds squared)
  to use when starting to move. The default is ``inf`` which means infinite acceleration, so the
  stepper will try to drive with the full speed immediately.
- **deceleration** (*Optional*, float): The same as ``acceleration``, but for when the motor is decelerating
  shortly before reaching the set position. Defaults to ``inf`` (immediate deceleration).

.. note::

    If the stepper is driving in the wrong direction, you can invert the ``dir_pin``:

    .. code-block:: yaml

        stepper:
          - platform: a4988
            # ...
            dir_pin:
              number: D1
              inverted: True

ULN2003 Configuration
---------------------

.. code-block:: yaml

    # Example configuration entry
    stepper:
      - platform: uln2003
        id: my_stepper
        pin_a: D0
        pin_b: D1
        pin_c: D2
        pin_d: D3
        max_speed: 250 steps/s

        # Optional:
        acceleration: inf
        deceleration: inf


Configuration variables:

- **id** (**Required**, :ref:`config-id`): Specify the ID of the stepper so that you can control it.
- **pin_a**, **pin_b**, **pin_c**, **pin_d** (**Required**, :ref:`Pin Schema <config-pin_schema>`):
  The four pins of the stepper control board.
- **sleep_when_done** (*Optional*, boolean): Whether to turn off all coils when the stepper has
  reached the target position
- **step_mode** (*Optional*, string): The step mode to operate the motor with. One of:

    - ``FULL_STEP`` (Default)
    - ``HALF_STEP``
    - ``WAVE_DRIVE``

- **max_speed** (**Required**, float): The maximum speed in ``steps/s`` (steps per seconds) to drive the
  stepper at. Note most steppers can't step properly with speeds higher than 250 steps/s.
- **acceleration** (*Optional*, float): The acceleration in ``steps/s^2`` (steps per seconds squared)
  to use when starting to move. The default is ``inf`` which means infinite acceleration, so the
  stepper will try to drive with the full speed immediately.
- **deceleration** (*Optional*, float): The same as ``acceleration``, but for when the motor is decelerating
  shortly before reaching the set position. Defaults to ``inf`` (immediate deceleration).

.. _stepper-set_target_action:

``stepper.set_target`` Action
-----------------------------

To use your stepper motor in :ref:`automations <automation>` or templates, you can use this action to set the target
position (in steps). The stepper will always run towards the target position and stop once it has reached the target.

.. code-block:: yaml

    on_...:
      then:
      - stepper.set_target:
          id: my_stepper
          target: 250

      # Templated
      - stepper.set_target:
          id: my_stepper
          target: !lambda |-
            if (id(my_binary_sensor).state) {
              return 1000;
            } else {
              return -1000;
            }

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the stepper.
- **target** (*Optional*, int, :ref:`templatable <config-templatable>`): The target position in steps.

.. note::

    This action can also be expressed as a :ref:`lambda <config-lambda>`:

    .. code-block:: cpp

        id(my_stepper).set_target(250);

        // Get the currently set target position:
        int target = id(my_stepper).target_position;

.. _stepper-report_position_action:

``stepper.report_position`` Action
----------------------------------

All steppers start out with a target and current position of ``0`` on boot. However, if you for example want to home
a stepper motor, it can be useful to **report** the stepper where it is currently at.

With this action, you can set the stepper's internal position counter to a specific value (in steps). Please note
that reporting the position can create unexpected moves of the stepper. For example, if the stepper's target and
current position is at 1000 steps and you "report" a position of 0, the stepper will move 1000 steps forward to match
the target again.

.. code-block:: yaml

    on_...:
      then:
      - stepper.report_position:
          id: my_stepper
          position: 250
      # It's best to call set_target directly after report_position, so that the stepper doesn't move
      - stepper.set_target:
          id: my_stepper
          target: 250

      # Templated
      - stepper.report_position:
          id: my_stepper
          position: !lambda |-
            if (id(my_binary_sensor).state) {
              return 0;
            } else {
              return -1000;
            }

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the stepper.
- **target** (*Optional*, int, :ref:`templatable <config-templatable>`): The target position in steps.

.. note::

    This action can also be expressed as a :ref:`lambda <config-lambda>`:

    .. code-block:: cpp

        id(my_stepper).report_position(250);

        // Get the current position:
        int pos = id(my_stepper).current_position;

See Also
--------

- :doc:`API Reference </api/misc/stepper>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/stepper.rst>`__

.. disqus::
