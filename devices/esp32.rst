Generic ESP32
=============

.. esphome:device-definition::
   :alias: esp32
   :category: espressif
   :friendly_name: Generic ESP32
   :toc_group: Espressif
   :toc_image: esp32.svg

.. seo::
    :description: Information about how to use generic ESP32 boards in ESPHome.
    :image: esp32.svg
    :keywords: ESP32

All devices based on the original ESP32 are supported by ESPHome. Simply select ``ESP32`` when
the ESPHome wizard asks you for your platform and choose a board type
from `this link <https://registry.platformio.org/platforms/platformio/espressif32/boards>`__ when the wizard
asks you for the board type.

.. code-block:: yaml

    # Example configuration entry
    esphome:
      name: livingroom

    esp32:
      board: <BOARD_TYPE>

.. note::

    Support for the ESP32-S2 and ESP32-C3 is currently in development.

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
    esphome:
      name: livingroom

    esp32:
      board: <BOARD_TYPE>

    binary_sensor:
      - platform: gpio
        name: "Pin GPIO23"
        pin: GPIO23

See Also
--------

- :esphome:device:`nodemcu:nodemcu-esp32`
- :ghedit:`Edit`
