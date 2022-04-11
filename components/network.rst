Network component
=================

.. seo::
    :description:
    :image: network-wifi.svg
    :keywords: Network, WiFi, WLAN, Ethernet, ESP32

The network component is a global configuration for all types of 
networks (WiFi, Ethernet).

.. code-block:: yaml

    # Example configuration
    network:
        enable_ipv6: true
        
Configuration variables:
------------------------

- **enable_ipv6** (*Optional*, boolean): Enables IPv6 support. Defaults to ``false``. Only available on ESP32 with ESP-IDF framework.

