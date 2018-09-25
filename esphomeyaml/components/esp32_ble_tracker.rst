ESP32 Bluetooth Low Energy Tracker Hub
======================================

The ``esp32_ble_tracker`` component creates a global hub so that you can track bluetooth low
energy devices using your ESP32 node.

See `Setting up devices </esphomeyaml/components/binary_sensor/esp32_ble.html#setting-up-devices>`__
for information on how you can find out the MAC address of a device and track it using esphomelib.

.. code:: yaml

    # Example configuration entry
    esp32_ble_tracker:
      scan_interval: 300s

    binary_sensor:
      - platform: esp32_ble_tracker
        mac_address: AC:37:43:77:5F:4C
        name: "ESP32 BLE Tracker Google Home Mini"

    sensor:
      - platform: ble_rssi
        mac_address: AC:37:43:77:5F:4C
        name: "BLE Google Home Mini RSSI value"
      - platform: xiaomi_miflora
        mac_address: 94:2B:FF:5C:91:61
        temperature:
          name: "Xiaomi MiFlora Temperature"
        moisture:
          name: "Xiaomi MiFlora Moisture"
        illuminance:
          name: "Xiaomi MiFlora Illuminance"
        conductivity:
          name: "Xiaomi MiFlora Soil Conductivity"
        battery_level:
          name: "Xiaomi MiFlora Battery Level"
      - platform: xiaomi_mijia
        mac_address: 7A:80:8E:19:36:BA
        temperature:
          name: "Xiaomi MiJia Temperature"
        humidity:
          name: "Xiaomi MiJia Humidity"
        battery_level:
          name: "Xiaomi MiJia Battery Level"

Configuration variables:
------------------------

- **scan_interval** (*Optional*, :ref:`config-time`): The length of each scan.
  If a device is not found within this time window, it will be marked as not present. Defaults to 300s.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this ESP32 BLE Hub.

See Also
--------

- :doc:`binary_sensor/esp32_ble_tracker`
- :doc:`API Reference </api/misc/esp32_ble_tracker>`
- `ESP32 BLE for Arduino <https://github.com/nkolban/ESP32_BLE_Arduino>`__ by `Neil Kolban <https://github.com/nkolban>`__.
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/esp32_ble_tracker.rst>`__
