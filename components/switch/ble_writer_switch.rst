BLE Writer Switch
=================

.. seo::
    :description: A switch that triggers a write to a specified BLE characteristic
    :image: bluetooth.svg

The ``ble_writer_switch`` component is a switch platform that triggers a write to a BLE characteristic when toggled.

It depends on :doc:`/components/ble_client`.

.. code-block:: yaml

    # Example config.yaml
    esp32_ble_tracker:

    ble_client:
      - mac_address: DD:B6:AF:13:23:A8
        id: ble_client_id

    switch:
      - platform: ble_writer_switch
        ble_client_id: ble_client_id
        name: "BLE Writer Switch"
        service_uuid: F61E3BE9-2826-A81B-970A-4D4DECFABBAE
        characteristic_uuid: 6490FAFE-0734-732C-8705-91B653A081FC

Configuration variables:
------------------------

- **ble_client_id** (**Required**, :ref:`config-id`): ID of the associated BLE client.
- **service_uuid** (**Required**, UUID): UUID of the service on the device.
- **characteristic_uuid** (**Required**, UUID): UUID of the service's characteristic to query.
- **descriptor_uuid** (*Optional*, UUID): UUID of the characteristic's descriptor to query.
- All other options from :ref:`Switch <config-switch>`.

See Also
--------

- :doc:`/components/ble_client`
- :ghedit:`Edit`
