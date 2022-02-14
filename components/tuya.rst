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

    # Make sure logging is not using the serial port
    logger:
      baud_rate: 0

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

Automations:

- **on_datapoint_update**: (*Optional*): An automation to perform when a Tuya datapoint update is received. See :ref:`tuya-on_datapoint_update`.

Tuya Automation
---------------

.. _tuya-on_datapoint_update:

``on_datapoint_update``
***********************

This automation will be triggered when a a Tuya datapoint update is received.
A variable ``x`` is passed to the automation for use in lambdas.
The type of ``x`` variable is depending on ``datapoint_type`` configuration variable:

- *raw*: ``x`` is ``std::vector<uint8_t>``
- *string*: ``x`` is ``std::string``
- *bool*: ``x`` is ``bool``
- *int*: ``x`` is ``int``
- *uint*: ``x`` is ``uint32_t``
- *enum*: ``x`` is ``uint8_t``
- *bitmask*: ``x`` is ``uint32_t``
- *any*: ``x`` is :apistruct:`tuya::TuyaDatapoint`

.. code-block:: yaml

    tuya:
      on_datapoint_update:
        - sensor_datapoint: 6
          datapoint_type: raw
          then:
            - lambda: |-
                ESP_LOGD("main", "on_datapoint_update %s", hexencode(x).c_str());
                id(voltage).publish_state((x[0] << 8 | x[1]) * 0.1);
                id(current).publish_state((x[3] << 8 | x[4]) * 0.001);
                id(power).publish_state((x[6] << 8 | x[7]) * 0.1);
        - sensor_datapoint: 7 # sample dp
          datapoint_type: string
          then:
            - lambda: |-
                ESP_LOGD("main", "on_datapoint_update %s", x.c_str());
        - sensor_datapoint: 8 # sample dp
          datapoint_type: bool
          then:
            - lambda: |-
                ESP_LOGD("main", "on_datapoint_update %s", ONOFF(x));
        - sensor_datapoint: 6
          datapoint_type: any # this is optional
          then:
            - lambda: |-
                if (x.type == tuya::TuyaDatapointType::RAW) {
                  ESP_LOGD("main", "on_datapoint_update %s", hexencode(x.value_raw).c_str());
                } else {
                  ESP_LOGD("main", "on_datapoint_update %hhu", x.type);
                }

Configuration variables:

- **sensor_datapoint** (*Required*, int): The datapoint id number of the sensor.
- **datapoint_type** (*Required*, string): The datapoint type one of *raw*, *string*, *bool*, *int*, *uint*, *enum*, *bitmask* or *any*.
- See :ref:`Automation <automation>`.


See Also
--------

- :doc:`/components/fan/tuya`
- :doc:`/components/light/tuya`
- :doc:`/components/switch/tuya`
- :doc:`/components/climate/tuya`
- :doc:`/components/binary_sensor/tuya`
- :doc:`/components/sensor/tuya`
- :doc:`/components/text_sensor/tuya`
- :apiref:`tuya/tuya.h`
- :ghedit:`Edit`
