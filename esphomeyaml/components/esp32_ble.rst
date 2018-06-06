ESP32 Bluetooth Low Energy Hub
==============================

The ``esp32_ble`` component creates a global hub so that you can track bluetooth low
energy devices using your ESP32 node.

Currently this component only works with few supported bluetooth devices (most of them
being BLE "beacons") and currently only is capable of creating binary sensors indicating
whether a specific BLE MAC Address can be found or not.

In the future, this integration will be expanded to support reading RSSI values and hopefully
support lots more devices like tracking smartphones and reading temperature values from BLE sensors.

.. note::

    Be warned: This integration is currently not very stable and sometimes causes sporadic
    restarts of the node. Additionally, using this integration will increase the required
    flash memory size by up to 500kB.

See `Setting up devices </esphomeyaml/components/binary_sensor/esp32_ble.html#setting-up-devices>`__
for information on how you can find out the MAC address of a device and track it using esphomelib.

.. code:: yaml

    # Example configuration entry
    esp32_ble:
      scan_interval: 300s

    binary_sensor:
      - platform: esp32_ble
        mac_address: AC:37:43:77:5F:4C
        name: "ESP32 BLE Tracker Google Home Mini"

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **scan_interval** (*Optional*, :ref:`config-time`): The length of each scan.
  If a device is not found within this time window, it will be marked as not present. Defaults to 300s.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this ESP32 BLE Hub.

See Also
^^^^^^^^

- :doc:`binary_sensor/esp32_ble`
- :doc:`API Reference </api/misc/esp32_ble_tracker>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/esp32_ble.rst>`__
