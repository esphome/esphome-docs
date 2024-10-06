OpenThread Component
=====================

.. seo::
    :description: Instructions for setting up OpenThread component.
    :image: openthread.png

`Thread <https://www.threadgroup.org>`__ is a low-power mesh networking standard for IoT devices. The low-power aspect is important for battery-powered smart home devices. However, it’s also low-bandwidth, making it ideal for applications that don’t send a lot of data, like switches or motion sensors.

Thread uses the same RF technology as Zigbee (IEEE 802.15.4) but provides IP connectivity similar to Wi-Fi. Unlike Zigbee, Thread by itself does not allow controlling devices: It is just a communication protocol. To control the Thread devices, a higher-level protocol is required: Matter or Apple HomeKit or `ESPHome API </components/api.html>`__ .

The purpose of this component is to allow ESPHome nodes to communicate over a Thread network. It permits the state of sensors and binary sensors to be send to Home Assistant via 6LoWPAN packets. This OpenThread component relies on `OpenThread <https://openthread.io>`__ which is an open-source implementation of Thread.

.. note::

    You will need a `Thread border router <https://www.home-assistant.io/integrations/thread#about-thread-border-routers>`__ to connect your node to a Thread network.


Usage
-----
This component requires an ESP32 (ESP32-C6 or ESP-H2 because they have Thread radio chip) and the use of
ESP-IDF.

.. _config-openthread:


Configuration examples
----------------------

This example show how to configure Thread Dataset for a node.

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

- **channel** (int): Channel number from 11 to 26
- **network_name** (string): A human-readable Network Name
- **network_key** (string): OpenThread network key
- **panid** (string): 2-byte Personal Area Network ID (PAN ID)
- **extpanid** (string): 8-byte Extended Personal Area Network ID (XPAN ID)
- **pskc** (string): PSKc is used to authenticate an external Thread Commissioner to a Thread network

