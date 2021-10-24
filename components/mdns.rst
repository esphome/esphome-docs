mDNS Component
==============

.. seo::
    :description: Instructions for setting up the MDNS configuration for your ESP node in ESPHome.
    :image: network-wifi.png
    :keywords: WiFi, WLAN, ESP8266, ESP32, MDNS

This core ESPHome component that enables/disables mDNS for you. mDNS is used to find IP address of each ESPHome node. Please note the regarding the consequences of disabling mDNS. Static IP for nodes may be required as well as explicit setting of ping usage in the ESPHome config with the HA addon config.

It’s recommended to leave MDNS enabled. Default is enabled.

.. code-block:: yaml

    # Example configuration entry
    mdns:
      disabled: false
      
.. _mdns-configuration_variables:

Configuration variables:
------------------------

- **disabled** (*Optional*, string): Set to disabled, if you want to prevent mDNS usage.
