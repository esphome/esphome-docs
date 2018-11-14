Xiaomi MiFlora BLE Sensor
=========================

.. seo::
    :description: Instructions for setting up Xiaomi Mi Flora bluetooth-based plant monitors in esphomelib.
    :image: xiaomi_miflora.jpg
    :keywords: Xiaomi, Mi Flora, BLE, Bluetooth

The ``xiaomi_miflora`` sensor platform lets you track the output of Xiaomi MiFlora Bluetooth Low Energy
devices using the :doc:`/esphomeyaml/components/esp32_ble_tracker`. This component will track the
temperature, humidity and optionally the battery level of the MiFlora device every time the sensor
sends out a BLE broadcast. Note that contrary to other implementations, esphomelib can track as many
MiFlora devices at once as you want.

.. code:: yaml

    # Example configuration entry
    esp32_ble_tracker:

    sensor:
      - platform: xiaomi_miflora
        mac_address: 94:2B:FF:5C:91:61
        temperature:
          name: "Xiaomi MiFlora Temperature"
        moisture:
          name: "Xiaomi MiFlora Moisture"
        illuminance:
          name: "Xiaomi MiFlora Illuminance"
        conductivity:
          name: "Xiaomi MiFlora Soil Conductivity"
        battery_level:
          name: "Xiaomi MiFlora Battery Level"

Configuration variables:
------------------------

- **mac_address** (**Required**, MAC Address): The MAC address of the Xiaomi MiFlora device.
- **temperature** (*Optional*): The information for the temperature sensor.

  - **name** (**Required**, string): The name for the temperature sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

- **moisture** (*Optional*): The information for the moisture sensor

  - **name** (**Required**, string): The name for the moisture sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

- **illuminance** (*Optional*): The information for the illuminance sensor

  - **name** (**Required**, string): The name for the illuminance sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

- **conductivity** (*Optional*): The information for the soil conductivity sensor

  - **name** (**Required**, string): The name for the soil conductivity sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

- **battery_level** (*Optional*): The information for the battery level sensor

  - **name** (**Required**, string): The name for the humidity sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.


Setting Up Devices
------------------

To set up Xiaomi MiFlora devices you first need to find their MAC Address so that esphomelib can
identify them. So first, create a simple configuration without any ``xiaomi_miflora`` entries like so:

.. code:: yaml

    esp32_ble_tracker:

After uploading the ESP32 will immediately try to scan for BLE devices such as the Xiaomi MiFlora. When
it detects these sensors, it will automatically parse the BLE message print a message like this one:

.. code::

    Xiaomi MiFlora 94:2B:FF:5C:91:61 Got temperature=23.4°C

Note that it can sometimes take some time for the first BLE broadcast to be received.

Then just copy the address (``94:2B:FF:5C:91:61``) into a new ``sensor.xiaomi_miflora`` platform entry like
in the configuration example at the top.


See Also
--------

- :doc:`/esphomeyaml/components/esp32_ble_tracker`
- :doc:`/esphomeyaml/components/sensor/xiaomi_mijia`
- :doc:`/esphomeyaml/components/sensor/index`
- :doc:`API Reference </api/misc/esp32_ble_tracker>`
- `OpenMQTTGateway <https://github.com/1technophile/OpenMQTTGateway>`__ by `@1technophile <https://github.com/1technophile>`__
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/xiaomi_miflora.rst>`__

.. disqus::
