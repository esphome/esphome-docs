Climate Component
=================

.. seo::
    :description: Information about the base representation of all climate devices.
    :image: folder-open.svg

ESPHome has support for climate devices. Climate devices can represent different types of
hardware, but the defining factor is that climate devices have a settable target temperature
and can be put in different modes like ``HEAT``, ``COOL``, ``HEAT_COOL`` or ``OFF``.

.. figure:: images/climate-ui.png
    :align: center
    :width: 60.0%

    Climate Device UI in Home Assistant.

.. note::

    Not all climate components support all possible features. Check the corresponding documentation page for details on what is supported.

.. _config-climate:

Base Climate Configuration
--------------------------

All climate platforms in ESPHome inherit from the climate configuration schema. In ESPHome, ``°C`` is assumed for all temperature values. Some platforms allow conversion or setting in ``°F``, this is specified separately.

.. code-block:: yaml

    climate:
      - platform: ...
        visual:
          min_temperature: 18
          max_temperature: 25
          temperature_step: 0.1
          min_humidity: 30%
          max_humidity: 99%
      - platform: ...
        visual:
          min_temperature: 18
          max_temperature: 25
          temperature_step:
            target_temperature: 0.5
            current_temperature: 0.1

Configuration variables:

- **id** (*Optional*, string): Manually specify the ID for code generation. At least one of **id** and **name** must be specified.
- **name** (*Optional*, string): The name of the climate device. At least one of **id** and **name** must be specified.

  .. note::

      If you have a :ref:`friendly_name <esphome-configuration_variables>` set for your device and
      you want the climate to use that name, you can set ``name: None``.

- **icon** (*Optional*, icon): Manually set the icon to use for the climate device in the frontend.
- **visual** (*Optional*): Visual settings for the climate device - these do not
  affect operation and are solely for controlling how the climate device shows up in the
  frontend.

  - **min_temperature** (*Optional*, float): The minimum temperature the climate device can reach.
    Used to set the range of the frontend gauge.
  - **max_temperature** (*Optional*, float): The maximum temperature the climate device can reach.
    Used to set the range of the frontend gauge.
  - **temperature_step** (*Optional*, float): The granularity with which the target temperature
    can be controlled. Can be a single number, or split as below:

    - **target_temperature** (**Required**, float): The granularity for target temperature
    - **current_temperature** (**Required**, float): The granularity for current temperature

  - **min_humidity** (*Optional*, percentage): The minimum humidity the climate device can reach.
    Used to set the range of the frontend gauge.
  - **max_humidity** (*Optional*, percentage): The maximum humidity the climate device can reach.
    Used to set the range of the frontend gauge.

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
- If Webserver enabled and version 3 is selected, All other options from Webserver Component.. See :ref:`Webserver Version 3 <config-webserver-version-3-options>`.

MQTT options:

- **action_state_topic** (*Optional*, string): The topic to publish
  climate device action changes to.
- **current_temperature_state_topic** (*Optional*, string): The topic to publish
  current temperature changes to.
- **current_humidity_state_topic** (*Optional*, string): The topic to publish
  current humidity changes to.
- **fan_mode_state_topic** (*Optional*, string): The topic to publish
  fan mode changes to.
- **fan_mode_command_topic** (*Optional*, string): The topic to receive
  fan mode commands on.
- **mode_state_topic** (*Optional*, string): The topic to publish
  climate device mode changes to.
- **mode_command_topic** (*Optional*, string): The topic to receive
  climate device mode commands on.
- **preset_state_topic** (*Optional*, string): The topic to publish
  preset changes to.
- **preset_command_topic** (*Optional*, string): The topic to receive
  preset commands on.
- **swing_mode_state_topic** (*Optional*, string): The topic to publish
  swing mode changes to.
- **swing_mode_command_topic** (*Optional*, string): The topic to receive
  swing mode commands on.
- **target_temperature_state_topic** (*Optional*, string): The topic to publish
  target temperature changes to.
- **target_temperature_command_topic** (*Optional*, string): The topic to receive
  target temperature commands on.
- **target_temperature_high_state_topic** (*Optional*, string): The topic to publish
  higher target temperature changes to.
- **target_temperature_high_command_topic** (*Optional*, string): The topic to receive
  higher target temperature commands on.
- **target_temperature_low_state_topic** (*Optional*, string): The topic to publish
  lower target temperature changes to.
- **target_temperature_low_command_topic** (*Optional*, string): The topic to receive
  lower target temperature commands on.
- **target_humidity_state_topic** (*Optional*, string): The topic to publish
  target humidity changes to.
- **target_humidity_command_topic** (*Optional*, string): The topic to receive
  target humidity commands on.
- All other options from :ref:`MQTT Component <config-mqtt-component>`.

Climate Automation
------------------

.. _climate-control_action:

``climate.control`` Action
**************************

This is an :ref:`Action <config-action>` for setting parameters for climate devices.

.. code-block:: yaml

    - climate.control:
        id: my_climate
        mode: HEAT_COOL
        target_temperature: 25°C

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the climate device to control.
- **mode** (*Optional*, string, :ref:`templatable <config-templatable>`): Put the climate device
  in a specific mode. One of

  - ``OFF`` - The device is manually set to off, the device is inactive.
  - ``AUTO`` - The device is should adjust the temperature dynamically. For example based on a schedule, or learned behavior.
  - ``HEAT`` - The device is set to heat to reach a target temperature.
  - ``COOL`` - The device is set to cool to reach a target temperature.
  - ``HEAT_COOL`` - The device should heat/cool to maintain a target temperature.
  - ``FAN_ONLY`` - The device only has the fan enabled, no heating or cooling is taking place.
  - ``DRY`` - The device is set to dry/humidity mode.

- **target_temperature** (*Optional*, float, :ref:`templatable <config-templatable>`): Set the
  target temperature of a climate device.
- **target_temperature_low** (*Optional*, float, :ref:`templatable <config-templatable>`): Set the
  lower target temperature of a climate device with a two-point target temperature.
- **target_temperature_high** (*Optional*, float, :ref:`templatable <config-templatable>`): Set the
  higher target temperature of a climate device with a two-point target temperature.
- **target_humidity** (*Optional*, float, :ref:`templatable <config-templatable>`): Set the
  target humidity of a climate device.
- **preset** (*Optional*, string, :ref:`templatable <config-templatable>`): Set the preset
  of the climate device. One of ``ECO``, ``AWAY``, ``BOOST``, ``COMFORT``, ``HOME``, ``SLEEP``,
  ``ACTIVITY``.
- **custom_preset** (*Optional*, string, :ref:`templatable <config-templatable>`): Set one of the
  supported custom_presets of the climate device.
- **fan_mode** (*Optional*, string, :ref:`templatable <config-templatable>`): Set the fan mode
  of the climate device. One of ``ON``, ``OFF``, ``AUTO``, ``LOW``, ``MEDIUM``, ``HIGH``, ``MIDDLE``,
  ``FOCUS``, ``DIFFUSE``, ``QUIET``.
- **custom_fan_mode** (*Optional*, string, :ref:`templatable <config-templatable>`): Set one of the
  supported custom_fan_modes of the climate device.
- **swing_mode** (*Optional*, string, :ref:`templatable <config-templatable>`): Set the swing mode
  of the climate device. One of ``OFF``, ``BOTH``, ``VERTICAL``, ``HORIZONTAL``.

.. _climate-lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all binary sensors to do some
advanced stuff.

- Attributes: All climate devices have read-only attributes to get the current state of the device.

  .. code-block:: cpp

      // Current mode, type: ClimateMode (enum)
      id(my_climate).mode
      // Current temperature, type: float (degrees)
      id(my_climate).current_temperature
      // Current humidity, type: float (percentage)
      id(my_climate).current_humidity
      // Target temperature, type: float (degrees)
      id(my_climate).target_temperature
      // Lower Target temperature, type: float (degrees)
      id(my_climate).target_temperature_low
      // High Target temperature, type: float (degrees)
      id(my_climate).target_temperature_high
      // Target humidity, type: float (percentage)
      id(my_climate).target_humidity
      // Fan mode, type: FanMode (enum)
      id(my_climate).fan_mode
      // Custom Fan mode, type: string
      id(my_climate).custom_fan_mode
      // Swing mode, type: SwingMode (enum)
      id(my_climate).swing_mode
      // Current action (currentl on idle, cooling, heating, etc.), ClimateAction (enum)
      id(my_climate).action
      // Preset, type: Preset (enum)
      id(my_climate).preset
      // Custom Preset, type: string
      id(my_climate).custom_preset


- ``.make_call``: Control the climate device

  .. code-block:: cpp

      auto call = id(my_climate).make_call();
      call.set_mode("OFF");
      // etc. see API reference
      call.perform();

.. _climate-on_state_trigger:

``climate.on_state`` Trigger
****************************

This trigger is activated each time the state of the climate device is updated
(for example, if the current temperature measurement or the mode set by the users changes).
The ``Climate`` itself is available to automations as the reference ``x``.

.. code-block:: yaml

    climate:
      - platform: midea  # or any other platform
        # ...
        on_state:
          - logger.log: "State updated!"
          - lambda: |-
              if (x.mode != CLIMATE_MODE_OFF)
                id(some_binary_sensor).publish_state(true);


.. _climate-on_control_trigger:

``climate.on_control`` Trigger
******************************

This trigger is activated each time a *control* input of the climate device
is updated via a ``ClimateCall`` (which includes changes coming in from Home
Assistant).  That is, this trigger is activated for, for example, changes to
the mode, *but not* on temperature measurements.  It will be invoked prior to
the ``on_state`` trigger, if both are defined. The ``ClimateCall`` control
object is available to automations as the reference ``x`` that can be changed.

.. code-block:: yaml

    climate:
      - platform: ...
        # ...
        on_control:
          - logger.log: "Control input received; configuration updated!"
          - lambda: |-
              if (x.get_mode() != CLIMATE_MODE_OFF) {
                  id(turnoff_script).stop();
                  x.set_target_temperature(25.0f);
              }


See Also
--------

- :apiref:`climate/climate.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
