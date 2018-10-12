esphomeyaml
===========

.. raw:: html

    <a href="https://github.com/OttoWinter/esphomelib"><img src="https://img.shields.io/github/stars/OttoWinter/esphomelib.svg?style=social&label=Star&maxAge=2592000" alt="GitHub stars" style="max-width:100%;"></a>
    <a href="https://esphomelib.com/esphomeyaml/guides/changelog.html"><img src="https://img.shields.io/pypi/v/esphomeyaml.svg" alt="Release" style="max-width:100%;"></a>
    <a href="https://discord.gg/KhAMKrd"><img src="https://img.shields.io/discord/429907082951524364.svg" alt="Discord Chat" style="max-width:100%;"></a>

Hi there! This is the documentation for esphomeyaml, a project that aims to make using ESP8266/ESP32 boards with
Home Assistant very easy with no programming experience required.

esphomeyaml will:

 * Read your configuration file and warn you about potential errors (like using the invalid pins.)
 * Create a custom C++ sketch file for you using esphomeyaml's powerful C++ generation engine.
 * Compile the sketch file for you using `platformio <http://platformio.org/>`__.
 * Upload the binary to your ESP via Over the Air updates.
 * Automatically start remote logs via MQTT.


Features
--------

 * **No programming experience required:** just edit YAML configuration
   files like you're used to with Home Assistant.
 * **Flexible:** Use `esphomelib <https://github.com/OttoWinter/esphomelib>`__'s powerful core to create custom sensors/outputs.
 * **Fast and efficient:** Written in C++ and keeps memory consumption to a minimum.
 * **Small binaries:** Only the sensors/devices you actually use will appear in the binary.
 * **Made for Home Assistant:** Almost all Home Assistant features are supported out of the box. Including RGB lights and many more.
 * **Easy reproducible configuration:** No need to go through a long setup process for every single node. Just copy a configuration file and run a single command.
 * **Smart Over The Air Updates:** esphomeyaml has OTA updates deeply integrated into the system. It even automatically enters a recovery mode if a boot loop is detected.
 * **Powerful logging engine:** View colorful logs and debug issues remotely.
 * **It's Open Source 😺**


Guides
------

================================================== ================================================== ==================================================
|Getting Started through Command Line|_            |Getting Started through HassIO Add-On|_           |Configuration Types|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Getting Started through Command Line`_            `Getting Started through HassIO Add-On`_           `Configuration Types`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Migrating from Sonoff-Tasmota|_                   |Migrating from ESPurna|_                          |Migrating from ESPEasy|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Migrating from Sonoff-Tasmota`_                   `Migrating from ESPurna`_                          `Migrating from ESPEasy`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Automations|_                                     |FAQ and Tips|_                                    |Contributing|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Automations`_                                     `FAQ and Tips`_                                    `Contributing`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Changelog|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Changelog`_
================================================== ================================================== ==================================================

.. |Getting Started through Command Line| image:: /esphomeyaml/images/console.svg
    :class: component-image
.. _Getting Started through Command Line: /esphomeyaml/guides/getting_started_command_line.html
.. |Getting Started through HassIO Add-On| image:: /esphomeyaml/images/home-assistant.svg
    :class: component-image
.. _Getting Started through HassIO Add-On: /esphomeyaml/guides/getting_started_hassio.html
.. |Configuration Types| image:: /esphomeyaml/images/settings.svg
    :class: component-image
.. _Configuration Types: /esphomeyaml/guides/configuration-types.html
.. |Migrating from Sonoff-Tasmota| image:: /esphomeyaml/images/tasmota.svg
    :class: component-image
.. _Migrating from Sonoff-Tasmota: /esphomeyaml/guides/migrate_sonoff_tasmota.html
.. |Migrating from ESPurna| image:: /esphomeyaml/images/espurna.svg
    :class: component-image
.. _Migrating from ESPurna: /esphomeyaml/guides/migrate_espurna.html
.. |Migrating from ESPEasy| image:: /esphomeyaml/images/espeasy.svg
    :class: component-image
.. _Migrating from ESPEasy: /esphomeyaml/guides/migrate_espeasy.html
.. |Automations| image:: /esphomeyaml/images/auto-fix.svg
    :class: component-image
.. _Automations: /esphomeyaml/guides/automations.html
.. |FAQ and Tips| image:: /esphomeyaml/images/question_answer.svg
    :class: component-image
.. _FAQ and Tips: /esphomeyaml/guides/faq.html
.. |Contributing| image:: /esphomeyaml/images/github-circle.svg
    :class: component-image
.. _Contributing: /esphomeyaml/guides/contributing.html
.. |Changelog| image:: /esphomeyaml/images/new-box.svg
    :class: component-image
.. _Changelog: /esphomeyaml/guides/changelog.html


.. _devices:

Devices
-------

This list contains a bunch of getting started and more advanced guides for using esphomeyaml.
Technically, all ESP8266/ESP32 devices (and therefore all Sonoff devices) are supported by esphomeyaml/lib.
These are only the devices for which I've had the time to set up dedicated guides.

================================================== ================================================== ==================================================
|Generic ESP8266|_                                 |Generic ESP32|_                                   |NodeMCU ESP8266|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Generic ESP8266`_                                 `Generic ESP32`_                                   `NodeMCU ESP8266`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|NodeMCU ESP32|_                                   |Sonoff S20|_                                      |Sonoff 4CH|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`NodeMCU ESP32`_                                   `Sonoff S20`_                                      `Sonoff 4CH`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Generic Sonoff|_                                  |Sonoff Basic|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Generic Sonoff`_                                  `Sonoff Basic`_
================================================== ================================================== ==================================================

.. |Generic ESP8266| image:: /esphomeyaml/images/esp8266.svg
    :class: component-image
.. _Generic ESP8266: /esphomeyaml/devices/esp8266.html
.. |Generic ESP32| image:: /esphomeyaml/images/esp32.svg
    :class: component-image
.. _Generic ESP32: /esphomeyaml/devices/esp32.html
.. |NodeMCU ESP8266| image:: /esphomeyaml/images/nodemcu_esp8266.jpg
    :class: component-image
.. _NodeMCU ESP8266: /esphomeyaml/devices/nodemcu_esp8266.html
.. |NodeMCU ESP32| image:: /esphomeyaml/images/nodemcu_esp32.jpg
    :class: component-image
.. _NodeMCU ESP32: /esphomeyaml/devices/nodemcu_esp32.html
.. |Sonoff S20| image:: /esphomeyaml/images/sonoff_s20.jpg
    :class: component-image
.. _Sonoff S20: /esphomeyaml/devices/sonoff_s20.html
.. |Sonoff 4CH| image:: /esphomeyaml/images/sonoff_4ch.jpg
    :class: component-image
.. _Sonoff 4CH: /esphomeyaml/devices/sonoff_4ch.html
.. |Generic Sonoff| image:: /esphomeyaml/images/sonoff.svg
    :class: component-image
.. _Generic Sonoff: /esphomeyaml/devices/sonoff.html
.. |Sonoff Basic| image:: /esphomeyaml/images/sonoff_basic.jpg
    :class: component-image
.. _Sonoff Basic: /esphomeyaml/devices/sonoff_basic.html


Core Components
---------------

================================================== ================================================== ==================================================
|Core|_                                            |WiFi|_                                            |MQTT|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Core`_                                            `WiFi`_                                            `MQTT`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|I²C Bus|_                                         |SPI Bus|_                                         |UART Bus|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`I²C Bus`_                                         `SPI Bus`_                                         `UART Bus`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|OTA Updates|_                                     |Logger|_                                          |Web Server|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`OTA Updates`_                                     `Logger`_                                          `Web Server`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Power Supply|_                                    |Deep Sleep|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Power Supply`_                                    `Deep Sleep`_
================================================== ================================================== ==================================================

.. |Core| image:: /esphomeyaml/images/cloud-circle.svg
    :class: component-image
.. _Core: /esphomeyaml/components/esphomeyaml.html
.. |WiFi| image:: /esphomeyaml/images/network-wifi.svg
    :class: component-image
.. _WiFi: /esphomeyaml/components/wifi.html
.. |MQTT| image:: /esphomeyaml/images/mqtt.png
    :class: component-image
.. _MQTT: /esphomeyaml/components/mqtt.html
.. |I²C Bus| image:: /esphomeyaml/images/i2c.svg
    :class: component-image
.. _I²C Bus: /esphomeyaml/components/i2c.html
.. |SPI Bus| image:: /esphomeyaml/images/spi.svg
    :class: component-image
.. _SPI Bus: /esphomeyaml/components/spi.html
.. |UART Bus| image:: /esphomeyaml/images/uart.svg
    :class: component-image
.. _UART Bus: /esphomeyaml/components/uart.html
.. |OTA Updates| image:: /esphomeyaml/images/system-update.svg
    :class: component-image
.. _OTA Updates: /esphomeyaml/components/ota.html
.. |Logger| image:: /esphomeyaml/images/file-document-box.svg
    :class: component-image
.. _Logger: /esphomeyaml/components/logger.html
.. |Web Server| image:: /esphomeyaml/images/http.svg
    :class: component-image
.. _Web Server: /esphomeyaml/components/web_server.html
.. |Power Supply| image:: /esphomeyaml/images/power.svg
    :class: component-image
.. _Power Supply: /esphomeyaml/components/power_supply.html
.. |Deep Sleep| image:: /esphomeyaml/images/hotel.svg
    :class: component-image
.. _Deep Sleep: /esphomeyaml/components/deep_sleep.html




Sensor Components
-----------------

================================================== ================================================== ==================================================
|Sensor Core|_                                     |ADC|_                                             |ADS1115|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Sensor Core`_                                     `ADC`_                                             `ADS1115`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|BH1750|_                                          |BLE RSSI|_                                        |BME280|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`BH1750`_                                          `BLE RSSI`_                                        `BME280`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|BME680|_                                          |BMP085|_                                          |BMP280|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`BME680`_                                          `BMP085`_                                          `BMP280`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Dallas|_                                          |DHT|_                                             |DHT12|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Dallas`_                                          `DHT`_                                             `DHT12`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Duty Cycle|_                                      |ESP32 Hall Sensor|_                               |HDC1080|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Duty Cycle`_                                      `ESP32 Hall Sensor`_                               `HDC1080`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|HLW8012|_                                         |HMC5883L|_                                        |HX711|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`HLW8012`_                                         `HMC5883L`_                                        `HX711`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|INA219|_                                          |INA3221|_                                         |HTU21D|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`INA219`_                                          `INA3221`_                                         `HTU21D`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|MAX6675|_                                         |MH-Z19|_                                          |MPU6050|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`MAX6675`_                                         `MH-Z19`_                                          `MPU6050`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|MS5611|_                                          |Pulse Counter|_                                   |Rotary Encoder|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`MS5611`_                                          `Pulse Counter`_                                   `Rotary Encoder`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|SHT3X-D|_                                         |TCS34725|_                                        |Template Sensor|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`SHT3X-D`_                                         `TCS34725`_                                        `Template Sensor`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|TSL2561|_                                         |Ultrasonic Sensor|_                               |Uptime Sensor|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`TSL2561`_                                         `Ultrasonic Sensor`_                               `Uptime Sensor`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|WiFi Signal Strength|_                            |Xiaomi MiFlora|_                                  |Xiaomi MiJia|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`WiFi Signal Strength`_                            `Xiaomi MiFlora`_                                  `Xiaomi MiJia`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Custom Sensor|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Custom Sensor`_
================================================== ================================================== ==================================================

.. |Sensor Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Sensor Core: /esphomeyaml/components/sensor/index.html
.. |ADC| image:: /esphomeyaml/images/flash.svg
    :class: component-image
.. _ADC: /esphomeyaml/components/sensor/adc.html
.. |ADS1115| image:: /esphomeyaml/images/ads1115.jpg
    :class: component-image
.. _ADS1115: /esphomeyaml/components/sensor/ads1115.html
.. |BH1750| image:: /esphomeyaml/images/bh1750.jpg
    :class: component-image
.. _BH1750: /esphomeyaml/components/sensor/bh1750.html
.. |BLE RSSI| image:: /esphomeyaml/images/bluetooth.svg
    :class: component-image
.. _BLE RSSI: /esphomeyaml/components/sensor/ble_rssi.html
.. |BME280| image:: /esphomeyaml/images/bme280.jpg
    :class: component-image
.. _BME280: /esphomeyaml/components/sensor/bme280.html
.. |BME680| image:: /esphomeyaml/images/bme680.jpg
    :class: component-image
.. _BME680: /esphomeyaml/components/sensor/bme680.html
.. |BMP085| image:: /esphomeyaml/images/bmp180.jpg
    :class: component-image
.. _BMP085: /esphomeyaml/components/sensor/bmp085.html
.. |BMP280| image:: /esphomeyaml/images/bmp280.jpg
    :class: component-image
.. _BMP280: /esphomeyaml/components/sensor/bmp280.html
.. |Dallas| image:: /esphomeyaml/images/dallas.jpg
    :class: component-image
.. _Dallas: /esphomeyaml/components/sensor/dallas.html
.. |DHT| image:: /esphomeyaml/images/dht.jpg
    :class: component-image
.. _DHT: /esphomeyaml/components/sensor/dht.html
.. |DHT12| image:: /esphomeyaml/images/dht12.jpg
    :class: component-image
.. _DHT12: /esphomeyaml/components/sensor/dht12.html
.. |Duty Cycle| image:: /esphomeyaml/images/percent.svg
    :class: component-image
.. _Duty Cycle: /esphomeyaml/components/sensor/duty_cycle.html
.. |ESP32 Hall Sensor| image:: /esphomeyaml/images/magnet.svg
    :class: component-image
.. _ESP32 Hall Sensor: /esphomeyaml/components/sensor/esp32_hall.html
.. |HDC1080| image:: /esphomeyaml/images/hdc1080.jpg
    :class: component-image
.. _HDC1080: /esphomeyaml/components/sensor/hdc1080.html
.. |HLW8012| image:: /esphomeyaml/images/hlw8012.svg
    :class: component-image
.. _HLW8012: /esphomeyaml/components/sensor/hlw8012.html
.. |HMC5883L| image:: /esphomeyaml/images/hmc5883l.jpg
    :class: component-image
.. _HMC5883L: /esphomeyaml/components/sensor/hmc5883l.html
.. |HX711| image:: /esphomeyaml/images/hx711.jpg
    :class: component-image
.. _HX711: /esphomeyaml/components/sensor/hx711.html
.. |INA219| image:: /esphomeyaml/images/ina219.jpg
    :class: component-image
.. _INA219: /esphomeyaml/components/sensor/ina219.html
.. |INA3221| image:: /esphomeyaml/images/ina3221.jpg
    :class: component-image
.. _INA3221: /esphomeyaml/components/sensor/ina3221.html
.. |HTU21D| image:: /esphomeyaml/images/htu21d.jpg
    :class: component-image
.. _HTU21D: /esphomeyaml/components/sensor/htu21d.html
.. |MAX6675| image:: /esphomeyaml/images/max6675.jpg
    :class: component-image
.. _MAX6675: /esphomeyaml/components/sensor/max6675.html
.. |MH-Z19| image:: /esphomeyaml/images/mhz19.jpg
    :class: component-image
.. _MH-Z19: /esphomeyaml/components/sensor/mhz19.html
.. |MPU6050| image:: /esphomeyaml/images/mpu6050.jpg
    :class: component-image
.. _MPU6050: /esphomeyaml/components/sensor/mpu6050.html
.. |MS5611| image:: /esphomeyaml/images/ms5611.jpg
    :class: component-image
.. _MS5611: /esphomeyaml/components/sensor/ms5611.html
.. |Pulse Counter| image:: /esphomeyaml/images/pulse.svg
    :class: component-image
.. _Pulse Counter: /esphomeyaml/components/sensor/pulse_counter.html
.. |Rotary Encoder| image:: /esphomeyaml/images/rotary_encoder.jpg
    :class: component-image
.. _Rotary Encoder: /esphomeyaml/components/sensor/rotary_encoder.html
.. |SHT3X-D| image:: /esphomeyaml/images/sht3xd.jpg
    :class: component-image
.. _SHT3X-D: /esphomeyaml/components/sensor/sht3xd.html
.. |TCS34725| image:: /esphomeyaml/images/tcs34725.jpg
    :class: component-image
.. _TCS34725: /esphomeyaml/components/sensor/tcs34725.html
.. |Template Sensor| image:: /esphomeyaml/images/description.svg
    :class: component-image
.. _Template Sensor: /esphomeyaml/components/sensor/template.html
.. |TSL2561| image:: /esphomeyaml/images/tsl2561.jpg
    :class: component-image
.. _TSL2561: /esphomeyaml/components/sensor/tsl2561.html
.. |Ultrasonic Sensor| image:: /esphomeyaml/images/ultrasonic.jpg
    :class: component-image
.. _Ultrasonic Sensor: /esphomeyaml/components/sensor/ultrasonic.html
.. |Uptime Sensor| image:: /esphomeyaml/images/timer.svg
    :class: component-image
.. _Uptime Sensor: /esphomeyaml/components/sensor/uptime.html
.. |WiFi Signal Strength| image:: /esphomeyaml/images/network-wifi.svg
    :class: component-image
.. _WiFi Signal Strength: /esphomeyaml/components/sensor/wifi_signal.html
.. |Xiaomi MiFlora| image:: /esphomeyaml/images/xiaomi_miflora.jpg
    :class: component-image
.. _Xiaomi MiFlora: /esphomeyaml/components/sensor/xiaomi_miflora.html
.. |Xiaomi MiJia| image:: /esphomeyaml/images/xiaomi_mijia.jpg
    :class: component-image
.. _Xiaomi MiJia: /esphomeyaml/components/sensor/xiaomi_mijia.html
.. |Custom Sensor| image:: /esphomeyaml/images/language-cpp.svg
    :class: component-image
.. _Custom Sensor: /esphomeyaml/components/sensor/custom.html

Looking for a sensor that outputs its values as an analog voltage? Have a look at the
:doc:`ADC Sensor <components/sensor/adc>` together with a formula like in the :doc:`TEMT6000
example </esphomeyaml/cookbook/temt6000>`.


Binary Sensor Components
------------------------

================================================== ================================================== ==================================================
|Binary Sensor Core|_                              |GPIO|_                                            |Status|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Binary Sensor Core`_                              `GPIO`_                                            `Status`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|ESP32 BLE Device|_                                |ESP32 Touch Pad|_                                 |Nextion Touch|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`ESP32 BLE Device`_                                `ESP32 Touch Pad`_                                 `Nextion Touch`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Template Binary Sensor|_                          |Remote Receiver|_                                 |PN532 Tag|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Template Binary Sensor`_                          `Remote Receiver`_                                 `PN532 Tag`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|RDM6300 Tag|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`RDM6300 Tag`_
================================================== ================================================== ==================================================

.. |Binary Sensor Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Binary Sensor Core: /esphomeyaml/components/binary_sensor/index.html
.. |GPIO| image:: /esphomeyaml/images/pin.svg
    :class: component-image
.. _GPIO: /esphomeyaml/components/binary_sensor/gpio.html
.. |Status| image:: /esphomeyaml/images/server-network.svg
    :class: component-image
.. _Status: /esphomeyaml/components/binary_sensor/status.html
.. |ESP32 BLE Device| image:: /esphomeyaml/images/bluetooth.svg
    :class: component-image
.. _ESP32 BLE Device: /esphomeyaml/components/binary_sensor/esp32_ble_tracker.html
.. |ESP32 Touch Pad| image:: /esphomeyaml/images/touch.svg
    :class: component-image
.. _ESP32 Touch Pad: /esphomeyaml/components/binary_sensor/esp32_touch.html
.. |Nextion Touch| image:: /esphomeyaml/images/nextion.jpg
    :class: component-image
.. _Nextion Touch: /esphomeyaml/components/binary_sensor/nextion.html
.. |Template Binary Sensor| image:: /esphomeyaml/images/description.svg
    :class: component-image
.. _Template Binary Sensor: /esphomeyaml/components/binary_sensor/template.html
.. |Remote Receiver| image:: /esphomeyaml/images/remote.svg
    :class: component-image
.. _Remote Receiver: /esphomeyaml/components/binary_sensor/remote_receiver.html
.. |PN532 Tag| image:: /esphomeyaml/images/pn532.jpg
    :class: component-image
.. _PN532 Tag: /esphomeyaml/components/binary_sensor/pn532.html
.. |RDM6300 Tag| image:: /esphomeyaml/images/rdm6300.jpg
    :class: component-image
.. _RDM6300 Tag: /esphomeyaml/components/binary_sensor/rdm6300.html


Output Components
-----------------

============================== ============================== ==============================
|Output Core|_                 |ESP8266 Software PWM|_        |GPIO Output|_
------------------------------ ------------------------------ ------------------------------
`Output Core`_                 `ESP8266 Software PWM`_        `GPIO Output`_
------------------------------ ------------------------------ ------------------------------
|ESP32 LEDC|_                  |PCA9685|_
------------------------------ ------------------------------ ------------------------------
`ESP32 LEDC`_                  `PCA9685`_
============================== ============================== ==============================

.. |Output Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Output Core: /esphomeyaml/components/output/index.html
.. |ESP8266 Software PWM| image:: /esphomeyaml/images/pwm.png
    :class: component-image
.. _ESP8266 Software PWM: /esphomeyaml/components/output/esp8266_pwm.html
.. |GPIO Output| image:: /esphomeyaml/images/pin.svg
    :class: component-image
.. _GPIO Output: /esphomeyaml/components/output/gpio.html
.. |ESP32 LEDC| image:: /esphomeyaml/images/pwm.png
    :class: component-image
.. _ESP32 LEDC: /esphomeyaml/components/output/ledc.html
.. |PCA9685| image:: /esphomeyaml/images/pca9685.jpg
    :class: component-image
.. _PCA9685: /esphomeyaml/components/output/pca9685.html


Light Components
----------------

================================================== ================================================== ==================================================
|Light Core|_                                      |Binary Light|_                                    |Monochromatic Light|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Light Core`_                                      `Binary Light`_                                    `Monochromatic Light`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Cold+Warm White Light|_                           |RGB Light|_                                       |RGBW Light|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Cold+Warm White Light`_                           `RGB Light`_                                       `RGBW Light`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|RGBWW Light|_                                     |FastLED Clockless Light|_                         |FastLED SPI Light|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`RGBWW Light`_                                     `FastLED Clockless Light`_                         `FastLED SPI Light`_
================================================== ================================================== ==================================================

.. |Light Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Light Core: /esphomeyaml/components/light/index.html
.. |Binary Light| image:: /esphomeyaml/images/lightbulb.svg
    :class: component-image
.. _Binary Light: /esphomeyaml/components/light/binary.html
.. |Monochromatic Light| image:: /esphomeyaml/images/brightness-medium.svg
    :class: component-image
.. _Monochromatic Light: /esphomeyaml/components/light/monochromatic.html
.. |Cold+Warm White Light| image:: /esphomeyaml/images/brightness-medium.svg
    :class: component-image
.. _Cold+Warm White Light: /esphomeyaml/components/light/cwww.html
.. |RGB Light| image:: /esphomeyaml/images/rgb.png
    :class: component-image
.. _RGB Light: /esphomeyaml/components/light/rgb.html
.. |RGBW Light| image:: /esphomeyaml/images/rgbw.png
    :class: component-image
.. _RGBW Light: /esphomeyaml/components/light/rgbw.html
.. |RGBWW Light| image:: /esphomeyaml/images/rgbw.png
    :class: component-image
.. _RGBWW Light: /esphomeyaml/components/light/rgbww.html
.. |FastLED Clockless Light| image:: /esphomeyaml/images/color_lens.svg
    :class: component-image
.. _FastLED Clockless Light: /esphomeyaml/components/light/fastled_clockless.html
.. |FastLED SPI Light| image:: /esphomeyaml/images/color_lens.svg
    :class: component-image
.. _FastLED SPI Light: /esphomeyaml/components/light/fastled_spi.html


Looking for WS2811 and similar individually addressable lights? Have a look at the
:doc:`FastLED Clockless Light <components/light/fastled_clockless>`.

Switch Components
-----------------

================================================== ================================================== ==================================================
|Switch Core|_                                     |GPIO Switch|_                                     |Remote Transmitter|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Switch Core`_                                     `GPIO Switch`_                                     `Remote Transmitter`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Restart Switch|_                                  |Shutdown Switch|_                                 |Generic Output Switch|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Restart Switch`_                                  `Shutdown Switch`_                                 `Generic Output Switch`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Template Switch|_                                 |UART Switch|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Template Switch`_                                 `UART Switch`_
================================================== ================================================== ==================================================

.. |Switch Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Switch Core: /esphomeyaml/components/switch/index.html
.. |GPIO Switch| image:: /esphomeyaml/images/pin.svg
    :class: component-image
.. _GPIO Switch: /esphomeyaml/components/switch/gpio.html
.. |Remote Transmitter| image:: /esphomeyaml/images/remote.svg
    :class: component-image
.. _Remote Transmitter: /esphomeyaml/components/switch/remote_transmitter.html
.. |Restart Switch| image:: /esphomeyaml/images/restart.svg
    :class: component-image
.. _Restart Switch: /esphomeyaml/components/switch/restart.html
.. |Shutdown Switch| image:: /esphomeyaml/images/power_settings.svg
    :class: component-image
.. _Shutdown Switch: /esphomeyaml/components/switch/shutdown.html
.. |Generic Output Switch| image:: /esphomeyaml/images/upload.svg
    :class: component-image
.. _Generic Output Switch: /esphomeyaml/components/switch/output.html
.. |Template Switch| image:: /esphomeyaml/images/description.svg
    :class: component-image
.. _Template Switch: /esphomeyaml/components/switch/template.html
.. |UART Switch| image:: /esphomeyaml/images/uart.svg
    :class: component-image
.. _UART Switch: /esphomeyaml/components/switch/uart.html


Fan Components
--------------

============================== ============================== ==============================
|Fan Core|_                    |Binary Fan|_                  |Speed Fan|_
------------------------------ ------------------------------ ------------------------------
`Fan Core`_                    `Binary Fan`_                  `Speed Fan`_
============================== ============================== ==============================

.. |Fan Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Fan Core: /esphomeyaml/components/fan/index.html
.. |Binary Fan| image:: /esphomeyaml/images/fan.svg
    :class: component-image
.. _Binary Fan: /esphomeyaml/components/fan/binary.html
.. |Speed Fan| image:: /esphomeyaml/images/fan.svg
    :class: component-image
.. _Speed Fan: /esphomeyaml/components/fan/speed.html


Display Components
------------------

================================================== ================================================== ==================================================
|Display Core|_                                    |GPIO LCD|_                                        |PCF8574 LCD|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Display Core`_                                    `GPIO LCD`_                                        `PCF8574 LCD`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|MAX7219|_                                         |Nextion|_                                         |SSD1306 I2C|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`MAX7219`_                                         `Nextion`_                                         `SSD1306 I2C`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|SSD1306 SPI|_                                     |Waveshare E-Paper|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`SSD1306 SPI`_                                     `Waveshare E-Paper`_
================================================== ================================================== ==================================================

.. |Display Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Display Core: /esphomeyaml/components/display/index.html
.. |GPIO LCD| image:: /esphomeyaml/images/lcd.jpg
    :class: component-image
.. _GPIO LCD: /esphomeyaml/components/display/lcd_gpio.html
.. |PCF8574 LCD| image:: /esphomeyaml/images/lcd.jpg
    :class: component-image
.. _PCF8574 LCD: /esphomeyaml/components/display/lcd_pcf8574.html
.. |MAX7219| image:: /esphomeyaml/images/max7219.jpg
    :class: component-image
.. _MAX7219: /esphomeyaml/components/display/max7219.html
.. |Nextion| image:: /esphomeyaml/images/nextion.jpg
    :class: component-image
.. _Nextion: /esphomeyaml/components/display/nextion.html
.. |SSD1306 I2C| image:: /esphomeyaml/images/ssd1306.jpg
    :class: component-image
.. _SSD1306 I2C: /esphomeyaml/components/display/ssd1306_i2c.html
.. |SSD1306 SPI| image:: /esphomeyaml/images/ssd1306.jpg
    :class: component-image
.. _SSD1306 SPI: /esphomeyaml/components/display/ssd1306_spi.html
.. |Waveshare E-Paper| image:: /esphomeyaml/images/waveshare_epaper.jpg
    :class: component-image
.. _Waveshare E-Paper: /esphomeyaml/components/display/waveshare_epaper.html

Cover Components
----------------

============================== ============================== ==============================
|Cover Core|_                  |Template Cover|_
------------------------------ ------------------------------ ------------------------------
`Cover Core`_                  `Template Cover`_
============================== ============================== ==============================

.. |Cover Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Cover Core: /esphomeyaml/components/cover/index.html
.. |Template Cover| image:: /esphomeyaml/images/description.svg
    :class: component-image
.. _Template Cover: /esphomeyaml/components/cover/template.html


Misc Components
---------------

================================================== ================================================== ==================================================
|Dallas Hub|_                                      |Remote Transmitter Hub|_                          |Remote Receiver Hub|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Dallas Hub`_                                      `Remote Transmitter Hub`_                          `Remote Receiver Hub`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|PCA9685 Hub|_                                     |ADS1115 Hub|_                                     |Debug Component|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`PCA9685 Hub`_                                     `ADS1115 Hub`_                                     `Debug Component`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|PCF8574 I/O Expander|_                            |ESP32 BLE Tracker|_                               |ESP32 BLE Beacon|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`PCF8574 I/O Expander`_                            `ESP32 BLE Tracker`_                               `ESP32 BLE Beacon`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|ESP32 Touch Hub|_                                 |Status LED|_                                      |PN532|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`ESP32 Touch Hub`_                                 `Status LED`_                                      `PN532`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|RDM6300|_                                         |Time|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`RDM6300`_                                         `Time`_
================================================== ================================================== ==================================================

.. |Dallas Hub| image:: /esphomeyaml/images/dallas.jpg
    :class: component-image
.. _Dallas Hub: /esphomeyaml/components/dallas.html
.. |Remote Transmitter Hub| image:: /esphomeyaml/images/remote.svg
    :class: component-image
.. _Remote Transmitter Hub: /esphomeyaml/components/remote_transmitter.html
.. |Remote Receiver Hub| image:: /esphomeyaml/images/remote.svg
    :class: component-image
.. _Remote Receiver Hub: /esphomeyaml/components/remote_receiver.html
.. |PCA9685 Hub| image:: /esphomeyaml/images/pca9685.jpg
    :class: component-image
.. _PCA9685 Hub: /esphomeyaml/components/pca9685.html
.. |ADS1115 Hub| image:: /esphomeyaml/images/ads1115.jpg
    :class: component-image
.. _ADS1115 Hub: /esphomeyaml/components/ads1115.html
.. |Debug Component| image:: /esphomeyaml/images/bug-report.svg
    :class: component-image
.. _Debug Component: /esphomeyaml/components/debug.html
.. |PCF8574 I/O Expander| image:: /esphomeyaml/images/pcf8574.jpg
    :class: component-image
.. _PCF8574 I/O Expander: /esphomeyaml/components/pcf8574.html
.. |ESP32 BLE Tracker| image:: /esphomeyaml/images/bluetooth.svg
    :class: component-image
.. _ESP32 BLE Tracker: /esphomeyaml/components/esp32_ble_tracker.html
.. |ESP32 BLE Beacon| image:: /esphomeyaml/images/bluetooth.svg
    :class: component-image
.. _ESP32 BLE Beacon: /esphomeyaml/components/esp32_ble_beacon.html
.. |ESP32 Touch Hub| image:: /esphomeyaml/images/touch.svg
    :class: component-image
.. _ESP32 Touch Hub: /esphomeyaml/components/esp32_touch.html
.. |Status LED| image:: /esphomeyaml/images/led-on.svg
    :class: component-image
.. _Status LED: /esphomeyaml/components/status_led.html
.. |PN532| image:: /esphomeyaml/images/pn532.jpg
    :class: component-image
.. _PN532: /esphomeyaml/components/pn532.html
.. |RDM6300| image:: /esphomeyaml/images/rdm6300.jpg
    :class: component-image
.. _RDM6300: /esphomeyaml/components/rdm6300.html
.. |Time| image:: /esphomeyaml/images/clock-outline.svg
    :class: component-image
.. _Time: /esphomeyaml/components/time.html

.. _cookbook:

Cookbook
--------

This list contains items that are technically already supported by other components.

================================================== ================================================== ==================================================
|Garage Door|_                                     |PIR Sensor|_                                      |Relay|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Garage Door`_                                     `PIR Sensor`_                                      `Relay`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|BRUH Multisensor|_                                |TEMT6000|_                                        |Non-Invasive Power Meter|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`BRUH Multisensor`_                                `TEMT6000`_                                        `Non-Invasive Power Meter`_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
|Dual relay cover motor control|_
-------------------------------------------------- -------------------------------------------------- --------------------------------------------------
`Dual relay cover motor control`_
================================================== ================================================== ==================================================

.. |Garage Door| image:: /esphomeyaml/images/window-open.svg
    :class: component-image
.. _Garage Door: /esphomeyaml/cookbook/garage-door.html
.. |PIR Sensor| image:: /esphomeyaml/images/pir.jpg
    :class: component-image
.. _PIR Sensor: /esphomeyaml/cookbook/pir.html
.. |Relay| image:: /esphomeyaml/images/relay.jpg
    :class: component-image
.. _Relay: /esphomeyaml/cookbook/relay.html
.. |BRUH Multisensor| image:: /esphomeyaml/images/bruh.png
    :class: component-image
.. _BRUH Multisensor: /esphomeyaml/cookbook/bruh.html
.. |TEMT6000| image:: /esphomeyaml/images/temt6000.jpg
    :class: component-image
.. _TEMT6000: /esphomeyaml/cookbook/temt6000.html
.. |Non-Invasive Power Meter| image:: /esphomeyaml/images/power_meter.jpg
    :class: component-image
.. _Non-Invasive Power Meter: /esphomeyaml/cookbook/power_meter.html
.. |Dual relay cover motor control| image:: /esphomeyaml/images/sonoff_dual_r2.jpg
    :class: component-image
.. _Dual relay cover motor control: /esphomeyaml/cookbook/dual-r2-cover.html

Do you have other awesome automations or 2nd order components? Please feel free to add them to the
documentation for others to copy. See :doc:`Contributing <guides/contributing>`.

.. toctree::
    :hidden:

    components/index
    cookbook/index
    devices/index
    guides/index
