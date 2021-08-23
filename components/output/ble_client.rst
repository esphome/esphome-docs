BLE Client Binary Output
========================

.. seo::
    :description: Writes a binary value to a BLE device.
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

    output:
      - platform: ble_client
        ble_client_id: itag_black
        service_uuid: "10110000-5354-4F52-5A26-4249434B454C"
        characteristic_uuid: "10110013-5354-4f52-5a26-4249434b454c"

Configuration variables:
------------------------

- **ble_client_id** (**Required**, :ref:`config-id`): ID of the associated BLE client.
- **service_uuid** (**Required**, UUID): UUID of the service on the device.
- **characteristic_uuid** (**Required**, UUID): UUID of the service's characteristic to write to.
- **id** (*Optional*, :ref:`config-id`): The ID to use for code generation, and for reference by dependent components.
- All other options from :ref:`Output <config-output>`.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/ble_client`
- :ghedit:`Edit`
