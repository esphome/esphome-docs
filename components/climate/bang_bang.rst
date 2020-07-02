Bang Bang Climate Controller
============================

.. seo::
    :description: Instructions for setting up Bang Bang climate controllers with ESPHome.
    :image: air-conditioner.png

The ``bang_bang`` climate platform allows you to regulate a value with a
`bang-bang controller <https://en.wikipedia.org/wiki/Bang%E2%80%93bang_control>`__ (also called hysteresis controller).

.. note::

    While the bang-bang controller is considered a climate component, most users will find that the
    :doc:`thermostat <thermostat>` component behaves in a way more consistent with most climate control
    devices. Despite that the bang-bang controller provides two set points, it is **not recommended**
    for systems that both heat *and* cool; it also does not use the user interface in Home Assistant
    in a way that most users will expect.

The bang-bang controller's principle of operation is quite simple. First, you specify an observable
value (for example the temperature of a room). The controller will try to keep this observed value
in a defined range. To do this, the controller can activate objects like a heating unit to change
the observed value.

The range that the controller will try to keep the observed value in can be controlled through the
front-end with the ``target_temperature_low`` and ``target_temperature_high`` values (see screenshot below).
As soon as the observed temperature dips below or above this range it will activate one of the
defined actions ``cool_action``, ``heat_action`` and ``idle_action``.

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

Do note that the actions are only called when the current temperature leaves the target temperature range.

.. figure:: images/climate-ui.png
    :align: center
    :width: 60.0%

.. code-block:: yaml

    # Example configuration entry
    climate:
      - platform: bang_bang
        name: "Bang Bang Climate Controller"
        sensor: my_temperature_sensor
        default_target_temperature_low: 20 °C
        default_target_temperature_high: 22 °C

        heat_action:
          - switch.turn_on: heater
        idle_action:
          - switch.turn_off: heater

Configuration variables:
------------------------

- **sensor** (**Required**, :ref:`config-id`): The sensor that is used to measure the current temperature.
- **default_target_temperature_low** (**Required**, float): The default low target temperature for
  the control algorithm. This can be dynamically set in the frontend later.
- **default_target_temperature_high** (**Required**, float): The default high target temperature for
  the control algorithm. This can be dynamically set in the frontend later.
- **idle_action** (**Required**, :ref:`Action <config-action>`): The action to call when
  the climate device wants to enter idle mode.
- **heat_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device wants to heating mode and increase the current temperature. At least one
  of ``heat_action`` and ``cool_action`` need to be specified.
- **cool_action** (*Optional*, :ref:`Action <config-action>`): The action to call when
  the climate device wants to cooling mode and decrease the current temperature.
- All other options from :ref:`Climate <config-climate>`.

Advanced options:

- **away_config** (*Optional*): Additionally specify target temperature range settings for away mode.
  Away mode can be used to have a second set of target temperatures (for example while the user is
  away or during nighttime)

  - **default_target_temperature_low** (**Required**, float): The default low target temperature for
    the control algorithm during away mode.
  - **default_target_temperature_high** (**Required**, float): The default high target temperature for
    the control algorithm during away mode.

.. note::

    While this platform uses the term temperature everywhere, it can also be used for other values.
    For example, controlling humidity is also possible with this platform.

See Also
--------

- :doc:`/components/climate/index`
- :apiref:`bang_bang/bang_bang_climate.h`
- :ghedit:`Edit`
