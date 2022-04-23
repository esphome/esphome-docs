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
        oscillation_output: output_fan_oscillating
        decay_mode: SLOW
        min_speed: 0.1
        acceleration: 10000ms
        deceleration: 5000ms
        brake_when_stopped: 2000ms
        brake_buildup_when_stopped: 3000ms


Output assignment
*****************

- **pin_a** (**Required**, :ref:`config-id`): The id of the :ref:`float output <output>` 
  connected to Pin A (alternatively IN1, etc.) of the h-bridge.
- **pin_b** (**Required**, :ref:`config-id`): The id of the :ref:`float output <output>` 
  connected to Pin B (alternatively IN2, etc.) of the h-bridge.
- **enable_pin** (*Optional*, :ref:`config-id`): The id of the :ref:`float output <output>` 
  connected to the Enable pin of the h-bridge (if h-bridge uses enable). Default is ``null`` (not used)
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


Motor drive options
*******************
- **decay_mode** (*Optional*, string): The current decay mode you want to use with
  the h-bridge. Either ``SLOW`` (braking) or ``FAST`` (coasting). 
  For more information on current decay see `this link <https://learn.adafruit.com/improve-brushed-dc-motor-performance/current-decay-mode>`__.
  Defaults to ``SLOW``.
- **min_speed** (*Optional*, float): The minimum dutycycle your motor needs to run.
  This is the minimum speed dutycycle the motor will be driven at for the lowest speed.
  Defaults to ``0``.
- **acceleration** (*Optional*, int): Time a 0 to 100% acceleration will be extended over. 
  If for example the speed is increased from 40% to 50% it will be extended over 10% of the set value respectively.
  Defaults to ``0``, meaning change power at once. 
- **deceleration** (*Optional*, int): Time a 0 to 100% deceleration will be extended over. 
  If for example the speed is increased from 70% to 60% it will be extended over 10% of the set value respectively.
  Defaults to ``0``, meaning change power at once. 
- **brake_when_stopped** (*Optional*, int): Time the motor is braked (short windings) after it is stopped (set speed to 0%)
  Defaults to ``0`` (no braking)
- **brake_buildup_when_stopped** (*Optional*, int): Time the braking (shorting of windings) is gradually increased from 0% to 100% after it is stopped (set speed to 0%)
  This duration is the gradual buildup time only, it does not include the full brake time. This option is ignored when **decay_mode** is set to ``SLOW``.
  Defaults to ``0`` (skip gradual buildup)

.. note::

    Shorting/braking is only done when doing a full-stop or reversing direction. Since we have no feedback how fast the motor is actually going and cannot "brake until speed X"



.. _fan-hbridge_brake_action:

``fan.hbridge.brake`` Action
----------------------------

Initiate a brake action (see transition description for further information).

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
