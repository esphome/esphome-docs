OpenThread Component
=====================

.. seo::
    :description: Instructions for setting up [OpenThread](https://openthread.io/) component.
    :image: folder-open.svg

Text sensors are a lot like normal :doc:`sensors </components/sensor/index>`.
But where the "normal" sensors only represent sensors that output **numbers**, this
component can represent any *text*.

.. _config-text_sensor:

Base Text Sensor Configuration
------------------------------

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

- **id** (*Optional*, string): Manually specify the ID for code generation. At least one of **id** and **name** must be specified.
- **name** (*Optional*, string): The name for the sensor. At least one of **id** and **name** must be specified.

  .. note::

      If you have a :ref:`friendly_name <esphome-configuration_variables>` set for your device and
      you want the text sensor to use that name, you can set ``name: None``.

- **channel** (*Optional*, icon): Manually set the icon to use for the sensor in the frontend.
- **network_name** (*Optional*, string): TODO
- **network_key** (*Optional*, boolean): TODO
- **panid** (*Optional*, boolean): TODO
- **extpanid** (*Optional*, boolean): TODO
- **pskc** (*Optional*, boolean): OpenThread pskc. The PSKc is used to authenticate an external Thread Commissioner to a Thread network.

