Xiaomi Miscale2 Sensors
========================

.. seo::
    :description: Instructions for setting up Xiaomi Miscale2 bluetooth-based sensors in ESPHome.
    :image: xiaomi_miscale2.jpg
    :keywords: Xiaomi, BLE, Bluetooth, XMTZC02HM, XMTZC05HM

The ``xiaomi_miscale2`` sensor platform lets you track the output of Xiaomi Bluetooth Low Energy devices using the :doc:`/components/esp32_ble_tracker`. This component will track, for example, the weight and the impedance of the device every time the sensor sends out a BLE broadcast. Contrary to other implementations, ``xiaomi_miscale2`` listens passively to advertisement packets and does not pair with the device. Hence ESPHome has no impact on battery life.

To get the body scores using your weight, height, age and gender see the custom_components `<https://github.com/dckiller51/bodymiscale>`__

Supported Devices
-----------------

XMTZC02HM, XMTZC05HM
********************

Miscale2 measures weight and impedance.

.. figure:: images/xiaomi_miscale2.jpg
    :align: center
    :width: 60.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: xiaomi_miscale2
        mac_address: '5C:CA:D3:70:D4:A2'
        weight:
          name: "Xiaomi Mi Scale Weight"
        impedance:
          name: "Xiaomi Mi Scale Impedance"

Configuration example with multiple users :

You have to replace the numbers in the lambdas to determine your weight which is between X weight and X weight.

.. code-block:: yaml

    sensor:
      - platform: xiaomi_miscale2
        mac_address: '5C:CA:D3:70:D4:A2'
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

        impedance:
          name: "Xiaomi Mi Scale Impedance"
          id: impedance_xiaomi
          on_value:
            then:
              - lambda: |-
                  if (id(weight_miscale).state >= 69 && id(weight_miscale).state <= 74.49) {
                    return id(impedance_user1).publish_state(x);}
                  else if (id(weight_miscale).state >= 74.50 && id(weight_miscale).state <= 83) {
                    return id(impedance_user2).publish_state(x);}
                  else if (id(weight_miscale).state >= 46 && id(weight_miscale).state <= 65) {
                    return id(impedance_user3).publish_state(x);}
                  else if (id(weight_miscale).state >= 28 && id(weight_miscale).state <= 45) {
                    return id(impedance_user4).publish_state(x);}
                  else if (id(weight_miscale).state >= 5 && id(weight_miscale).state <= 20) {
                    return id(impedance_user5).publish_state(x);}

      - platform: template
        name: Weight Aurélien
        id: weight_user1
        unit_of_measurement: 'kg'
        icon: mdi:weight-kilogram
        accuracy_decimals: 2
      - platform: template
        name: Impedance Aurélien
        id: impedance_user1
        unit_of_measurement: 'ohm'
        icon: mdi:omega
        accuracy_decimals: 0
      - platform: template
        name: Weight Siham
        id: weight_user2
        unit_of_measurement: 'kg'
        icon: mdi:weight-kilogram
        accuracy_decimals: 2
      - platform: template
        name: Impedance Siham
        id: impedance_user2
        unit_of_measurement: 'ohm'
        icon: mdi:omega
        accuracy_decimals: 0
      - platform: template
        name: Weight Théo
        id: weight_user3
        unit_of_measurement: 'kg'
        icon: mdi:weight-kilogram
        accuracy_decimals: 2
      - platform: template
        name: Impedance Théo
        id: impedance_user3
        unit_of_measurement: 'ohm'
        icon: mdi:omega
        accuracy_decimals: 0
      - platform: template
        name: Weight Sacha
        id: weight_user4
        unit_of_measurement: 'kg'
        icon: mdi:weight-kilogram
        accuracy_decimals: 2
      - platform: template
        name: Impedance Sacha
        id: impedance_user4
        unit_of_measurement: 'ohm'
        icon: mdi:omega
        accuracy_decimals: 0
      - platform: template
        name: Weight Noham
        id: weight_user5
        unit_of_measurement: 'kg'
        icon: mdi:weight-kilogram
        accuracy_decimals: 2
      - platform: template
        name: Impedance Noham
        id: impedance_user5
        unit_of_measurement: 'ohm'
        icon: mdi:omega
        accuracy_decimals: 0


See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/sensor/index`
- bodymiscale score integration for Home Assistant (bodymiscale custom component) `<https://github.com/dckiller51/bodymiscale>`__

- :ghedit:`Edit`
