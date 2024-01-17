Smart Config
==============

.. seo::
    :description: Instructions for setting up Wifi via SmartConfig in ESPHome.
    :image: smartconfig.png

The SmartConfig is a provisioning technology developed by TI to connect a new Wi-Fi device to a Wi-Fi network. It uses a mobile application to broadcast the network credentials from a smartphone, or a tablet, to an un-provisioned Wi-Fi device
The `smartconfig` component in ESPHome implements the smartconfig standard for configuring Wi-Fi on an ESP32/ESP8266 device.

.. code-block:: yaml

    # Example configuration entry
    wifi:
      # ...

    smartconfig:
      on_ready:
        - logger.log: "SmartConfig is ready"


Configuration variables:
------------------------

- **on_ready** (*Optional*, :ref:`Automation <automation>`): An action to be performed when smartconfig is ready.

See Also
--------

- :doc:`wifi`
- :doc:`improv_serial`
- :doc:`captive_portal`
- :apiref:`smartconfig/smartconfig_component.h`
- :ghedit:`Edit`
