Heap Sensors
==================

.. seo::
    :description: Instructions for setting up heap sensors in ESPHome
    :image: heap.gif

The ``heap`` sensors allows you to monitor the state of the ESP heap memory. The sensor
reports heap free space, maximal free block and fragmentation level.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: heap
        update_interval: 5s
        free:
          name: Heap Free
        fragmentation:
          name: Heap Fragmentation
        block:
          name: Heap Max Block

Configuration variables:
------------------------

- **free** (*Optional*): reports the free heap size.
- **fragmentation** (*Optional*): reports the fragmentation metric (0% is clean, more than ~50% is not harmless)
- **block** (*Optional*): reports the largest contiguous free RAM block in the heap, useful for checking heap fragmentation. 

- All other options from :ref:`Sensor <config-sensor>`.

Requires ``arduino_version: 2.5.2`` or above defined in :ref:`esphome <arduino_version>`

See Also
--------

- https://arduino-esp8266.readthedocs.io/en/latest/libraries.html
- :ref:`sensor-filters`
- :apiref:`heap/heap_sensor.h`
- :ghedit:`Edit`
