Binary Sensor Map
=================

.. seo::
    :description: Instructions for setting up a Binary Sensor Map
    :image: binary_sensor_map.jpg

The ``binary_sensor_map`` sensor platform allows you to map :doc:`binary sensor </components/binary_sensor/index>`
to values. When a given binary sensor is on, the value associated with it in this platform's configuration will be published.

This sensor is **mostly used for touch** devices but could be used for any ``binary_sensor`` that publishes its ``ON`` or ``OFF`` state.

Add your binary sensors as ``channels`` to the binary sensor map. The binary sensor map then publishes a value depending
on the type of the binary sensor map and the values specified with each channel.

This platform currently supports two measurement types: ``GROUP`` and ``SUM``, but others might get added later.
You need to specify which type of mapping you want with the ``type:`` configuration value:

- ``GROUP`` Each channel has its own value. The sensor publishes the average value of all active
  binary sensors.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: binary_sensor_map
        id: group_0
        name: 'Group Map 0'
        type: GROUP
        channels:
          - binary_sensor: touchkey0
            value: 0
          - binary_sensor: touchkey1
            value: 10
          - binary_sensor: touchkey2
            value: 20
          - binary_sensor: touchkey3
            value: 30

    # Example binary sensors using MPR121 component
    mpr121:
      id: mpr121_first
      address: 0x5A

    binary_sensor:
      - platform: mpr121
        channel: 0
        id: touchkey0
      # ...
      
- ``SUM`` Each channel has its own value. The sensor publishes the sum of all active
  binary sensors values.

.. code-block:: yaml

    # Example configuration entry
    sensor:
  - platform: binary_sensor_map
    id: group_0
    name: 'Group Map 0'
    type: sum
    channels:
      - binary_sensor: bit0
        value: 1
      - binary_sensor: bit1
        value: 2
      - binary_sensor: bit2
        value: 4
      - binary_sensor: bit3
        value: 8

binary_sensor:
  - platform: gpio
    pin: 4
    id: bit0

  - platform: gpio
    pin: 5
    id: bit1

  - platform: gpio
    pin: 6
    id: bit2

  - platform: gpio
    pin: 7
    id: bit3
      # ...

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **type** (**Required**, string): The sensor type. Should be one of: ``GROUP``.
- **channels** (**Required**): A list of channels that are mapped to certain values.

  - **binary_sensor** (**Required**): The id of the :doc:`binary sensor </components/binary_sensor/index>`
    to add as a channel for this sensor.
  - **value** (**Required**): The value this channel should report when its binary sensor is active.

- All other options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :doc:`/components/binary_sensor/mpr121`
- :ref:`sensor-filters`
- :apiref:`binary_sensor_map/binary_sensor_map.h`
- :ghedit:`Edit`
