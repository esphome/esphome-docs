ESPHome
=======

.. meta::
    :google-site-verification: Q5q5TFbCofxA8-cSa1Frv5Hj4RopF5zwEZf_zaNHqf4

.. seo::
    :description: ESPHome Homepage - Reimagining DIY Home Automation. ESPHome is a framework that
      tries to provide the best possible use experience for using ESP8266 and ESP32 microcontrollers
      for Home Automation. Just write a simple YAML configuration file and get your own customized firmware.
    :image: logo.png

.. image:: /images/logo-text.svg

ESPHome is a system to control your ESP8266/ESP32 by simple yet powerful configuration files and control them remotely through Home Automation systems.

.. raw:: html

    <a href="https://github.com/esphome/esphome"><img src="/_images/shield-github.svg" alt="GitHub" class="index-shield"></a>
    <a href="https://discord.gg/KhAMKrd"><img src="/_images/shield-discord.svg" alt="Discord" class="index-shield"></a>
    <a href="https://twitter.com/esphome_"><img src="/_images/shield-twitter.svg" alt="Twitter" class="index-shield"></a>

.. _guides:

Guides
------

.. imgtable::

    Getting Started through Command Line, guides/getting_started_command_line, console.svg
    Getting Started with Home Assistant Add-on, guides/getting_started_hassio, home-assistant.svg
    FAQ and Tips, guides/faq, question_answer.svg

    Migrating from Tasmota, guides/migrate_sonoff_tasmota, tasmota.svg
    Automations, guides/automations, auto-fix.svg
    Contributing, guides/contributing, github-circle.svg

    Changelog, changelog/index, new-box.svg
    Supporters, guides/supporters, heart.svg
    DIY Examples, guides/diy, earth.svg

    Configuration types, guides/configuration-types, puzzle.svg

.. _devices:

Devices
-------

This list contains a bunch of getting started and more advanced guides for using ESPHome.
Technically, all ESP8266/ESP32 devices are supported by ESPHome.

.. imgtable::

    Generic ESP8266, devices/esp8266, esp8266.svg
    Generic ESP32, devices/esp32, esp32.svg
    NodeMCU ESP8266, devices/nodemcu_esp8266, nodemcu_esp8266.jpg

    NodeMCU ESP32, devices/nodemcu_esp32, nodemcu_esp32.jpg
    Sonoff S20, devices/sonoff_s20, sonoff_s20.jpg
    Sonoff 4CH, devices/sonoff_4ch, sonoff_4ch.jpg

    Generic Sonoff, devices/sonoff, sonoff.svg
    Sonoff Basic, devices/sonoff_basic, sonoff_basic.jpg
    Sonoff T1 UK 3 Gang V1.1, devices/sonoff_t1_uk_3gang_v1.1, sonoff_t1_uk_3g_v1.1.jpg
    Sonoff T3 EU 3 Gang V1.0, devices/sonoff_t3_eu_3gang_v1.0, sonoff_t3_eu_3g_v1.0.jpg

Core Components
---------------

.. imgtable::

    Core, components/esphome, cloud-circle.svg
    WiFi, components/wifi, network-wifi.svg
    MQTT, components/mqtt, mqtt.png

    I²C Bus, components/i2c, i2c.svg
    SPI Bus, components/spi, spi.svg
    UART Bus, components/uart, uart.svg
    CAN Bus, components/canbus, canbus.svg

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
    ADE7953, components/sensor/ade7953, ade7953.svg
    ADS1115, components/sensor/ads1115, ads1115.jpg
    AHT10, components/sensor/aht10, aht10.jpg
    AM2320, components/sensor/am2320, am2320.jpg
    APDS9960, components/sensor/apds9960, apds9960.jpg
    ATM90E32, components/sensor/atm90e32, atm90e32.jpg
    AS3935, components/sensor/as3935, as3935.jpg
    BH1750, components/sensor/bh1750, bh1750.jpg
    Binary Sensor Map, components/sensor/binary_sensor_map, binary_sensor_map.jpg
    BLE RSSI, components/sensor/ble_rssi, bluetooth.svg
    BME280, components/sensor/bme280, bme280.jpg
    BME680, components/sensor/bme680, bme680.jpg
    BMP085, components/sensor/bmp085, bmp180.jpg
    BMP280, components/sensor/bmp280, bmp280.jpg
    CCS811, components/sensor/ccs811, ccs811.jpg
    CSE7766, components/sensor/cse7766, cse7766.svg
    CT Clamp, components/sensor/ct_clamp, ct_clamp.jpg
    Dallas, components/sensor/dallas, dallas.jpg
    DHT, components/sensor/dht, dht.jpg
    DHT12, components/sensor/dht12, dht12.jpg
    Duty Cycle, components/sensor/duty_cycle, percent.svg
    ESP32 Hall Sensor, components/sensor/esp32_hall, magnet.svg
    EZO sensor circuits, components/sensor/ezo, ezo-ph-circuit.png
    HDC1080, components/sensor/hdc1080, hdc1080.jpg
    HLW8012, components/sensor/hlw8012, hlw8012.svg
    HMC5883L, components/sensor/hmc5883l, hmc5883l.jpg
    QMC5883L, components/sensor/qmc5883l, qmc5883l.jpg
    Home Assistant, components/sensor/homeassistant, home-assistant.svg
    HX711, components/sensor/hx711, hx711.jpg
    INA219, components/sensor/ina219, ina219.jpg
    INA226, components/sensor/ina226, ina226.jpg
    INA3221, components/sensor/ina3221, ina3221.jpg
    Integration, components/sensor/integration, sigma.svg
    HTU21D, components/sensor/htu21d, htu21d.jpg
    HM3301, components/sensor/hm3301, hm3301.jpg
    MAX31855, components/sensor/max31855, max31855.jpg
    MAX31856, components/sensor/max31856, max31856.jpg
    MAX31865, components/sensor/max31865, max31865.jpg
    MAX6675, components/sensor/max6675, max6675.jpg
    MCP3008, components/sensor/mcp3008, mcp3008.jpg
    MCP9808, components/sensor/mcp9808, mcp9808.jpg
    MH-Z19, components/sensor/mhz19, mhz19.jpg
    MPU6050, components/sensor/mpu6050, mpu6050.jpg
    MQTT Subscribe, components/sensor/mqtt_subscribe, mqtt.png
    MS5611, components/sensor/ms5611, ms5611.jpg
    NTC Thermistor, components/sensor/ntc, ntc.jpg
    PMSX003, components/sensor/pmsx003, pmsx003.svg
    Pulse Counter, components/sensor/pulse_counter, pulse.svg
    Pulse Width, components/sensor/pulse_width, pulse.svg
    PZEM004T, components/sensor/pzem004t, pzem004t.svg
    PZEM AC, components/sensor/pzemac, pzemac.svg
    PZEM DC, components/sensor/pzemdc, pzemdc.svg
    Resistance, components/sensor/resistance, omega.svg
    Rotary Encoder, components/sensor/rotary_encoder, rotary_encoder.jpg
    RuuviTag, components/sensor/ruuvitag, ruuvitag.jpg
    SenseAir, components/sensor/senseair, senseair_s8.jpg
    SDS011 Sensor, components/sensor/sds011, sds011.jpg
    SCD30, components/sensor/scd30, scd30.jpg
    SHTCx, components/sensor/shtcx, shtc3.jpg
    SHT3X-D, components/sensor/sht3xd, sht3xd.jpg
    SPS30, components/sensor/sps30, sps30.jpg
    STS3X, components/sensor/sts3x, sts3x.jpg
    SGP30, components/sensor/sgp30, sgp30.jpg
    TCS34725, components/sensor/tcs34725, tcs34725.jpg
    Teleinfo, components/sensor/teleinfo, teleinfo.jpg
    Template Sensor, components/sensor/template, description.svg
    TMP102, components/sensor/tmp102, tmp102.jpg
    TMP117, components/sensor/tmp117, tmp117.jpg
    Total Daily Energy, components/sensor/total_daily_energy, sigma.svg
    TSL2561, components/sensor/tsl2561, tsl2561.jpg
    Tuya Sensor, components/sensor/tuya, tuya.png
    TX20, components/sensor/tx20, tx20.jpg
    Ultrasonic Sensor, components/sensor/ultrasonic, ultrasonic.jpg
    Uptime Sensor, components/sensor/uptime, timer.svg
    VL53L0x, components/sensor/vl53l0x, vl53l0x.jpg
    WiFi Signal Strength, components/sensor/wifi_signal, network-wifi.svg
    Xiaomi BLE, components/sensor/xiaomi_ble, xiaomi_mijia_logo.jpg
    ZyAura, components/sensor/zyaura, zgm053.jpg
    Custom Sensor, components/sensor/custom, language-cpp.svg

Looking for a sensor that outputs its values as an analog voltage? Have a look at the
:doc:`ADC Sensor </components/sensor/adc>` together with a formula like in the :doc:`TEMT6000
example </cookbook/temt6000>`.


Binary Sensor Components
------------------------

.. imgtable::

    Binary Sensor Core, components/binary_sensor/index, folder-open.svg
    GPIO, components/binary_sensor/gpio, pin.svg
    Home Assistant, components/binary_sensor/homeassistant, home-assistant.svg
    Status, components/binary_sensor/status, server-network.svg
    ESP32 BLE Presence, components/binary_sensor/ble_presence, bluetooth.svg
    ESP32 Touch Pad, components/binary_sensor/esp32_touch, touch.svg
    MPR121  Capacitive Touch Sensor, components/binary_sensor/mpr121, mpr121.jpg
    Nextion Touch, components/binary_sensor/nextion, nextion.jpg
    Template Binary Sensor, components/binary_sensor/template, description.svg
    PN532, components/binary_sensor/pn532, pn532.jpg
    RC522, components/binary_sensor/rc522, rc522.jpg
    RDM6300, components/binary_sensor/rdm6300, rdm6300.jpg
    TTP229, components/binary_sensor/ttp229, ttp229.jpg
    Tuya Binary Sensor, components/binary_sensor/tuya, tuya.png
    Custom Binary Sensor, components/binary_sensor/custom, language-cpp.svg

Output Components
-----------------

.. imgtable::

    Output Core, components/output/index, folder-open.svg
    ESP8266 Software PWM, components/output/esp8266_pwm, pwm.png
    Slow PWM, components/output/slow_pwm, pwm.png
    GPIO Output, components/output/gpio, pin.svg
    ESP32 DAC, components/output/esp32_dac, dac.svg
    ESP32 LEDC, components/output/ledc, pwm.png
    AC Dimmer, components/output/ac_dimmer, ac_dimmer.svg
    PCA9685, components/output/pca9685, pca9685.jpg
    TLC59208F, components/output/tlc59208f, tlc59208f.jpg
    MY9231/MY9291, components/output/my9231, my9231.svg
    SM16716, components/output/sm16716, sm16716.svg
    Custom Output, components/output/custom, language-cpp.svg
    Template Output, components/output/template, description.svg

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
    FastLED Light, components/light/fastled, color_lens.svg
    NeoPixelBus Light, components/light/neopixelbus, color_lens.svg

    Light Partition, components/light/partition, color_lens.svg
    Tuya Dimmer, components/light/tuya, tuya.png
    Custom Light, components/light/custom, language-cpp.svg

    H-bridge Light, components/light/hbridge, brightness-medium.svg

Looking for WS2811 and similar individually addressable lights? Have a look at the
:doc:`FastLED Light </components/light/fastled>`.

Switch Components
-----------------

.. imgtable::

    Switch Core, components/switch/index, folder-open.svg
    GPIO Switch, components/switch/gpio, pin.svg
    Restart Switch, components/switch/restart, restart.svg
    Shutdown Switch, components/switch/shutdown, power_settings.svg
    Generic Output Switch, components/switch/output, upload.svg
    Template Switch, components/switch/template, description.svg
    UART Switch, components/switch/uart, uart.svg
    Custom Switch, components/switch/custom, language-cpp.svg
    Tuya Switch, components/switch/tuya, tuya.png

Fan Components
--------------

.. imgtable::

    Fan Core, components/fan/index, folder-open.svg
    Binary Fan, components/fan/binary, fan.svg
    Speed Fan, components/fan/speed, fan.svg
    Tuya Fan, components/fan/tuya, tuya.png

Display Components
------------------

.. imgtable::

    Display Core, components/display/index, folder-open.svg
    LCD Display, components/display/lcd_display, lcd.jpg
    MAX7219, components/display/max7219, max7219.jpg
    MAX7219 Dot Matrix, components/display/max7219digit, max7219digit.png
    TM1637, components/display/tm1637, tm1637.jpg
    Nextion, components/display/nextion, nextion.jpg
    SSD1306, components/display/ssd1306, ssd1306.jpg
    SSD1322, components/display/ssd1322, ssd1322.jpg
    SSD1325, components/display/ssd1325, ssd1325.jpg
    SSD1327, components/display/ssd1327, ssd1327.jpg
    SSD1331, components/display/ssd1331, ssd1331.jpg
    SSD1351, components/display/ssd1351, ssd1351.jpg
    ST7735, components/display/st7735, st7735.jpg
    ST7789V, components/display/st7789v, st7789v.jpg
    ILI9341, components/display/ili9341, ili9341.jpg
    Waveshare E-Paper, components/display/waveshare_epaper, waveshare_epaper.jpg
    Inkplate 6, components/display/Inkplate, Inkplate.jpg
    PCD8544 (Nokia 5110/ 3310), components/display/pcd8544, pcd8544.jpg

Cover Components
----------------

.. imgtable::

    Cover Core, components/cover/index, folder-open.svg
    Template Cover, components/cover/template, description.svg
    Endstop Cover, components/cover/endstop, electric-switch.svg
    Time-Based Cover, components/cover/time_based, timer.svg
    Custom Cover, components/cover/custom, language-cpp.svg

Text Sensor Components
----------------------

.. imgtable::

    Text Sensor Core, components/text_sensor/index, folder-open.svg
    Home Assistant, components/text_sensor/homeassistant, home-assistant.svg
    MQTT Subscribe Text, components/text_sensor/mqtt_subscribe, mqtt.png
    Version, components/text_sensor/version, new-box.svg
    WiFi Info, components/text_sensor/wifi_info, network-wifi.svg
    BLE Scanner, components/text_sensor/ble_scanner, bluetooth.svg
    Template Text Sensor, components/text_sensor/template, description.svg
    Custom Text Sensor, components/text_sensor/custom, language-cpp.svg
    Custom UART Text Sensor, components/text_sensor/uart, language-cpp.svg

Climate Components
------------------

.. imgtable::

    Climate Core, components/climate/index, folder-open.svg
    Bang Bang Controller, components/climate/bang_bang, air-conditioner.svg
    Thermostat Controller, components/climate/thermostat, air-conditioner.svg
    Custom Climate, components/climate/custom, language-cpp.svg
    PID Controller, components/climate/pid, function.svg
    IR Remote Climate, components/climate/ir_climate, air-conditioner-ir.svg
    Tuya Climate, components/climate/tuya, tuya.png

Misc Components
---------------

.. imgtable::

    Remote Receiver, components/remote_receiver, remote.svg
    Remote Transmitter, components/remote_transmitter, remote.svg
    Status LED, components/status_led, led-on.svg
    HTTP Request, components/http_request, connection.svg

    Time, components/time, clock-outline.svg
    Sun, components/sun, weather-sunny.svg
    GPS, components/gps, crosshairs-gps.svg

    ESP32 BLE Tracker, components/esp32_ble_tracker, bluetooth.svg
    ESP32 BLE Beacon, components/esp32_ble_beacon, bluetooth.svg
    ESP32 Ethernet, components/ethernet, ethernet.svg

    ESP32 Camera, components/esp32_camera, camera.svg
    Stepper, components/stepper/index, stepper.svg
    Servo, components/servo, servo.svg

    PCF8574 I/O Expander, components/pcf8574, pcf8574.jpg
    MCP230XX I/O Expander - I²C Bus, components/mcp230xx, mcp230xx.svg
    MCP23SXX I/O Expander - SPI Bus, components/mcp23Sxx, mcp230xx.svg
    SX1509 I/O Expander, components/sx1509, sx1509.jpg
    SN74HC595 I/O Expander, components/sn74hc595, sn74hc595.jpg
    SIM800L, components/sim800l, sim800l.jpg
    DFPlayer, components/dfplayer, dfplayer.svg
    Captive Portal, components/captive_portal, wifi-strength-alert-outline.svg
    Debug Component, components/debug, bug-report.svg
    TM1651 Battery Display, components/tm1651, tm1651_battery_display.jpg
    RF Bridge, components/rf_bridge, rf_bridge.jpg
    Tuya MCU, components/tuya, tuya.png
    Exposure Notifications, components/exposure_notifications, exposure_notifications.png
    RTTTL Buzzer, components/rtttl, buzzer.jpg
    Prometheus, components/prometheus, prometheus.svg

Additional Custom Components
----------------------------

.. imgtable::

    Generic Custom Component, custom/custom_component, language-cpp.svg
    Custom I²C Component, custom/i2c, language-cpp.svg
    Custom SPI Component, custom/spi, language-cpp.svg
    Custom UART Component, custom/uart, language-cpp.svg

.. _cookbook:

Cookbook
--------

.. imgtable::

    Arduino Port Extender, cookbook/arduino_port_extender, arduino_logo.svg
    Endstop Cover, cookbook/endstop-cover, window-open.svg
    PIR Sensor, cookbook/pir, pir.jpg
    Relay, cookbook/relay, relay.jpg
    BRUH Multisensor, cookbook/bruh, bruh.png
    TEMT6000, cookbook/temt6000, temt6000.jpg
    Non-Invasive Power Meter, cookbook/power_meter, power_meter.jpg
    Dual Relay Motor Cover, cookbook/dual-r2-cover, sonoff_dual_r2.jpg
    BME280 Environment, cookbook/bme280_environment, bme280.jpg
    Sonoff Fishpond Pump, cookbook/sonoff-fishpond-pump, cookbook-sonoff-fishpond-pump.jpg
    H801 LED Controller, cookbook/h801, h801.jpg
    Time & Temperature on OLED Display, cookbook/display_time_temp_oled, display_time_temp_oled_2.jpg
    Mirabella Genio Bulb, cookbook/mirabella-genio-bulb, cookbook-mirabella-genio-b22-rgbw.jpg
    Garage Door, cookbook/garage-door, window-open.svg
    Brilliant / Mirabella Genio Smart Plugs, cookbook/brilliant-mirabella-genio-smart-plugs, cookbook-brilliant-mirabella-genio-smart-plugs.jpg
    Etekcity Voltson (ESW01-EU) , cookbook/esw01-eu, esw01-eu.jpg
    Sonoff iFan02, cookbook/ifan02, fan.svg
    Zemismart RGBW Downlights, cookbook/zemismart-rgbw-downlights, cookbook-zemismart-rgbw-downlight.jpg
    Teckin SB50, cookbook/teckin_sb50, teckin_sb50.jpg
    Sonoff light switch options, cookbook/sonoff-light-switch, light_switch.png
    ESP32 Water Leak Detector, cookbook/leak-detector-m5stickC, leak-detector-m5stickC_main_index.jpg
    IAQ (Indoor Air Quality) Board, cookbook/iaq_board, iaq_board2.jpg
    IWOOLE Table Lamp, cookbook/iwoole_rgbw_table_lamp, iwoole_rgbw_table_lamp.png

Do you have other awesome automations or cool setups? Please feel free to add them to the
documentation for others to copy. See :doc:`Contributing </guides/contributing>`.

.. toctree::
    :hidden:

    web-api/index
    misc/index
    components/index
    cookbook/index
    devices/index
    guides/index
    changelog/index
    custom/index
    images/index
