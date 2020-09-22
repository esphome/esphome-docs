Xiaomi Mijia BLE Sensors
========================

.. seo::
    :description: Instructions for setting up Xiaomi Mi Home (Mijia) bluetooth-based sensors in ESPHome.
    :image: xiaomi_mijia_logo.jpg
    :keywords: Xiaomi, Mi Home, Mijia, BLE, Bluetooth, HHCCJCY01, GCLS002, HHCCPOT002, LYWSDCGQ, LYWSD02, CGG1, LYWSD03MMC, CGD1, JQJCY01YM, MUE4094RT, WX08ZM

The ``xiaomi_ble`` sensor platform lets you track the output of Xiaomi Bluetooth Low Energy devices using the :doc:`/components/esp32_ble_tracker`. This component will track, for example, the temperature, humidity, moisture, conductivity, illuminance, formaldehyde, mosquito tablet and battery level of the device every time the sensor sends out a BLE broadcast. Contrary to other implementations, ``xiaomi_ble`` listense passively to advertisement packets and does not pair with the device. Hence ESPHome has no impact on battery life.

Supported Devices
-----------------

HHCCJCY01
*********

MiFlora, Huahuacaocao, measures temperature, moisture, ambient light and nutrient levels in the soil.

.. figure:: images/xiaomi_hhccjcy01.jpg
    :align: center
    :width: 60.0%

Configuration example:

.. code-block:: yaml

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

GCLS002
*******

VegTrug Grow Care Garden, Takasho, suitable for outside, similar to the MiFlora.

.. figure:: images/xiaomi_gcls002.jpg
    :align: center
    :width: 30.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: xiaomi_gcls002
        mac_address: "94:2B:FF:5C:91:61"
        temperature:
          name: "GCLS02 Temperature"
        moisture:
          name: "GCLS02 Moisture"
        conductivity:
          name: "GCLS02 Soil Conductivity"
        illuminance:
          name: "GCLS02 Illuminance"

HHCCPOT002
**********

FlowerPot, Huahuacaocao, RoPot, broadcasts moisture and conductivity

.. figure:: images/xiaomi_hhccpot002.jpg
    :align: center
    :width: 30.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: xiaomi_hhccpot002
        mac_address: "94:2B:FF:5C:91:61"
        moisture:
          name: "HHCCPOT002 Moisture"
        conductivity:
          name: "HHCCPOT002 Soil Conductivity"

LYWSDCGQ
********

Hygro thermometer, round body, segment LCD, broadcasts temperature, humidity and battery level.

.. figure:: images/xiaomi_lywsdcgq.jpg
    :align: center
    :width: 30.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: xiaomi_lywsdcgq
        mac_address: "7A:80:8E:19:36:BA"
        temperature:
          name: "LYWSDCGQ Temperature"
        humidity:
          name: "LYWSDCGQ Humidity"
        battery_level:
          name: "LYWSDCGQ Battery Level"

LYWSD02
*******

Hygro thermometer, rectangular body, e-ink display, broadcasts temperature and humidity values, no battery status

.. figure:: images/xiaomi_lywsd02.jpg
    :align: center
    :width: 30.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: xiaomi_lywsd02
        mac_address: "3F:5B:7D:82:58:4E"
        temperature:
          name: "LYWSD02 Temperature"
        humidity:
          name: "LYWSD02 Humidity"

CGG1
****

Hygro thermometer, round body, e-ink display

.. figure:: images/xiaomi_cgg1.jpg
    :align: center
    :width: 30.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: xiaomi_cgg1
        mac_address: "7A:80:8E:19:36:BA"
        temperature:
          name: "CGG1 Temperature"
        humidity:
          name: "CGG1 Humidity"
        battery_level:
          name: "CGG1 Battery Level"

LYWSD03MMC
**********

Hygro thermometer, small square body, segment LCD, encrypted, broadcasts temperature, humidity and battery status. Requires a bindkey in order to decrypt the received data (see :ref:`obtaining_the_bindkey`).

.. figure:: images/xiaomi_lywsd03mmc.jpg
    :align: center
    :width: 30.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: xiaomi_lywsd03mmc
        mac_address: "A4:C1:38:B1:CD:7F"
        bindkey: "eef418daf699a0c188f3bfd17e4565d9"
        temperature:
          name: "LYWSD03MMC Temperature"
        humidity:
          name: "LYWSD03MMC Humidity"
        battery_level:
          name: "LYWSD03MMC Battery Level"

CGD1
****

Cleargrass (Qingping) alarm clock, segment LCD, encrypted, broadcasts temperature, humidity and battery status. Requires a bindkey in order to decrypt the received data (see :ref:`obtaining_the_bindkey`).

.. figure:: images/xiaomi_cgd1.jpg
    :align: center
    :width: 30.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: xiaomi_cgd1
        mac_address: "A4:C1:38:8C:34:B7"
        bindkey: "fe39106baeedb7c801e3d63c4396f97e"
        temperature:
          name: "CGD1 Temperature"
        humidity:
          name: "CGD1 Humidity"
        battery_level:
          name: "CGD1 Battery Level"

JQJCY01YM
*********

Xiaomi (Honeywell) formaldehyde sensor, OLED display, broadcasts temperature, humidity, formaldehyde concentration (mg/m³) and battery status. 

.. figure:: images/xiaomi_jqjcy01ym.jpg
    :align: center
    :width: 30.0%

Configuration example:

.. code-block:: yaml

    sensor:
      - platform: xiaomi_jqjcy01ym
        mac_address: "7A:80:8E:19:36:BA"
        temperature:
          name: "JQJCY01YM Temperature"
        humidity:
          name: "JQJCY01YM Humidity"
        formaldehyde:
          name: "JQJCY01YM Formaldehyde"
        battery_level:
          name: "JQJCY01YM Battery Level"

WX08ZM
******

Mosquito Repellent Smart Version, broadcasts the tablet resource level, on/off state and battery level, implemented as a hybrid sensor, needs both ``sensor`` and ``binary_sensor`` in config.

.. figure:: images/xiaomi_wx08zm.jpg
    :align: center
    :width: 30.0%

Configuration example:

.. code-block:: yaml

    sensor:

    binary_sensor:
      - platform: xiaomi_wx08zm
        mac_address: "74:a3:4a:b5:07:34"
        tablet:
          name: "WX08ZM Mosquito Tablet"
        battery_level:
          name: "WX08ZM Battery Level"

MUE4094RT
*********

Xiaomi Philips BLE night light, broadcasts motion detection (detected/clear, on/off), default timeout is 5s, implemented as a hybrid sensor, needs both ``sensor`` and ``binary_sensor`` in config.

.. figure:: images/xiaomi_mue4094rt.jpg
    :align: center
    :width: 30.0%

Configuration example:

.. code-block:: yaml

    sensor:

    binary_sensor:
      - platform: xiaomi_mue4094rt
        name: "MUE4094RT Night Light"
        mac_address: "7A:80:8E:19:36:BA"
        timeout: "5s"

MJYD02YL-A
**********

Xiaomi Yeelight night light, in-shape replacement of MJYD02YL with BLE, broadcasts light on/off status, motion detection, idle time since last motion event and battery status. Requires a bindkey in order to decrypt the received data (see :ref:`obtaining_the_bindkey`). Implemented as a hybrid sensor, needs both ``sensor`` and ``binary_sensor`` in config.

.. figure:: images/xiaomi_mjyd02yla.jpg
    :align: center
    :width: 30.0%

Configuration example:

.. code-block:: yaml

    sensor:

    binary_sensor:
      - platform: xiaomi_mjyd02yla
        name: "MJYD02YL-A Night Light"
        mac_address: "50:EC:50:CD:32:02"
        bindkey: "48403ebe2d385db8d0c187f81e62cb64"
        idle_time:
          name: "MJYD02YL-A Idle Time"
        light:
          name: "MJYD02YL-A Light Status"
        battery_level:
          name: "MJYD02YL-A Battery Level"

Setting Up Devices
------------------

Required:

- **mac_address** (MAC Address): The MAC address of the device.
- **bindkey** (string, 32 characters, case insensitive): The key to decrypt the BLE advertisements for encrypted sensor types

Optional with **name**, **id** (:ref:`config-id`) and all other options from :ref:`Sensor <config-sensor>`:

- **temperature**
- **humidity**
- **moisture**
- **illuminance**
- **conductivity**
- **tablet**
- **formaldehyde**
- **battery_level**

To find the MAC Address so that ESPHome can identify the device, you can create a simple configuration without any sensor entries:

.. code-block:: yaml

    esp32_ble_tracker:

After uploading, the ESP32 will immediately try to scan for BLE devices. When it detects a new sensor, it will automatically parse the BLE message print a message like this one:

.. code::

    Found device A4:C1:38:4E:16:78 RSSI=-78
      Address Type: PUBLIC
      Name: 'LYWSD03MMC'

It can sometimes take some time for the first BLE broadcast to be received. Once the device has been found, copy the address ``A4:C1:38:4E:16:78`` into a new platform entry like shown in the example configurations.

.. _obtaining_the_bindkey:

Obtaining The Bindkey
---------------------

To set up an encrypted device such as the LYWSD03MMC or CGD1, you first need to obain the bind key. The ``xiaomi_ble`` sensor component is not able to automatically generate a bind key, so you need to use the original Mi Home app to add the sensor once (there are `efforts <https://github.com/danielkucera/mi-standardauth>`__ to generate a bindkey without the need for packet sniffing, but it's not working correctly yet). While adding the device, a new key is generated and uploaded into the Xiaomi cloud and to the device itself. Currently a chinese server needs to be selected as the rest of the world doesn't support most of these devices yet. Once generated, the key will not change again until the device is removed and re-added in the Xiaomi app.

In order to obtain the bind key, a SSL packet sniffer needs to be setup on either an Android phone or the iPhone. A good choice for Android is the `Remote PCAP <https://play.google.com/store/apps/details?id=com.egorovandreyrm.pcapremote&hl=en>`__ in combination with `Wireshark <https://www.wireshark.org/>`__. A tutorial on how to setup the Remote PCAP packet sniffer can be found `here <https://egorovandreyrm.com/pcap-remote-tutorial/>`__. Instructions how to obtain the key using an iPhone are `here <https://github.com/custom-components/sensor.mitemp_bt/blob/master/faq.md#my-sensors-ble-advertisements-are-encrypted-how-can-i-get-the-key>`__. Once the traffic between the Mi Home app and the Xiaomi has been recorded, the bind key will show in clear text:

.. code-block:: yaml

    packet: POST /app/device/bltbind

    "data" = "{"did":"blt.3.129q4nasgeg00","token":"20c665a7ff82a5bfb5eefc36","props":[{"type":"prop","key":"bind_key","value":"cfc7cc892f4e32f7a733086cf3443cb0"},   {"type":"prop","key":"smac","value":"A4:C1:38:8C:34:B7"}]}"

The ``bind_key`` is the 32 digits "value" item in the above output which needs to be inserted into the config file. 
    

See Also
--------

- :doc:`/components/esp32_ble_tracker`
- :doc:`/components/sensor/index`
- :apiref:`xiaomi_lywsd03mmc/xiaomi_ble.h`
- Xiaomi Home Assistant mitemp_bt custom component `<https://github.com/custom-components/sensor.mitemp_bt>`__
  by `@Magalex2x14 <https://github.com/Magalex2x14>`__
- Xiaomi LYWSD03MMC passive sensor readout `<https://github.com/ahpohl/xiaomi_lywsd03mmc>`__ by `@ahpohl <https://github.com/ahpohl>`__
- Mi-standardauth `<https://github.com/danielkucera/mi-standardauth>`__

- :ghedit:`Edit`
