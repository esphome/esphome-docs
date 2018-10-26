Sonoff RF Bridge
================

The ``sonoff_rf_bridge`` component allows you to use the RF transmitter/receiver of the
Sonoff RF Bridge (`datasheet <https://www.itead.cc/wiki/images/5/5e/RF_Universal_Transeceive_Module_Serial_Protocol_v1.0.pdf>`__).

This component communicates with the RF chip over the :ref:`UART bus <uart>` with a baud rate
of 19200. So you need to add an ``uart:`` component into your configuration as seen below.

.. code:: yaml

    # Example configuration entry
    uart:
      rx_pin: RX
      tx_pin: TX
      baud_rate: 19200

    logger:
      # Disable logging over USB - the serial interface is used for communicating
      # with the RF chip
      baud_rate: 0

    sonoff_rf_bridge:

    binary_sensor:
      # For sensing when a button is pressed
      - platform: sonoff_rf_bridge
        name: "Sonoff RF Bridge Sensor"
        sync: 100
        low: 100
        high: 100
        data: '01101110110101000010101010101011'

    switch:
      # For sending an RF code
      - platform: sonoff_rf_bridge
        name: "Sonoff RF Bridge Switch"
        sync: 100
        low: 100
        data: '01101110110101000010101010101011'


.. note::

    The first time this component is enabled for an ESP32, the code partition needs to be
    resized. Please flash the ESP32 via USB when adding this to your configuration. After that,
    you can use OTA updates again.


Configuration variables:
------------------------

- **scan_interval** (*Optional*, :ref:`config-time`): The length of each scan.
  If a device is not found within this time window, it will be marked as not present. Defaults to 300s.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this ESP32 BLE Hub.

See Also
--------

- :doc:`binary_sensor/esp32_ble_tracker`
- :doc:`API Reference </api/misc/esp32_ble_tracker>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/esp32_ble_tracker.rst>`__

.. disqus::
