ESP32 Bluetooth Low Energy Scanner
======================================

.. seo::
    :description: Instructions for setting up BLE text sensors for the ESP32.
    :image: bluetooth.png
    :keywords: ESP32

The ``ble_scanner`` text sensor platform lets you track reachable BLE devices.
See the `BLE Tracker Configuration variables <https://esphome.io/components/esp32_ble_tracker.html#configuration-variables>`__ for
instructions for setting up scan parameters.
The sensor platform is similar to :doc:`/components/sensor/ble_rssi` but does not support device filtering and sends more information about found devices. The sensor platform itself does not support any settings but :ref:`Text Sensor <config-text_sensor>` options.

.. code-block:: yaml

    # Example configuration entry
    esp32_ble_tracker:

    text_sensor:
      - platform: ble_scanner
        name: "BLE Devices Scanner"

Example json log:

.. code-block:: json

    {
        "timestamp":1578254525,
        "address":"D7:E7:E7:66:DD:33",
        "rssi":"-80",
        "name":"MI Band 2"
    }

Configuration variables:
------------------------

-  **name** (**Required**, string): The name of the sensor.
- All other options from :ref:`Text Sensor <config-text_sensor>`.

See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/text_sensor/index`
- :apiref:`ble_scanner/ble_scanner.h`
- :ghedit:`Edit`
