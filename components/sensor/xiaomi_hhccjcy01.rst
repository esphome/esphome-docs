Xiaomi HHCCJCY01 BLE Sensor
===========================

.. seo::
    :description: Instructions for setting up Xiaomi HHCCJCY01 bluetooth-based plant monitors model HHCCJCY01 in ESPHome.
    :image: xiaomi_hhccjcy01.jpg
    :keywords: Xiaomi, Mi Flora, BLE, Bluetooth, HHCCJCY01

The ``xiaomi_hhccjcy01`` sensor platform lets you track the output of Xiaomi HHCCJCY01 Bluetooth Low Energy
devices using the :doc:`/components/esp32_ble_tracker`. This component will track the
temperature, humidity and optionally the battery level of the HHCCJCY01 device every time the sensor
sends out a BLE broadcast. Note that contrary to other implementations, ESPHome can track as many
HHCCJCY01 devices at once as you want.

.. code-block:: yaml

    # Example configuration entry
    esp32_ble_tracker:

    sensor:
      - platform: xiaomi_hhccjcy01
        mac_address: '94:2B:FF:5C:91:61'
        temperature:
          name: "Xiaomi HHCCJCY01 Temperature"
        moisture:
          name: "Xiaomi HHCCJCY01 Moisture"
        illuminance:
          name: "Xiaomi HHCCJCY01 Illuminance"
        conductivity:
          name: "Xiaomi HHCCJCY01 Soil Conductivity"
        battery_level:
          name: "Xiaomi HHCCJCY01 Battery Level"

Configuration variables:
------------------------

- **mac_address** (**Required**, MAC Address): The MAC address of the Xiaomi HHCCJCY01 device.
- **temperature** (*Optional*): The information for the temperature sensor.

  - **name** (**Required**, string): The name for the temperature sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **moisture** (*Optional*): The information for the moisture sensor

  - **name** (**Required**, string): The name for the moisture sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **illuminance** (*Optional*): The information for the illuminance sensor

  - **name** (**Required**, string): The name for the illuminance sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **conductivity** (*Optional*): The information for the soil conductivity sensor

  - **name** (**Required**, string): The name for the soil conductivity sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **battery_level** (*Optional*): The information for the battery level sensor

  - **name** (**Required**, string): The name for the battery sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

.. note::

    This integration requires the device to have a recent firmware version, see
    https://github.com/esphome/issues/issues/260#issuecomment-487684720 for more info.

    The ``battery_level`` does not appear to work with some firmware versions of the device (the other sensors
    do work though). See https://github.com/esphome/issues/issues/107 for more information.

Setting Up Devices
------------------

Before you can even scan for the sensor, you need to activate it using the Flower Care app. Set it up there and you'll be able to discover it.

To set up Xiaomi HHCCJCY01 devices you first need to find their MAC Address so that ESPHome can
identify them. So first, create a simple configuration without any ``xiaomi_hhccjcy01`` entries like so:

.. code-block:: yaml

    esp32_ble_tracker:

After uploading the ESP32 will immediately try to scan for BLE devices such as the Xiaomi HHCCJCY01. When
it detects these sensors, it will automatically parse the BLE message print a message like this one:

.. code::

    Got Xiaomi HHCCJCY01 94:2B:FF:5C:91:61 Got temperature=23.4°C

Note that it can sometimes take some time for the first BLE broadcast to be received.

Then just copy the address (``94:2B:FF:5C:91:61``) into a new ``sensor.xiaomi_hhccjcy01`` platform entry like
in the configuration example at the top.

.. note::

    The ESPHome Xiaomi integration listens passively to packets the xiaomi device sends by itself.
    ESPHome therefore has no impact on the battery life of the device.

See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/sensor/xiaomi_lywsdcgq`
- :doc:`/components/sensor/index`
- :apiref:`xiaomi_hhccjcy01/xiaomi_hhccjcy01.h`
- `OpenMQTTGateway <https://github.com/1technophile/OpenMQTTGateway>`__ by `@1technophile <https://github.com/1technophile>`__
- :ghedit:`Edit`
