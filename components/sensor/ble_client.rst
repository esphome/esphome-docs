BLE Client Sensor
=================

.. seo::
    :description: Fetch numeric values from BLE devices.
    :image: bluetooth.svg

The ``ble_client`` component is a sensor platform that can
query BLE devices for specific values of service characteristics.

For more information on BLE services and characteristics, see
:doc:`/components/ble_client`.

.. code-block:: yaml

    esp32_ble_tracker:

    ble_client:
      - mac_address: FF:FF:20:00:0F:15
        id: itag_black

    sensor:
      - platform: ble_client
        ble_client_id: itag_black
        name: "iTag battery level"
        service_uuid: '180f'
        characteristic_uuid: '2a19'
        icon: 'mdi:battery'
        unit_of_measurement: '%'

Configuration variables:
------------------------

- **ble_client_id** (**Required**, :ref:`config-id`): ID of the associated BLE client.
- **service_uuid** (**Required**, UUID): UUID of the service on the device.
- **characteristic_uuid** (**Required**, UUID): UUID of the service's characteristic to query.
- **descriptor_uuid** (*Optional*, UUID): UUID of the characteristic's descriptor to query.
- **id** (*Optional*, :ref:`config-id`): The ID to use for code generation, and for reference by dependent components.
- **lambda** (*Optional*, :ref:`config-lambda`): The lambda to use for converting a raw data
  reading to a sensor value. See :ref:`ble-sensor-lambda` for more information.
- **notify** (*Optional*, boolean): Instruct the server to send notifications for this
  characteristic.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to poll the device.
- All other options from :ref:`Sensor <config-sensor>`.

Automations:

- **on_notify** (*Optional*, :ref:`Automation <automation>`): An automation to
  perform when a notify message is received from the device. See :ref:`ble_sensor-on_notify`.

.. _ble-sensor-lambda:

Raw Data Parsing Lambda
-----------------------

By default only the first byte of each message received on the service's characteristic is used
for the sensor reading. For more complex messages, this behavior can be overridden by a custom
lambda function to parse the raw data. The received data bytes are passed to the lambda as a
variable ``x`` of type ``std::vector<uint8_t>``. The function must return a single ``float`` value.

.. code-block:: yaml

    ...

    sensor:
      - platform: ble_client
        ble_client_id: t_sensor
        name: "Temperature Sensor 32bit float"
        ...
        device_class: "temperature"
        lambda: |-
          return *((float*)(&x[0]));


BLE Sensor Automation
---------------------

.. _ble_sensor-on_notify:

``on_notify``
*************

This automation is triggered when the device/server sends a notify message for
a characteristic. The config variable *notify* must be true or this will have
no effect.
A variable ``x`` of type ``float`` is passed to the automation for use in lambdas.

Example UUIDs
-------------
The UUIDs available on a device are dependent on the type of
device and the functionality made available. Check the ESPHome
device logs for those that are found on the device.

Some common ones:

+----------+------------------+-----------------------+
| Service  | Characteristic   | Description           |
+==========+==================+=======================+
| 180F     | 2A19             | Battery level         |
+----------+------------------+-----------------------+
| 181A     | 2A6F             | Humidity              |
+----------+------------------+-----------------------+


See Also
--------

- :doc:`/components/ble_client`
- :ref:`sensor-filters`
- :apiref:`ble_sensor/ble_sensor.h`
- :ghedit:`Edit`
