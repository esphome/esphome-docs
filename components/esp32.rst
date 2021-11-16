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
  `this list <https://platformio.org/boards?count=1000&filter%5Bplatform%5D=espressif32>`__.
  *This only affects pin aliases, flash size and some internal settings*, if unsure choose a generic board.
- **framework** (*Optional*): Options for the underlying framework used by ESPHome.
  See :ref:`esp32-arduino_framework` and :ref:`esp32-espidf_framework`.

- **variant** (*Optional*, boolean): Defaults to the variant detected from the board. If the board is not known this option becomes mandatory.
  One of ``esp32``, ``esp32s2``, ``esp32s3``, ``esp32c3`` and ``esp32h2``.

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
        CONFIG_COMPILER_OPTIMIZATION_SIZE: y

- **version** (*Optional*, string): The base framework version number to use, from
  `ESP32 ESP-IDF releases <https://github.com/espressif/esp-idf/releases>`__. Defaults to ``recommended``. Additional values are:

  - ``dev``: Use the latest commit from https://github.com/espressif/esp-idf, note this may break at any time
  - ``latest``: Use the latest *release* from https://github.com/espressif/esp-idf/releases, even if it hasn't been recommended yet.
  - ``recommended``: Use the recommended framework version.

- **source** (*Optional*, string): The PlatformIO package or repository to use for the framework. This can be used to use a custom or patched version of the framework.
- **platform_version** (*Optional*, string): The version of the `platformio/espressif32 <https://github.com/platformio/platform-espressif32/releases/>`__ package to use.
- **sdkconfig_options** (*Optional*, mapping): Custom sdkconfig options to set in the ESP-IDF project.

See Also
--------

- :doc:`esphome`
- :ghedit:`Edit`
