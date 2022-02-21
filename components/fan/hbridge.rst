H-bridge Fan
============

.. seo::
    :description: Instructions for setting up h-bridge controlled fans (or motors).
    :image: fan.svg

The ``hbridge`` fan platform allows you to use a `h-bridge` circuit or IC (L298N, DRV8871, MX1508, BTS7960, L9110S, DRV8833, TB6612, etc.) 
to control a fan or generic dc-motor.

Home assistant has no generic component for a motor. The ``Fan`` component is the closest match.

.. figure:: images/L298N_module.jpg
    :alt: hbdrige module
    :align: center
    :target: `kuongshun`_
    :width: 40.0%

    L298N H-bridge module. Image by `kuongshun`_.

.. _kuongshun: https://kuongshun.com/products/l298n-stepper-motor-driver-board-red

.. figure:: images/fan-ui.png
    :alt: Fan UI
    :align: center
    :width: 80.0%

Configuration
-------------

.. code-block:: yaml

    # Output config list
    # Note: For PWM output use "esp8266_pwm" for ESP8266 or "ledc" for ESP32 as platform
    output:
      - platform: ... # PWM Capable output platform
        id: output_fan_a
        pin: ... # Output pin assignment
        frequency: 50 Hz
      - platform: ... # PWM Capable output platform
        id: output_fan_b
        pin: ... # Output pin assignment
        frequency: 50 Hz
      - platform: ... # PWM Capable output platform
        id: output_fan_enable
        pin: ... # Output pin assignment
        frequency: 50 Hz
      - platform: gpio
        id: output_fan_oscillating
        pin: ... # Output pin assignment


    # Fan config
    fan:
      - platform: hbridge
        id: hbridge_fan
        name: "H-Bridge Fan"
        pin_a: output_fan_a
        pin_b: output_fan_b
        enable_pin: output_fan_enable
        decay_mode: SLOW
        oscillation_output: output_fan_oscillating
        transition_delta_per_ms: 0.001
        transition_short_buildup_duration: 5000ms
        transition_full_short_duration: 3000ms


Output assignment
*****************

- **pin_a** (**Required**, :ref:`config-id`): The id of the :ref:`float output <output>` 
  connected to Pin A (alternatively IN1, etc.) of the h-bridge.
- **pin_b** (**Required**, :ref:`config-id`): The id of the :ref:`float output <output>` 
  connected to Pin B (alternatively IN2, etc.) of the h-bridge.
- **enable_pin** (*Optional*, :ref:`config-id`): The id of the :ref:`float output <output>` 
  connected to the Enable pin of the h-bridge (if h-bridge uses enable). Default is ``null`` (not used)
- **decay_mode** (*Optional*, string): The current decay mode you want to use with
  the h-bridge. Either ``SLOW`` (braking) or ``FAST`` (coasting). Defaults to ``SLOW``.
  For more information on current decay see `this link <https://learn.adafruit.com/improve-brushed-dc-motor-performance/current-decay-mode>`__

- **oscillation_output** (*Optional*, :ref:`config-id`): The id of the :ref:`output <output>` 
  to use for the oscillation state of this fan. Default is ``null`` (not used)

Fan configuration
*****************

- **speed_count** (*Optional*, int): Set the number of supported discrete speed levels. The value is used
  to calculate the percentages for each speed. E.g. ``2`` means that you have 50% and 100% while ``100``
  will allow 1% increments in the output. Defaults to ``100``.
- **name** (**Required**, string): The name for this fan.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Fan Component <config-fan>`.

Transition configuration
********************************

- **transition_delta_per_ms** (*Optional*, float): Delta to apply each millisecond  when changing the set speed. 
  Defaults to ``2`` (no transition)
- **transition_short_buildup_duration** (*Optional*, float): duration in milliseconds to buildup from no to full short.
  Defaults to ``0`` (no shorting/braking = coasting)
- **transition_full_short_duration** (*Optional*, float): duration in milliseconds to apply full short (after optional buildup).
  Defaults to ``0`` (no shorting/braking = coasting)



Transitions explained
---------------------

When changing speeds (especially on a motor driving a large load) inertia will play its part.
Trying to speed up the motor inertia will require to motor to use large amounts of current to get things going.
You can reduce the load on your system by gradually increasing the speed. Use the *transition_delta_per_ms* parameter for this.
This will increment the speed with the set value every millisecond until the set speed has been reached.
For example use ``0.001`` to stretch a 0 (still) to 1 (full speed) increment over 1 second.
This parameter also applies to slowing down.

The reverse is true for stopping/reducing speed. Inertia will cause the motor to keep going (coasting).
To reduce the speed faster you need to brake. Fortunately you can electrically brake a motor by shorting its windings.
Use the *transition_short_buildup_duration* to set a duration to buildup the braking/shorting. from a bit to full. 
You can skip this step (set it to ``0``) if you need to.
How long to apply the brake/short (when reaching full brake/short) is set by the *transition_full_short_duration* parameter. 
Depending on your application you want to make sure you handle a full-speed to standstill stop with this duration.

.. note::

    Shorting/braking is only done when doing a full-stop or reversing direction. Since we have no feedback how fast the motor is actually going and cannot "brake until speed X"



.. _fan-hbridge_brake_action:

``fan.hbridge.brake`` Action
----------------------------

Initiate a brake/short action (see transition description for further information).

.. code-block:: yaml

    on_...:
      then:
        - fan.hbridge.brake: my_fan

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/fan/index`
- :doc:`/components/output/ledc`
- :doc:`/components/output/esp8266_pwm`
- :apiref:`fan/fan_state.h`
- `Adafruit's basic H-bridge tutorial <https://learn.adafruit.com/adafruit-arduino-lesson-15-dc-motor-reversing/overview>`__
- `Adafruit's advanced H-bridge tutorial <https://learn.adafruit.com/improve-brushed-dc-motor-performance>`__
- :ghedit:`Edit`
