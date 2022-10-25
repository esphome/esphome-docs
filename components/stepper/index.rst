Stepper Component
=================

.. seo::
    :description: Instructions for setting up stepper motor drivers in ESPHome
    :image: folder-open.svg
    :keywords: stepper motor, stepper driver, a4988

The ``stepper`` component allows you to use stepper motors with ESPHome.
Currently only the A4988 stepper driver
(`datasheet <https://www.pololu.com/file/0J450/a4988_DMOS_microstepping_driver_with_translator.pdf>`__)
and ULN2003 (`datasheet <http://www.ti.com/lit/ds/symlink/uln2003a.pdf>`__) are supported.

.. note::

    This component will not show up in the Home Assistant front-end automatically because
    Home Assistant doesn't have support for steppers. Please see :ref:`stepper-ha-config`.

.. _base_stepper_config:

Base Stepper Configuration
--------------------------

All stepper configuration schemas inherit these options.

Configuration variables:

- **max_speed** (**Required**, float): The maximum speed in ``steps/s`` (steps per seconds) to drive the
  stepper at. Note most steppers can't step properly with speeds higher than 250 steps/s.
- **acceleration** (*Optional*, float): The acceleration in ``steps/s^2`` (steps per seconds squared)
  to use when starting to move. The default is ``inf`` which means infinite acceleration, so the
  stepper will try to drive with the full speed immediately. This value is helpful if that first motion of
  the motor is too jerky for what it's moving.  If you make this a small number, it will take the motor a
  moment to get up  to speed.
- **deceleration** (*Optional*, float): The same as ``acceleration``, but for when the motor is decelerating
  shortly before reaching the set position. Defaults to ``inf`` (immediate deceleration).

A4988 Component
---------------

Put this code into the configuration file on ESPHome for this device.

.. code-block:: yaml

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
- **sleep_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): Optionally also use the ``SLEEP`` pin
  of the A4988 stepper driver. If specified, the driver will be put into sleep mode as soon as the stepper
  reaches the target steps.

- All other from :ref:`base_stepper_config`.

.. note::

    If the stepper is driving in the wrong direction, you can invert the ``dir_pin``:

    .. code-block:: yaml

        stepper:
          - platform: a4988
            # ...
            dir_pin:
              number: D1
              inverted: true
              
.. note::

    If you want to replace the A4988 with a TMC2208 module, there are some minor changes to do:
    
    - The TMC2208 only has two microstepping pins (MS1, MS2). The configuration is slightly counter-intuitive:

        +---+---+--------+
        |MS2|MS1|Stepping|
        +===+===+========+
        |GND|GND|1/8     |
        +---+---+--------+
        |GND|VIO|1/2     |
        +---+---+--------+
        |VIO|GND|1/4     |
        +---+---+--------+
        |VIO|VIO|1/16    |
        +---+---+--------+

    - There is no physical ``SLEEP`` pin anymore. You need to use the ``ENABLE`` pin, which has an inverted logic. So you should use this block and connect it to the ``ENABLE`` pin of the module:

    .. code-block:: yaml

        stepper:
          - platform: a4988
            # ...
            sleep_pin:
              number: D2
              inverted: true

ULN2003 Component
-----------------

Put this code into the configuration file on ESPHome for this device.

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
- **pin_a** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin **a** of the stepper control board.
- **pin_b** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin **b** of the stepper control board.
- **pin_c** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin **c** of the stepper control board.
- **pin_d** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin **d** of the stepper control board.
- **sleep_when_done** (*Optional*, boolean): Whether to turn off all coils when the stepper has
  reached the target position
- **step_mode** (*Optional*, string): The step mode to operate the motor with. One of:

    - ``FULL_STEP`` (Default)
    - ``HALF_STEP``
    - ``WAVE_DRIVE``

- All other from :ref:`base_stepper_config`.

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
- **target** (**Required**, int, :ref:`templatable <config-templatable>`): The target position in steps.

.. warning::

    This turns the stepper to an absolute position! To have the servo move *relative* to the current
    position, first reset the current position and then set the target to the relative value.

    .. code-block:: yaml

        on_...:
          then:
            # Move 150 steps forward
            - stepper.report_position:
                id: my_stepper
                position: 0
            - stepper.set_target:
                id: my_stepper
                target: 150

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

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the stepper.
- **position** (**Required**, int, :ref:`templatable <config-templatable>`): The position to report in steps.

.. _stepper-set_speed_action:

``stepper.set_speed`` Action
----------------------------

This :ref:`Action <config-action>` allows you to set the speed of a stepper at runtime.

.. code-block:: yaml

    on_...:
      - stepper.set_speed:
          id: my_stepper
          speed: 250 steps/s

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the stepper.
- **speed** (**Required**, :ref:`templatable <config-templatable>`, float): The speed
  in ``steps/s`` (steps per seconds) to drive the stepper at.

.. _stepper-set_acceleration_action:

``stepper.set_acceleration`` Action
-----------------------------------

This :ref:`Action <config-action>` allows you to set the acceleration of a stepper at runtime.

.. code-block:: yaml

    on_...:
      - stepper.set_acceleration:
          id: my_stepper
          acceleration: 250 steps/s^2

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the stepper.
- **acceleration** (**Required**, :ref:`templatable <config-templatable>`, float): The acceleration
  in ``steps/s^2`` (steps per seconds squared) to use when starting to move.

.. _stepper-set_deceleration_action:

``stepper.set_deceleration`` Action
-----------------------------------

This :ref:`Action <config-action>` allows you to set the deceleration of a stepper at runtime.

.. code-block:: yaml

    on_...:
      - stepper.set_deceleration:
          id: my_stepper
          deceleration: 250 steps/s^2

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the stepper.
- **deceleration** (**Required**, :ref:`templatable <config-templatable>`, float): The same as ``acceleration``,
  but for when the motor is decelerating shortly before reaching the set position.

.. _stepper-ha-config:

Home Assistant Configuration
----------------------------

This component will not show up in the Home Assistant front-end (Overview) automatically because
Home Assistant does not support steppers natively.

You can add the stepper component code below to your Home Assistant configuration (``configuration.yaml``) to
be able to control the stepper from the front-end.

.. code-block:: yaml

    # Add a slider control to Home Assistant to set an integer value
    input_number:
      stepper_control:
        name: Stepper Control
        initial: 0
        min: -1000
        max: 1000
        step: 1
        mode: slider

    # Do something when the slider changes
    automation:
      - alias: Write Stepper Value to ESP
        trigger:
          platform: state
          entity_id: input_number.stepper_control
        action:
          # Replace livingroom with the name you gave the ESP
          - service: esphome.livingroom_control_stepper
            data_template:
              target: '{{ trigger.to_state.state | int }}'

In the above code, "stepper_control" is the ID of a numeric input field. It must be unique and it is
used in the automation section as a reference name. The display name for this field is in
stepper_control's ``name`` key.

If you want your user interface to give you more control over your stepper controller, such as
setting the acceleration, deceleration, etc, then you can add more input fields after ``stepper_control``
but before ``automation``. They can be a simple number-entry field (mode: box) or a slider like this.
Each of these extra input fields needs an associated input parameter defined on the ESPHome device's
API service.

The automation section tells Home Assistant what to do when the slider changes. It needs a trigger
(state of the ``stepper_control`` slider) and an action. In the trigger section, ``entity_id`` must refer
back to the configuration ID that triggers the automation. For us, that is the ``stepper_control``
field in the ``input_number`` item. That's why the value is ``input_number.stepper_control``.

In the action section, the service name is vital to get right: it's the glue that connects Home Automation's
front-end to the ESPHome device configuration. While you might expect the syntax to be ``esphome.<your_device>.<api_service>``,
the correct syntax is to join the device ID to the API service ID with an underscore,
as in ``esphome.livingroom_control_stepper`` where "Livingroom" is a device in ESPHome and "control_stepper" is an
API service for that device.

The template string is used to get the "state" value from the ``target`` field (defined in the target section) on the
``input_number`` component of the Home Assistant front-end. This value is then passed to the API service as defined in
the ESPHome device's configuration. The ``data_template`` section lists one value for each of the input parameters on
the service being called by the automation. In our case, the ESPHome device has an API service with a single parameter,
"target". If you called this "my_target", then the last line above should be ``my_target: '{{ trigger.to_state.state | int }}'``.
Getting this linkage right is very important.

The following code needs to go in the ESPHome configuration file for this device. Above, we mention "API service"
a lot. This code is where that is defined. You may have already added it (or something similar). Note
that the input variable for the ``control_stepper`` service is called ``target``. That's what matches with the
automation configuration above. Also note that the variable ``target`` is defined as an integer. That means it
must be an integer number, not a string.

.. code-block:: yaml

    # ESPHome configuration
    api:
      services:
        - service: control_stepper
          variables:
            target: int
          then:
            - stepper.set_target:
                id: my_stepper
                target: !lambda 'return target;'

    stepper:
      - platform: ...
        # [...] stepper config
        id: my_stepper

.. _stepper-lambda_calls:

lambda calls
------------

From :ref:`lambdas <config-lambda>`, you can call several methods on stepper motors to do some
advanced stuff (see the full API Reference for more info).

- ``set_target``: Set the target position of the motor as an integer.

    .. code-block:: cpp

        // Argument is integer (signed int)
        // Set the (absolute) target position to 250 steps
        id(my_stepper).set_target(250);

- ``report_position``: Report the current position as an integer.

    .. code-block:: cpp

        // Report the (absolute) current position as 250 steps
        id(my_stepper).report_position(250);

- ``current_position``: Get the current position of the stepper as an integer.

    .. code-block:: cpp

        int pos = id(my_stepper).current_position;


- ``target_position``: Get the set target position of the stepper  as an integer.

    .. code-block:: cpp

        int pos = id(my_stepper).target_position;

See Also
--------

- :apiref:`stepper/stepper.h`
- :ghedit:`Edit`
