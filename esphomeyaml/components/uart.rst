.. _uart:

UART Bus
========

UART is a common serial protocol for a lot of devices. For example, when uploading a binary to your ESP
you have probably used UART to access the chip. UART (or for Arduino often also called Serial) usually
consists of 2 pins:

- **TX**: This line is used to send data to the device at the other end.
- **RX**: This line is used to receive data from the device at the other end.

Please note that these the naming of these two pins depends on the chosen perspective and can be ambiguous. For example,
while the ESP might send (``TX``) on pin A and receive (``RX``) data on pin B, from the other devices
perspective these two pins are switched (i.e. *it* sends on pin B and receives on pin A). So you might
need to try with the two pins switched if it doesn't work immediately.

Additionally, each UART bus can operate at different speeds (baud rates), so esphomelib needs to know what speed to
receive/send data at using the ``baud_rate`` option. The most common baud rates are 9600 and 115200.

In some cases only **TX** or **RX** exists as the device at the other end only accepts data or sends data.

.. note::

    On the ESP32, this component uses the hardware UART units and is thus very accurate. On the ESP8266 however,
    esphomelib has to use a software implementation as there are no other hardware UART units available other than the
    ones used for logging. Therefore the UART data on the ESP8266 can have occasional data glitches especially with
    higher baud rates..

.. code:: yaml

    # Example configuration entry
    uart:
      tx_pin: D0
      rx_pin: D1
      baud_rate: 9600


Configuration variables:
------------------------

- **baud_rate** (**Required**, int): The baud rate of the UART bus.
- **tx_pin** (*Optional*, :ref:`config-pin`): The pin to send data to from the ESP's perspective.
- **rx_pin** (*Optional*, :ref:`config-pin`): The pin to receive data on from the ESP's perspective.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this UART hub if you need multiple UART hubs.

See Also
--------

- :doc:`API Reference </api/core/uart>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/uart.rst>`__
