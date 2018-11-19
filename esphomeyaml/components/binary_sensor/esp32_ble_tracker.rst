ESP32 Bluetooth Low Energy Device
=================================

.. seo::
    :description: Instructions for setting up BLE binary sensors for the ESP32.
    :image: bluetooth.png

The ``esp32_ble_tracker`` binary sensor platform lets you track the presence of a
bluetooth low energy device.

.. figure:: images/esp32_ble-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    esp32_ble_tracker:
      scan_interval: 300s

    binary_sensor:
      - platform: esp32_ble_tracker
        mac_address: AC:37:43:77:5F:4C
        name: "ESP32 BLE Tracker Google Home Mini"

Configuration variables:
------------------------

-  **mac_address** (**Required**, MAC Address): The MAC address to track for this
   binary sensor.
-  **name** (**Required**, string): The name of the binary sensor.
-  **id** (*Optional*, :ref:`config-id`): Manually specify
   the ID used for code generation.
-  All other options from :ref:`Binary Sensor <config-binary_sensor>`
   and :ref:`MQTT Component <config-mqtt-component>`.

.. _esp32_ble_tracker-setting_up_devices:

Setting Up Devices
------------------

To set up binary sensors for specific BLE beacons you first have to know which MAC address
to track. Most devices show this screen in some setting menu. If you don't know the MAC address,
however, you can use the ``esp32_ble_tracker`` hub without any binary sensors attached and read through
the logs to see discovered Bluetooth Low Energy devices.

.. code-block:: yaml

    # Example configuration entry for finding MAC addresses
    esp32_ble_tracker:

Using above configuration, first you should see a ``Starting scan...`` debug message at
boot-up. Then, when a BLE device is discovered, you should see messages like
``Found device AC:37:43:77:5F:4C`` together with some information about their
address type and advertised name. If you don't see these messages, your device is unfortunately
currently not supported.

Please note that devices that show a ``RANDOM`` address type in the logs cannot be used for
tracking, since their MAC-address periodically changes.

See Also
--------

- :doc:`/esphomeyaml/components/esp32_ble_tracker`
- :doc:`/esphomeyaml/components/binary_sensor/index`
- :doc:`API Reference </api/misc/esp32_ble_tracker>`
- `ESP32 BLE for Arduino <https://github.com/nkolban/ESP32_BLE_Arduino>`__ by `Neil Kolban <https://github.com/nkolban>`__.
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/binary_sensor/esp32_ble_tracker.rst>`__

.. disqus::
