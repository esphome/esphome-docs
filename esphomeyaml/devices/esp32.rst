Generic ESP32
=============

.. seo::
    :description: Information about how to use generic ESP32 boards in esphomelib.
    :image: esp32.svg

All ESP32-based devices are supported by esphomeyaml. Simply select ``ESP32`` when
the esphomeyaml wizard asks you for your platform and choose a board type
from `this link <http://docs.platformio.org/en/latest/platforms/espressif32.html>`__ when the wizard
asks you for the board type.

.. code:: yaml

    # Example configuration entry
    esphomeyaml:
      name: livingroom
      platform: ESP32
      board: <BOARD_TYPE>

The ESP32 boards often use the internal GPIO pin numbering on the board, this means that
you don't have to worry about other kinds of pin numberings, yay!

Some notes about the pins on the ESP32:

- ``GPIO0`` is used to determine the boot mode on startup. It should therefore not be pulled LOW
  on startup to avoid booting into flash mode. You can, however, still use this as an output pin.
- ``GPIO34``-``GPIO39`` can not be used as outputs (even though GPIO stands for "general purpose input
  **output**"...)
- ``GPIO32``-``GPIO39``: These pins can be used with the :doc:`/esphomeyaml/components/sensor/adc` to measure
  voltages.
- ``GPIO2``: This pin is connected to the blue LED on the board as seen in above picture. It also supports
  the :doc:`touch pad binary sensor </esphomeyaml/components/binary_sensor/esp32_touch>` like some other
  pins.

.. code:: yaml

    # Example configuration entry
    esphomeyaml:
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
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/devices/esp32.rst>`__

.. disqus::
