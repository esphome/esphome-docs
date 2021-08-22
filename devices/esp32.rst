Generic ESP32
=============

.. seo::
    :description: Information about how to use generic ESP32 boards in ESPHome.
    :image: esp32.png

All ESP32-based devices are supported by ESPHome. Simply select ``ESP32`` when
the ESPHome wizard asks you for your platform and choose a board type
from `this link <https://platformio.org/boards?count=1000&filter%5Bplatform%5D=espressif32>`__ when the wizard
asks you for the board type.

.. code-block:: yaml

    # Example configuration entry
    esphome:
      name: livingroom
      platform: ESP32
      board: <BOARD_TYPE>

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
      platform: ESP32
      board: <BOARD_TYPE>

    binary_sensor:
      - platform: gpio
        name: "Pin GPIO23"
        pin: GPIO23

See Also
--------

- :doc:`nodemcu_esp32`
- :ghedit:`Edit`
