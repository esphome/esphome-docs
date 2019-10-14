Xiaomi CGG1 BLE Sensor
=======================

.. seo::
    :description: Instructions for setting up Xiaomi CGG1 bluetooth-based temperature and humidity sensors in ESPHome.
    :image: xiaomi_cgg1-full.jpg
    :keywords: Xiaomi, CGG1, BLE, Bluetooth

The ``xiaomi_cgg1`` sensor platform lets you track the output of Xiaomi CGG1 Bluetooth Low Energy
devices using the :doc:`/components/esp32_ble_tracker`. This component will track the
temperature, humidity and the battery level of the CGG! device every time the sensor
sends out a BLE broadcast. Note that contrary to other implementations, ESPHome can track as many
CGG1 devices at once as you want.

.. figure:: images/xiaomi_CGG1-full.jpg
    :align: center
    :width: 60.0%

    Xiaomi CGG1 Temperature and Humidity Sensor over BLE.

.. code-block:: yaml

    # Example configuration entry
    esp32_ble_tracker:

    sensor:
      - platform: xiaomi_cgg1
        mac_address: 58:2D:34:10:7A:8C
        temperature:
          name: "Xiaomi CGG1 Temperature"
        humidity:
          name: "Xiaomi CGG1 Humidity"
        battery_level:
          name: "Xiaomi CGG1 Battery Level"

Configuration variables:
------------------------

- **mac_address** (**Required**, MAC Address): The MAC address of the Xiaomi CGG1 device.
- **temperature** (*Optional*): The information for the temperature sensor.

  - **name** (**Required**, string): The name for the temperature sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **humidity** (*Optional*): The information for the humidity sensor

  - **name** (**Required**, string): The name for the humidity sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **battery_level** (*Optional*): The information for the battery level sensor

  - **name** (**Required**, string): The name for the humidity sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.


Setting Up Devices
------------------

To set up Xiaomi CGG1 devices you first need to find their MAC Address so that ESPHome can
identify them. So first, create a simple configuration without any ``xiaomi_CGG1`` entries like so:

.. code-block:: yaml

    esp32_ble_tracker:

After uploading the ESP32 will immediately try to scan for BLE devices such as the Xiaomi CGG1. When
it detects these sensors, it will automatically parse the BLE message print a message like this one:

.. code::

    Xiaomi CGG1 58:2D:34:10:7A:8C Got temperature=23.4°C, humidity=65.0%

Note that it can sometimes take some time for the first BLE broadcast to be received. You can speed up
the process by pressing the grey bluetooth button on the back of the device.

Then just copy the address (``58:2D:34:10:7A:8C``) into a new ``sensor.xiaomi_CGG1`` platform entry like
in the configuration example at the top.

.. note::

    The ESPHome Xiaomi integration listens passively to packets the xiaomi device sends by itself.
    ESPHome therefore has no impact on the battery life of the device.

See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/sensor/xiaomi_mijia`
- :doc:`/components/sensor/index`
- :apiref:`xiaomi_CGG1/xiaomi_CGG1.h`
- `Xiaomi Mi Jia BLE protocol <https://github.com/mspider65/Xiaomi-MiJia-Bluetooth-Temperature-and-Humidity-Sensor>`__
  by `@mspider65 <https://github.com/mspider65>`__
- :ghedit:`Edit`
