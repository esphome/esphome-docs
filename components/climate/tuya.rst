Tuya Climate
============

.. seo::
    :description: Instructions for setting up a Tuya climate device.
    :image: air-conditioner.png

The ``tuya`` climate platform creates a climate device from a tuya component.

The Tuya fan requires a :doc:`/components/tuya` to be configured.

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
- 7 represents the eco mode switch. (use the :doc:`/components/switch/tuya` component to control this)

Based on this, you can create the climate device as follows:

.. code-block:: yaml

    climate:
      - platform: tuya
        name: "My Climate Device"
        switch_datapoint: 1
        target_temperature_datapoint: 3
        current_temperature_datapoint: 4

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the climate device.
- **switch_datapoint** (**Required**, int): The datapoint id number of the climate switch.
- **target_temperature_datapoint** (**Required**, int): The datapoint id number of the target temperature.
- **current_temperature_datapoint** (**Required**, int): The datapoint id number of the current temperature.
- **temperature_multiplier** (**Optional**, float): A multiplier to modify the incoming and outgoing temperature values - :ref:`see below <temperature-multiplier>`.
  If the device has different multipliers for current and target temperatures, **temperature_multiplier** can be replaced with both of:

    - **current_temperature_multiplier** (**Optional**, float): A multiplier to modify the current temperature value.
    - **target_temperature_multiplier** (**Optional**, float): A multiplier to modify the target temperature value.
- All other options from :ref:`Climate <config-climate>`.

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
