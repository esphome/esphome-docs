Xiaomi Miscale Sensors
========================

.. seo::
    :description: Instructions for setting up Xiaomi Miscale bluetooth-based sensors in ESPHome.
    :image: xiaomi_miscale.jpg
    :keywords: Xiaomi, BLE, Bluetooth, XMTZC01HM, XMTZC04HM

The ``xiaomi_miscale`` sensor platform lets you track the output of Xiaomi Bluetooth Low Energy devices using the :doc:`/components/esp32_ble_tracker`. This component will track, for example, the weight of the device every time the sensor sends out a BLE broadcast. Contrary to other implementations, ``xiaomi_miscale`` listens passively to advertisement packets and does not pair with the device. Hence ESPHome has no impact on battery life.

To get the body scores using your weight, height, age and gender see the custom_components `<https://github.com/dckiller51/bodymiscale>`__

Supported Devices
-----------------

XMTZC01HM, XMTZC04HM
********************

Miscale measures weight.

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

Configuration example with multiple users :

You have to replace the numbers in the lambdas to determine your weight which is between X weight and X weight.

.. code-block:: yaml

    sensor:
      - platform: xiaomi_miscale
        mac_address: 'C8:47:8C:9F:7B:0A'
        weight:
          name: "Xiaomi Mi Scale Weight"
          id: weight_miscale
          on_value:
            then:
              - lambda: |-
                  if (id(weight_miscale).state >= 69 && id(weight_miscale).state <= 74.49) { 
                    return id(weight_user1).publish_state(x);}
                  else if (id(weight_miscale).state >= 74.50 && id(weight_miscale).state <= 83) {
                    return id(weight_user2).publish_state(x);}
                  else if (id(weight_miscale).state >= 46 && id(weight_miscale).state <= 65) {
                    return id(weight_user3).publish_state(x);}
                  else if (id(weight_miscale).state >= 28 && id(weight_miscale).state <= 45) {
                    return id(weight_user4).publish_state(x);}
                  else if (id(weight_miscale).state >= 5 && id(weight_miscale).state <= 20) {
                    return id(weight_user5).publish_state(x);}

      - platform: template
        name: Weight Aurélien
        id: weight_user1
        unit_of_measurement: 'kg'
        icon: mdi:weight-kilogram
        accuracy_decimals: 2
      - platform: template
        name: Weight Siham
        id: weight_user2
        unit_of_measurement: 'kg'
        icon: mdi:weight-kilogram
        accuracy_decimals: 2
      - platform: template
        name: Weight Théo
        id: weight_user3
        unit_of_measurement: 'kg'
        icon: mdi:weight-kilogram
        accuracy_decimals: 2
      - platform: template
        name: Weight Sacha
        id: weight_user4
        unit_of_measurement: 'kg'
        icon: mdi:weight-kilogram
        accuracy_decimals: 2
      - platform: template
        name: Weight Noham
        id: weight_user5
        unit_of_measurement: 'kg'
        icon: mdi:weight-kilogram
        accuracy_decimals: 2


See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/sensor/index`
- bodymiscale score integration for Home Assistant (bodymiscale custom component) `<https://github.com/dckiller51/bodymiscale>`__
- bodymiscale Lovelace Card `<https://github.com/dckiller51/lovelace-body-miscale-card>`__

- :ghedit:`Edit`
