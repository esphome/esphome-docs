Xiaomi Miscale Sensors
========================

.. seo::
    :description: Instructions for setting up Xiaomi Miscale bluetooth-based sensors in ESPHome.
    :image: xiaomi_miscale.jpg
    :keywords: Xiaomi, BLE, Bluetooth, XMTZC01HM, XMTZC04HM

The ``xiaomi_miscale`` sensor platform lets you track the output of Xiaomi Bluetooth Low Energy devices using the :doc:`/components/esp32_ble_tracker`. This component will track, for example, the weight of the device every time the sensor sends out a BLE broadcast. Contrary to other implementations, ``xiaomi_miscale`` listense passively to advertisement packets and does not pair with the device. Hence ESPHome has no impact on battery life.

Supported Devices
-----------------

XMTZC01HM, XMTZC04HM
*********

Micale measures weight.

.. figure:: images/xiaomi_miscale.jpg
    :align: center
    :width: 60.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: xiaomi_miscale
        mac_address: 'C8:47:8C:9F:7B:0A'
        weight:
          name: "Xiaomi Mi Scale Weight"


See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/sensor/index`
- bodymiscale score integration for Home Assistant (bodymiscale custom component) `<https://github.com/dckiller51/bodymiscale>`__

- :ghedit:`Edit`
