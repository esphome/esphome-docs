Template Alarm Control Panel
============================

.. seo::
    :description: Instructions for setting up template Alarm Control Panels in ESPHome.
    :image: description.svg

The ``template`` alarm control panel platform allows you to turn your binary sensors into a state machine
managed alarm control panel.

.. code-block:: yaml

    # Example configuration entry
    alarm_control_panel:
      - platform: template
        name: Alarm Panel
        codes:
          - "1234"
        binary_sensors:
          - input: zone_1
          - input: zone_2
            bypass_armed_home: true

Configuration variables:
------------------------

- **codes** (*Optional*, list of string): A list of codes for disarming the alarm, if *requires_code_to_arm* set to true then for arming the alarm too.
- **requires_code_to_arm** (*Optional*, boolean): Code required for arming the alarm, *codes* must be provided.
- **arming_away_time** (*Optional*, :ref:`config-time`): The exit delay before the alarm is armed to away mode. Defaults to ``0s``.
- **arming_home_time** (*Optional*, :ref:`config-time`): The exit delay before the alarm is armed to home mode.  
- **pending_time** (*Optional*, :ref:`config-time`): The entry delay before the alarm is triggered. Defaults to ``0s``.
- **trigger_time** (*Optional*, :ref:`config-time`): The time after a triggered alarm before resetting to previous state if the sensors are cleared/off. Defaults to ``0s``.
- **binary_sensors** (*Optional*, *list*): A list of binary sensors the panel should use. Each consists of:

  - **input** (**Required**, string): The id of the binary sensor component
  - **bypass_armed_home** (*Optional*, boolean): This binary sensor will not trigger the alarm when in ``armed_home`` state.

- **restore_mode** (*Optional*, enum):

  - ``ALWAYS_DISARMED`` (Default): Always start in ``disarmed`` state.
  - ``RESTORE_DEFAULT_DISARMED``: Restore state or default to ``disarmed`` state if no saved state was found.

- All other options from :ref:`Alarm Control Panel <config-alarm_control_panel>`

.. note::

    If ``binary_sensors`` is ommited then you're expected to trigger the alarm using
    :ref:`alarm_control_panel_pending_action` or :ref:`alarm_control_panel_triggered_action`.


.. _template_alarm_control_panel-state_flow:

State Flow:
-----------

1. The alarm starts in ``DISARMED`` state
2. When the ``arm_...`` method is invoked

  a. ``arming_..._time`` is greater than 0 the state is ``ARMING``
  b. ``arming_..._time`` is 0 or after the delay the state is ``ARMED_...``

3. When the alarm is tripped by a sensor state changing to ``on`` or ``alarm_control_panel_pending_action`` invoked

  a. ``pending_time`` greater than 0 the state is ``PENDING``
  b. ``pending_time`` is 0 or after the ``pending_time`` delay the state is ``TRIGGERED``

4. If ``trigger_time`` greater than 0 and no sensors are ``on`` after ``trigger_time`` delay
   the state returns to ``ARM_...``

.. note::

    Although the interface supports all arming modes only ``away`` and ``home`` have been implemented for now.
    ``arm_...`` is for either ``arm_away`` or ``arm_home``
    ``arming_..._time`` is for either ``arming_away_time`` or ``arming_home_time``
    ``ARMED_...`` is for either ``ARMED_AWAY`` or ``ARMED_HOME``


Example:
--------

.. code-block:: yaml

    alarm_control_panel:
      platform: template
      name: Alarm Panel
      id: acp1
      codes:
        - "1234"
      requires_code_to_arm: true
      arming_away_time: 30s
      arming_home_time: 5s
      pending_time: 30s
      trigger_time: 5min
      binary_sensors:
        - input: zone_1
        - input: zone_2
          bypass_armed_home: true
        - input: ha_test
      on_state:
        then:
          - lambda: !lambda |-
              ESP_LOGD("TEST", "State change %s", alarm_control_panel_state_to_string(id(acp1)->get_state()));
      on_triggered:
        then:
          - switch.turn_on: siren
      on_cleared:
        then:
          - switch.turn_off: siren

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

    switch:
      - platform: gpio
        id: siren
        name: Siren
        icon: mdi:alarm-bell
        pin: D7


See Also
--------

- :doc:`index`
- :doc:`/components/binary_sensor/index`
- :apiref:`template/alarm_control_panel/template_alarm_control_panel.h`
- :ghedit:`Edit`
