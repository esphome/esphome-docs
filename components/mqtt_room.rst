MQTT Room Component
===================

.. seo::
    :description: introduction for setting up a MQTT Room component for BLE trackers.
    :image: room_mqtt.svg
    :keywords: ESP32 BLE MQTT

The MQTT Room Component uses the :doc:`/components/esp32_ble_tracker` to track BLE devices and publish that information using the :doc:`/components/mqtt` to Home Assistant.

.. warning::

    This component does not communicate using the native api.
    This means there is some manual configuration required inside Home Assistant to get it working.

.. code-block:: yaml

    # Example configuration entry
    mqtt:
      broker: 10.0.0.2

    esp32_ble_tracker:
      scan_parameters:
        duration: 30s

    mqtt_room:
      room: Living room
      trackers:
        - device_id: ibeacon:11223344-5566-7788-99aa-bbccddeeff00-1-100
          name: My own tracker
          rssi:
            name: My own tracker RSSI
            filters:
              - median:
                  window_size: 3
                  send_every: 1
          distance:
            name: My own tracker distance


.. note::

    It is recommended that you change the scan duration of the :doc:`/components/esp32_ble_tracker` to something lower like 30 seconds.

Configuration variables:
------------------------

- **state_topic** (*Optional*, string): The topic for all the messages. Defaults to ``esphome/rooms``.
- **room** (**Required**, string): The location of the device.
- **trackers** (*Optional*, list): A list of devices to track.

  - **device_id** (**Required**, string): The unique id that identifies your tracker.
  - **name** (*Optional*, string): A name for your tracker. Defaults to the device_id.
  - **signal_power** (*Optional*, number): The transmit power of the tracker, default to -72 or what the device reports.
  - **rssi** (*Optional*): The information for the RSSI sensor.

    - **name** (**Required**, string): The name for the RSSI sensor.
    - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
    - All other options from :ref:`Sensor <config-sensor>`.
  
  - **distance** (*Optional*): The information for the distance sensor.

    - **name** (**Required**, string): The name for the distance sensor.
    - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
    - All other options from :ref:`Sensor <config-sensor>`.

Setting up devices
------------------

To set up a tracker for specific BLE beacons you first have to know which device_id to track.
To find the device_id you can use the ``mqtt_room`` component without any trackers attached and read through the logs to see discovered BLE devices.

.. code-block:: yaml

    # Example configuration entry for finding device_id's
    mqtt:
      broker: 10.0.0.2

    esp32_ble_tracker:
      scan_parameters:
        duration: 30s

    mqtt_room:
      room: Living room

Using the configuration above, you should see messages starting with ``Found device with id:``.
If you don't see these messages, your device is unfortunately currently not supported.

Home Assistant configuration:
-----------------------------

To configure the MQTT Room Component inside Home Assistant you need to add extra code to your ``configuration.yaml``,
for more information go to `MQTT Room Presence <https://www.home-assistant.io/integrations/mqtt_room/>`__.

.. code-block:: yaml

    sensor:
      - platform: mqtt_room
        device_id: ibeacon:11223344-5566-7788-99aa-bbccddeeff00-1-100
        state_topic: esphome/rooms
        name: My own tracker

Using multiple nodes
--------------------

The great with about `MQTT Room Presence <https://www.home-assistant.io/integrations/mqtt_room/>`__ is that you can easily use multiple nodes.
Please make sure that all of your trackers are set up on each node.

A great way to share your trackers between multiple ESPHome nodes is by using :ref:`packages <config-packages>`.

.. code-block:: yaml

    # In config.yaml
    substitutions:
      node_location: Living Room
    
    packages:
      tracker: !include common/tracker.yaml

.. code-block:: yaml

    # In tracker.yaml
    mqtt:
      broker: 10.0.0.2

    esp32_ble_tracker:
      scan_parameters:
        duration: 30s

    mqtt_room:
      room: $node_location
      trackers:
        - device_id: ibeacon:11223344-5566-7788-99aa-bbccddeeff00-1-100
          name: My own tracker

See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/mqtt`
- `MQTT Room Presence <https://www.home-assistant.io/integrations/mqtt_room/>`__
- :apiref:`mqtt_room/mqtt_room.h`
- :ghedit:`Edit`
