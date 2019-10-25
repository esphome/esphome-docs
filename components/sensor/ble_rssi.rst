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
      - platform: ble_rssi
        service_uuid: '11aa'
        name: "BLE Test Service 16 bit RSSI value"
      - platform: ble_rssi
        service_uuid: '11aa11aa'
        name: "BLE Test Service 32 bit RSSI value"
      - platform: ble_rssi
        service_uuid: '11223344-5566-7788-99aa-bbccddeeff00'
        name: "BLE Test Service 128 bit RSSI value"

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **mac_address** (*Optional*, MAC Address): The MAC address to track for this
  sensor. Either this or **service_uuid** has to be present.
- **service_uuid** (*Optional*, 16 bit, 32 bit, or 128 bit BLE Service UUID): The BLE
  Service UUID which can be tracked if the device randomizes the MAC address. Either
  this or **mac_address** has to be present.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/sensor/index`
- :apiref:`ble_rssi/ble_rssi_sensor.h`
- :ghedit:`Edit`
