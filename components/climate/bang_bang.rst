Bang Bang Climate Controller
============================

.. seo::
    :description: Instructions for setting up Bang Bang climate controllers with ESPHome.
    :image: air-conditioner.png

The ``bang_bang`` climate platform allows you to regulate a value with a
`bang-bang controller <https://en.wikipedia.org/wiki/Bang%E2%80%93bang_control>`__ (also called hysteresis controller).

If you are looking to create your own climate control device (aka thermostat), this is the component for you.

The operation principle of a bang_bang controller is quite simple. First, you specify an observable
value (for example, the temperature of a room). The controller will try to keep this observed value
in a defined range. To do this, the controller can activate objects like a heating unit to change
the observed value.

The range that the controller will try to keep the observed value in can be controlled through the
front-end with the ``target_temperature_low`` and ``target_temperature_high`` values (see screenshot below).
When the observed temperature moves outside of this range, it will activate the appropriate action--either
the ``cool_action`` or the ``heat_action``--to compensate; when the observed temperature reaches a value
between the upper and lower target values, it will activate the ``idle_action``.

There are three types of bang bang controllers this platform can represent:

- **Heaters**: For devices where the observed temperature can only be increased.

  - As soon as the temperature goes below the lower target temperature, ``heat_action`` will be called.
  - When the temperature goes above the higher temperature, ``idle_action`` will be called.

- **Coolers**: For devices where the observed temperature can only be decreased.

  - As soon as the temperature goes above the higher target temperature, ``cool_action`` will be called.
  - When the temperature goes below the lower temperature, ``idle_action`` will be called.

- **Heater+Cooler**: For devices where the temperature can both actively be increased and decreased.

  - When the current temperature is below the lower target temperature, ``heat_action`` is called.
  - When the current temperature is within the target temperature range, ``idle_action`` is called.
  - When the current temperature is above the higher target temperature, ``cool_action`` is called.

In addition to simple heating and/or cooling, a number of fan control modes are built into the
climate/thermostat interface in Home Assistant; this component may also be configured to trigger actions
based on the entire range of fan modes that Home Assistant offers (at the time this document was written).

**Note that actions are only called when the current temperature leaves the target temperature range
or when the respective fan mode or swing mode is changed.**

.. figure:: images/climate-ui.png
    :align: center
    :width: 60.0%

.. code-block:: yaml

    # Example minimal configuration entry (for heating)
    climate:
      - platform: bang_bang
        sensor: my_temperature_sensor
        default_target_temperature_low: 20 °C
        default_target_temperature_high: 22 °C

        heat_action:
          - switch.turn_on: heater
        idle_action:
          - switch.turn_off: heater

Important Terminology
---------------------

Before we get into more configuration detail, let's take a step back and talk about the word "action"; we
need to carefully consider the context of the word in the upcoming section, as it has a double meaning and
will otherwise lead to some ambiguity.

- **ESPHome Action**: A task the ESPHome application performs as requested, such as
  turning on a switch. See :ref:`Action <config-action>`.
- **Climate Action**: What the climate device is actively doing
- **Climate Mode**: What the climate device should (or should not) do

We'll call out which definition "action" we are referring to as we describe them below -- read carefully!

With respect to climate control, it is important to understand the subtle difference between the terms
"action" and "mode" as they *are not the same thing*:

Examples:

- **Heat Mode**: The climate device may heat but may **not** cool.
- **Heat Action**: The climate device is *actively distributing heated air* into the dwelling.

Got all that? Great. Let's take a closer look at some configuration.

Configuration variables
-----------------------

- **sensor** (**Required**, :ref:`config-id`): The sensor that is used to measure the current temperature.
- **default_target_temperature_low** (**Required**, float): The default low target temperature for
  the control algorithm. This can be dynamically set in the frontend later.
- **default_target_temperature_high** (**Required**, float): The default high target temperature for
  the control algorithm. This can be dynamically set in the frontend later.

Basic heating and cooling actions
*********************************

These are triggered when the climate control **action** is changed by the bang bang controller. Here,
"action" takes on both meanings described above, as these are both climate actions *and* ESPHome
:ref:`actions <config-action>`.

- **idle_action** (**Required**, :ref:`Action <config-action>`): The action to call when
  the climate device should enter its idle state (not cooling, not heating).
- **heat_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device should enter heating mode to increase the current temperature.
- **cool_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device should enter cooling mode to decrease the current temperature.
- **dry_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device should perform its drying (dehumidification) action. The bang bang
  controller does not trigger this action; it is invoked by ``dry_mode`` (see below).
- **fan_only_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device should activate its fan only (but does not heat or cool). The bang bang
  controller does not trigger this action; it is invoked by ``fan_only_mode`` (see below).
- All other options from :ref:`Climate <config-climate>`.

**At least one of** ``heat_action`` **and** ``cool_action`` **must be specified.**

Basic heating and cooling modes
*******************************

These are triggered when the climate control **mode** is changed. Note the absence of "action" in the
parameter name here -- these are still ESPHome :ref:`actions <config-action>`, however they are *not*
climate actions. Instead, they are climate *modes*. These :ref:`actions <config-action>` are useful
in that they could be used, for example, to toggle a group of LEDs on and/or off to provide a visual
indication of the current climate mode.

- **auto_mode** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device is placed into "auto" mode (it may both cool and heat as required).
- **off_mode** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device is placed into "off" mode (it is completely disabled).
- **heat_mode** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device is placed into heat mode (it may heat as required, but not cool).
- **cool_mode** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device is placed into cool mode (it may cool as required, but not heat).
- **dry_mode** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device is placed into dry mode (for dehumidification).
- **fan_only_mode** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device is placed into fan only mode (it may not heat or cool).

Fan mode actions
****************

These are triggered when the climate control fan mode is changed. These are ESPHome :ref:`actions <config-action>`.

- **fan_mode_auto_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should be set to "auto" mode (the fan is controlled by the climate control system as required).
- **fan_mode_on_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should run continuously.
- **fan_mode_off_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should never run.
- **fan_mode_low_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should run at its minimum speed.
- **fan_mode_medium_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should run at an intermediate speed.
- **fan_mode_high_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should run at its maximum speed.
- **fan_mode_middle_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should direct its airflow at an intermediate area.
- **fan_mode_focus_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should direct its airflow at a specific area.
- **fan_mode_diffuse_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should direct its airflow over a broad area.

Swing mode actions
******************

These are triggered when the climate control swing mode is changed. These are ESPHome :ref:`actions <config-action>`.

- **swing_off_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan should
  remain in a stationary position.
- **swing_horizontal_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should oscillate in a horizontal direction.
- **swing_vertical_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should oscillate in a vertical direction.
- **swing_both_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should oscillate in horizontal and vertical directions.

Advanced options
****************

- **hysteresis** (*Optional*, float): Defines how far the temperature may vary from the target values before
  an action (heating or cooling) is engaged or disengaged. Defaults to 0.5 °C.
- **away_config** (*Optional*): Additionally specify target temperature range settings for away mode.
  Away mode can be used to have a second set of target temperatures (for example, while the user is
  away or during nighttime)

  - **default_target_temperature_low** (**Required**, float): The default low target temperature for
    the control algorithm during away mode.
  - **default_target_temperature_high** (**Required**, float): The default high target temperature for
    the control algorithm during away mode.
  - **hysteresis** (*Optional*, float): Defines how far the temperature may vary from the target values before
    an action (heating or cooling) is engaged or disengaged in away mode. Defaults to 0.5 °C.

.. note::

    While this platform uses the term temperature everywhere, it can also be used for other values.
    For example, controlling humidity is also possible with this platform.

See Also
--------

- :doc:`/components/binary_sensor/index`
- :ref:`config-pin_schema`
- :ref:`config-action`
- :apiref:`gpio/binary_sensor/gpio_binary_sensor.h`
- :ghedit:`Edit`
