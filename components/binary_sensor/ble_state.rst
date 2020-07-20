BLE State
==========

.. seo::
    :description: Expose the connection state to a BLE device.
    :image: bluetooth.svg

The ``ble_state`` binary sensor platform creates a binary sensor based on
the connection state to a BLE device. It requires an ESP32 and to have the
:doc:`/components/ble_client` component configured with the MAC address
of the desired device.

Configuration variables:
------------------------

.. code-block:: yaml

  # Example configuration entry
  esp32_ble_tracker:

  ble_client:
    - mac_address: FF:FF:20:00:0F:15
      id: itag_black

  binary_sensor:
    - platform: ble_state
      ble_client_id: itag_black
      name: "Black iTag"

- **ble_client_id** (**Required**, :ref:`config-id`): The ID of the ``ble_client`` for the device.
- **name** (**Required**, string): The name of the binary sensor.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.


Usage
-----
Once the device is connected, the binary sensor will have the state ON. Conversely
when disconnected, the state will be OFF. As it is a ``binary_sensor``, you can use
automations to take actions upon these events.

See Also
--------

- :doc:`/components/ble_client`
- :doc:`/components/binary_sensor/index`
- :apiref:`ble_state/ble_state.h`
- :ghedit:`Edit`
