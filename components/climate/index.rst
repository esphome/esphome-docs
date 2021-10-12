Climate Component
=================

.. seo::
    :description: Information about the base representation of all climate devices.
    :image: folder-open.png

ESPHome has support for climate devices. Climate devices can represent different types of
hardware, but the defining factor is that climate devices have a settable target temperature
and can be put in different modes like HEAT, COOL, HEAT_COOL or OFF.

.. figure:: images/climate-ui.png
    :align: center
    :width: 60.0%

    Climate Device UI in Home Assistant.

.. _config-climate:

Base Climate Configuration
--------------------------

All climate platforms in ESPHome inherit from the climate configuration schema.

.. code-block:: yaml

    climate:
      - platform: ...
        visual:
          min_temperature: 18 °C
          max_temperature: 25 °C
          temperature_step: 0.1 °C

Configuration variables:

- **icon** (*Optional*, icon): Manually set the icon to use for the climate device in the frontend.
- **visual** (*Optional*): Visual settings for the climate device - these do not
  affect operation and are solely for controlling how the climate device shows up in the
  frontend.

  - **min_temperature** (*Optional*, float): The minimum temperature the climate device can reach.
    Used to set the range of the frontend gauge.
  - **max_temperature** (*Optional*, float): The maximum temperature the climate device can reach.
    Used to set the range of the frontend gauge.
  - **temperature_step** (*Optional*, float): The granularity with which the target temperature
    can be controlled.

Advanced options:

- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Requires Home Assistant 2021.9 or newer. Defaults to ``false``.

MQTT options:

- **action_state_topic** (*Optional*, string): The topic to publish
  climate device action changes to.
- **away_state_topic** (*Optional*, string): The topic to publish
  away mode changes on.
- **away_command_topic** (*Optional*, string): The topic to receive
  away mode commands on.
- **current_temperature_state_topic** (*Optional*, string): The topic to publish
  current temperature changes to.
- **fan_mode_state_topic** (*Optional*, string): The topic to publish
  fan mode changes to.
- **fan_mode_command_topic** (*Optional*, string): The topic to receive
  fan mode commands on.
- **mode_state_topic** (*Optional*, string): The topic to publish
  climate device mode changes to.
- **mode_command_topic** (*Optional*, string): The topic to receive
  climate device mode commands on.
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
- **away** (*Optional*, boolean, :ref:`templatable <config-templatable>`): Set the away mode
  of the climate device.
- **preset** (*Optional*, string, :ref:`templatable <config-templatable>`): Set the preset
  of the climate device. One of ``ECO``, ``AWAY``, ``BOOST``, ``COMFORT``, ``HOME``, ``SLEEP``,
  ``ACTIVITY``.
- **custom_preset** (*Optional*, string, :ref:`templatable <config-templatable>`): Set one of the
  supported custom_presets of the climate device.
- **fan_mode** (*Optional*, string, :ref:`templatable <config-templatable>`): Set the fan mode
  of the climate device. One of ``ON``, ``OFF``, ``AUTO``, ``LOW``, ``MEDIUM``, ``HIGH``, ``MIDDLE``,
  ``FOCUS``, ``DIFFUSE``.
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
      // Target temperature, type: float (degrees)
      id(my_climate).target_temperature
      // Lower Target temperature, type: float (degrees)
      id(my_climate).target_temperature_low
      // High Target temperature, type: float (degrees)
      id(my_climate).target_temperature_high
      // Away mode, type: bool
      id(my_climate).away
      // Fan mode, type: FanMode (enum)
      id(my_climate).fan_mode
      // Swing mode, type: SwingMode (enum)
      id(my_climate).swing_mode

- ``.make_call``: Control the climate device

  .. code-block:: cpp

      auto call = id(my_climate).make_call();
      call.set_mode("OFF");
      // etc. see API reference
      call.perform();


See Also
--------

- :apiref:`climate/climate.h`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
