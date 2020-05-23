Bang-Bang Climate Controller
============================

.. seo::
    :description: Instructions for setting up Bang Bang climate controllers with ESPHome.
    :image: air-conditioner.png

The ``bang_bang`` climate platform allows you to regulate a value with a
`bang-bang controller <https://en.wikipedia.org/wiki/Bang%E2%80%93bang_control>`__ (also called hysteresis controller).

If you are looking to create your own climate control device (aka thermostat), this is the component for you.

The operation principle of a bang-bang controller is quite simple. First, you specify an observable
value (for example, the temperature of a room). The controller will try to keep this observed value
within a defined range. To do this, the controller can activate devices like a heating unit to change
the observed value.

The bang-bang controller as implemented in this component can operate in one of two ways:

- **Single-point**: A single threshold (setpoint) is defined; cooling may be activated when the observed temperature
  exceeds the setpoint **or** heating may be activated when the observed temperature drops below the setpoint.

- **Dual-point**: Two thresholds (setpoints) are defined; cooling is activated when the observed temperature exceeds the
  upper setpoint while heating is activated when the observed temperature drops below the lower setpoint.

The setpoint(s) may be adjusted through the front-end user interface. In single-point mode, ``target_temperature``
defines the setpoint, while in dual-point mode ``target_temperature_low`` and ``target_temperature_high`` define
the setpoints. The screenshot below illustrates a bang-bang controller in dual-point mode.

.. figure:: images/climate-ui.png
    :align: center
    :width: 60.0%

    Dual-setpoint climate UI

This component works by triggering a number of :ref:`actions <config-action>` as required to keep the observed
temperature above/below/within the target range as defined by the setpoint(s). When the observed temperature drops
below either ``target_temperature`` (single-point mode configured for heating) or ``target_temperature_low`` (dual-point
mode) ``heat_action`` is called to activate heating. When the observed temperature exceeds either either
``target_temperature`` (single-point mode configured for cooling) or ``target_temperature_high`` (dual-point mode)
``cool_action`` is called to activate cooling. When the temperature has reached a point above/below/within the desired
range, ``idle_action`` is called to stop heating/cooling.

In addition to the setpoints, a hysteresis value determines how far the temperature may vary from the setpoint value(s)
before an :ref:`action <config-action>` (cooling, heating, etc.) is triggered. It defaults to 0.5 °C.

A number of fan control modes are built into the climate/thermostat interface in Home Assistant; this component may
also be configured to trigger :ref:`actions <config-action>` based on the entire range (at the time this document was
written) of fan modes that Home Assistant offers.

**Note that actions are only called when the current temperature leaves the target temperature range
or when the respective fan mode or swing mode is changed.**

.. code-block:: yaml

    # Example dual-point configuration entry
    climate:
      - platform: bang_bang
        sensor: my_temperature_sensor
        dual_target_temperature:
          default_target_temperature_low: 20 °C
          default_target_temperature_high: 22 °C
          cool_action:
            - switch.turn_on: air_cond
          heat_action:
            - switch.turn_on: heater
          idle_action:
            - switch.turn_off: air_cond
            - switch.turn_off: heater

.. code-block:: yaml

    # Example single-point configuration entry
    climate:
      - platform: bang_bang
        sensor: my_temperature_sensor
        single_target_temperature:
          default_target_temperature: 20 °C
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

Configuration Variables
-----------------------

- **sensor** (**Required**, :ref:`config-id`): The sensor that is used to measure the current temperature.

- **dual_target_temperature** (*Optional*, dictionary): Configures the controller for dual-point mode.
- **single_target_temperature** (*Optional*, dictionary): Configures the controller for single-point mode.

**Exactly one of** ``dual_target_temperature`` **and** ``single_target_temperature`` **must be specified.**

Default Target Temperatures
***************************

These temperatures are used when the device first starts up.

- **default_target_temperature** (**Required**, float, single-point mode only): The default target
  temperature for the control algorithm. This can be dynamically set in the frontend later.
- **default_target_temperature_low** (**Required**, float, dual-point mode only): The default low target
  temperature for the control algorithm. This can be dynamically set in the frontend later.
- **default_target_temperature_high** (**Required**, float, dual-point mode only): The default high target
  temperature for the control algorithm. This can be dynamically set in the frontend later.

Basic Heating and Cooling Actions
*********************************

These are triggered when the climate control **action** is changed by the bang bang controller. Here,
"action" takes on both meanings described above, as these are both climate actions *and* ESPHome
:ref:`actions <config-action>`. These should be used to activate heating, cooling, etc. devices.

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
  controller triggers this action based on the upper target temperature when set to
  ``fan_only_mode`` (see below).
- All other options from :ref:`Climate <config-climate>`.

**Exactly one of** ``cool_action``, ``fan_only_action``, ``heat_action``, **and** ``dry_action``
**must be specified in single-point mode.**

**Both** ``heat_action`` **and** ``cool_action`` **must be specified in dual-point mode.**

Basic Heating and Cooling Modes
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
  the climate device is placed into fan only mode (it may not heat or cool, but will activate
  its fan as needed based on the upper target temperature value).

**Note that the above actions are not to be used to activate cooling or heating devices!**
See the previous section for those.

Fan Mode Actions
****************

These are triggered when the climate control fan mode is changed. These are ESPHome :ref:`actions <config-action>`.
These should be used to control the fan only, if available.

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

Swing Mode Actions
******************

These are triggered when the climate control swing mode is changed. These are ESPHome :ref:`actions <config-action>`.
These should be used to control the fan only, if available.

- **swing_off_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan should
  remain in a stationary position.
- **swing_horizontal_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should oscillate in a horizontal direction.
- **swing_vertical_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should oscillate in a vertical direction.
- **swing_both_action** (*Optional*, :ref:`Action <config-action>`): The action to call when the fan
  should oscillate in horizontal and vertical directions.

Advanced Options
****************

- **hysteresis** (*Optional*, float): Defines how far the temperature may vary from the target values before
  an :ref:`action <config-action>` (cooling, heating, etc.) is triggered. Defaults to 0.5 °C.
- **away_config** (*Optional*): Additionally specify target temperature range settings for away mode.
  Away mode can be used to have a second set of target temperatures (for example, while the user is
  away or sleeping/at night).

  - **default_target_temperature** (**Required**, float, single-point mode only): The default target
    temperature for the control algorithm when Away mode is selected. This can be dynamically set in the frontend later.
  - **default_target_temperature_low** (**Required**, float, dual-point mode only): The default low target
    temperature for the control algorithm when Away mode is selected. This can be dynamically set in the frontend later.
  - **default_target_temperature_high** (**Required**, float, dual-point mode only): The default high target
    temperature for the control algorithm when Away mode is selected. This can be dynamically set in the frontend later.
  - **hysteresis** (*Optional*, float): Defines how far the temperature may vary from the target values before
    an :ref:`action <config-action>` (cooling, heating, etc.) is triggered in away mode. Defaults to 0.5 °C.

.. note::

    While this platform uses the term temperature everywhere, it can also be used to regulate other values.
    For example, controlling humidity is also possible with this platform.

See Also
--------

- :doc:`/components/binary_sensor/index`
- :ref:`config-pin_schema`
- :ref:`config-action`
- :apiref:`gpio/binary_sensor/gpio_binary_sensor.h`
- :ghedit:`Edit`
