.. meta::
    :google-site-verification: Q5q5TFbCofxA8-cSa1Frv5Hj4RopF5zwEZf_zaNHqf4

.. seo::
    :description: ESPHome Homepage - Reimagining DIY Home Automation. ESPHome is a framework that
      tries to provide the best possible use experience for using ESP8266 and ESP32 microcontrollers
      for Home Automation. Just write a simple YAML configuration file and get your own customized firmware.
    :image: logo.png

.. image:: /images/logo-text.svg

ESPHome is a system to control your ESP8266/ESP32 by simple yet powerful configuration files and control them remotely through Home Automation systems.

.. image:: /images/hero.png

.. raw:: html

    <div class="guide-container">
        <div class="guide-card">
            <h3 class="guide-card-title">Getting started</h3>
            <ul>
                <li>
                    <a class="reference" href="/guides/getting_started_hassio.html">
                        ESPHome Dashboard
                    </a>
                </li>
                <li>
                    <a class="reference" href="/guides/getting_started_command_line.html">
                        Command Line Interface
                    </a>
                </li>
                <li>
                    <a class="reference" href="/guides/migrate_sonoff_tasmota.html">
                        Migrating from Tasmota
                    </a>
                </li>
            </ul>
            <pre class="guide-code">
                esphome:
                &nbsp;&nbsp;name: awesome
                &nbsp;&nbsp;platform: ESP32
                &nbsp;&nbsp;board: nodemcu-32s
            </pre>
        </div>
        <div class="guide-card">
            <h3 class="guide-card-title">Next steps</h3>
            <ul>
                <li>
                    <a class="reference" href="/guides/faq.html">
                        FAQ and Tips
                    </a>
                </li>
                <li>
                    <a class="reference" href="/guides/automations.html">
                        Automations
                    </a>
                </li>
                <li>
                    <a class="reference" href="/guides/diy.html">
                        DIY Examples
                    </a>
                </li>
                <li>
                    <a class="reference" href="/guides/configuration-types.html">
                        Configuration types
                    </a>
                </li>
                <li>
                    <a class="reference" href="/guides/creators.html">
                        Creating a Project
                    </a>
                </li>
            </ul>
        </div>
        <div class="guide-card">
            <h3 class="guide-card-title">Keeping up</h3>
            <ul>
                <li>
                    <a class="reference" href="/changelog/index.html">
                        Changelog
                    </a>
                </li>
                <li>
                    <a class="reference" href="/guides/supporters.html">
                        Supporters
                    </a>
                </li>
                <li>
                    <a class="reference" href="/guides/contributing.html">
                        Contributing
                    </a>
                </li>
            </ul>
        </div>
    </div>

.. _devices:

General ESPHome
---------------

Automations
***********

.. raw:: html

    <p>
    <A href="/guides/automations.html">Automations</A> allow you to perform actions under certain conditions and <a href="/guides/automations.html#templates-lambdas"> templates (lambdas)</A> are a way to easily customize everything about your node, using short snippets of C++ code.
    </p>

Configuration Types
*******************

.. raw:: html

    <p>
    <a href="/guides/configuration-types.html">Configuration Types</a> covers naming of your components with "ID", how to reference GPIO pins and configure them as input or output, pullups / pull downs etc and use substitutions which are like #defines in C++.
    </p>

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
    External Components, components/external_components, external_components.svg

Sensor Components
-----------------

Sensors have been split into categories. If a sensors fits into more than one categoey, it will be listed multiple times.

Core / Home Assistant
*********************
.. imgtable::

    Sensor Core, components/sensor/index, folder-open.svg
    Custom Sensor, components/sensor/custom, language-cpp.svg
    Home Assistant, components/sensor/homeassistant, home-assistant.svg
    Integration, components/sensor/integration, sigma.svg
    MQTT Subscribe, components/sensor/mqtt_subscribe, mqtt.png
    Resistance, components/sensor/resistance, omega.svg
    Template Sensor, components/sensor/template, description.svg
    Uptime Sensor, components/sensor/uptime, timer.svg
    WiFi Signal Strength, components/sensor/wifi_signal, network-wifi.svg


Air Quality / Gas
*****************
.. imgtable::

    CCS811 (CO2 & volatile organics), components/sensor/ccs811, ccs811.jpg
    MH-Z19 (CO2 & temperature), components/sensor/mhz19, mhz19.jpg
    HM3301 (particulate), components/sensor/hm3301, hm3301.jpg
    PMSX003 (particulate), components/sensor/pmsx003, pmsx003.svg
    SenseAir (CO2), components/sensor/senseair, senseair_s8.jpg
    SDS011 Sensor (particulate), components/sensor/sds011, sds011.jpg
    SM300D2 (air quality), components/sensor/sm300d2, sm300d2.jpg
    SPS30 (particulate), components/sensor/sps30, sps30.jpg
    STS3X (temperature), components/sensor/sts3x, sts3x.jpg
    SGP30 (CO2 & volatile organic), components/sensor/sgp30, sgp30.jpg
    SGP40 (volatile organic), components/sensor/sgp40, sgp40.jpg
    ZyAura (CO2 & temp & humidity), components/sensor/zyaura, zgm053.jpg


Ambient Light / Colour
**********************
.. imgtable::

    APDS9960 (Colour & gesture), components/sensor/apds9960, apds9960.jpg
    BH1750 (lux), components/sensor/bh1750, bh1750.jpg
    TCS34725 (lux & RGB colour), components/sensor/tcs34725, tcs34725.jpg
    TSL2561 (lux), components/sensor/tsl2561, tsl2561.jpg
    Teleinfo (RGB colour), components/sensor/teleinfo, teleinfo.jpg


Analogue To Digital
*******************
.. imgtable::

    ADC, components/sensor/adc, flash.svg
    ADS1115 (4-ch A/D), components/sensor/ads1115, ads1115.jpg
    MCP3008 (8-ch A/D), components/sensor/mcp3008, mcp3008.jpg


Bluetooth Low Energy (BLE)
**************************
.. imgtable::

    BLE RSSI, components/sensor/ble_rssi, bluetooth.svg
    BLE Client Sensor, components/sensor/ble_client, bluetooth.svg
    Inkbird IBS-TH1 Mini (temp & humid), components/sensor/inkbird_ibsth1_mini, inkbird_isbth1_mini.jpg
    Xiaomi BLE (various), components/sensor/xiaomi_ble, xiaomi_mijia_logo.jpg
    RuuviTag (temp & humid & accelerometer), components/sensor/ruuvitag, ruuvitag.jpg


Digital Signals
***************
.. imgtable::

    Duty Cycle, components/sensor/duty_cycle, percent.svg
    Pulse Counter, components/sensor/pulse_counter, pulse.svg
    Pulse Meter, components/sensor/pulse_meter, pulse.svg
    Pulse Width, components/sensor/pulse_width, pulse.svg


Distance
********
.. imgtable::

    Ultrasonic Sensor (distance), components/sensor/ultrasonic, ultrasonic.jpg
    TOF10120 (IR optical distance), components/sensor/tof10120, tof10120.jpg
    VL53L0x (IR optical distance), components/sensor/vl53l0x, vl53l0x.png


Load Cell (Force / Weight)
**************************
.. imgtable::

    HX711 (load cell amp), components/sensor/hx711, hx711.jpg
    Xiaomi Miscale, components/sensor/xiaomi_miscale, xiaomi_miscale.jpg
    Xiaomi Miscale2, components/sensor/xiaomi_miscale2, xiaomi_miscale2.jpg


Magnetic / Hall Effect
**********************
.. imgtable::
    
    ESP32 Hall Sensor, components/sensor/esp32_hall, magnet.svg
    HMC5883L (3 axis magnetometer), components/sensor/hmc5883l, hmc5883l.jpg
    QMC5883L (3 axis magnetometer), components/sensor/qmc5883l, qmc5883l.jpg    


Miscellaneous
*************
.. imgtable::

    AS3935 (Storm Lightning), components/sensor/as3935, as3935.jpg
    Binary Sensor Map (binary to value), components/sensor/binary_sensor_map, binary_sensor_map.jpg
    b-parasite (moisture temp humid), components/sensor/b_parasite, b_parasite.jpg
    EZO sensor circuits (pH), components/sensor/ezo, ezo-ph-circuit.png
    Nextion (sensors from display), components/sensor/nextion, nextion.jpg
    Rotary Encoder, components/sensor/rotary_encoder, rotary_encoder.jpg
    Tuya Sensor (countdown timer), components/sensor/tuya, tuya.png
    TX20 (wind speed & direction), components/sensor/tx20, tx20.jpg

Motion, Gesture
****************
.. imgtable::

    APDS9960 (Colour and gesture), components/sensor/apds9960, apds9960.jpg
    MPU6050 (accelerometer & gyroscope), components/sensor/mpu6050, mpu6050.jpg
    RuuviTag (temp & humid & accelerometer), components/sensor/ruuvitag, ruuvitag.jpg


Current / Power / Energy
**********************
.. imgtable::

    ADE7953 (power), components/sensor/ade7953, ade7953.svg
    ATM90E32 (voltage current power), components/sensor/atm90e32, atm90e32.jpg
    CSE7766 (voltage current power), components/sensor/cse7766, cse7766.svg
    CS5460A (voltage current power), components/sensor/cs5460a, cs5460a.png
    CT Clamp (AC current), components/sensor/ct_clamp, ct_clamp.jpg
    HLW8012 (voltage current power), components/sensor/hlw8012, hlw8012.svg
    INA219 (DC current), components/sensor/ina219, ina219.jpg
    INA226 (DC current power), components/sensor/ina226, ina226.jpg
    INA3221 (3-ch DC current), components/sensor/ina3221, ina3221.jpg
    PZEM004T (voltage current power), components/sensor/pzem004t, pzem004t.svg
    PZEM AC (voltage current power freq pf), components/sensor/pzemac, pzem-ac.png
    PZEM DC (voltage current power), components/sensor/pzemdc, pzem-dc.png
    SDM Meter (modbus energy monitor), components/sensor/sdm_meter, sdm220m.png
    Total Daily Energy, components/sensor/total_daily_energy, sigma.svg

Solar (PV) Inverters
********************
.. imgtable::

    Havells Inverter (Solar rooftop), components/sensor/havells_inverter, havellsgti5000d_s.jpg


Temperature / Humidity / Pressure
********************************************

.. Note::

    "temp" = Temperature

    "humid" = Relative Humidity

    "baro" = Barometric Pressure (i.e. atmospheric pressure)

.. imgtable::
    
    AHT10 (temp & humid), components/sensor/aht10, aht10.jpg
    AM2320 (temp & humid), components/sensor/am2320, am2320.jpg
    BMP085 (temp & baro), components/sensor/bmp085, bmp180.jpg
    BMP280 (temp & humid & baro), components/sensor/bmp280, bmp280.jpg
    BME280 (temp & humid & baro), components/sensor/bme280, bme280.jpg
    BME680 (temp & humid & baro & gas), components/sensor/bme680, bme680.jpg
    BME680 via BSEC, components/sensor/bme680_bsec, bme680.jpg
    b-parasite (moisture temp humid), components/sensor/b_parasite, b_parasite.jpg    
    Dallas DS18B20 (temperature), components/sensor/dallas, dallas.jpg
    DHT (temp & humid), components/sensor/dht, dht.jpg
    DHT12 (temp & humid), components/sensor/dht12, dht12.jpg
    HDC1080 (temp & humid), components/sensor/hdc1080, hdc1080.jpg
    HTU21D (temp & humid), components/sensor/htu21d, htu21d.jpg
    Inkbird IBS-TH1 Mini (temp & humid), components/sensor/inkbird_ibsth1_mini, inkbird_isbth1_mini.jpg
    MS5611 (baro), components/sensor/ms5611, ms5611.jpg
    NTC Thermistor (temp), components/sensor/ntc, ntc.jpg
    TMP102 (temp), components/sensor/tmp102, tmp102.jpg
    TMP117 (temp), components/sensor/tmp117, tmp117.jpg
    MCP9808 (temp), components/sensor/mcp9808, mcp9808.jpg
    MH-Z19 (CO2 & temp), components/sensor/mhz19, mhz19.jpg
    RuuviTag (temp & humid & accelerometer), components/sensor/ruuvitag, ruuvitag.jpg
    SCD30 (temp & humid), components/sensor/scd30, scd30.jpg
    SHTCx (temp & humid), components/sensor/shtcx, shtc3.jpg
    SHT3X-D (temp & humid), components/sensor/sht3xd, sht3xd.jpg
    SHT4X (temp & humid), components/sensor/sht4x, sht4x.jpg


Thermocouple
************
.. imgtable::

    MAX31855 (K-Type via SPI), components/sensor/max31855, max31855.jpg
    MAX31856 (All types via SPI), components/sensor/max31856, max31856.jpg
    MAX31865 (Platinum RTD via SPI), components/sensor/max31865, max31865.jpg
    MAX6675 (K-Type via SPI), components/sensor/max6675, max6675.jpg


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
    Nextion Binary Sensor, components/binary_sensor/nextion, nextion.jpg
    Template Binary Sensor, components/binary_sensor/template, description.svg
    PN532, components/binary_sensor/pn532, pn532.jpg
    RC522, components/binary_sensor/rc522, rc522.jpg
    RDM6300, components/binary_sensor/rdm6300, rdm6300.jpg
    TTP229, components/binary_sensor/ttp229, ttp229.jpg
    Tuya Binary Sensor, components/binary_sensor/tuya, tuya.png
    XPT2046, components/binary_sensor/xpt2046, xpt2046.jpg
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
    SM2135, components/output/sm2135, sm2135.svg
    MCP4725, components/output/mcp4725, mcp4725.jpg
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
    BLE Client Switch, components/switch/ble_client, bluetooth.svg
    Nextion Switch, components/switch/nextion, nextion.jpg

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
    Addressable Light, components/display/addressable_light, addressable_light.jpg
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
    Inkplate 6, components/display/inkplate6, inkplate6.jpg
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
    Nextion Text Sensor, components/text_sensor/nextion, nextion.jpg

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
    Midea Air Conditioner, components/climate/midea_ac, midea.svg
    Anova Cooker, components/climate/anova, anova.png

Number Components
-----------------

.. imgtable::

    Number Core, components/number/index, folder-open.svg
    Template Number, components/number/template, description.svg

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

    ESP32 BLE Client, components/ble_client, bluetooth.svg
    ESP32 BLE Tracker, components/esp32_ble_tracker, bluetooth.svg
    ESP32 BLE Beacon, components/esp32_ble_beacon, bluetooth.svg
    ESP32 Ethernet, components/ethernet, ethernet.svg

    ESP32 Camera, components/esp32_camera, camera.svg
    Stepper, components/stepper/index, stepper.svg
    Servo, components/servo, servo.svg

    PCF8574 I/O Expander, components/pcf8574, pcf8574.jpg
    MCP230XX I/O Expander - I²C Bus, components/mcp230xx, mcp230xx.svg
    TCA9548A I²C Multiplexer, components/tca9548a, tca9548a.jpg
    MCP23SXX I/O Expander - SPI Bus, components/mcp23Sxx, mcp230xx.svg
    SX1509 I/O Expander, components/sx1509, sx1509.jpg
    SN74HC595 I/O Expander, components/sn74hc595, sn74hc595.jpg
    SIM800L, components/sim800l, sim800l.jpg
    DFPlayer, components/dfplayer, dfplayer.svg
    Captive Portal, components/captive_portal, wifi-strength-alert-outline.svg
    Improv, components/esp32_improv, improv.svg
    Debug Component, components/debug, bug-report.svg
    TM1651 Battery Display, components/tm1651, tm1651_battery_display.jpg
    RF Bridge, components/rf_bridge, rf_bridge.jpg
    Tuya MCU, components/tuya, tuya.png
    Exposure Notifications, components/exposure_notifications, exposure_notifications.png
    RTTTL Buzzer, components/rtttl, buzzer.jpg
    Prometheus, components/prometheus, prometheus.svg
    Grow Fingerprint Reader, components/fingerprint_grow, fingerprint.svg

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
    ESP32 BLE iTag Button, cookbook/ble_itag, esp32_ble_itag.jpg
    IAQ (Indoor Air Quality) Board, cookbook/iaq_board, iaq_board2.jpg
    Custom UART Text Sensor, cookbook/uart_text_sensor, language-cpp.svg
    IWOOLE Table Lamp, cookbook/iwoole_rgbw_table_lamp, iwoole_rgbw_table_lamp.png
    Ilonda Wifi Smart Fish Feeder, cookbook/ilonda-wifi-smart-fish-feeder, ilonda-wifi-smart-fish-feeder-cookbook.jpg

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
