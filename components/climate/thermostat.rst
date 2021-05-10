Thermostat Climate Controller
=============================

.. seo::
    :description: Instructions for setting up Thermostat climate controllers with ESPHome.
    :image: air-conditioner.png

The ``thermostat`` climate platform allows you to control a climate control system in much the same manner as a
physical thermostat. Its operation is similar to the :doc:`bang-bang <bang_bang>` controller; a sensor measures a value
(the air temperature) and the controller will try to keep this value within a range defined by the set point(s). To do this,
the controller can activate devices like a heating unit and/or a cooling unit to change the value observed by the sensor.
When configured for both heating and cooling, it is essentially two :doc:`bang-bang <bang_bang>` controllers in one; it
differs, however, in that interation with the thermostat component is nearly identical to that of a real thermostat.

This component can operate in one of two ways:

- **Single-point**: A single threshold (set point) is defined; cooling may be activated when the observed temperature
  exceeds the set point **or** heating may be activated when the observed temperature drops below the set point; that is,
  the controller can only raise the temperature or lower the temperature. It cannot do both in this mode.

- **Dual-point**: Two thresholds (set points) are defined; cooling is activated when the observed temperature exceeds the
  upper set point while heating is activated when the observed temperature drops below the lower set point; in other words,
  the controller is able to both raise and lower the temperature as required.

This component/controller automatically determines which mode it should operate in based on what :ref:`actions <config-action>`
are configured -- more on this in a moment. Two parameters define the set points; they are ``target_temperature_low`` and
``target_temperature_high``. In single-point mode, however, only one is used. The set point(s) may be adjusted through the
front-end user interface. The screenshot below illustrates a thermostat controller in dual-point mode, where two set points
are available.

.. figure:: images/climate-ui.png
    :align: center
    :width: 60.0%

    Dual-setpoint climate UI

This component works by triggering a number of :ref:`actions <config-action>` as required to keep the observed
temperature above/below/within the target range as defined by the set point(s). In general, when the observed temperature
drops below ``target_temperature_low`` the controller will trigger the ``heat_action`` to activate heating. When the observed
temperature exceeds ``target_temperature_high``  the controller will trigger the ``cool_action`` or the ``fan_only_action``
(as determined by the climate mode) to activate cooling. When the temperature has reached a point within the desired range, the
controller will trigger the ``idle_action`` to stop heating/cooling. Please see the next section for more detail.

A number of fan control modes are built into the climate/thermostat interface in Home Assistant; this component may also be
configured to trigger :ref:`actions <config-action>` based on the entire range (at the time this document was written) of fan
modes that Home Assistant offers.

.. code-block:: yaml

    # Example dual-point configuration entry
    climate:
      - platform: thermostat
        name: "Thermostat Climate Controller"
        sensor: my_temperature_sensor
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

    # Example single-point configuration entry (for heating only)
    climate:
      - platform: thermostat
        sensor: my_temperature_sensor
        default_target_temperature_low: 20 °C
        heat_action:
          - switch.turn_on: heater
        idle_action:
          - switch.turn_off: heater

.. code-block:: yaml

    # Example single-point configuration entry (for cooling only)
    climate:
      - platform: thermostat
        sensor: my_temperature_sensor
        default_target_temperature_high: 22 °C
        cool_action:
          - switch.turn_on: air_cond
        idle_action:
          - switch.turn_off: air_cond


Controller Behavior and Hysteresis
----------------------------------

In addition to the set points, a hysteresis value determines how far the temperature may vary from the set point value(s)
before an :ref:`action <config-action>` (cooling, heating, etc.) is triggered. It defaults to 0.5 °C.

A question that often surfaces about this component is, "What is the expected behavior?" Let's quickly discuss
*exactly when* the configured actions are called by the controller.

Consider the low set point (the one that typically activates heating) for a moment, and assume it is set to a common room
temperature of 21 °C. As mentioned above, the controller uses a default hysteresis value of 0.5 °C, so let's assume that
value here, as well. The controller as implemented in this component will allow the temperature to drop as low as the set
point's value (21 °C) *minus* the hysteresis value (0.5 °C), or 20.5 °C, before calling ``heat_action`` to activate heating.

After heating has been activated, it will remain active until the observed temperature reaches the set point (21 °C) *plus*
the hysteresis value (0.5 °C), or 21.5 °C. Once this temperature is reached, ``idle_action`` will be called to deactivate
heating.

The same behavior applies to the high set point, although the behavior is reversed in a sense; given an upper set point of
22 °C, ``cool_action`` would be called at 22.5 °C and ``idle_action`` would not be called until the temperature is reduced
to 21.5 °C.

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

Configuration Variables:

The thermostat controller uses the sensor to determine whether it should heat or cool.

- **sensor** (**Required**, :ref:`config-id`): The sensor that is used to measure the current temperature.

Default Target Temperatures
***************************

These temperatures are used when the device first starts up.

- **default_target_temperature_low** (*Optional*, float): The default low target
  temperature for the control algorithm. This can be dynamically set in the frontend later.
- **default_target_temperature_high** (*Optional*, float): The default high target
  temperature for the control algorithm. This can be dynamically set in the frontend later.

**At least one of** ``default_target_temperature_low`` **and** ``default_target_temperature_high``
**must be specified.**

``min_temperature`` and ``max_temperature`` from the base climate component **are used to define the range**
of allowed temperature values in the thermostat component. See :doc:`/components/climate/index`

Heating and Cooling Actions
***************************

These are triggered when the climate control **action** is changed by the thermostat controller. Here,
"action" takes on both meanings described above, as these are both climate actions *and* ESPHome
:ref:`actions <config-action>`. These should be used to activate heating, cooling, etc. devices.

- **idle_action** (**Required**, :ref:`Action <config-action>`): The action to call when
  the climate device should enter its idle state (not cooling, not heating).
- **heat_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device should enter heating mode to increase the current temperature.
- **cool_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device should enter cooling mode to decrease the current temperature.
- **dry_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device should perform its drying (dehumidification) action. The thermostat
  controller does not trigger this action; it is invoked by ``dry_mode`` (see below).
- **fan_only_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device should activate its fan only (but does not heat or cool). The thermostat
  controller triggers this action based on the upper target temperature when set to
  ``fan_only_mode`` (see below).
- All other options from :ref:`Climate <config-climate>`.

**At least one of** ``cool_action``, ``fan_only_action``, ``heat_action``, **and** ``dry_action``
**must be specified.**

If only one of ``cool_action``, ``fan_only_action``, ``heat_action``, and ``dry_action`` is specified,
the controller will configure itself to operate in single-point mode and, as such, Home Assistant will
display the single-point climate user interface for the device.

Heating and Cooling Modes
*************************

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

**The above actions are not to be used to activate cooling or heating devices!**
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

  - **default_target_temperature_low** (*Optional*, float): The default low target temperature for the control
    algorithm when Away mode is selected. This can be dynamically set in the frontend later.
  - **default_target_temperature_high** (*Optional*, float): The default high target temperature for the control
    algorithm when Away mode is selected. This can be dynamically set in the frontend later.

**If configured, at least one of** ``default_target_temperature_low`` **and** ``default_target_temperature_high``
**must be specified in the away mode configuration.**

.. note::

    While this platform uses the term temperature everywhere, it can also be used to regulate other values.
    For example, controlling humidity is also possible with this platform. Note that ``min_temperature`` and
    ``max_temperature`` from the base climate component are used the define the range of adjustability and the
    defaults will probably not make sense for control of things like humidity. See :doc:`/components/climate/index`

Bang-bang vs. Thermostat
------------------------

Please see the :doc:`Bang-bang <bang_bang>` component's documentation for a detailed comparison of these two components.

See Also
--------

- :doc:`/components/climate/index`
- :doc:`/components/sensor/index`
- :ref:`config-action`
- :ghedit:`Edit`
