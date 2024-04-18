QESAN BLE Remote
================

.. seo::
    :description: Instructions for receiving QESAN BLE remotes using ESPHome
    :keywords: tuya, qesan, remote, bluetooth, ble, lamp

The ``qesan_ble_remote`` component allows you to receive button presses from BLE remotes that are often used
for tuya lamps.

This component requires the ``esp32_ble_tracker`` component.

To find the address and button codes of your remote, configure the component without specifying any address.
When pressing buttons on the remote the codes will appear in the ESPHome log.

Component/Hub
-------------

.. code-block:: yaml

    # Example configuration entry
    qesan_ble_remote:
      - id: my_remote
        mac_address: 51:45:53:AA:BB:CC
        address: 0x1234

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **id** (**Required**, :ref:`config-id`): The id to use for this component.
- **mac_address** (*Optional*, MAC Address): The MAC address of the remote. Can be found in the ESPHome log. If unspecified, the component reacts to all remotes.
- **address** (*Optional*, int): The 16-bit address of the remote. Can be found in the ESPHome log. If unspecified, the component reacts to all remotes.

Binary Sensor
-------------

.. code-block:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: qesan_ble_remote
        id: my_button
        remote_id: my_remote
        code: 0x7e

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **remote_id** (*Optional*): Manually specify the ID of the qesan_ble_remote instance if there are multiple.
- **code** (**Required**, int): The button code to react to. Can be found in the ESPHome log.
- All options from :ref:`Binary Sensor <config-binary_sensor>`.

See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :ghedit:`Edit`
