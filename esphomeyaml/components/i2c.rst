.. _i2c:

I²C Bus
=======

.. seo::
    :description: Instructions for setting up the i2c bus to communicate with 2-wire devices in esphomelib
    :image: i2c.png
    :keywords: i2c, iic, bus

This component sets up the i²c bus for your ESP32 or ESP8266. In order for those components
to work correctly, you need to define the i²c bus in your configuration. Please note the ESP
will enable its internal 10kΩ pullup resistors for these pins, so you usually don't need to
put on external ones.

.. code-block:: yaml

    # Example configuration entry
    i2c:
      sda: 21
      scl: 22
      scan: False

Configuration variables:
------------------------

- **sda** (*Optional*, :ref:`config-pin`): The pin for the data line of the i²c bus.
  Defaults to the default of your board (usually GPIO21 for ESP32 and GPIO4 for ESP8266).
- **scl** (*Optional*, :ref:`config-pin`): The pin for the clock line of the i²c bus.
  Defaults to the default of your board (usually GPIO22 for ESP32 and
  GPIO5 for ESP8266).
- **scan** (*Optional*, boolean): If esphomelib should do a search of the i2c address space on startup.
  Note that this can slow down startup and is only recommended for when setting up new sensors. Defaults to
  ``False``.
- **frequency** (*Optional*, float): Set the frequency the i²c bus should operate on. Defaults to “100kHz”.

.. note::

    If you're using the ESP32 and i2c frequently is showing errors in the logs, try with the latest
    version of the Arduino framework. See :ref:`esphomeyaml-arduino_version` for information on how to do this.

See Also
--------

- :doc:`API Reference </api/core/i2c>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/i2c.rst>`__

.. disqus::
