Tuya Climate
============

.. seo::
    :description: Instructions for setting up a Tuya climate device.
    :image: air-conditioner.svg

The ``tuya`` climate platform creates a climate device from a tuya component.

Tuya climate requires a :doc:`/components/tuya` to be configured.

.. code-block:: text

    [22:03:11][C][tuya:023]: Tuya:
    [22:03:11][C][tuya:032]:   Datapoint 1: switch (value: ON)
    [22:03:11][C][tuya:032]:   Datapoint 2: switch (value: OFF)
    [22:03:11][C][tuya:034]:   Datapoint 3: int value (value: 20)
    [22:03:11][C][tuya:034]:   Datapoint 4: int value (value: 19)
    [22:03:11][C][tuya:034]:   Datapoint 5: int value (value: 0)
    [22:03:11][C][tuya:036]:   Datapoint 7: enum (value: 1)
    [22:03:11][C][tuya:046]:   Product: '{"p":"ynjanlglr4qa6dxf","v":"1.0.0","m":0}'

On this controller, the data points are:

- 1 represents the climate on/off state.
- 2 represents the child lock switch. (use the :doc:`/components/switch/tuya` component to control this)
- 3 represents the target temperature.
- 4 represents the current temperature.
- 5 represents the timer but is not yet available to be used in ESPHome.
- 7 represents the eco mode switch.

Based on this, you can create the climate device as follows:

.. code-block:: yaml

    climate:
      - platform: tuya
        name: "My Climate Device"
        switch_datapoint: 1
        target_temperature_datapoint: 3
        current_temperature_datapoint: 4
        preset:
          eco:
            datapoint: 8
            temperature: 28

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the climate device.
- **supports_heat** (*Optional*, boolean): Specifies if the device has a heating mode. Defaults to ``true``.
- **supports_cool** (*Optional*, boolean): Specifies if the device has a cooling mode. Defaults to ``false``.
- **switch_datapoint** (**Required**, int): The datapoint id number of the climate switch (device on/off).
- **active_state** (*Optional*): Configuration for the Active State Configuration.

    - **datapoint** (**Required**, int): The datapoint id number of the active state - :ref:`see below <active_state_detection>`.
    - **heating_value** (*Optional*, int): The active state datapoint value the device reports when heating. Defaults to ``1`` - :ref:`see below <active_state_detection>`.
    - **cooling_value** (*Optional*, int): The active state datapoint value the device reports when cooling - :ref:`see below <active_state_detection>`.
    - **drying_value** (*Optional*, int): The active state datapoint value the device reports when in drying mode.
    - **fanonly_value** (*Optional*, int): The active state datapoint value the device reports when in Fan Only mode.
- **preset** (*Optional*): Configuration for presets.

    - **eco** (*Optional*): Configuration for Eco preset.

        - **datapoint** (**Required**, int): The datapoint id number of the Eco action.
        - **temperature** (*Optional*, int): Temperature setpoint for Eco preset.
    - **sleep** (*Optional*): Configuration for Sleep preset

        - **datapoint** (**Required**, int): The Datapoint id number of the Sleep Action
- **swing_mode** (*Optional*): Configuration for the swing (oscillation) modes.

    - **vertical_datapoint** (*Optional*, int): The datapoint id number of the vertical swing action.
    - **horizontal_datapoint** (*Optional*, int): The datapoint id number of the horizontal swing action.
- **fan_mode** (*Optional*): Configuration for fan modes/fan speeds.

    - **datapoint** (**Required**, int): The datapoint id number of the Fan value state.
    - **auto_value** (*Optional*, int): The datapoint value the device reports when the fan is on ``auto`` speed.
    - **low_value** (*Optional*, int):  The datapoint value the device reports when the fan is on ``low`` speed.
    - **medium_value** (*Optional*, int):  The datapoint value the device reports when the fan is on ``medium`` speed.
    - **middle_value** (*Optional*, int):  The datapoint value the device reports when the fan is on ``middle`` speed. (May set to device's ``high`` value if you have a ``Turbo`` option).
    - **high_value** (*Optional*, int):  The datapoint value the device reports when the fan is on ``high`` speed. (Sometimes called ``Turbo``).
- **heating_state_pin** (*Optional*, :ref:`config-pin`): The input pin indicating that the device is heating - :ref:`see below <active_state_detection>`. Only used if **active_state_datapoint** is not configured.
- **cooling_state_pin** (*Optional*, :ref:`config-pin`): The input pin indicating that the device is cooling - :ref:`see below <active_state_detection>`. Only used if **active_state_datapoint** is not configured.
- **target_temperature_datapoint** (**Required**, int): The datapoint id number of the target temperature.
- **current_temperature_datapoint** (**Required**, int): The datapoint id number of the current temperature.
- **temperature_multiplier** (*Optional*, float): A multiplier to modify the incoming and outgoing temperature values - :ref:`see below <temperature-multiplier>`.

- **reports_fahrenheit** (*Optional*, boolean): Set to ``true`` if the device reports temperatures in Fahrenheit. ESPHome expects all climate temperatures to be in Celcius, otherwise unexpected conversions will take place when it is published to Home Assistant. Defaults to ``false``.

If the device has different multipliers for current and target temperatures, **temperature_multiplier** can be replaced with both of:

    - **current_temperature_multiplier** (*Optional*, float): A multiplier to modify the current temperature value.
    - **target_temperature_multiplier** (*Optional*, float): A multiplier to modify the target temperature value.

- All other options from :ref:`Climate <config-climate>`.

.. _active_state_detection:

Active state detection
----------------------

Some Tuya climate devices report the active state (idle/heating/cooling) via a tuya data point. In this case, you can use the **active_state_datapoint** variable together with **active_state_heating_value** and **active_state_cooling_value**.

If your device does not make a data point available for this, it is possible to modify the hardware so that the relay outputs can be read by the ESP. Please refer to `this discussion <https://github.com/klausahrenberg/WThermostatBeca/issues/17>` for more details on the required modifications. You can then use the **heating_state_pin** and/or **cooling_state_pin** configuration variables to detect the current state.

If none of the above variables are set, the current state is inferred from the difference between the current and target temperatures.
If **supports_heat** is ``True`` and the current temperature is more than 1 °C below the target temperature, the device is expected to be heating.
If **supports_cool** is ``True`` and the current temperature is more than 1 °C above the target temperature, the device is expected to be cooling.

.. _temperature-multiplier:

Temperature multiplier
----------------------

Some Tuya climate devices report the temperature with a multiplied factor. This is because the MCU only utlizes
integers for data reporting and to get a .5 temperature you need to divide by 2 on the ESPHome side.

See Also
--------

- :doc:`/components/tuya`
- :doc:`/components/climate/index`
- :apiref:`tuya/climate/tuya_climate.h`
- :ghedit:`Edit`
