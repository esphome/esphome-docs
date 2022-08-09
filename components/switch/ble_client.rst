BLE Client Switch
=================

.. esphome:component-definition::
   :alias: ble-client
   :category: switch-components
   :friendly_name: BLE Client Switch
   :toc_group: Switch Components
   :toc_image: bluetooth.svg

.. seo::
    :description: Control the state of BLE clients.
    :image: bluetooth.svg

The ``ble_client`` component is a switch platform that is used to enable
and disable a ``ble_client``. This has several uses, such as minimizing
battery usage or for allowing other clients (Eg phone apps) to connect to
the device.

For more information on BLE services and characteristics, see
:doc:`/components/ble_client`.

.. code-block:: yaml

    esp32_ble_tracker:

    ble_client:
      - mac_address: FF:FF:20:00:0F:15
        id: itag_black

    switch:
      - platform: ble_client
        ble_client_id: itag_black
        name: "Enable iTag"

Configuration variables:
------------------------

- **ble_client_id** (**Required**, :ref:`config-id`): ID of the associated BLE client.
- **id** (*Optional*, :ref:`config-id`): The ID to use for code generation, and for reference by dependent components.
- All other options from :ref:`Switch <config-switch>`.

See Also
--------

- :doc:`/components/ble_client`
- :apiref:`ble_client/switch/ble_switch.h`
- :ghedit:`Edit`
