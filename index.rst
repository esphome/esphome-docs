.. title:: ESPHome

.. meta::
    :google-site-verification: Q5q5TFbCofxA8-cSa1Frv5Hj4RopF5zwEZf_zaNHqf4

.. seo::
    :description: ESPHome Homepage - Reimagining DIY Home Automation. ESPHome is a framework that
      tries to provide the best possible use experience for using ESP8266 and ESP32 microcontrollers
      for Home Automation. Just write a simple YAML configuration file and get your own customized firmware.
    :image: logo.svg

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
                        from Home Assistant
                    </a>
                </li>
                <li>
                    <a class="reference" href="/guides/getting_started_command_line.html">
                        using the command line
                    </a>
                </li>
                <li>
                    <a class="reference" href="/guides/migrate_sonoff_tasmota.html">
                        by migrating from Tasmota
                    </a>
                </li>
            </ul>
            <pre class="guide-code">
                esphome:
                &nbsp;&nbsp;name: awesome
                esp32:
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
                        Sharing ESPHome devices
                    </a>
                </li>
                <li>
                    <a class="reference" href="/guides/made_for_esphome.html">
                        Made for ESPHome program
                    </a>
                </li>
            </ul>
        </div>
        <div class="guide-card">
            <h3 class="guide-card-title">Keeping up</h3>
            <ul>
                <li>
                    <a class="reference" href="https://discord.gg/KhAMKrd" target="_blank">
                        Discord
                    </a>
                </li>
                <li>
                    <a class="reference" href="https://community.home-assistant.io/c/esphome/" target="_blank">
                        Forums
                    </a>
                </li>
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

Devices
========

This list contains a bunch of getting started and more advanced guides for using ESPHome.
Technically, all ESP8266/ESP32 devices are supported by ESPHome.

.. esphome:index:: Devices

Components
==========

Core Components
---------------

.. esphome:index:: Components
  :toc_group: Core Components

Sensor Components
-----------------

Sensors have been split into categories. If a sensor fits into more than one category, it will be listed multiple times.

Core
****

.. esphome:index:: Components
  :toc_group: Core Sensors

Air Quality
***********

.. esphome:index:: Components
  :toc_group: Air Quality Sensors

Analogue
********

.. esphome:index:: Components
  :toc_group: Analogue Sensors

Bluetooth Low Energy (BLE)
**************************

.. esphome:index:: Components
  :toc_group: Bluetooth Low Energy (BLE) Sensors

Digital Signals
***************

.. esphome:index:: Components
  :toc_group: Digital Signal Sensors

Distance
********

.. esphome:index:: Components
  :toc_group: Distance Sensors

Electricity
***********

.. esphome:index:: Components
  :toc_group: Electrical Sensors

Environmental
*************

.. esphome:index:: Components
  :toc_group: Environmental Sensors

Light
*****

.. esphome:index:: Components
  :toc_group: Light Sensors

Magnetic
********

.. esphome:index:: Components
  :toc_group: Magnetic Sensors

Miscellaneous
*************

.. esphome:index:: Components
  :toc_group: Miscellaneous Sensors

Motion
******

.. esphome:index:: Components
  :toc_group: Motion Sensors

Thermocouple
************

.. esphome:index:: Components
  :toc_group: Thermocouple Sensors


Weight
******

.. esphome:index:: Components
  :toc_group: Weight Sensors

Looking for a sensor that outputs its values as an analog voltage? Have a look at the
:doc:`ADC Sensor </components/sensor/adc>` together with a formula like in the :doc:`TEMT6000
example </cookbook/temt6000>`.


Binary Sensor Components
------------------------

.. esphome:index:: Components
  :toc_group: Binary Sensor Components

Output Components
-----------------

.. esphome:index:: Components
  :toc_group: Output Components

Light Components
----------------

.. esphome:index:: Components
  :toc_group: Light Components

Looking for WS2811 and similar individually addressable lights? Have a look at the
:doc:`FastLED Light </components/light/fastled>`.

Switch Components
-----------------

.. esphome:index:: Components
  :toc_group: Switch Components

Button Components
-----------------

.. esphome:index:: Components
  :toc_group: Button Components

Fan Components
--------------

.. esphome:index:: Components
  :toc_group: Fan Components

Display Components
------------------

.. esphome:index:: Components
  :toc_group: Display Components

Touchscreen Components
----------------------

.. esphome:index:: Components
  :toc_group: Touchscreen Components

Cover Components
----------------

.. esphome:index:: Components
  :toc_group: Cover Components

Text Sensor Components
----------------------

.. esphome:index:: Components
  :toc_group: Text Sensor Components

Climate Components
------------------

.. esphome:index:: Components
  :toc_group: Climate Components

Number Components
-----------------

.. esphome:index:: Components
  :toc_group: Number Components

Select Components
-----------------

.. esphome:index:: Components
  :toc_group: Select Components

Lock Components
-----------------

.. esphome:index:: Components
  :toc_group: Lock Components

Media Player Components
-----------------------

.. esphome:index:: Components
  :toc_group: Media Player Components

Miscellaneous Components
-------------------------

.. esphome:index:: Components
  :toc_group: Miscellaneous Components

Additional Custom Components
----------------------------

.. esphome:index:: Components
  :toc_group: Additional Custom Components

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
    TUYA Smart Life RGBW Controller, cookbook/tuya_rgbw, tuya_rgbw.jpg
    Custom UART Text Sensor, cookbook/uart_text_sensor, language-cpp.svg
    IWOOLE Table Lamp, cookbook/iwoole_rgbw_table_lamp, iwoole_rgbw_table_lamp.png
    EPEVER Tracer, cookbook/tracer-an, tracer-an.jpg
    Ilonda Wifi Smart Fish Feeder, cookbook/ilonda-wifi-smart-fish-feeder, ilonda-wifi-smart-fish-feeder-cookbook.jpg
    AirGradient DIY Air Quality Sensor, cookbook/air_gradient_diy_air_quality_sensor, air_gradient_diy_air_quality_sensor.jpg

Do you have other awesome automations or cool setups? Please feel free to add them to the
documentation for others to copy. See :doc:`Contributing </guides/contributing>`.

.. toctree::
    :hidden:

    web-api/index
    components/index
    cookbook/index
    devices/index
    guides/index
    changelog/index
    custom/index
    images/index
