Mopeka Pro Check BLE Sensor
===============================

.. seo::
    :description: Instructions for setting up Mopeka Pro Check bluetooth-based sensors in ESPHome.
    :image: mopeka.png
    :keywords: Mopeka, Mopeka Pro Check, BLE, Bluetooth

The ``mopeka_pro_check`` sensor platform lets you track the output of Mopeka 
Pro Check LP Bluetooth Low Energy devices using the :doc:`/components/esp32_ble_tracker`.
This component will track the tank level, distance, temperature, and battery
percentage of a Mopeka Pro Check LP device every time the sensor sends
out a BLE broadcast.

.. warning::

    This sensor component only supports the Mopeka Pro Check device.  The original
    Mopeka Check sensors are not supported.

.. figure:: images/mopeka_pro_check.jpg
    :align: center
    :width: 80.0%

    Mopeka Pro Check LP over BLE.

.. code-block:: yaml

    esp32_ble_tracker:

    sensor:
    # Example using 20lb vertical propane tank.
    - platform: mopeka_pro_check
        mac_address: D3:75:F2:DC:16:91
        tank_type: 20LB_V
        temperature:
            name: "Propane test temp"
        level:
            name: "Propane test level"
        distance:
            name: "Propane test distance"
        battery_level:
            name: "Propane test battery level"

    # Custom example - user defined empty / full points
    - platform: mopeka_pro_check
        mac_address: D3:75:F2:DC:16:91
        tank_type: CUSTOM
        distance_full: 40cm
        distance_empty: 10mm
        temperature:
            name: "Propane c test temp"
        level:
            name: "Propane c test level"
        distance:
            name: "Propane c test distance"
        battery_level:
            name: "Propane c test battery level"


Configuration variables:
------------------------

- **mac_address** (**Required**, MAC Address): The MAC address of the Mopeka
  device.

- **tank_type** (*Optional*, Default: 20LB_V): The tank type the sensor is
  measuring.

- **distance_full** (*Optional*): distance sensor will read when it should be
  considered full (100%).  This is only used when tank_type = CUSTOM

- **distance_empty** (*Optional*): distance sensor will read when it should be
  considered empty (0%).  This is only used when tank_type = CUSTOM

- **level** (*Optional*): The percentage of full for the tank sensor

  - **name** (**Required**, string): The name for the level sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use
    in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **distance** (*Optional*): The raw distance/depth of the liquid for the sensor in mm.

  - **name** (**Required**, string): The name for the distance sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use
    in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **temperature** (*Optional*): The information for the temperature sensor.
  This temperature is on the sensor and is not calibrated to ambient temperature.

  - **name** (**Required**, string): The name for the temperature sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use
    in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

- **battery_level** (*Optional*): The information for the battery percentage
  sensor.  Sensor uses a standard CR2032 battery.

  - **name** (**Required**, string): The name for the battery level sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use
    in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.

Tank Types
----------

Currently supported Tank types are:

- ``20LB_V`` - 20 LB vertical tank
- ``30LB_V`` - 30 LB vertical tank
- ``40LB_V`` - 40 LB vertical tank
- ``CUSTOM`` - Allows you to define your own full and empty points

Setting Up Devices
------------------

To set up Mopeka Pro Check devices you first need to find their MAC Address so that
ESPHome can identify them. So first, create a simple configuration with the ``esp32_ble_tracker``
and the ``mopeka_ble`` component like so:

.. code-block:: yaml

    esp32_ble_tracker:

    mopeka_ble:

After uploading, the ESP32 will immediately try to scan for BLE devices.  For Mopeka Pro
Check devices you must press and hold the green sync button for it to be identified.  For all sensors
found the ``mopeka_ble`` component will print a message like this one:

.. code::

    [20:43:26][I][mopeka_ble:053]: SENSOR FOUND: D3:75:F2:DC:16:91

Then just copy the address (``D3:75:F2:DC:16:91``) into a new
``sensor.mopeka_pro_check`` platform entry like in the configuration example at the top.

.. note::

    The ESPHome Mopeka Pro Check BLE integration listens passively to packets the Mopeka device sends by itself.
    ESPHome therefore has no impact on the battery life of the device.

See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/sensor/index`
- :apiref:`mopeka_pro_check/mopeka_pro_check.h`
- `Mopeka  <https://mopeka.com/product/mopeka-check-pro-lp-sensor/>`__
- :ghedit:`Edit`
