ESP32 Bluetooth Classic Presence
================================

.. seo::
    :description: Instructions for setting up BT Classic binary sensors for the ESP32.
    :image: bluetooth.svg

The ``bt_classic_presence`` binary sensor platform lets you poll the presence of a Bluetooth Classic device.

.. code-block:: yaml

    # Example configuration entry
    esp32_bt_classic:

    binary_sensor:
      - platform: bt_classic_presence
        mac_address: 61:73:9f:ca:16:e9
        name: "Smartwatch Presence"
        num_scans: 5
        update_interval: 60s


Configuration variables:
------------------------

-  **name** (**Required**, string): The name of the binary sensor.
-  **mac_address** (**Required**, MAC Address): The MAC address to track for this binary sensor.
-  **num_scans** (*optional*, int): Number of scans performed to find the device. When not found after these attemtpts the device is marked absent. Defaults to ``1``.
-  **update_interval** (*Optional*, :ref:`config-time`): Interval at which presence for this device is scanned. Defaults to ``5min``.
-  **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
-  All other options from :ref:`Binary Sensor <config-binary_sensor>`.


See Also
--------

- :doc:`/components/esp32_bt_classic`
- :doc:`/components/binary_sensor/index`
- :apiref:`bt_classic_presence/bt_classic_presence_device.h`
- :ghedit:`Edit`
