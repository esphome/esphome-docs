Humidifier Component
====================

.. seo::
    :description: Information about the base representation of all humidifier devices.
    :image: folder-open.svg

ESPHome has support for humidifier devices. Humidifier devices can represent different types of
hardware, but the defining factor is that humidifier devices have a settable target humidity
and can be put in different output modes like ``NORMAL``, ``BOOST``, ``ECO``, ``SLEEP``, ``BABY``, ``AUTO`` or ``OFF``.

.. note::

    Not all humidifier components support all possible features. Check the corresponding documentation page for details on what is supported.

.. _config-humidifier:

Base Humidifier Configuration
-----------------------------

.. code-block:: yaml

    humidifier:
      - platform: ...
        visual:
          min_humidity: 40%
          max_humidity: 85%
          humidity_step: 1
      - platform: ...
        visual:
          min_humidity: 40%
          max_humidity: 85%
          humidity_step: 
            target_humidity: 2
            current_humidity: 1

Configuration variables:

- **name** (**Required**, string): The name of the humidifier device.

  .. note::

      If you have a :ref:`friendly_name <esphome-configuration_variables>` set for your device and
      you want the humidifier to use that name, you can set ``name: None``.

- **icon** (*Optional*, icon): Manually set the icon to use for the humidifier device in the frontend.
- **visual** (*Optional*): Visual settings for the humidifier device - these do not
  affect operation and are solely for controlling how the humidifier device shows up in the
  frontend.

  - **min_humidity** (*Optional*, float): The minimum humidity the humidifier device can reach.
    Used to set the range of the frontend gauge.
  - **max_humidity** (*Optional*, float): The maximum humidity the humidifier device can reach.
    Used to set the range of the frontend gauge.
  - **humidity_step** (*Optional*, float): The granularity with which the target humidity
    can be controlled. Can be a single number, or split as below:

    - **target_humidity** (**Required**, float): The granularity for target humidity
    - **current_humidity** (**Required**, float): The granularity for current humidity


Advanced options:

- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Defaults to ``false``.
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options.
  Set to ``""`` to remove the default entity category.

MQTT options:

- **action_state_topic** (*Optional*, string): The topic to publish
  humidifier device action changes to.
- **current_humidity_state_topic** (*Optional*, string): The topic to publish
  current humidity changes to.
- **target_humidity_state_topic** (*Optional*, string): The topic to publish
  target humidity changes to.
- **target_humidity_command_topic** (*Optional*, string): The topic to receive
  target humidity commands on.
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
        mode: BOOST
        target_humidity: 25°C

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the humidifier device to control.
- **mode** (*Optional*, string, :ref:`templatable <config-templatable>`): Put the humidifier device
  in a specific mode. One of

  - ``OFF`` - The device is manually set to off, the device is inactive.
  - ``NORMAL`` - The device has a normal outflow of humidified air.
  - ``ECO`` - The device has a reduce outflow of humidified air.
  - ``BOOST`` - The device has a increased outflow of humidified air.
  - ``AUTO`` - The device is should adjust the humidity dynamically. For example based on a schedule, or learned behavior.
  - ``SLEEP`` - Manufacturer set setting based on best output for running the device while sleeping.
  - ``BABY`` - Manufacturer set setting based on best output for running the device while a baby is in the room.

- **target_humidity** (*Optional*, float, :ref:`templatable <config-templatable>`): Set the
  target humidity of a humidifier device.

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
      // Current action (currently on Boost, Eco, Normal, etc.), HumidifierAction (enum)
      id(my_humidifier).action


- ``.make_call``: Control the humidifier device

  .. code-block:: cpp

      auto call = id(my_humidifier).make_call();
      call.set_mode("OFF");
      // etc. see API reference
      call.perform();

.. _humidifier-on_state_trigger:

``humidifier.on_state`` Trigger
*******************************

This trigger is activated each time the state of the humidifier device is updated
(for example, if the current humidity measurement or the mode set by the users changes).
The ``Humidifier`` itself is available to automations as the reference ``x``.

.. code-block:: yaml

    humidifier:
      - platform: generic_humidifier  # or any other platform
        # ...
        on_state:
          - logger.log: "State updated!"
          - lambda: |-
              if (x.mode != HUMIDIFIER_MODE_OFF)
                id(some_binary_sensor).publish_state(true);


.. _humidifier-on_control_trigger:

``humidifier.on_control`` Trigger
*********************************

This trigger is activated each time a *control* input of the humidifier device
is updated via a ``HumidifierCall`` (which includes changes coming in from Home
Assistant).  That is, this trigger is activated for, for example, changes to
the mode, *but not* on humidity measurements.  It will be invoked prior to
the ``on_state`` trigger, if both are defined. The ``HumidifierCall`` control
object is available to automations as the reference ``x`` that can be changed.

.. code-block:: yaml

    humidifier:
      - platform: ...
        # ...
        on_control:
          - logger.log: "Control input received; configuration updated!"
          - lambda: |-
              if (x.get_mode() != HUMIDIFIER_MODE_OFF) {
                  id(turnoff_script).stop();
                  x.set_target_humidity(25.0f);
              }


See Also
--------

- :apiref:`humidifier/humidifier.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
