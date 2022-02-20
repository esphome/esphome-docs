mDNS Component
==============

.. seo::
    :description: Instructions for setting up the mDNS configuration for your ESP node in ESPHome.
    :image: radio-tower.svg
    :keywords: WiFi, WLAN, ESP8266, ESP32, mDNS

The ``mdns`` component makes the node announce itself on the local network using the multicast DNS (mDNS) protocol.

Both Home Assistant and the ESPHome dashboard use mDNS to identify the IP address of all ESPHome nodes on the network.
If mDNS is disabled, they will no longer be able to automatically find your devices. It may be necessary to use a static
IP for all nodes and to enable the ping option in the Home Assistant add-on.

It is recommended to leave mDNS enabled.

.. code-block:: yaml

    # Example configuration entry
    mdns:
      disabled: false

.. _mdns-configuration_variables:

Configuration variables:
------------------------

- **disabled** (*Optional*, boolean): Set to true to disable mDNS usage. Defaults to false.

See Also
--------

- :ghsources:`esphome/components/mdns`
- :ghedit:`Edit`
