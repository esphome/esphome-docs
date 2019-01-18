esphomeyaml
===========

.. image:: images/esphomeyaml-logo-full.svg

.. seo::
    :description: esphomeyaml Component index - esphomeyaml Homepage - Reimagining DIY Home Automation. esphomelib is a framework that tries to provide the best possible use experience for using ESP8266 and ESP32 microcontrollers for Home Automation. esphomeyaml is the tool that converts YAML configuration files into custom firmwares and has many helpers so that you only have to worry about creating the hardware, esphomeyaml will take care of the rest.
    :image: esphomeyaml-logo-full.png

.. raw:: html

    <a href="https://github.com/OttoWinter/esphomelib"><img src="https://img.shields.io/github/stars/OttoWinter/esphomelib.svg?style=social&label=Star&maxAge=2592000" alt="GitHub stars" style="max-width:100%;"></a>
    <a href="https://esphomelib.com/esphomeyaml/changelog/index.html"><img src="https://img.shields.io/pypi/v/esphomeyaml.svg" alt="Release" style="max-width:100%;"></a>
    <a href="https://discord.gg/KhAMKrd"><img src="https://img.shields.io/discord/429907082951524364.svg" alt="Discord Chat" style="max-width:100%;"></a>

.. _guides:

Guides
------

.. imgtable::

    Getting Started through Command Line, guides/getting_started_command_line, console.svg
    Getting Started through Hass.io Add-On, guides/getting_started_hassio, home-assistant.svg
    Configuration Types, guides/configuration-types, settings.svg

    Migrating from Sonoff-Tasmota, guides/migrate_sonoff_tasmota, tasmota.svg
    Migrating from ESPurna, guides/migrate_espurna, espurna.svg
    Migrating from ESPEasy, guides/migrate_espeasy, espeasy.svg

    Automations, guides/automations, auto-fix.svg
    FAQ and Tips, guides/faq, question_answer.svg
    Contributing, guides/contributing, github-circle.svg

    Changelog, changelog/index, new-box.svg

.. _devices:

Devices
-------

This list contains a bunch of getting started and more advanced guides for using esphomeyaml.
Technically, all ESP8266/ESP32 devices (and therefore all Sonoff devices) are supported by esphomeyaml/lib.
These are only the devices for which I've had the time to set up dedicated guides.

.. imgtable::

    Generic ESP8266, devices/esp8266, esp8266.svg
    Generic ESP32, devices/esp32, esp32.svg
    NodeMCU ESP8266, devices/nodemcu_esp8266, nodemcu_esp8266.jpg

    NodeMCU ESP32, devices/nodemcu_esp32, nodemcu_esp32.jpg
    Sonoff S20, devices/sonoff_s20, sonoff_s20.jpg
    Sonoff 4CH, devices/sonoff_4ch, sonoff_4ch.jpg

    Generic Sonoff, devices/sonoff, sonoff.svg
    Sonoff Basic, devices/sonoff_basic, sonoff_basic.jpg

Core Components
---------------

.. imgtable::

    Core, components/esphomeyaml, cloud-circle.svg
    WiFi, components/wifi, network-wifi.svg
    MQTT, components/mqtt, mqtt.png

    I²C Bus, components/i2c, i2c.svg
    SPI Bus, components/spi, spi.svg
    UART Bus, components/uart, uart.svg

    OTA Updates, components/ota, system-update.svg
    Logger, components/logger, file-document-box.svg
    Web Server, components/web_server, http.svg

    Native API, components/api, server-network.svg
    Power Supply, components/power_supply, power.svg
    Deep Sleep, components/deep_sleep, hotel.svg

Sensor Components
-----------------

.. imgtable::

    Sensor Core, components/sensor/index, folder-open.svg
    ADC, components/sensor/adc, flash.svg
    ADS1115, components/sensor/ads1115, ads1115.jpg
    APDS9960, components/sensor/apds9960, apds9960.jpg
    BH1750, components/sensor/bh1750, bh1750.jpg
    BLE RSSI, components/sensor/ble_rssi, bluetooth.svg
    BME280, components/sensor/bme280, bme280.jpg
    BME680, components/sensor/bme680, bme680.jpg
    BMP085, components/sensor/bmp085, bmp180.jpg
    BMP280, components/sensor/bmp280, bmp280.jpg
    CSE7766, components/sensor/cse7766, cse7766.svg
    Dallas, components/sensor/dallas, dallas.jpg
    DHT, components/sensor/dht, dht.jpg
    DHT12, components/sensor/dht12, dht12.jpg
    Duty Cycle, components/sensor/duty_cycle, percent.svg
    ESP32 Hall Sensor, components/sensor/esp32_hall, magnet.svg
    HDC1080, components/sensor/hdc1080, hdc1080.jpg
    HLW8012, components/sensor/hlw8012, hlw8012.svg
    HMC5883L, components/sensor/hmc5883l, hmc5883l.jpg
    Home Assistant, components/sensor/homeassistant, home-assistant.svg
    HX711, components/sensor/hx711, hx711.jpg
    INA219, components/sensor/ina219, ina219.jpg
    INA3221, components/sensor/ina3221, ina3221.jpg
    HTU21D, components/sensor/htu21d, htu21d.jpg
    MAX31855, components/sensor/max31855, max31855.jpg
    MAX6675, components/sensor/max6675, max6675.jpg
    MH-Z19, components/sensor/mhz19, mhz19.jpg
    MPU6050, components/sensor/mpu6050, mpu6050.jpg
    MQTT Subscribe, components/sensor/mqtt_subscribe, mqtt.png
    MS5611, components/sensor/ms5611, ms5611.jpg
    PMSX003, components/sensor/pmsx003, pmsx003.svg
    Pulse Counter, components/sensor/pulse_counter, pulse.svg
    Rotary Encoder, components/sensor/rotary_encoder, rotary_encoder.jpg
    SHT3X-D, components/sensor/sht3xd, sht3xd.jpg
    TCS34725, components/sensor/tcs34725, tcs34725.jpg
    Template Sensor, components/sensor/template, description.svg
    Total Daily Energy, components/sensor/total_daily_energy, sigma.svg
    TSL2561, components/sensor/tsl2561, tsl2561.jpg
    Ultrasonic Sensor, components/sensor/ultrasonic, ultrasonic.jpg
    Uptime Sensor, components/sensor/uptime, timer.svg
    WiFi Signal Strength, components/sensor/wifi_signal, network-wifi.svg
    Xiaomi MiFlora, components/sensor/xiaomi_miflora, xiaomi_miflora.jpg
    Xiaomi MiJia, components/sensor/xiaomi_mijia, xiaomi_mijia.jpg
    Custom Sensor, components/sensor/custom, language-cpp.svg

Looking for a sensor that outputs its values as an analog voltage? Have a look at the
:doc:`ADC Sensor <components/sensor/adc>` together with a formula like in the :doc:`TEMT6000
example </esphomeyaml/cookbook/temt6000>`.


Binary Sensor Components
------------------------

.. imgtable::

    Binary Sensor Core, components/binary_sensor/index, folder-open.svg
    GPIO, components/binary_sensor/gpio, pin.svg
    Status, components/binary_sensor/status, server-network.svg
    ESP32 BLE Device, components/binary_sensor/esp32_ble_tracker, bluetooth.svg
    ESP32 Touch Pad, components/binary_sensor/esp32_touch, touch.svg
    Nextion Touch, components/binary_sensor/nextion, nextion.jpg
    Template Binary Sensor, components/binary_sensor/template, description.svg
    Remote Receiver, components/binary_sensor/remote_receiver, remote.svg
    PN532 Tag, components/binary_sensor/pn532, pn532.jpg
    RDM6300 Tag, components/binary_sensor/rdm6300, rdm6300.jpg
    Custom Binary Sensor, components/binary_sensor/custom, language-cpp.svg

Output Components
-----------------

.. imgtable::

    Output Core, components/output/index, folder-open.svg
    ESP8266 Software PWM, components/output/esp8266_pwm, pwm.png
    GPIO Output, components/output/gpio, pin.svg
    ESP32 LEDC, components/output/ledc, pwm.png
    PCA9685, components/output/pca9685, pca9685.jpg
    MY9231/MY9291, components/output/my9231, my9231.svg
    Custom Output, components/output/custom, language-cpp.svg

Light Components
----------------

.. imgtable::

    Light Core, components/light/index, folder-open.svg
    Binary Light, components/light/binary, lightbulb.svg
    Monochromatic Light, components/light/monochromatic, brightness-medium.svg

    Cold+Warm White Light, components/light/cwww, brightness-medium.svg
    RGB Light, components/light/rgb, rgb.png
    RGBW Light, components/light/rgbw, rgbw.png

    RGBWW Light, components/light/rgbww, rgbw.png
    FastLED Clockless Light, components/light/fastled_clockless, color_lens.svg
    FastLED SPI Light, components/light/fastled_spi, color_lens.svg

    NeoPixelBus Light, components/light/neopixelbus, color_lens.svg

Looking for WS2811 and similar individually addressable lights? Have a look at the
:doc:`FastLED Clockless Light <components/light/fastled_clockless>`.

Switch Components
-----------------

.. imgtable::

    Switch Core, components/switch/index, folder-open.svg
    GPIO Switch, components/switch/gpio, pin.svg
    Remote Transmitter, components/switch/remote_transmitter, remote.svg
    Restart Switch, components/switch/restart, restart.svg
    Shutdown Switch, components/switch/shutdown, power_settings.svg
    Generic Output Switch, components/switch/output, upload.svg
    Template Switch, components/switch/template, description.svg
    UART Switch, components/switch/uart, uart.svg
    Custom Switch, components/switch/custom, language-cpp.svg

Fan Components
--------------

.. imgtable::

    Fan Core, components/fan/index, folder-open.svg
    Binary Fan, components/fan/binary, fan.svg
    Speed Fan, components/fan/speed, fan.svg

Display Components
------------------

.. imgtable::

    Display Core, components/display/index, folder-open.svg
    GPIO LCD, components/display/lcd_gpio, lcd.jpg
    PCF8574 LCD, components/display/lcd_pcf8574, lcd.jpg
    MAX7219, components/display/max7219, max7219.jpg
    Nextion, components/display/nextion, nextion.jpg
    SSD1306 I2C, components/display/ssd1306_i2c, ssd1306.jpg
    SSD1306 SPI, components/display/ssd1306_spi, ssd1306.jpg
    Waveshare E-Paper, components/display/waveshare_epaper, waveshare_epaper.jpg

Cover Components
----------------

.. imgtable::

    Cover Core, components/cover/index, folder-open.svg
    Template Cover, components/cover/template, description.svg

Text Sensor Components
----------------------

.. imgtable::

    Text Sensor Core, components/text_sensor/index, folder-open.svg
    Home Assistant, components/text_sensor/homeassistant, home-assistant.svg
    MQTT Subscribe Text, components/text_sensor/mqtt_subscribe, mqtt.png
    Version, components/text_sensor/version, new-box.svg
    Template Text Sensor, components/text_sensor/template, description.svg
    Custom Text Sensor, components/text_sensor/custom, language-cpp.svg

Misc Components
---------------

.. imgtable::

    Dallas Hub, components/dallas, dallas.jpg
    Remote Transmitter Hub, components/remote_transmitter, remote.svg
    Remote Receiver Hub, components/remote_receiver, remote.svg
    PCA9685 Hub, components/pca9685, pca9685.jpg
    ADS1115 Hub, components/ads1115, ads1115.jpg
    Debug Component, components/debug, bug-report.svg
    PCF8574 I/O Expander, components/pcf8574, pcf8574.jpg
    ESP32 BLE Tracker, components/esp32_ble_tracker, bluetooth.svg
    ESP32 BLE Beacon, components/esp32_ble_beacon, bluetooth.svg
    ESP32 Touch Hub, components/esp32_touch, touch.svg
    Status LED, components/status_led, led-on.svg
    PN532, components/pn532, pn532.jpg
    RDM6300, components/rdm6300, rdm6300.jpg
    Time, components/time, clock-outline.svg
    Stepper, components/stepper/index, stepper.svg
    MY9231/MY9291 LED driver, components/my9231, my9231.svg
    ESP32 Ethernet, components/ethernet, ethernet.svg

Additional Custom Components
----------------------------

.. imgtable::

    Generic Custom Component, custom/custom_component, language-cpp.svg
    Custom I2C Component, custom/i2c, language-cpp.svg
    Custom SPI Component, custom/spi, language-cpp.svg
    Custom UART Component, custom/uart, language-cpp.svg

.. _cookbook:

Cookbook
--------

This list contains items that are technically already supported by other components.

.. imgtable::

    Garage Door, cookbook/garage-door, window-open.svg
    PIR Sensor, cookbook/pir, pir.jpg
    Relay, cookbook/relay, relay.jpg
    BRUH Multisensor, cookbook/bruh, bruh.png
    TEMT6000, cookbook/temt6000, temt6000.jpg
    Non-Invasive Power Meter, cookbook/power_meter, power_meter.jpg
    Dual Relay Motor Cover, cookbook/dual-r2-cover, sonoff_dual_r2.jpg
    BME280 Environment, cookbook/bme280_environment, bme280.jpg
    Sonoff Fishpond Pump, cookbook/sonoff-fishpond-pump, cookbook-sonoff-fishpond-pump.jpg

Do you have other awesome automations or cool setups? Please feel free to add them to the
documentation for others to copy. See :doc:`Contributing <guides/contributing>`.

.. toctree::
    :hidden:

    components/index
    cookbook/index
    devices/index
    guides/index
    changelog/index
    custom/index
