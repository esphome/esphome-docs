ESP32 Platform
==============

.. seo::
    :description: Configuration for the ESP32 platform for ESPHome.
    :image: esp32.svg

This component contains platform-specific options for the ESP32 platform.

.. code-block:: yaml

    # Example configuration entry
    esp32:
      board: nodemcu-32s

Configuration variables:
------------------------

- **board** (**Required**, string): The PlatformIO board ID that should
  be used. Choose the appropriate board from
  `this list <https://registry.platformio.org/packages/platforms/platformio/espressif32/boards>`__ (the icon next to the name
  can be used to copy the board ID). *This only affects pin aliases, flash size and some internal settings*, if unsure
  choose a generic board from Espressif such as ``esp32dev``.
- **framework** (*Optional*): Options for the underlying framework used by ESPHome.
  See :ref:`esp32-arduino_framework` and :ref:`esp32-espidf_framework`.
- **flash_size** (*Optional*, string): The amount of flash memory available on the ESP32 board/module. One of ``2MB``,
  ``4MB``, ``8MB``, ``16MB`` or ``32MB``. Defaults to ``4MB``. **Warning: specifying a size larger than that available
  on your board will cause the ESP32 to fail to boot.**
- **partitions** (*Optional*, filename): The name of (optionally including the path to) the file containing the
  partitioning scheme to be used. When not specified, partitions are automatically generated based on ``flash_size``.
- **variant** (*Optional*, string): The variant of the ESP32 that is used on this board. One of ``esp32``,
  ``esp32s2``, ``esp32s3``, ``esp32c3`` and ``esp32h2``. Defaults to the variant that is detected from the board; if
  a board that's unknown to ESPHome is used, this option is mandatory.

.. note::

    Support for ESP32 variants such as the S2, S3 and C3 is still in development and there could be issues.

GPIO Pin Numbering
------------------

The ESP32 boards often use the internal GPIO pin numbering on the board, this means that
you don't have to worry about other kinds of pin numberings, yay!

Some notes about the pins on the ESP32:

- ``GPIO0`` is used to determine the boot mode on startup. It should therefore not be pulled LOW
  on startup to avoid booting into flash mode. You can, however, still use this as an output pin.
- ``GPIO34``-``GPIO39`` can not be used as outputs (even though GPIO stands for "general purpose input
  **output**"...).
- ``GPIO32``-``GPIO39``: These pins can be used with the :doc:`/components/sensor/adc` to measure
  voltages.
- ``GPIO2``: This pin is connected to the blue LED on the board. It also supports
  the :doc:`touch pad binary sensor </components/binary_sensor/esp32_touch>` like some other
  pins.

.. code-block:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: gpio
        name: "Pin GPIO23"
        pin: GPIO23

.. _esp32-arduino_framework:

Arduino framework
-----------------

This is the default framework for ESP32 chips at the moment.

.. code-block:: yaml

    # Example configuration entry
    esp32:
      board: nodemcu-32s
      framework:
        type: arduino
        version: 2.0.0

Configuration variables:
------------------------

- **version** (*Optional*, string): The base framework version number to use, from
  `ESP32 arduino releases <https://github.com/espressif/arduino-esp32/releases>`__. Defaults to ``recommended``. Additional values are:

  - ``dev``: Use the latest commit from https://github.com/espressif/arduino-esp32, note this may break at any time
  - ``latest``: Use the latest *release* from https://github.com/espressif/arduino-esp32/releases, even if it hasn't been recommended yet.
  - ``recommended``: Use the recommended framework version.

- **source** (*Optional*, string): The PlatformIO package or repository to use for framework. This can be used to use a custom or patched version of the framework.
- **platform_version** (*Optional*, string): The version of the `platformio/espressif32 <https://github.com/platformio/platform-espressif32/releases/>`__ package to use.

.. _esp32-espidf_framework:

ESP-IDF framework
-----------------

This is an alternative base framework for ESP32 chips, and recommended for variants
of the ESP32 like ESP32S2, ESP32S3, ESP32C3 and single-core ESP32 chips.

.. code-block:: yaml

    # Example configuration entry
    esp32:
      board: esp32-c3-devkitm-1
      framework:
        type: esp-idf
        version: recommended
        # Custom sdkconfig options
        sdkconfig_options:
          COMPILER_OPTIMIZATION_SIZE: y
        # Advanced tweaking options
        advanced:
          ignore_efuse_mac_crc: false

Configuration variables:
------------------------

- **version** (*Optional*, string): The base framework version number to use, from
  `ESP32 ESP-IDF releases <https://github.com/espressif/esp-idf/releases>`__. Defaults to ``recommended``. Additional values are:

  - ``dev``: Use the latest commit from https://github.com/espressif/esp-idf, note this may break at any time
  - ``latest``: Use the latest *release* from https://github.com/espressif/esp-idf/releases, even if it hasn't been recommended yet.
  - ``recommended``: Use the recommended framework version.

- **source** (*Optional*, string): The PlatformIO package or repository to use for the framework. This can be used to use a custom or patched version of the framework.
- **platform_version** (*Optional*, string): The version of the `platformio/espressif32 <https://github.com/platformio/platform-espressif32/releases/>`__ package to use.
- **sdkconfig_options** (*Optional*, mapping): Custom sdkconfig `compiler options <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/kconfig.html#compiler-options>`__ to set in the ESP-IDF project.
- **advanced** (*Optional*, mapping): Advanced options for highly specific tweaks.

  - **ignore_efuse_mac_crc** (*Optional*, boolean): Can be set to ``true`` for devices on which the burnt in MAC address does not
    match the also burnt in CRC for that MAC address, resulting in an error like ``Base MAC address from BLK0 of EFUSE CRC error``.

See Also
--------

- :doc:`esphome`
- :ghedit:`Edit`
