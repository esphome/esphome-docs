ESP32 Bluetooth Low Energy RSSI Sensor
======================================

.. seo::
    :description: Instructions for setting up RSSI sensors for the ESP32 BLE.
    :image: bluetooth.png
    :keywords: ESP32

The ``ble_rssi`` sensor platform lets you track the RSSI value or signal strength of a
BLE device. See :ref:`the binary sensor setup <esp32_ble_tracker-setting_up_devices>` for
instructions for setting up this platform.

.. code-block:: yaml

    # Example configuration entry
    esp32_ble_tracker:
      scan_interval: 300s

    sensor:
      - platform: ble_rssi
        mac_address: AC:37:43:77:5F:4C
        name: "BLE Google Home Mini RSSI value"

Configuration variables:
------------------------

-  **mac_address** (**Required**, MAC Address): The MAC address to track for this
   sensor.
-  **name** (**Required**, string): The name of the sensor.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

See Also
--------

- :doc:`/esphomeyaml/components/esp32_ble_tracker`
- :doc:`/esphomeyaml/components/sensor/index`
- :doc:`API Reference </api/misc/esp32_ble_tracker>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/esp32_ble_tracker.rst>`__

.. disqus::
