Tuya Dimmer
===========

.. seo::
    :description: Instructions for setting up a Tuya dimmer switch.
    :image: brightness-medium.png

The ``tuya`` light platform creates a simple brightness-only light from a
tuya serial component.

.. warning::

    Some of these dimmers have no way of serial flashing without destroying them.
    Make sure you have some way to OTA upload configured before flashing.  This means you need
    to have working wifi, ota, and maybe api sections in the config.
    The dimmer switch I got would hang if the logger was configured to use the serial port
    which meant it was bricked until I cut it open.

There are two components, the Tuya bus and the dimmer that uses it.  The :doc:`/components/tuya`
component requires a :ref:`UART bus <uart>` to be configured.  Put the ``tuya`` component in
the config and it will list the possible devices for you in the config log.

.. code-block:: yaml

    # Example configuration entry
    # Make sure your WiFi will connect
    wifi:
      ssid: "ssid"
      password: "password"

    # Make sure logging is not using the serial port
    logger:
      baud_rate: 0

    # Enable Home Assistant API
    api:

    # Make sure you can upload new firmware OTA
    ota:

    # My dimmer used the hardware serial port on the alternate pins
    uart:
      rx_pin: GPIO13
      tx_pin: GPIO15
      baud_rate: 9600

    # Register the Tuya MCU connection
    tuya:

Here is an example output for a Tuya dimmer:

.. code-block:: text

    [21:50:28][C][tuya:024]: Tuya:
    [21:50:28][C][tuya:031]:   Datapoint 3: int value (value: 139)
    [21:50:28][C][tuya:029]:   Datapoint 1: switch (value: OFF)

On this dimmer, the toggle switch is datapoint 1 and the dimmer value is datapoint 3.
Now you can create the light.

.. code-block:: yaml

    # Create a light using the dimmer
    light:
      - platform: "tuya"
        name: "dim1"
        dimmer_datapoint: 3
        min_value_datapoint: 2
        switch_datapoint: 1

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the light.
- **dimmer_datapoint** (*Optional*, int): The datapoint id number of the dimmer value.
- **min_value_datapoint** (*Optional*, int): The datapoint id number of the MCU minimum value
  setting.  If this is set then ESPHome will sync the **min_value** to the MCU on startup.
- **switch_datapoint** (*Optional*, int): The datapoint id number of the power switch.  My dimmer
  required this to be able to turn the light on and off.  Without this you would only be able to
  change the brightness and would have to toggle the light using the physical buttons.
- **color_temperature_datapoint** (*Optional*, int): The datapoint id number of the color
  temperature value.
- **min_value** (*Optional*, int, default 0): The lowest dimmer value allowed.  My dimmer had a
  minimum of 25 and wouldn't even accept anything lower, but this option is available if necessary.
- **max_value** (*Optional*, int, default 255): The highest dimmer value allowed.  Most dimmers have a
  maximum of 255, but dimmers with a maximum of 1000 can also be found. Try what works best.
- **color_temperature_max_value** (*Optional*, int, default 255): The highest color temperature
  value allowed. Some ceiling fans have a value of 100 (also for ``max_value``).
- **cold_white_color_temperature** (*Optional*, float): The color temperate (in `mireds
  <https://en.wikipedia.org/wiki/Mired>`__ or Kelvin) of the cold white channel.
- **warm_white_color_temperature** (*Optional*, float): The color temperate (in `mireds
  <https://en.wikipedia.org/wiki/Mired>`__ or Kelvin) of the warm white channel.
- All other options from :ref:`Light <config-light>`.
- At least one of *dimmer_datapoint* or *switch_datapoint* must be provided.

.. note::

    The MCU on the Tuya dimmer handles transitions and gamma correction on its own.
    Therefore the ``gamma_correct`` setting default is ``1.0`` and the the
    ``default_transition_length`` parameter is ``0s`` by default.

See Also
--------

- :doc:`/components/tuya`
- :doc:`/components/light/index`
- :apiref:`tuya/light/tuya_light.h`
- :ghedit:`Edit`
