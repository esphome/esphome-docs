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
        min_ipv6_addr_count: 2
        
Configuration variables:
------------------------

- **enable_ipv6** (*Optional*, boolean): Enables IPv6 support. Defaults to ``false``.
- **min_ipv6_addr_count** (*Optional*, integer): ESPhome considers network connected when it has gotten one IPv4 address and this amount of IPv6 addresses. Defaults to ``0`` to not hang on boot with networks with no IPv6 enabled. ``2`` could be a good value for a configuration that requires IPv6.

See Also
--------

- :doc:`/components/wifi`
- :doc:`/components/ethernet`
- :ghedit:`Edit`
