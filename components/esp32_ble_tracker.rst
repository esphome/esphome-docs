ESP32 Bluetooth Low Energy Tracker Hub
======================================

.. seo::
    :description: Instructions for setting up ESP32 bluetooth low energy device trackers using ESPHome.
    :image: bluetooth.png

The ``esp32_ble_tracker`` component creates a global hub so that you can track bluetooth low
energy devices using your ESP32 node.

See :ref:`Setting up devices <esp32_ble_tracker-setting_up_devices>`
for information on how you can find out the MAC address of a device and track it using ESPHome.

.. code-block:: yaml

    # Example configuration entry
    esp32_ble_tracker:

    binary_sensor:
      - platform: ble_presence
        mac_address: AC:37:43:77:5F:4C
        name: "ESP32 BLE Presence Google Home Mini"

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

.. note::

    The first time this component is enabled for an ESP32, the code partition needs to be
    resized. Please flash the ESP32 via USB when adding this to your configuration. After that,
    you can use OTA updates again.


Configuration variables:
------------------------


- **scan_parameters** (*Optional*): Advanced parameters for configuring the scan behavior of the ESP32.
  See also `this guide by Texas Instruments <http://dev.ti.com/tirex/content/simplelink_academy_cc2640r2sdk_1_12_01_16/modules/ble_scan_adv_basic/ble_scan_adv_basic.html#scanning>`__
  for reference.

  - **interval** (*Optional*, :ref:`config-time`): The interval between each consecutive scan window.
    This is the time the ESP spends on each of the 3 BLE advertising channels.
    Defaults to ``320ms``.
  - **window** (*Optional*, :ref:`config-time`): The time the ESP is actively listening for packets
    on a channel during each scan interval. If this is close to the ``interval`` value, the ESP will
    spend more time listening to packets (but also consume more power).
  - **duration** (*Optional*, :ref:`config-time`): The duration of each complete scan. This has no real
    impact on the device but can be used to debug the BLE stack. Defaults to ``5min``.
  - **active** (*Optional*, boolean): Whether to actively send scan requests to request more data
    after having received an advertising packet. With some devices this is necessary to receive all data,
    but also drains those devices' power a (tiny) bit more. Defaults to ``true``.

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this ESP32 BLE Hub.

See Also
--------

- :doc:`binary_sensor/ble_presence`
- :apiref:`esp32_ble_tracker/esp32_ble_tracker.h`
- `ESP32 BLE for Arduino <https://github.com/nkolban/ESP32_BLE_Arduino>`__ by `Neil Kolban <https://github.com/nkolban>`__.
- :ghedit:`Edit`
