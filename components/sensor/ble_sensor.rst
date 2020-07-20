BLE Sensor
==========

.. seo::
    :description: Fetch numeric values from BLE devices.
    :image: bluetooth.svg

The ``ble_sensor`` component is a sensor platform that can
query BLE devices for specific values of service characteristics.

For more information on BLE services and characteristics, see
:doc:`/components/ble_client`.

.. code-block:: yaml

  esp32_ble_tracker:

  ble_client:
    - mac_address: FF:FF:20:00:0F:15
      id: itag_black

  sensor:
    ble_client_id: itag_black
    name: "iTag battery level"
    service_uuid: '180f'
    char_uuid: '2a19'
    icon: 'mdi:battery'
    unit_of_measurement: '%'

Configuration variables:
------------------------

- **ble_client_id** (**Required**, :ref:`config-id`): ID of the associated BLE client.
- **id** (**Required**, :ref:`config-id`): The ID to use for code generation, and for reference by dependent components.
- **service_uuid** (**Required**, UUID): UUID of the service on the device.
- **char_uuid** (**Required**, UUID): UUID of the service's characteristic to query.
- **descr_uuid** (*Optional*, UUID): UUID of the characteristic's descriptor to query.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to poll the device.
- All other options from :ref:`Sensor <config-sensor>`.

Example UUIDs
-------------
The UUIDs available on a device are dependent on the type of
device and the functionality made available. Check the ESPHome
device logs for those that are found on the device.

Some common ones:

+----------+--------+-----------------------+
| Service  | Char   | Description           |
+==========+========+=======================+
| 180F     | 2A19   | Battery level         |
+----------+--------+-----------------------+
| 181A     | 2A6F   | Humidity              |
+----------+--------+-----------------------+


See Also
--------

- :doc:`/components/ble_client`
- :ref:`sensor-filters`
- :apiref:`ble_sensor/ble_sensor.h`
- :ghedit:`Edit`
