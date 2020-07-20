BLE Button
==========

.. seo::
    :description: Receive events from a cheap BLE keyring button.
    :image: bluetooth.svg

The ``ble_button`` binary sensor platform creates a binary sensor based on
a cheap BLE keyring tag's button. It requires an ESP32 and to have the
:doc:`/components/ble_client` component configured with the MAC address
of the tag.

.. figure:: images/esp32_ble_itag.png
    :align: center
    :width: 40%


Configuration variables:
------------------------

.. code-block:: yaml

  # Example configuration entry
  esp32_ble_tracker:

  ble_client:
    - mac_address: FF:FF:20:00:0F:15
      id: itag_black

  binary_sensor:
    - platform: ble_button
      ble_client_id: itag_black
      name: "Black iTag Button"

- **ble_client_id** (**Required**, :ref:`config-id`): The ID of the ``ble_client`` for the tag.
- **name** (**Required**, string): The name of the binary sensor.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.


Usage
-----
Once the device is connected, a button press will send a sensor ON event immediately
followed by an OFF. Being a regular binary sensor, you can create automations from
it to perform other tasks, for example with ``on_press:...``

As the component immediately sends a state OFF after the ON, you may wish to delay the
OFF to give some automations a chance to see the event:

.. code-block:: yaml

  binary_sensor:
    - platform: ble_button
      ble_client_id: itag_black
      id: itag_black_button
      filters:
        - delayed_off: 200ms


See Also
--------

- :doc:`/components/ble_client`
- :doc:`/components/binary_sensor/index`
- :apiref:`ble_button/ble_button.h`
- :ghedit:`Edit`
