Alarm Control Panel Component
=============================

.. seo::
    :description: Instructions for setting up generic Alarm Control Panels in ESPHome.
    :image: alarm-panel.svg

.. _config-alarm_control_panel:

Base Alarm Control Panel Configuration
--------------------------------------

.. code-block:: yaml

    alarm_control_panel:
      - platform: ...
        name: Alarm Panel


Configuration variables:

- **name** (**Required**, string): The name of the alarm control panel.

  .. note::

      If you have a :ref:`friendly_name <esphome-configuration_variables>` set for your device and
      you want the switch to use that name, you can set ``name: None``.

- **on_state** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the alarm changes state. See :ref:`alarm_control_panel_on_state_trigger`.
- **on_triggered** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the alarm triggers. See :ref:`alarm_control_panel_on_triggered_trigger`.
- **on_cleared** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the alarm clears. See :ref:`alarm_control_panel_on_cleared_trigger`.


Automation:
-----------

.. _alarm_control_panel_on_state_trigger:

``on_state`` Trigger
********************

This trigger is activated each time the alarm changes state.

.. code-block:: yaml

    alarm_control_panel:
      # ...
      on_state:
        then:
          - logger.log: "Alarm Panel State Changed!"

.. _alarm_control_panel_on_triggered_trigger:

``on_triggered`` Trigger
************************

This trigger is activated when the alarm changes to triggered state.

.. code-block:: yaml

    alarm_control_panel:
      # ...
      on_triggered:
        then:
          - logger.log: "Alarm Triggered!"

.. _alarm_control_panel_on_cleared_trigger:

``on_cleared`` Trigger
**********************

This trigger is activated when the alarm changes from triggered back to either the previous armed state or disarmed.

.. code-block:: yaml

    alarm_control_panel:
      # ...
      on_cleared:
        then:
          - logger.log: "Alarm Cleared!"

.. _alarm_control_panel_arm_away_action:

``arm_away`` Action
*******************

This action arms the alarm in away mode. The ``code`` is required when *requires_code_to_arm* is *true*.

.. code-block:: yaml

    on_...:
      then:
        - alarm_control_panel.arm_away:
            id: acp1
            code: "1234"

.. _alarm_control_panel_arm_home_action:

``arm_home`` Action
*******************

This action arms the alarm in home mode. The ``code`` is required when *requires_code_to_arm* is *true*.

.. code-block:: yaml

    on_...:
      then:
        - alarm_control_panel.arm_home:
            id: acp1
            code: "1234"

.. _alarm_control_panel_disarm_action:

``disarm`` Action
*****************

This action disarms the alarm. The ``code`` is required when *codes* is not empty.

.. code-block:: yaml

    on_...:
      then:
        - alarm_control_panel.disarm:
            id: acp1
            code: "1234"

.. _alarm_control_panel_pending_action:

``pending`` Action
******************

This action puts the alarm in pending state (the state before triggered after *pending_time*).

.. code-block:: yaml

    on_...:
      then:
        - alarm_control_panel.pending: acp1

.. _alarm_control_panel_triggered_action:

``triggered`` Action
********************

This action puts the alarm in triggered state.

.. code-block:: yaml

    on_...:
      then:
        - alarm_control_panel.triggered: acp1

.. _alarm_control_panel_is_armed_condition:

``is_armed`` Condition
**********************

This :ref:`Condition <config-condition>` checks if the alarm control panel is armed.

.. code-block:: yaml

    on_...:
      if:
        condition:
          alarm_control_panel.is_armed: acp1


.. _alarm_control_panel_lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call the following methods:

- ``arm_away(code)``
- ``arm_home(code)``
- ``disarm(code)``

.. code-block:: cpp

    id(acp1).arm_away();
    id(acp1).arm_home();
    id(acp1).disarm("1234");


Platforms
---------

.. toctree::
    :maxdepth: 1
    :glob:

    *

See Also
--------

- :doc:`/components/binary_sensor/index`
- :apiref:`alarm_control_panel/alarm_control_panel.h`
- :ghedit:`Edit`
