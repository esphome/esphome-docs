ESP32 Bluetooth Classic Component
=================================

.. seo::
    :description: Instructions for setting up Bluetooth Classic in ESPHome.
    :image: bluetooth.svg

The ``esp32_bt_classic`` component in ESPHome sets up the Bluetooth Classic stack on the device as a backend for :doc:`/components/binary_sensor/bt_classic_presence` sensors.

.. code-block:: yaml

    # Example configuration

    esp32_bt_classic:
      on_scan_start:
        # Enable LED while scanning for BT devices
        - light.turn_on:
            id: state_led
      on_scan_result:
        # Can listen for ANY scan result:
        - then:
          # Send custom event to HomeAssistant
          - homeassistant.event:
              event: esphome.bt_scan_result
              data:
                node: "ESP32-Hallway"
                status: !lambda "return status.str();"
                name: !lambda "return name;"
                address: !lambda "return address.str();"
          - light.turn_off:
              id: state_led
       # Can listen for specific MAC addresses:
       - mac_address:
           - AA:BB:CC:DD:EE:F0
           - AA:BB:CC:DD:EE:F2
         then:
           lambda: |-
             ESP_LOGI("BT_SCAN_RESULT", "Result for one of the Watches!\n  address: %s\n  name: %s\n  status: %s (%d)", address.c_str(), name, status.c_str(), status.bt_status());


.. _config-esp32_bt_classic:

Configuration variables:
------------------------

Automations:

- **on_scan_start** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a Bluetooth scan has started.
- **on_scan_result** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a Bluetooth scan result arrives. See :ref:`esp32_bt_classic-on_scan_result`.


ESP32 Bluetooth Classic Automations
---------------------------------------------

.. _esp32_bt_classic-on_scan_result:

``on_scan_result`` Trigger
************************************************

This automation will be triggered when a Bluetooth scan result arrives. The following variables are passed to the automation for use in lambdas: ``address`` of type :apiclass:`esp32_bt_classic::BtAddress`, ``status`` of type :apiclass:`esp32_bt_classic::BtStatus`, and ``name`` of type ``const char*``.

.. code-block:: yaml

    esp32_bt_classic:
      on_scan_result:
        - then:
            - lambda: |-
                ESP_LOGD("BT_SCAN_RESULT", "This is not the device you're looking for:\n  address: %s\n  name: %s\n  status: %s (%d)", address.c_str(), name, status.c_str(), status.bt_status());
        - mac_address: 11:22:33:44:55:66
          then:
            - lambda: |-
                ESP_LOGD("BT_SCAN_RESULT", "Found the device you're looking for!");
                ESP_LOGD("BT_SCAN_RESULT", "  address: %s", address.c_str());
                ESP_LOGD("BT_SCAN_RESULT", "  name: %s", name);
                ESP_LOGD("BT_SCAN_RESULT", "  status: %s (%d)", status.c_str(), status.bt_status());

Configuration variables:

- **mac_address** (*Optional*, MAC Address): The MAC address to filter for this automation.
- See :ref:`Automation <automation>`.


``bt_classic.bt_classic_scan`` Action
************************************************

Start a Bluetooth scan. If there is a scan already in progress, then the scan request is queued. 
This Action may be particularly useful as a user-defined service (See :ref:`api-services`), in combination with a :ref:`homeassistant.event <api-homeassistant_event_action>` hooked up to an ``on_scan_result`` trigger.


.. code-block:: yaml

    esp32_bt_classic:

    # Use with any generic Trigger: 
    on_...:
      - bt_classic.bt_classic_scan:

    # Home assistant service example:
    api:
      services:
        - service: scan_bt_devices
          variables:
            addresses: string[]
            num_scans: int
          then:
            - bt_classic.bt_classic_scan:
                mac_address: !lambda "return addresses;"
                num_scans: !lambda "return num_scans;"

Configuration variables:

- **mac_address** (**Required**, List of MAC Addresses, :ref:`templatable <config-templatable>`): The MAC addresses to scan. For templates accepts a ``std::vector<std::string>``. Any non MAC address entry is ignored.
- **num_scans** (*optional*, int, :ref:`templatable <config-templatable>`): Number of scans performed to find the device. Defaults to ``1``.

See Also
--------

- :doc:`/components/binary_sensor/bt_classic_presence`
- :apiref:`esp32_bt_classic/bt_classic.h`
- :ghedit:`Edit`
