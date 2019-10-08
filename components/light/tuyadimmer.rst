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

There are two components, the Tuya bus and the dimmer that uses it.  The ``tuya``
component requires a :ref:`UART bus <uart>` to be configured.  If you don't know the ids to
use, just put the ``tuya`` component in the config and it will list the possible devices for
you in the config log.

Here is the output for my dimmer::

    [18:04:13][C][tuya:059]: Tuya:
    [18:04:13][C][tuya:066]:   3: int value
    [18:04:13][C][tuya:064]:   1: switch

.. code-block:: yaml

    # Example configuration entry
    # Make sure your wifi will connect
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

    # Create a light using the dimmer
    light:
      - platform: "tuya"
        name: "dim1"
        dimmer: 3
        switch: 1
        gamma_correct: 1.0
        default_transition_length: 0s

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the light.
- **dimmer** (**Required**, int): The id number of the dimmer value.
- **switch** (*Optional*, int): The number of the power switch.  My dimmer required this to be able to
  turn the light on and off.  Without this you would only be able to change the brightness and would
  have to toggle the light using the physical buttons.
- **min_value** (*Optional*, int, default 0): The lowest dimmer value allowed.  My dimmer had a
  minimum of 25 and wouldn't even accept anything lower, but this option is available if necessary.
- **max_value** (*Optional*, int, default 255): The highest dimmer value allowed.  My dimmer had a
  maximum of 255 which seems like it would be the typical value.
- All other options from :ref:`Light <config-light>`.
- **gamma_correct**: Recommended to be set to ``1.0``.
- **default_transition_length**: Recommended to be set to ``0s`` because the dimmer MCU does its own
  fade transition.

See Also
--------

- :doc:`/components/light/index`
- :apiref:`tuya/light/tuya_light.h`
- :ghedit:`Edit`
