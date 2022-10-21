OpenTherm
=========

.. seo::
    :description: Instructions for setting up an OpenTherm device

The OpenTherm component allos you to use various OpenTherm shields:

- `DIYLess <https://diyless.com/product/master-opentherm-shield>`__ OpenTherm shield
- `Ihor Melnyk <http://ihormelnyk.com/opentherm_adapter>`__'s OpenTherm adapter

It can be connected to for example an ESP32, and after that connected to your boiler.

What this component does:

- Expose various sensors
- Allow to enable/disable CH and DHW
- Allow to set CH and DHW setpoints

What this component does not:

- Implement a full featured `climate` component

  - Use automations inside ESPHome or Home Assistant
- Protect your device for misconfiguration

  - Please make sure that you know what you're doing

Glossary:

- *CH*: Central Heating
- *DHW*: Domestic Hot Water


.. code-block:: yaml

    opentherm:
      read_pin: 21
      write_pin: 22

    sensor:
      - platform: opentherm
        ch_min_temperature:
          name: "Boiler CH minimum temperature"

    binary_sensor:
      - platform: opentherm
        ch_active:
          name: "Boiler CH active"

    switch:
      - platform: opentherm
        ch_enabled:
          name: "Boiler CH enabled"

    number:
      - platform: opentherm
        ch_setpoint_temperature:
          name: "Boiler CH setpoint temperature"
          min_value: 20.0
          max_value: 45.0
          step: 0.5
          restore_value: true

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

Component settings:

- **read_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The read pin.
  Connected to the `in` on the shield/adapter
- **write_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The write pin.
  Connected to the `out` on the shield/adapter

Sensors:

- **ch_min_temperature** (*Optional*): The boiler's minimum CH temperature.
  All options from :ref:`Sensor <config-sensor>`.
- **ch_max_temperature** (*Optional*): The boiler's maximum CH temperature.
  All options from :ref:`Sensor <config-sensor>`.
- **dhw_min_temperature** (*Optional*): The boiler's minimum DHW temperature.
  All options from :ref:`Sensor <config-sensor>`.
- **dhw_max_temperature** (*Optional*): The boiler's maximum DHW temperature.
  All options from :ref:`Sensor <config-sensor>`.
- **modulation** (*Optional*): The current boiler modulation level.
  All options from :ref:`Sensor <config-sensor>`.
- **boiler_temperature** (*Optional*): The outgoing water temperature.
  All options from :ref:`Sensor <config-sensor>`.
- **return_temperature** (*Optional*): The returning water temperature.
  All options from :ref:`Sensor <config-sensor>`.

Binary sensors:

- **ch_active** (*Optional*): Indicates whether CH is active
  All options from :ref:`Binary Sensor <config-binary_sensor>`
- **dhw_active** (*Optional*): Indicates whether DHW is active.
  All options from :ref:`Binary Sensor <config-binary_sensor>`
- **flame_active** (*Optional*): Indicates the flame is active.
  All options from :ref:`Binary Sensor <config-binary_sensor>`
- **cooling_active** (*Optional*): Indicates cooling is active.
  All options from :ref:`Binary Sensor <config-binary_sensor>`
- **fault** (*Optional*): Indicates a fault.
  All options from :ref:`Binary Sensor <config-binary_sensor>`
- **diagnostic** (*Optional*): Indicates that diagnostics are avialble.
  All options from :ref:`Binary Sensor <config-binary_sensor>`

Switches:

- **ch_enabled** (*Optional*): Enables CH.
  All options from :ref:`switch <config-switch>`
- **dhw_enabled** (*Optional*): Enables DHW. See note.
  All options from :ref:`switch <config-switch>`
- **cooling_enabled** (*Optional*): Enables cooling.
  All options from :ref:`switch <config-switch>`

.. note::
    Usually there is always DHW available on request.
    Enabling DHW might:
    - Indicate DHW "comfort" mode;
    - Keeps a (small) amount pre-heated;
    - Heat the DHW circuit at a regular interval to prevent bacteria growth.
    Refer to your boiler's manual for more information.

Numbers:

- **ch_setpoint_temperature** (*Optional*): The CH setpoint.

  - **min_value** (**Required**, float): The minimum value that can be set.
  - **max_value** (**Required**, float): The maximum value that can be set.
  - **step** (**Required**, float): The step size with which the value must be set.
  - **restore_value** (*Optional*, boolean): Indicates the set value should be saved to
    flash so it's restored on startup.
  - **initial_value** (*Optional*, boolean): If restore is set to `false`, or no previous
    value was stored, this initial value will be used. If not given, the `min_value` will
    be used.
  All other options from :ref:`Number <config-number>`
- **dhw_setpoint_temperature** (*Optional*): The DHW setpoint.

  - **min_value** (**Required**, float): The minimum value that can be set.
  - **max_value** (**Required**, float): The maximum value that can be set.
  - **step** (**Required**, float): The step size with which the value must be set.
  - **restore_value** (*Optional*, boolean): Indicates the set value should be saved to
    flash so it's restored on startup.
  - **initial_value** (*Optional*, boolean): If restore is set to `false`, or no previous
    value was stored, this initial value will be used. If not given, the `min_value` will
    be used.
  All other options from :ref:`Number <config-number>`


See Also
--------

- :ghedit:`Edit`
