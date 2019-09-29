Xiaomi MiScale v1 and v2 BLE Sensor
===================================

.. seo::
    :description: Instructions for setting up Xiaomi MiScale bluetooth-based scale in ESPHome.
    :image: xiaomi_miscale.jpg
    :keywords: Xiaomi, Mi Scale, Scale, BLE, Bluetooth

The ``xiaomi_miscale`` sensor platform lets you track the weight output of Xiaomi MiScale V1 and V2 Bluetooth Low Energy
devices using the :doc:`/components/esp32_ble_tracker`. This component will track the
weight measured of the MiScale device every time the sensor
sends out a BLE broadcast. Note that contrary to other implementations, ESPHome can track as many
MiScale devices at once as you want.

.. code-block:: yaml

    # Example configuration entry
    esp32_ble_tracker:

    sensor:
      - platform: xiaomi_miscale
        mac_address: '94:2B:FF:5C:91:61'
        weight:
          name: "Xiaomi Mi Scale Weight"
        battery_level:
          name: "Xiaomi Mi Scale Battery Level"
        impedance:
          name: "Xiaomi Mi Scale Impedance"

Configuration variables:
------------------------

- **mac_address** (**Required**, MAC Address): The MAC address of the Xiaomi MiScale device.
- **weight** (**Required**): The information for the weight sensor.
  - **name** (**Required**, string): The name for the weight sensor.
  - All other options from :ref:`Sensor <config-sensor>`.
  
- **battery_level** (**Optional**, Battery Level): The battery level of the Xiaomi MiScale device.
  - **name** (**Required**, string): The name for the battery level sensor.
  - All other options from :ref:`Sensor <config-sensor>`.
  
- **impedance** (**Optional**, Impedance): The information for the impedance sensor, useful for biometric extrapolation of fat and water content.
  - **name** (**Required**, string): The name for the impedance level sensor.
  - All other options from :ref:`Sensor <config-sensor>`.


Setting Up Devices
------------------

Before you can even scan for the MiScale sensor, you need to activate it using the Mifit app. Set it up there and you'll be able to discover it.

To set up Xiaomi MiScale devices you first need to find their MAC Address so that ESPHome can
identify them. So first, create a simple configuration without any ``xiaomi_miscale`` entries like so:

.. code-block:: yaml

    esp32_ble_tracker:

After uploading the ESP32 will immediately try to scan for BLE devices such as the Xiaomi MiScale. When
it detects these sensors, it will automatically parse the BLE message print a message like this one:

.. code::

    Xiaomi MiScale 94:2B:FF:5C:91:61 Got weight=75kg impedance=20Ohm battery_level=80%

Note that it can sometimes take some time for the first BLE broadcast to be received.

Then just copy the address (``94:2B:FF:5C:91:61``) into a new ``sensor.xiaomi_miscale`` platform entry like
in the configuration example at the top.

See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/sensor/xiaomi_mijia`
- :doc:`/components/sensor/index`
- `OpenMQTTGateway <https://github.com/1technophile/OpenMQTTGateway>`__ by `@1technophile <https://github.com/1technophile>`__
- :ghedit:`Edit`
