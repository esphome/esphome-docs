esphomeyaml
===========

Hi there! This is the documentation for esphomeyaml, a project that aims to make using ESP8266/ESP32 boards with Home Assistant very easy with no programming experience required.

To get started, please see the `Getting Started Guide </esphomeyaml/getting-started.html>`__. Also be sure
to check out `Frequently Asked Questions`_.

You can find the source for this project `on Github <https://github.com/OttoWinter/esphomeyaml>`__, and the core of this project, `esphomelib is also hosted on Github <https://github.com/OttoWinter/esphomelib>`__.

.. _Frequently Asked Questions: /esphomeyaml/faq.html

About esphomeyaml
~~~~~~~~~~~~~~~~~

esphomeyaml will:

 * Read your configuration file and warn you about potential errors (like using the invalid pins.)
 * Create a custom C++ sketch file for you using esphomeyaml's powerful C++ generation engine.
 * Compile the sketch file for you using `platformio <http://platformio.org/>`__.
 * Upload the binary to your ESP via Over the Air updates.
 * Automatically start remote logs via MQTT.


Features
~~~~~~~~

 * **No programming experience required:** just edit YAML configuration
    files like you're used to with Home Assistant.
 * **Flexible:** Use `esphomelib <https://github.com/OttoWinter/esphomelib>`__'s powerful core to create custom sensors/outputs.
 * **Fast and efficient:** Written in C++ and keeps memory consumption to a minimum.
 * **Made for Home Assistant:** Almost all Home Assistant features are supported out of the box. Including RGB lights and many more.
 * **Easy reproducible configuration:** No need to go through a long setup process for every single node. Just copy a configuration file and run a single command.
 * **Smart Over The Air Updates:** esphomeyaml has OTA updates deeply integrated into the system. It even automatically enters a recovery mode if a boot loop is detected.
 * **Powerful logging engine:** View colorful logs and debug issues remotely.
 * **It's Open Source 😺**


Using With
~~~~~~~~~~

==================  ==================  ==================
|Sonoff S20|_
------------------  ------------------  ------------------
`Sonoff S20`_
==================  ==================  ==================

.. |Sonoff S20| image:: /esphomeyaml/images/sonoff-s20.jpg
    :class: component-image
.. _Sonoff S20: /esphomeyaml/using-with/sonoff-s20.html


Core Components
~~~~~~~~~~~~~~~

==================  ==================  ==================
|Core|_             |WiFi|_             |MQTT|_
------------------  ------------------  ------------------
`Core`_             `WiFi`_             `MQTT`_
------------------  ------------------  ------------------
|I²C Bus|_          |OTA Updates|_      |Logger|_
------------------  ------------------  ------------------
`I²C Bus`_          `OTA Updates`_      `Logger`_
------------------  ------------------  ------------------
|Web Server|_       |Power Supply|_     |Deep Sleep|_
------------------  ------------------  ------------------
`Web Server`_       `Power Supply`_     `Deep Sleep`_
==================  ==================  ==================

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

.. |OTA Updates| image:: /esphomeyaml/images/system-update.svg
    :class: component-image
.. _OTA Updates: /esphomeyaml/components/ota.html

.. |Logger| image:: /esphomeyaml/images/file-document-box.svg
    :class: component-image
.. _Logger: /esphomeyaml/components/logger.html

.. |Web Server| image:: /esphomeyaml/images/http.svg
    :class: component-image
.. _Web Server: /esphomeyaml/components/web_server.html

.. |Deep Sleep| image:: /esphomeyaml/images/hotel.svg
    :class: component-image
.. _Deep Sleep: /esphomeyaml/components/deep_sleep.html

.. |Power Supply| image:: /esphomeyaml/images/power.svg
    :class: component-image
.. _Power Supply: /esphomeyaml/components/power_supply.html


Sensor Components
~~~~~~~~~~~~~~~~~

======================  ======================  ======================
|Sensor Core|_          |ADC|_                  |ADS1115|_
----------------------  ----------------------  ----------------------
`Sensor Core`_          `ADC`_                  `ADS1115`_
----------------------  ----------------------  ----------------------
|BMP085|_               |Dallas|_               |DHT|_
----------------------  ----------------------  ----------------------
`BMP085`_               `Dallas`_               `DHT`_
----------------------  ----------------------  ----------------------
|HDC1080|_              |HTU21D|_               |MPU6050|_
----------------------  ----------------------  ----------------------
`HDC1080`_              `HTU21D`_               `MPU6050`_
----------------------  ----------------------  ----------------------
|Pulse Counter|_        |Ultrasonic Sensor|_    |BH1750|_
----------------------  ----------------------  ----------------------
`Pulse Counter`_        `Ultrasonic Sensor`_    `BH1750`_
----------------------  ----------------------  ----------------------
|BME280|_               |BME680|_               |TSL2561|_
----------------------  ----------------------  ----------------------
`BME280`_               `BME680`_               `TSL2561`_
----------------------  ----------------------  ----------------------
|SHT3X-D|_
----------------------  ----------------------  ----------------------
`SHT3X-D`_
======================  ======================  ======================

.. |Sensor Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Sensor Core: /esphomeyaml/components/sensor/index.html

.. |ADC| image:: /esphomeyaml/images/flash.svg
    :class: component-image
.. _ADC: /esphomeyaml/components/sensor/adc.html

.. |ADS1115| image:: /esphomeyaml/images/ads1115.jpg
    :class: component-image
.. _ADS1115: /esphomeyaml/components/sensor/ads1115.html

.. |BMP085| image:: /esphomeyaml/images/bmp180.jpg
    :class: component-image
.. _BMP085: /esphomeyaml/components/sensor/bmp085.html

.. |Dallas| image:: /esphomeyaml/images/ds18b20.jpg
    :class: component-image
.. _Dallas: /esphomeyaml/components/sensor/dallas.html

.. |DHT| image:: /esphomeyaml/images/dht22.jpg
    :class: component-image
.. _DHT: /esphomeyaml/components/sensor/dht.html

.. |HDC1080| image:: /esphomeyaml/images/HDC1080.jpg
    :class: component-image
.. _HDC1080: /esphomeyaml/components/sensor/hdc1080.html

.. |HTU21D| image:: /esphomeyaml/images/htu21d.jpg
    :class: component-image
.. _HTU21D: /esphomeyaml/components/sensor/htu21d.html

.. |MPU6050| image:: /esphomeyaml/images/mpu6050.jpg
    :class: component-image
.. _MPU6050: /esphomeyaml/components/sensor/mpu6050.html

.. |Pulse Counter| image:: /esphomeyaml/images/pulse.svg
    :class: component-image
.. _Pulse Counter: /esphomeyaml/components/sensor/pulse_counter.html

.. |Ultrasonic Sensor| image:: /esphomeyaml/images/hc-sr04.png
    :class: component-image
.. _Ultrasonic Sensor: /esphomeyaml/components/sensor/ultrasonic.html

.. |BH1750| image:: /esphomeyaml/images/bh1750.jpg
    :class: component-image
.. _BH1750: /esphomeyaml/components/sensor/bh1750.html

.. |BME280| image:: /esphomeyaml/images/bme280.jpg
    :class: component-image
.. _BME280: /esphomeyaml/components/sensor/bme280.html

.. |BME680| image:: /esphomeyaml/images/bme680.jpg
    :class: component-image
.. _BME680: /esphomeyaml/components/sensor/bme680.html

.. |TSL2561| image:: /esphomeyaml/images/tsl2561.jpg
    :class: component-image
.. _TSL2561: /esphomeyaml/components/sensor/tsl2561.html

.. |SHT3X-D| image:: /esphomeyaml/images/sht3xd.jpg
    :class: component-image
.. _SHT3X-D: /esphomeyaml/components/sensor/sht3xd.html


Binary Sensor Components
~~~~~~~~~~~~~~~~~~~~~~~~

======================  ======================  ======================
|Binary Sensor Core|_   |GPIO|_                 |Status|_
----------------------  ----------------------  ----------------------
`Binary Sensor Core`_   `GPIO`_                 `Status`_
----------------------  ----------------------  ----------------------
|ESP32 BLE Device|_     |ESP32 Touch Pad|_
----------------------  ----------------------  ----------------------
`ESP32 BLE Device`_     `ESP32 Touch Pad`_
======================  ======================  ======================

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
.. _ESP32 BLE Device: /esphomeyaml/components/binary_sensor/esp32_ble.html

.. |ESP32 Touch Pad| image:: /esphomeyaml/images/touch.svg
    :class: component-image
.. _ESP32 Touch Pad: /esphomeyaml/components/binary_sensor/esp32_touch.html

Output Components
~~~~~~~~~~~~~~~~~

========================  ========================  ========================
|Output Core|_            |ESP8266 Software PWM|_   |GPIO Output|_
------------------------  ------------------------  ------------------------
`Output Core`_            `ESP8266 Software PWM`_   `GPIO Output`_
------------------------  ------------------------  ------------------------
|ESP32 LEDC|_             |PCA9685|_
------------------------  ------------------------  ------------------------
`ESP32 LEDC`_             `PCA9685`_
========================  ========================  ========================

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
~~~~~~~~~~~~~~~~

============================  ============================  ============================
|Light Core|_                 |Binary Light|_               |Monochromatic Light|_
----------------------------  ----------------------------  ----------------------------
`Light Core`_                 `Binary Light`_               `Monochromatic Light`_
----------------------------  ----------------------------  ----------------------------
|RGB Light|_                  |RGBW Light|_                 |FastLED Clockless Light|_
----------------------------  ----------------------------  ----------------------------
`RGB Light`_                  `RGBW Light`_                 `FastLED Clockless Light`_
----------------------------  ----------------------------  ----------------------------
|FastLED SPI Light|_
----------------------------  ----------------------------  ----------------------------
`FastLED SPI Light`_
============================  ============================  ============================


.. |Light Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Light Core: /esphomeyaml/components/light/index.html

.. |Binary Light| image:: /esphomeyaml/images/lightbulb.svg
    :class: component-image
.. _Binary Light: /esphomeyaml/components/light/binary.html

.. |Monochromatic Light| image:: /esphomeyaml/images/brightness-medium.svg
    :class: component-image
.. _Monochromatic Light: /esphomeyaml/components/light/monochromatic.html

.. |RGB Light| image:: /esphomeyaml/images/rgb.png
    :class: component-image
.. _RGB Light: /esphomeyaml/components/light/rgb.html

.. |RGBW Light| image:: /esphomeyaml/images/rgbw.png
    :class: component-image
.. _RGBW Light: /esphomeyaml/components/light/rgbw.html

.. |FastLED Clockless Light| image:: /esphomeyaml/images/color_lens.svg
    :class: component-image
.. _FastLED Clockless Light: /esphomeyaml/components/light/fastled_clockless.html

.. |FastLED SPI Light| image:: /esphomeyaml/images/color_lens.svg
    :class: component-image
.. _FastLED SPI Light: /esphomeyaml/components/light/fastled_spi.html


Switch Components
~~~~~~~~~~~~~~~~~

========================  ========================  ========================
|Switch Core|_            |GPIO Switch|_            |IR Transmitter|_
------------------------  ------------------------  ------------------------
`Switch Core`_            `GPIO Switch`_            `IR Transmitter`_
------------------------  ------------------------  ------------------------
|Restart Switch|_         |Shutdown Switch|_        |Output Switch|_
------------------------  ------------------------  ------------------------
`Restart Switch`_         `Shutdown Switch`_        `Output Switch`_
========================  ========================  ========================

.. |Switch Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Switch Core: /esphomeyaml/components/switch/index.html

.. |GPIO Switch| image:: /esphomeyaml/images/pin.svg
    :class: component-image
.. _GPIO Switch: /esphomeyaml/components/switch/gpio.html

.. |IR Transmitter| image:: /esphomeyaml/images/remote.svg
    :class: component-image
.. _IR Transmitter: /esphomeyaml/components/switch/ir_transmitter.html

.. |Restart Switch| image:: /esphomeyaml/images/restart.svg
    :class: component-image
.. _Restart Switch: /esphomeyaml/components/switch/restart.html

.. |Shutdown Switch| image:: /esphomeyaml/images/power_settings.svg
    :class: component-image
.. _Shutdown Switch: /esphomeyaml/components/switch/shutdown.html

.. |Output Switch| image:: /esphomeyaml/images/upload.svg
    :class: component-image
.. _Output Switch: /esphomeyaml/components/switch/output.html


Fan Components
~~~~~~~~~~~~~~

========================  ========================  ========================
|Fan Core|_               |Binary Fan|_             |Speed Fan|_
------------------------  ------------------------  ------------------------
`Fan Core`_               `Binary Fan`_             `Speed Fan`_
========================  ========================  ========================

.. |Fan Core| image:: /esphomeyaml/images/folder-open.svg
    :class: component-image
.. _Fan Core: /esphomeyaml/components/fan/index.html

.. |Binary Fan| image:: /esphomeyaml/images/fan.svg
    :class: component-image
.. _Binary Fan: /esphomeyaml/components/fan/binary.html

.. |Speed Fan| image:: /esphomeyaml/images/fan.svg
    :class: component-image
.. _Speed Fan: /esphomeyaml/components/fan/speed.html


Misc Components
~~~~~~~~~~~~~~~

========================  ========================  ========================
|Dallas Hub|_             |IR Transmitter Hub|_     |PCA9685 Hub|_
------------------------  ------------------------  ------------------------
`Dallas Hub`_             `IR Transmitter Hub`_     `PCA9685 Hub`_
------------------------  ------------------------  ------------------------
|ADS1115 Hub|_            |Debug Component|_        |PCF8574 I/O Expander|_
------------------------  ------------------------  ------------------------
`ADS1115 Hub`_            `Debug Component`_        `PCF8574 I/O Expander`_
------------------------  ------------------------  ------------------------
|ESP32 BLE Hub|_          |ESP32 Touch Hub|_
------------------------  ------------------------  ------------------------
`ESP32 BLE Hub`_          `ESP32 Touch Hub`_
========================  ========================  ========================

.. |Dallas Hub| image:: /esphomeyaml/images/ds18b20.jpg
    :class: component-image
.. _Dallas Hub: /esphomeyaml/components/dallas.html

.. |IR Transmitter Hub| image:: /esphomeyaml/images/remote.svg
    :class: component-image
.. _IR Transmitter Hub: /esphomeyaml/components/ir_transmitter.html

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

.. |ESP32 BLE Hub| image:: /esphomeyaml/images/bluetooth.svg
    :class: component-image
.. _ESP32 BLE Hub: /esphomeyaml/components/esp32_ble.html

.. |ESP32 Touch Hub| image:: /esphomeyaml/images/touch.svg
    :class: component-image
.. _ESP32 Touch Hub: /esphomeyaml/components/esp32_touch.html


Full Index
~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    getting-started.rst
    configuration-types.rst
    faq.rst
    components/esphomeyaml.rst
    components/dallas.rst
    components/sensor/dallas.rst
    components/i2c.rst
    components/logger.rst
    components/wifi.rst
    components/mqtt.rst
    components/ota.rst
    components/web_server.rst
    components/deep_sleep.rst
    components/debug.rst
    components/ads1115.rst
    components/binary_sensor/index.rst
    components/binary_sensor/gpio.rst
    components/binary_sensor/status.rst
    components/sensor/index.rst
    components/sensor/adc.rst
    components/sensor/ads1115.rst
    components/sensor/bmp085.rst
    components/sensor/dht.rst
    components/sensor/hdc1080.rst
    components/sensor/htu21d.rst
    components/sensor/pulse_counter.rst
    components/sensor/ultrasonic.rst
    components/sensor/mpu6050.rst
    components/output/index.rst
    components/power_supply.rst
    components/output/esp8266_pwm.rst
    components/output/gpio.rst
    components/output/ledc.rst
    components/pca9685.rst
    components/output/pca9685.rst
    components/light/index.rst
    components/light/binary.rst
    components/light/monochromatic.rst
    components/light/rgb.rst
    components/light/rgbw.rst
    components/switch/index.rst
    components/switch/gpio.rst
    components/switch/shutdown.rst
    components/switch/output.rst
    components/ir_transmitter.rst
    components/switch/ir_transmitter.rst
    components/switch/restart.rst
    components/fan/index.rst
    components/fan/binary.rst
    components/fan/speed.rst
    components/pcf8574.rst
    components/esp32_ble.rst
    components/binary_sensor/esp32_ble.rst
    components/esp32_touch.rst
    components/binary_sensor/esp32_touch.rst
    components/light/fastled_clockless.rst
    components/light/fastled_spi.rst
    components/sensor/bh1750.rst
    components/sensor/bme280.rst
    components/sensor/bme680.rst
    components/sensor/tsl2561.rst
    components/sensor/sht3xd.rst
    components/using-with/sonoff-s20.rst
