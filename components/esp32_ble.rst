BLE Component
=============

.. seo::
    :description: Instructions for setting up Bluetooth LE in ESPHome.
    :image: bluetooth.svg

The ``esp32_ble`` component in ESPHome sets up a simple BLE GATT server that exposes the device name,
manufacturer and board.

.. figure:: images/ble-server-example.png
    :align: center
    :width: 70.0%


.. code-block:: yaml

    # Example configuration

    esp32_ble:
      server:


Configuration variables:
------------------------

- **server** (*Optional*): Starts the BLE GATT server

  - **manufacturer** (*Optional*, string): The name of the manufacturer/firmware creator. Defaults to ``ESPHome``.
  - **model** (*Optional*, string): The model name of the device. Defaults to the friendly name of the ``board`` chosen
    in the :ref:`core configuration <esphome-configuration_variables>`.

See Also
--------

- :doc:`wifi`
- :doc:`captive_portal`
- :apiref:`esp32_improv/esp32_improv_component.h`
- :ghedit:`Edit`
