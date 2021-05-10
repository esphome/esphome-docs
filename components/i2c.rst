.. _i2c:

I²C Bus
=======

.. seo::
    :description: Instructions for setting up the I²C bus to communicate with 2-wire devices in ESPHome
    :image: i2c.png
    :keywords: i2c, iic, bus

This component sets up the I²C bus for your ESP32 or ESP8266. In order for these components
to work correctly, you need to define the I²C bus in your configuration. Please note the ESP
will enable its internal 10kΩ pullup resistors for these pins, so you usually don't need to
put on external ones. You can use multiple devices on one I²C bus as each device is given a
unique address for communicating between it and the ESP. You can do this by hopping
wires from the two lines (SDA and SCL) from each device board to the next device board or by
connecting the wires from each device back to the two I²C pins on the ESP.

.. code-block:: yaml

    # Example configuration entry for ESP32
    i2c:
      sda: 21
      scl: 22
      scan: True
      id: bus_a

Configuration variables:
------------------------

- **sda** (*Optional*, :ref:`config-pin`): The pin for the data line of the I²C bus.
  Defaults to the default of your board (usually GPIO21 for ESP32 and GPIO4 for ESP8266).
- **scl** (*Optional*, :ref:`config-pin`): The pin for the clock line of the I²C bus.
  Defaults to the default of your board (usually GPIO22 for ESP32 and
  GPIO5 for ESP8266).
- **scan** (*Optional*, boolean): If ESPHome should do a search of the I²C address space on startup.
  Defaults to ``True``.
- **frequency** (*Optional*, float): Set the frequency the I²C bus should operate on.
  Defaults to ``50kHz``. Values are ``50kHz``, ``100kHz``, ``200kHz``, ... ``800kHz``
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this I²C bus if you need multiple I²C buses.

.. note::

    If the device can support multiple I²C buses (ESP32 has 2) these buses need to be defined as below and sensors need to be setup specifying the correct bus:

    .. code-block:: yaml

        # Example configuration entry
        i2c:
          - id: bus_a
            sda: 13
            scl: 16
            scan: True
          - id: bus_b
            sda: 14
            scl: 15
            scan: True
       # Sensors should be specified as follows
       - platform: bme680
         i2c_id: bus_b
         address: 0x76
         # ...

       # If a I²C multiplexer is used all I²C devices can be additionally configured like:
       - platform: bmp280
         multiplexer:
           id: multiplex0
           channel: 0
         # ...

See Also
--------

- :apiref:`i2c/i2c.h`
- :ghedit:`Edit`
