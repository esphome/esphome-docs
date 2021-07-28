.. _uart:

UART Bus
========

.. seo::
    :description: Instructions for setting up a UART serial bus on ESPs
    :image: uart.png
    :keywords: UART, serial bus

UART is a common serial protocol for a lot of devices. For example, when uploading a binary to your ESP
you have probably used UART to access the chip. UART (or for Arduino often also called Serial) usually
consists of 2 pins:

- **TX**: This line is used to send data to the device at the other end.
- **RX**: This line is used to receive data from the device at the other end.

Please note that these the naming of these two pins depends on the chosen perspective and can be ambiguous. For example,
while the ESP might send (``TX``) on pin A and receive (``RX``) data on pin B, from the other devices
perspective these two pins are switched (i.e. *it* sends on pin B and receives on pin A). So you might
need to try with the two pins switched if it doesn't work immediately.

Additionally, each UART bus can operate at different speeds (baud rates), so ESPHome needs to know what speed to
receive/send data at using the ``baud_rate`` option. The most common baud rates are 9600 and 115200.

In some cases only **TX** or **RX** exists as the device at the other end only accepts data or sends data.

.. note::

    On the ESP32, this component uses the hardware UART units and is thus very accurate. On the ESP8266 however,
    ESPHome has to use a software implementation as there are no other hardware UART units available other than the
    ones used for logging. Therefore the UART data on the ESP8266 can have occasional data glitches especially with
    higher baud rates..

.. note::

    From ESPHome 1.21.0 the ``ESP8266SoftwareSerial`` UART ``write_byte`` function had the parity bit fixed to be correct
    for the data being sent. This could cause unexpected issue if you have built your own devices that do parity checking.


.. code-block:: yaml

    # Example configuration entry
    uart:
      tx_pin: 1
      rx_pin: 3
      baud_rate: 9600

Configuration variables:
------------------------

- **baud_rate** (**Required**, int): The baud rate of the UART bus.
- **tx_pin** (*Optional*, :ref:`config-pin`): The pin to send data to from the ESP's perspective.
- **rx_pin** (*Optional*, :ref:`config-pin`): The pin to receive data on from the ESP's perspective.
- **rx_buffer_size** (*Optional*, int): The size of the buffer used for receiving UART messages. Increase if you use integration that needs to read big payloads from UART. Defaults to ``256``.
- **data_bits** (*Optional*, int): The number of data bits used on the UART bus. Options: 5 to 8. Defaults to 8.
- **parity** (*Optional*): The parity used on the UART bus. Options: ``NONE``, ``EVEN``, ``ODD``. Defaults to ``NONE``.
- **stop_bits** (*Optional*, int): The number of stop bits to send. Options: 1, 2. Defaults to 1.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this UART hub if you need multiple UART hubs.

ESP32 options:

- **invert** (*Optional*, boolean): Invert the logic levels of the RX and TX pins. Options: ``True`` or ``False``. Defaults to ``False``.

.. _uart-hardware_uarts:

Hardware UARTs
--------------

Whenever possible, ESPHome will use the hardware UART unit on the processor for fast and accurate communication.
When the hardware UARTs are all occupied, ESPHome will fall back to a software implementation that may not
be accurate at higher baud rates.

``UART0`` is (by default) used by the :doc:`logger component </components/logger>`, using ``tx_pin: GPIO1`` and
``rx_pin: GPIO3``. If you configure a UART that overlaps with these pins, you can share the hardware with the
logger and leave others available. If you have configured the logger to use a different hardware UART, the pins
used for hardware sharing change accordingly.

The ESP32 has three UARTs. Any pair of GPIO pins can be used, as long as they support the proper output/input modes.

The ESP8266 has two UARTs; the second of which is TX-only. Only a limited set of pins can be used. ``UART0`` may
use either ``tx_pin: GPIO1`` and ``rx_pin: GPIO3``, or ``tx_pin: GPIO15`` and ``rx_pin: GPIO13``. ``UART1`` must
use ``tx_pin: GPIO2``. Any other combination of pins will result in use of a software UART.

.. _uart-write_action:

``uart.write`` Action
---------------------

This :ref:`Action <config-action>` sends a defined UART signal to the given UART bus.

.. code-block:: yaml

    on_...:
      - uart.write: 'Hello World'

      # For escape characters, you must use double quotes!
      - uart.write: "Hello World\r\n"

      # Raw data
      - uart.write: [0x00, 0x20, 0x42]

      # Templated, return type is std::vector<uint8_t>
      - uart.write: !lambda
          return {0x00, 0x20, 0x42};

      # in case you need to specify the uart id
      - uart.write:
          id: my_second_uart
          data: 'other data'

See Also
--------

- :doc:`/components/logger`
- :apiref:`uart/uart.h`
- :ghedit:`Edit`
