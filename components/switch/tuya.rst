Tuya Switch
===========

.. seo::
    :description: Instructions for setting up a Tuya device switch.
    :image: upload.svg

The ``tuya`` switch platform creates a switch a
tuya serial component.

There are two components, the Tuya bus and the switch that uses it.  The ``tuya``
component requires a :ref:`UART bus <uart>` to be configured.  Put the ``tuya`` component in
the config and it will list the possible devices for you in the config log.

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

    uart:
      rx_pin: GPIO3
      tx_pin: GPIO1
      baud_rate: 9600

    # Register the Tuya MCU connection
    tuya:

Here is an example output for a Tuya heater:

.. code-block:: text

    [13:46:01][C][tuya:023]: Tuya:
    [13:46:01][C][tuya:032]:   Datapoint 1: switch (value: OFF)
    [13:46:01][C][tuya:032]:   Datapoint 2: switch (value: OFF)
    [13:46:01][C][tuya:034]:   Datapoint 3: int value (value: 19)
    [13:46:01][C][tuya:034]:   Datapoint 4: int value (value: 17)
    [13:46:01][C][tuya:034]:   Datapoint 5: int value (value: 0)
    [13:46:01][C][tuya:036]:   Datapoint 7: enum (value: 1)
    [13:46:01][C][tuya:046]:   Product: '{"p":"ynjanlglr4qa6dxf","v":"1.0.0","m":0}'

On this controller, the datapoint 2 represents the child lock switch
setting which is what we are interested in controlling using this platform.

Based on this, you can create the switch as follows:

.. code-block:: yaml

    # Create a switch
    switch:
      - platform: "tuya"
        name: "MySwitch"
        switch_datapoint: 2

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the switch.
- **switch_datapoint** (**Required**, int): The datapoint id number of the switch.
- All other options from :ref:`Switch <config-switch>`.

See Also
--------

- :doc:`/components/switch/index`
- :apiref:`tuya/switch/tuya_switch.h`
- :ghedit:`Edit`
