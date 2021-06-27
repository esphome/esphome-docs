BLE Server
==========

.. seo::
    :description: Instructions for setting up Bluetooth LE GATT Server in ESPHome.
    :image: bluetooth.svg

The ``esp32_ble_server`` component in ESPHome sets up a simple BLE GATT server that exposes the device name,
manufacturer and board. This component allows other components to create their own services to expose
data and control.

.. code-block:: yaml

    # Example configuration

    esp32_ble_server:


Configuration variables:
------------------------

- **manufacturer** (*Optional*, string): The name of the manufacturer/firmware creator. Defaults to ``ESPHome``.
- **model** (*Optional*, string): The model name of the device. Defaults to the friendly name of the ``board`` chosen
  in the :ref:`core configuration <esphome-configuration_variables>`.

See Also
--------

- :doc:`esp32_ble`
- :doc:`esp32_improv`
- :apiref:`esp32_ble/ble.h`
- :ghedit:`Edit`
