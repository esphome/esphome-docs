AirThings BLE Sensors
=====================

.. seo::
    :description: Instructions for setting up AirThings bluetooth-based sensors in ESPHome.
    :keywords: AirThings, BLE, Bluetooth, Wave Plus, Wave Mini

The ``airthings_wave_plus`` and ``airthings_wave_mini`` sensor platforms lets you track the output of AirThings Bluetooth Low Energy devices.

This component will track radon, airborne chemicals, CO2, temperature and humidity and others depending on the device sensors.

Device Discovery
-----------------

AirThings devices can be found using the ``airthings_ble`` ble scanner.

To find out your device's MAC address, add the following to your ESPHome configuration:

.. code-block:: yaml

    logger:
      level: DEBUG # Required for the tracker to show the device

    esp32_ble_tracker:
    airthings_ble:

The device will then listen for nearby devices, and display a message like this one:

.. code-block:: text

    [D][airthings_ble:019]:
    Found AirThings device Serial: 123456789 (MAC: 01:02:03:04:05:06)

Once the device is found, remove the ``airthings_ble`` device tracker from your configuration and take note of the device MAC address, and use it when configuring a sensor below.

Supported Devices
-----------------

Airthings Wave Plus Sensor
**************************

AirThings Wave Plus tracks radon (24h and long term), airborne chemicals, CO2, temperature, atmospheric pressure and humidity.

.. figure:: images/airthings_wave_plus.jpg
    :align: center
    :width: 60.0%

Configuration example:
**********************


.. code-block:: yaml

    sensor:
      - platform: airthings_wave_plus
        ble_client_id: airthings01
        update_interval: 5min # default
        temperature:
          name: "WavePlus Temperature"
        radon:
          name: "WavePlus Radon"
        radon_long_term:
          name: "WavePlus Radon Long Term"
        pressure:
          name: "WavePlus Pressure"
        humidity:
          name: "WavePlus Humidity"
        co2:
          name: "WavePlus CO2"
        tvoc:
          name: "WavePlus VOC"

    ble_client:
      - mac_address: 01:02:03:04:05:06
        id: airthings01

    esp32_ble_tracker:

Airthings Wave Mini Sensor
**************************

AirThings Wave Mini tracks airborne chemicals, temperature, pressure and humidity.

.. figure:: images/airthings_wave_mini.jpg
    :align: center
    :width: 60.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: airthings_wave_mini
        ble_client_id: airthingsmini
        update_interval: 5min # default
        temperature:
          name: "WaveMini Temperature"
        pressure:
          name: "WaveMini Pressure"
        humidity:
          name: "WaveMini Humidity"
        tvoc:
          name: "WaveMini VOC"

    ble_client:
      - mac_address: 01:02:03:04:05:06
        id: airthingsmini

    esp32_ble_tracker:

Airthings Wave Radon Sensor
***************************

AirThings Wave Radon tracks radon (24h and long term), temperature, and humidity.

.. figure:: images/airthings_wave_radon.jpg
    :align: center
    :width: 60.0%

Configuration example:
**********************

.. code-block:: yaml

    sensor:
      - platform: airthings_wave_radon
        ble_client_id: airthingsradon
        update_interval: 5min #default
        temperature:
          name: "WaveRadon Temperature"
        radon:
          name: "WaveRadon Radon"
        radon_long_term:
          name: "WaveRadon Radon Long Term"
        humidity:
          name: "WaveRadon Humidity"

    ble_client:
      - mac_address: 01:02:03:04:05:06
        id: airthingsradon

    esp32_ble_tracker:

.. note::

    The sensor uses active polling of devices every 5 minutes as per the device reported internal refresh timeout.
