Alarm Control Panel
===================

.. seo::
    :description: Instructions for setting up an Alarm Control Panel in ESPHome.
    :image: alarm-panel.svg

Turn your binary sensors into an alarm control panel with the power of ESPHome.

.. code-block:: yaml

    alarm_control_panel:
      name: Alarm Panel
      code: "1234"
      binary_sensors:
        - input: zone_1
        - input: zone_2
          bypass_armed_home: true

Configuration:
--------------

- **name** (**Required**, string): The name of the alarm control panel.
- **code** (*Optional*, string): Code for disarming the alarm, if *requires_code_to_arm* set to true then for arming the alarm too.
- **requires_code_to_arm** (*Optional*, boolean): Code required for arming the alarm, *code* must be provided.
- **arming_time** (*Optional*, number): The exit delay before the alarm is armed.
- **delay_time** (*Optional*, number): The entry delay before the alarm is triggered.
- **trigger_time** (*Optional*, number): The time after a triggered alarm before resetting to previous state if the sensors are cleared/off.
- **binary_sensors** (**Required**, *list*): A list of binary sensors the panel should use. Each consists of:

  - **input** (**Required**, string): The id of the binary sensor component 
  - **bypass_armed_home** (*Optional*, boolean): This binary sensor will not trigger the alarm when in ``armed_home`` state.

- **on_state** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the alarm changes state. See :ref:`alarm_control_panel_on_state_trigger`.

Automation:
-----------

.. _alarm_control_panel_on_state_trigger:

``alarm_control_panel.on_state`` Trigger
****************************************

This trigger is activated each time the alarm changes state.

.. code-block:: yaml

    alarm_control_panel:
      # ...
      on_state:
        then:
          - logger.log: "Alarm Panel State Changed!"

.. _alarm_control_panel_lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call the following methods:

- ``arm_away(code)``
- ``arm_home(code)``
- ``arm_disarm(code)``

.. code-block:: cpp

    id(alarm).arm_away("");
    id(alarm).arm_home("");
    id(alarm).arm_disarm("1234");

.. _alarm_control_panel_state_flow:

State Flow:
-----------

1. The alarm starts in ``DISARMED`` state
2. When the ``arm_...`` method is invoked

  a. ``arming_time`` greater than 0 the state is ``ARMING``
  b. ``arming_time`` is 0 or after the ``arming_time`` delay the state is ``ARM_AWAY`` or ``ARM_HOME``

3. When the alarm is triggered by a sensor state changing to ``on``

  a. ``delay_time`` greater than 0 the state is ``PENDING``
  b. ``delay_time`` is 0 or after the ``delay_time`` delay the state is ``TRIGGERED``

4. If ``trigger_time`` greater than 0 and no sensors are ``on`` after ``trigger_time`` delay
   the state returns to ``ARM_AWAY`` or ``ARM_HOME``

.. _alarm_control_panel_example:

Example:
--------

.. code-block:: yaml

    alarm_control_panel:
      name: Alarm Panel
      code: "1234"
      requires_code_to_arm: true
      arming_time: 10
      delay_time: 15
      trigger_time: 30
      binary_sensors:
        - input: zone_1
        - input: zone_2
          bypass_armed_home: true
        - input: ha_test
      on_state:
        then:
          - lambda: !lambda |-
              ESP_LOGD("TEST", "State change %s", id(alarm)->to_string(id(alarm)->get_state()).c_str());

    binary_sensor:
      - platform: gpio
        id: zone_1
        name: Zone 1
        device_class: door
        pin:
          number: D1
          mode: INPUT_PULLUP
          inverted: True
      - platform: gpio
        id: zone_2
        name: Zone 2
        device_class: motion
        pin:
          number: D2
          mode: INPUT_PULLUP
          inverted: True
      - platform: homeassistant
        id: ha_test
        name: Zone 3
        entity_id: input_boolean.test_switch

See Also
--------

- :doc:`/components/binary_sensor/index`
- :apiref:`alarm_control_panel/alarm_control_panel.h`
- :ghedit:`Edit`
