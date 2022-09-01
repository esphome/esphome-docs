MQTT Room Component
===================

.. seo::
    :description: introduction for setting up a MQTT Room component for BLE trackers.
    :keywords: ESP32 BLE MQTT

The MQTT Room Component uses the :doc:`/components/esp32_ble_tracker` and :doc:`/components/sensor/ble_rssi` to track BLE devices and publish that information using MQTT to Home Assistant.

.. warning::

    This component does not communicates using the native api.
    This means there is some manual configuration required inside Home Assistant to get it working.

.. code-block:: yaml

  # Example configuration entry
  sensor:
    - platform: ble_rssi
      ibeacon_uuid: '11223344-5566-7788-99aa-bbccddeeff00'
      id: tracker_rssi

  mqtt_room:
    room: Living room
    trackers:
      - device_id: tracker_rssi
        name: My own tracker

.. note::

    It is recommended that you change the scan duration of the :doc:`/components/esp32_ble_tracker` to something lower like 30 seconds.

Configuration variables:
------------------------

- **state_topic** (*Optional*, string): The topic for all the messages. Defaults to ``esphome/rooms``.
- **room** (**Required**, string): The location of the device.
- **trackers** (**Required**, list): A list of trackers to follow and publish messages of.

  - **device_id** (**Required**, ble_rssi): The ble_rssi sensor for the tracker.
  - **name** (*Optional*, string): A name for your tracker. Default to the id.

Home Assistant configuration:
-----------------------------

To configure the MQTT Room Component inside Home Assistant you need to add extra code to your ``configuration.yaml``,
for more information goto `MQTT Room Presence <https://www.home-assistant.io/integrations/mqtt_room/>`__.

.. code-block:: yaml

    sensor:
      - platform: mqtt_room
        device_id: tracker_rssi
        state_topic: esphome/rooms
        name: My own tracker

See Also
--------

- :doc:`/components/sensor/ble_rssi`
- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/mqtt`
- `MQTT Room Presence <https://www.home-assistant.io/integrations/mqtt_room/>`__
- :apiref:`mqtt_room/mqtt_room.h`
- :ghedit:`Edit`
