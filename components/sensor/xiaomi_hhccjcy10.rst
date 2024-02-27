HHCCJCY10 xiaomi BLE (Pink version)
===================================

Supported Devices
-----------------

HHCCJCY10
*********

MiFlora, tuya (pink) version, measures temperature, moisture, ambient light and nutrient levels in the soil.

.. figure:: images/xiaomi_hhccjcy10.jpg
    :align: center
    :width: 60.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: xiaomi_hhccjcy10
        mac_address: '94:2B:FF:5C:91:61'
        temperature:
          name: "Xiaomi HHCCJCY10 Temperature"
        moisture:
          name: "Xiaomi HHCCJCY10 Moisture"
        illuminance:
          name: "Xiaomi HHCCJCY10 Illuminance"
        conductivity:
          name: "Xiaomi HHCCJCY10 Soil Conductivity"
        battery_level:
          name: "Xiaomi HHCCJCY10 Battery Level"

