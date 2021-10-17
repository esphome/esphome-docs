Tuya MCU
========

.. seo::
    :description: Instructions for setting up the Tuya component.
    :image: tuya.png

The ``tuya`` component creates a serial connection to the Tuya MCU for platforms to use.

.. figure:: /images/tuya.png
    :align: center
    :width: 40%

The ``tuya`` serial component requires a :ref:`UART bus <uart>` to be configured.
Put the ``tuya`` component in the config and it will list the possible devices for you in the config log.

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

Here is an example output for a Tuya fan controller:

.. code-block:: text

    [12:39:45][C][tuya:023]: Tuya:
    [12:39:45][C][tuya:032]:   Datapoint 1: switch (value: ON)
    [12:39:45][C][tuya:036]:   Datapoint 3: enum (value: 1)
    [12:39:45][C][tuya:036]:   Datapoint 6: enum (value: 0)
    [12:39:45][C][tuya:034]:   Datapoint 7: int value (value: 0)
    [12:39:45][C][tuya:032]:   Datapoint 9: switch (value: OFF)
    [12:39:45][C][tuya:046]:   Product: '{"p":"hqq73kftvzh8c92u","v":"1.0.0","m":0}'

Configuration variables:
------------------------

- **time_id** (*Optional*, :ref:`config-id`): Some Tuya devices support obtaining local time from ESPHome. 
  Specify the ID of the :ref:`Time Component <time>` which will be used.

- **ignore_mcu_update_on_datapoints** (*Optional*, list): A list of datapoints to ignore MCU updates for.  Useful for certain broken/erratic hardware and debugging.

See Also
--------

- :doc:`/components/fan/tuya`
- :doc:`/components/light/tuya`
- :apiref:`tuya/tuya.h`
- :ghedit:`Edit`
