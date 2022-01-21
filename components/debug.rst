Debug Component
===============

.. seo::
    :description: Instructions for setting up the debug component in ESPHome
    :image: bug-report.svg

The ``debug`` component can be used to debug problems with ESPHome. At startup, it prints
a bunch of useful information like reset reason, free heap size, ESPHome version and so on.
It also allows you get the same information as a text sensor, and to monitor the state of the
ESP heap memory (free space, maximal free block and fragmentation level) and the main-loop timing.

.. figure:: images/debug.png
    :align: center

    Example debug component output.

.. code-block:: yaml

    # Example configuration entry
    debug:
      update_interval: 5s
      device:
        name: Device Info
      free:
        name: Heap Free
      fragmentation:
        name: Heap Fragmentation
      block:
        name: Heap Max Block
      loop_time:
        name: Loop Time

    # Logger must be at least debug (default)
    logger:
      level: debug

Configuration variables:
------------------------

- **device** (*Optional*): reports the debug information text:

  - ESPHome Version
  - Free heap size at startup
  - Flash chip size, speed and mode
  - ESP32:

    - Chip model, cores, revision
    - Chip features (BLE / BT / WiFi_BGN / EMB_FLASH / ...)
    - ESP-IDF version
    - EFuse MAC
    - Reset reason
    - Wakeup reason
  - ESP8266:

    - Chip id, frequency
    - Flash id
    - SDK, Core & Boot versions
    - Reset reason & information

- **free** (*Optional*): reports the free heap size in bytes.
- **fragmentation** (*Optional*): reports the fragmentation metric
  (0% is clean, more than ~50% is not harmless)
- **block** (*Optional*): reports the largest contiguous free RAM block in the heap in bytes,
  useful for checking heap fragmentation.
- **loop-time** (*Optional*): reports the time between successive loop calls.

- All other options from :ref:`Sensor <config-sensor>`.

Requires ``arduino_version: 2.5.2`` or above see `esp8266 arduino releases <https://github.com/esp8266/Arduino/releases>`

See Also
--------

- https://arduino-esp8266.readthedocs.io/en/latest/libraries.html#esp-specific-apis
- :ref:`sensor-filters`
- :doc:`logger`
- :apiref:`debug/debug_component.h`
- :ghedit:`Edit`
