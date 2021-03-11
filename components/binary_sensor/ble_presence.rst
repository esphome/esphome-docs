ESP32 Bluetooth Low Energy Device
=================================

.. seo::
    :description: Instructions for setting up BLE binary sensors for the ESP32.
    :image: bluetooth.png

The ``ble_presence`` binary sensor platform lets you track the presence of a
Bluetooth Low Energy device.

.. figure:: images/esp32_ble-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    esp32_ble_tracker:

    binary_sensor:
      # Presence based on MAC address
      - platform: ble_presence
        mac_address: AC:37:43:77:5F:4C
        name: "ESP32 BLE Tracker Google Home Mini"
      # Presence based on BLE Service UUID
      - platform: ble_presence
        service_uuid: '11aa'
        name: "ESP32 BLE Tracker Test Service 16 bit"

.. note::

    Service UUID can be 16 bit long, as in the example, but it can also be 32 bit long
    like ``1122aaff``, or 128 bit long like ``11223344-5566-7788-99aa-bbccddeeff00``.



Configuration variables:
------------------------

-  **name** (**Required**, string): The name of the binary sensor.
-  **mac_address** (*Optional*, MAC Address): The MAC address to track for this
   binary sensor. Either this or ``service_uuid`` has to be present.
-  **service_uuid** (*Optional*, string): 16 bit, 32 bit, or 128 bit BLE Service UUID
   which can be tracked if the device randomizes the MAC address. Either
   this or ``mac_address`` has to be present.
-  **id** (*Optional*, :ref:`config-id`): Manually specify
   the ID used for code generation.
-  All other options from :ref:`Binary Sensor <config-binary_sensor>`.

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

Using the configuration above, first you should see a ``Starting scan...`` debug message at
boot-up. Then, when a BLE device is discovered, you should see messages like
``Found device AC:37:43:77:5F:4C`` together with some information about their
address type and advertised name. If you don't see these messages, your device is unfortunately
currently not supported.

Please note that devices that show a ``RANDOM`` address type in the logs cannot be used for
MAC address based tracking, since their MAC-address periodically changes. Instead you can create
a BLE beacon, set a unique 16 bit, 32 bit or 128 bit Service UUID and track your device based on that.
Make sure you don't pick a `GATT Service UUID <https://www.bluetooth.com/specifications/gatt/services/>`__,
otherwise generic services might give you incorrect tracking results.


See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/binary_sensor/index`
- :apiref:`ble_presence/ble_presence.h`
- `ESP32 BLE for Arduino <https://github.com/nkolban/ESP32_BLE_Arduino>`__ by `Neil Kolban <https://github.com/nkolban>`__.
- :ghedit:`Edit`
