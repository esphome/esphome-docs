OpenThread Component
=====================

.. seo::
    :description: Instructions for setting up OpenThread component.
    :image: folder-open.svg

[OpenThread](https://openthread.io/) component.

.. _config-openthread:

Base Text Sensor Configuration
------------------------------

[OpenThread](https://openthread.io/) component.

.. code-block:: yaml

    # Example OpenThread component configuration
    network:
      enable_ipv6: true
    
    openthread:
      channel: 13
      network_name: OpenThread-8f28
      network_key: dfd34f0f05cad978ec4e32b0413038ff
      panid: 0x8f28
      extpanid: d63e8e3e495ebbc3
      pskc: c23a76e98f1a6483639b1ac1271e2e27

Configuration variables:

- **channel** (int): Manually set the icon to use for the sensor in the frontend.
- **network_name** (string): OpenThread network name
- **network_key** (string): OpenThread network key
- **panid** (int): TODO
- **extpanid** (int): TODO
- **pskc** (string): OpenThread pskc: the PSKc is used to authenticate an external Thread Commissioner to a Thread network.

