Climate Component
=================

.. seo::
    :description: Information about the base representation of all climate devices.
    :image: folder-open.png

ESPHome has support for climate devices. Climate devices can represent different types of
hardware, but the defining factor is that climate devices have a settable target temperature
and can be put in different modes like HEAT, COOL, AUTO or OFF.

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
- If MQTT enabled, all other options from :ref:`MQTT Component <config-mqtt-component>`.

Climate Automation
------------------

.. _climate-control_action:

``climate.control`` Action
**************************

This is an :ref:`Action <config-action>` for setting parameters for climate devices.

.. code-block:: yaml

    - climate.control:
        id: my_climate
        mode: AUTO
        target_temperature: 25°C

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the climate device to control.
- **mode** (*Optional*, string, :ref:`templatable <config-templatable>`): Put the climate device
  in a specific mode. One of ``OFF``, ``AUTO``, ``COOL`` and ``HEAT``.
- **target_temperature** (*Optional*, float, :ref:`templatable <config-templatable>`): Set the
  target temperature of a climate device.
- **target_temperature_low** (*Optional*, float, :ref:`templatable <config-templatable>`): Set the
  lower target temperature of a climate device with a two-point target temperature.
- **target_temperature_high** (*Optional*, float, :ref:`templatable <config-templatable>`): Set the
  higher target temperature of a climate device with a two-point target temperature.
- **away** (*Optional*, boolean, :ref:`templatable <config-templatable>`): Set the away mode
  of the climate device.
- **fan_mode** (*Optional*, boolean, :ref:`templatable <config-templatable>`): Set the fan mode
  of the climate device. One of ``ON``, ``OFF``, ``AUTO``, ``LOW``, ``MEDIUM``, ``HIGH``, ``MIDDLE``,
  ``FOCUS``, ``DIFFUSE``.
- **swing_mode** (*Optional*, boolean, :ref:`templatable <config-templatable>`): Set the swing mode
  of the climate device. One of ``OFF``, ``BOTH``, ``VERTICAL``, ``HORIZONTAL``.

.. _climate-lambda_calls:

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all binary sensors to do some
advanced stuff.

- Attributes: All climate devices have read-only attributes to get the current state of the device.

  .. code-block:: yaml

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

  .. code-block:: yaml

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
