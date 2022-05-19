ESP32 Bluetooth Low Energy Tracker Hub
======================================

.. seo::
    :description: Instructions for setting up ESP32 bluetooth low energy device trackers using ESPHome.
    :image: bluetooth.svg

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
      - platform: xiaomi_hhccjcy01
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
      - platform: xiaomi_lywsdcgq
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

.. _config-esp32_ble_tracker:

Configuration variables:
------------------------


- **scan_parameters** (*Optional*): Advanced parameters for configuring the scan behavior of the ESP32.
  See also `this guide by Texas Instruments <https://dev.ti.com/tirex/explore/content/simplelink_academy_cc2640r2sdk_5_10_02_00/modules/blestack/ble_scan_adv_basic/ble_scan_adv_basic.html#scanning-basics>`__
  for reference.

  - **interval** (*Optional*, :ref:`config-time`): The interval between each consecutive scan window.
    This is the time the ESP spends on each of the 3 BLE advertising channels.
    Defaults to ``320ms``.
  - **window** (*Optional*, :ref:`config-time`): The time the ESP is actively listening for packets
    on a channel during each scan interval. If this is close to the ``interval`` value, the ESP will
    spend more time listening to packets (but also consume more power). Defaults to ``30ms``
  - **duration** (*Optional*, :ref:`config-time`): The duration of each complete scan. This has no real
    impact on the device but can be used to debug the BLE stack. Defaults to ``5min``.
  - **active** (*Optional*, boolean): Whether to actively send scan requests to request more data
    after having received an advertising packet. With some devices this is necessary to receive all data,
    but also drains those devices' power a (tiny) bit more. Defaults to ``true``.

- **security_parameters** (*Optional*): Advanced parameters for configuring the BLE security behavior of the ESP32.
  See also `this guide by Espressif <https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/bluedroid/ble/gatt_security_server/tutorial/Gatt_Security_Server_Example_Walkthrough.md#setting-security-parameters>`__
  for reference.

  - **io_capability** (*Optional*, :ref:`config-time`): IO Capability of the ESP32. Defaults to ``ESP_IO_CAP_NONE``.
  - **key_size** (*Optional*, int`): Maximum Encryption Key Size, in bytes. Should be between 7~16. Defaults to ``7``
  - **authentication_mode** (*Optional*, :ref:`config-time`): The duration of each complete scan. This has no real
    impact on the device but can be used to debug the BLE stack. Defaults to ``ESP_LE_AUTH_NO_BOND``.

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for this ESP32 BLE Hub.

Automations:

- **on_ble_advertise** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a Bluetooth advertising is received. See :ref:`esp32_ble_tracker-on_ble_advertise`.
- **on_ble_manufacturer_data_advertise** (*Optional*, :ref:`Automation <automation>`): An automation to
  perform when a Bluetooth advertising with manufacturer data is received. See
  :ref:`esp32_ble_tracker-on_ble_manufacturer_data_advertise`.
- **on_ble_service_data_advertise** (*Optional*, :ref:`Automation <automation>`): An automation to
  perform when a Bluetooth advertising with service data is received. See
  :ref:`esp32_ble_tracker-on_ble_service_data_advertise`.

ESP32 Bluetooth Low Energy Tracker Security
-------------------------------------------

.. note::

    Modifying the BLE Tracker Security Parameters is an advanced option that is likely to only be required when connecting to BLE Devices with specific authentication requirements.
    Learn all about ESP32 BLE `Security Parameters here <https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/bluedroid/ble/gatt_security_server/tutorial/Gatt_Security_Server_Example_Walkthrough.md#setting-security-parameters>`__

**BLE IO Capability**: describes if the device has input/output capabilities such as a display or a keyboard:

``io_capability`` possible options:

- ``ESP_IO_CAP_OUT`` (0, Display Only)
- ``ESP_IO_CAP_IO`` (1, Display Yes/No)
- ``ESP_IO_CAP_IN`` (2, Keyboard Only)
- ``ESP_IO_CAP_NONE`` (3, No Input, No Output (default))
- ``ESP_IO_CAP_KBDISP`` (4, Keyboard display)

**BLE Authorization Request**: indicates the requested security properties such as Bonding, Secure Connections (SC), MITM protection or none that will be present in the Pairing Request and Response packets:

``authentication_mode`` possible options:

- ``ESP_LE_AUTH_NO_BOND``: No bonding.
- ``ESP_LE_AUTH_BOND``: Bonding is performed.
- ``ESP_LE_AUTH_REQ_MITM``: MITM Protection is enabled.
- ``ESP_LE_AUTH_REQ_SC_ONLY``: Secure Connections without bonding enabled.
- ``ESP_LE_AUTH_REQ_SC_BOND``: Secure Connections with bonding enabled.
- ``ESP_LE_AUTH_REQ_SC_MITM``: Secure Connections with MITM Protection and no bonding enabled.
- ``ESP_LE_AUTH_REQ_SC_MITM_BOND``: Secure Connections with MITM Protection and bonding enabled.

ESP32 Bluetooth Low Energy Tracker Automation
---------------------------------------------

.. _esp32_ble_tracker-on_ble_advertise:

``on_ble_advertise``
********************

This automation will be triggered when a Bluetooth advertising is received. A variable ``x`` of type
:apiclass:`esp32_ble_tracker::ESPBTDevice` is passed to the automation for use in lambdas.

.. code-block:: yaml

    esp32_ble_tracker:
      on_ble_advertise:
        - mac_address: 11:22:33:44:55:66
          then:
            - lambda: |-
                ESP_LOGD("ble_adv", "New BLE device");
                ESP_LOGD("ble_adv", "  address: %s", x.address_str().c_str());
                ESP_LOGD("ble_adv", "  name: %s", x.get_name().c_str());
                ESP_LOGD("ble_adv", "  Advertised service UUIDs:");
                for (auto uuid : x.get_service_uuids()) {
                    ESP_LOGD("ble_adv", "    - %s", uuid.to_string().c_str());
                }
                ESP_LOGD("ble_adv", "  Advertised service data:");
                for (auto data : x.get_service_datas()) {
                    ESP_LOGD("ble_adv", "    - %s: (length %i)", data.uuid.to_string().c_str(), data.data.size());
                }
                ESP_LOGD("ble_adv", "  Advertised manufacturer data:");
                for (auto data : x.get_manufacturer_datas()) {
                    ESP_LOGD("ble_adv", "    - %s: (length %i)", data.uuid.to_string().c_str(), data.data.size());
                }

Configuration variables:

- **mac_address** (*Optional*, MAC Address): The MAC address to filter for this automation.
- See :ref:`Automation <automation>`.

.. _esp32_ble_tracker-on_ble_manufacturer_data_advertise:

``on_ble_manufacturer_data_advertise``
**************************************

This automation will be triggered when a Bluetooth advertising with manufcaturer data is received. A
variable ``x`` of type ``std::vector<uint8_t>`` is passed to the automation for use in lambdas.

.. code-block:: yaml

    sensor:
      - platform: template
        name: "BLE Sensor"
        id: ble_sensor

    esp32_ble_tracker:
      on_ble_manufacturer_data_advertise:
        - mac_address: 11:22:33:44:55:66
          manufacturer_id: 0590
          then:
            - lambda: |-
                if (x[0] != 0x7b || x[1] != 0x61) return;
                int value = x[2] + (x[3] << 8);
                id(ble_sensor).publish_state(value);

Configuration variables:

- **mac_address** (*Optional*, MAC Address): The MAC address to filter for this automation.
- **manufacturer_id** (**Required**, string): 16 bit, 32 bit, or 128 bit BLE Manufacturer ID.
- See :ref:`Automation <automation>`.

.. _esp32_ble_tracker-on_ble_service_data_advertise:

``on_ble_service_data_advertise``
*********************************

This automation will be triggered when a Bluetooth advertising with service data is received. A
variable ``x`` of type ``std::vector<uint8_t>`` is passed to the automation for use in lambdas.

.. code-block:: yaml

    sensor:
      - platform: template
        name: "BLE Sensor"
        id: ble_sensor

    esp32_ble_tracker:
      on_ble_service_data_advertise:
        - mac_address: 11:22:33:44:55:66
          service_uuid: 181A
          then:
            - lambda: 'id(ble_sensor).publish_state(x[0]);'

Configuration variables:

- **mac_address** (*Optional*, MAC Address): The MAC address to filter for this automation.
- **service_uuid** (**Required**, string): 16 bit, 32 bit, or 128 bit BLE Service UUID.
- See :ref:`Automation <automation>`.

See Also
--------

- :doc:`binary_sensor/ble_presence`
- :apiref:`esp32_ble_tracker/esp32_ble_tracker.h`
- `ESP32 BLE for Arduino <https://github.com/nkolban/ESP32_BLE_Arduino>`__ by `Neil Kolban <https://github.com/nkolban>`__.
- :ghedit:`Edit`
