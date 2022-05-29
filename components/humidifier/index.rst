Humidifier Component
====================

.. seo::
    :description: Information about the base representation of all humidifier devices.
    :image: folder-open.svg

ESPHome has support for humidifier devices. Humidifier devices can represent different types of
hardware, but the defining factor is that humidifier devices have a settable target humidity
and can be put in different modes like HUMIDIFY, DEHUMIDIFY, HUMIDIFY_DEHUMIDIFY, AUTO or OFF.

.. figure:: images/humidifier-ui.png
    :align: center
    :width: 60.0%

    Humidifier Device UI in Home Assistant.

.. _config-humidifier:

Base Humidifier Configuration
-----------------------------

All humidifier platforms in ESPHome inherit from the humidifier configuration schema.

.. code-block:: yaml

    humidifier:
      - platform: ...
        visual:
          min_humidity: 20%
          max_humidity: 70%
          humidity_step: 0.1%

Configuration variables:

- **icon** (*Optional*, icon): Manually set the icon to use for the humidifier device in the frontend.
- **visual** (*Optional*): Visual settings for the humidifier device - these do not
  affect operation and are solely for controlling how the humidifier device shows up in the
  frontend.

  - **min_humidity** (*Optional*, float): The minimum humidity the humidifier device can reach.
    Used to set the range of the frontend gauge.
  - **max_humidity** (*Optional*, float): The maximum humidity the humidifier device can reach.
    Used to set the range of the frontend gauge.
  - **humidity_step** (*Optional*, float): The granularity with which the target humidity
    can be controlled.

Advanced options:

- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Requires Home Assistant 2021.9 or newer. Defaults to ``false``.
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options. Requires Home Assistant 2021.11 or newer.
  Set to ``""`` to remove the default entity category.

MQTT options:

- **action_state_topic** (*Optional*, string): The topic to publish
  humidifier device action changes to.
- **away_state_topic** (*Optional*, string): The topic to publish
  away mode changes on.
- **away_command_topic** (*Optional*, string): The topic to receive
  away mode commands on.
- **current_humidity_state_topic** (*Optional*, string): The topic to publish
  current humidity changes to.
- **mode_state_topic** (*Optional*, string): The topic to publish
  humidifier device mode changes to.
- **mode_command_topic** (*Optional*, string): The topic to receive
  humidifier device mode commands on.
- **target_humidity_state_topic** (*Optional*, string): The topic to publish
  target humidity changes to.
- **target_humidity_command_topic** (*Optional*, string): The topic to receive
  target humidity commands on.
- **target_humidity_high_state_topic** (*Optional*, string): The topic to publish
  higher target humidity changes to.
- **target_humidity_high_command_topic** (*Optional*, string): The topic to receive
  higher target humidity commands on.
- **target_humidity_low_state_topic** (*Optional*, string): The topic to publish
  lower target humidity changes to.
- **target_humidity_low_command_topic** (*Optional*, string): The topic to receive
  lower target humidity commands on.
- All other options from :ref:`MQTT Component <config-mqtt-component>`.

Humidifier Automation
---------------------

.. _humidifier-control_action:

``humidifier.control`` Action
*****************************

This is an :ref:`Action <config-action>` for setting parameters for humidifier devices.

.. code-block:: yaml

    - humidifier.control:
        id: my_humidifier
        mode: HUMIDIFY_DEHUMIDIFY
        target_humidity: 40%

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the humidifier device to control.
- **mode** (*Optional*, string, :ref:`templatable <config-templatable>`): Put the humidifier device
  in a specific mode. One of

  - ``OFF`` - The device is manually set to off, the device is inactive.
  - ``AUTO`` - The device should adjust the humidity dynamically. For example based on a schedule, or learned behavior.
  - ``HUMIDIFY`` - The device is set to humidify to reach a target humidity.
  - ``DEHUMIDIFY`` - The device is set to dehumidify to reach a target humidity.
  - ``HUMIDIFY_DEHUMIDIFY`` - The device should humidify/dehumidify to maintain a target humidity.

- **target_humidity** (*Optional*, float, :ref:`templatable <config-templatable>`): Set the
  target humidity of a humidifier device.
- **target_humidity_low** (*Optional*, float, :ref:`templatable <config-templatable>`): Set the
  lower target humidity of a humidifier device with a two-point target humidity.
- **target_humidity_high** (*Optional*, float, :ref:`templatable <config-templatable>`): Set the
  higher target humidity of a humidifier device with a two-point target humidity.
- **away** (*Optional*, boolean, :ref:`templatable <config-templatable>`): Set the away mode
  of the humidifier device.
- **preset** (*Optional*, string, :ref:`templatable <config-templatable>`): Set the preset
  of the humidifier device. One of ``NONE``,``ECO``, ``AWAY``, ``BOOST``, ``COMFORT``, ``HOME``, ``SLEEP``,
  ``ACTIVITY``.

.. _humidifier-lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all binary sensors to do some
advanced stuff.

- Attributes: All humidifier devices have read-only attributes to get the current state of the device.

  .. code-block:: cpp

      // Current mode, type: HumidifierMode (enum)
      id(my_humidifier).mode
      // Current humidity, type: float (percentage)
      id(my_humidifier).current_humidity
      // Target humidity, type: float (percentage)
      id(my_humidifier).target_humidity
      // Lower Target humidity, type: float (percentage)
      id(my_humidifier).target_humidity_low
      // High Target humidity, type: float (percentage)
      id(my_humidifier).target_humidity_high

- ``.make_call``: Control the humidifier device

  .. code-block:: cpp

      auto call = id(my_humidifier).make_call();
      call.set_mode("OFF");
      // etc. see API reference
      call.perform();

.. _humidifier-on_state_trigger:

``humidifier.on_state`` Trigger
******************************************************

This trigger is activated each time the state of the humidifier device is updated 
(for example, if the current humidity measurement or the mode set by the users changes).

.. code-block:: yaml

    humidifier:
      - platform: hygrostat  # or any other platform
        # ...
        on_state:
        - logger.log: "State updated!"

See Also
--------

- :apiref:`humidifier/humidifier.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
