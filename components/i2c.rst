.. _i2c:

I²C Bus
=======

.. seo::
    :description: Instructions for setting up the I²C bus to communicate with 2-wire devices in ESPHome
    :image: i2c.svg
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
      sda: GPIOXX
      scl: GPIOXX
      scan: true
      id: bus_a

Configuration variables:
------------------------

- **sda** (*Optional*, :ref:`config-pin`): The pin for the data line of the I²C bus.
  Defaults to the default of your board (usually GPIO21 for ESP32 and GPIO4 for ESP8266).
- **scl** (*Optional*, :ref:`config-pin`): The pin for the clock line of the I²C bus.
  Defaults to the default of your board (usually GPIO22 for ESP32 and
  GPIO5 for ESP8266).
- **scan** (*Optional*, boolean): If ESPHome should do a search of the I²C address space on startup.
  Defaults to ``true``.
- **frequency** (*Optional*, float): Set the frequency the I²C bus should operate on.
  Defaults to ``50kHz``. Values are ``10kHz``, ``50kHz``, ``100kHz``, ``200kHz``, ... ``800kHz``
- **timeout** (*Optional*, :ref:`config-time`): Set the I²C bus timeout.
  Defaults to the framework defaults (``100us`` on ``esp32`` with ``esp-idf``, ``50ms`` on ``esp32`` with ``Arduino``,
  ``1s`` on ``esp8266`` and ``1s`` on ``rp2040``). Maximum on ``esp-idf`` is 13ms.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this I²C bus if you need multiple I²C buses.

.. note::

    If the device can support multiple I²C buses (ESP32 has 2, ESP8266 does not support more than one) these buses need to be defined as below and sensors need to be setup specifying the correct bus:

    .. code-block:: yaml

        # Example configuration entry
        i2c:
          - id: bus_a
            sda: GPIOXX
            scl: GPIOXX
            scan: true
          - id: bus_b
            sda: GPIOXX
            scl: GPIOXX
            scan: true
       # Sensors should be specified as follows
       - platform: bme680
         i2c_id: bus_b
         address: 0x76
         # ...

For I²C multiplexing see :doc:`/components/tca9548a`.

Generic I²C device component:
-----------------------------
.. _i2c_device:

Other components that depend on the I²C component will reference it, typically to communicate with specific
peripheral devices. There is also a general-purpose I²C device component that can be used to communicate with hardware not
supported by a specific component. It allows selection of the I²C address.
Reads and writes on the device can be performed with lambdas. For example:

.. code-block:: yaml

    i2c:
        sda: 4
        scl: 5
        scan: True

    i2c_device:
      id: i2cdev
      address: 0x2C

   on...:
     then:
       - lambda: !lambda |-
           id(i2cdev).write_byte(0x00, 0x12);
           if (auto b = id(i2cdev).read_byte(0x01)) {
             // TODO
           }


Configuration variables:
------------------------

- **address** (*Required*, int): I²C address of the device.

See Also
--------

- :doc:`/components/tca9548a`
- :apiref:`i2c/i2c.h`
- :ghedit:`Edit`
