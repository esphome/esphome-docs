ESP32 Bluetooth Low Energy Device
=================================

The ``esp32_ble`` binary sensor platform lets you track the presence of a
bluetooth low energy device.

.. note::

    See the `ESP32 BLE Hub Page </esphomeyaml/components/esp32_ble.html>`__ for
    current limitations of this platform

|image0|

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

-  **mac_address** (**Required**, MAC Address): The MAC address to track for this
   binary sensor.
-  **name** (**Required**, string): The name of the binary sensor.
-  **id** (*Optional*,
   `id </esphomeyaml/configuration-types.html#id>`__): Manually specify
   the ID used for code generation.
-  All other options from `Binary
   Sensor </esphomeyaml/components/binary_sensor/index.html#base-binary-sensor-configuration>`__
   and `MQTT
   Component </esphomeyaml/components/mqtt.html#mqtt-component-base-configuration>`__.

Setting Up Devices
~~~~~~~~~~~~~~~~~~

To set up binary sensors for specific BLE beacons you first have to know which MAC address
to track. Most devices show this screen in some setting menu. If you don't know the MAC address,
however, you can use the ``esp32_ble`` hub without any binary sensors attached and read through
the logs to see discovered Bluetooth Low Energy devices.

.. code:: yaml

    # Example configuration entry for finding MAC addresses
    esp32_ble:

Using above configuration, first you should see a ``Starting scan...`` debug message at
boot-up. Then, when a BLE device is discovered, you should see messages like
``Found device AC:37:43:77:5F:4C RSSI=-80`` together with some information about their
address type and advertised name. If you don't see these messages, your device is unfortunately
currently not supported.

Please note that devices that show a ``RANDOM`` address type in the logs cannot be used for
tracking, since their MAC-address periodically changes.


.. |image0| image:: /esphomeyaml/components/binary_sensor/esp32_ble.png
    :class: align-center
    :width: 80.0%
