Tuya Cover
==========

.. seo::
    :description: Instructions for setting up a Tuya cover motor.

The ``tuya`` cover platform creates a simple position-only cover from a
tuya serial component.

There are two components, the Tuya bus and the cover that uses it.  The :doc:`/components/tuya`
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
    [21:50:28][C][tuya:031]:   Datapoint 2: int value (value: 53)
    [21:50:28][C][tuya:029]:   Datapoint 5: switch (value: OFF)

On this cover motor, the position control is datapoint 2.
Now you can create the cover.

.. code-block:: yaml

    # Create a cover using the dimmer
    cover:
      - platform: "tuya"
        name: "motor1"
        position_datapoint: 2

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the cover.
- **position_datapoint** (**Required**, int): The datapoint id number of the cover position value.
- **min_value** (*Optional*, int): The lowest position value, meaning cover closed. Defaults to 0.
- **max_value** (*Optional*, int): the highest position value, meaning cover opened. Defaults to 255.
- **invert_position** (*Optional*, boolean): invert the meaning of ``min_value`` and ``max_value``.
  When set to ``true``, ``min_value`` will mean opened and ``max_value`` is closed.
- All other options from :ref:`Cover <config-cover>`.


See Also
--------

- :doc:`/components/tuya`
- :doc:`/components/cover/index`
- :apiref:`tuya/cover/tuya_cover.h`
- :ghedit:`Edit`

