.. seo::
    :description: IAQ (Indoor Air Quality) Board 
    :image: iaq_board2.jpg
    :keywords: IAQ Board

IAQ (Indoor Air Quality) Board 
==============================

.. figure:: images/iaq_board2.jpg
    :align: center
    :width: 100.0%

IAQ Board is a DIY device for measuring internal air quality running with esphome. It's quite small and is based on a custom PCB where part of the components are soldered and connected.

Here is what it can measure:

- **Temperature / Humidity / Pressure** 
- **Air particles PM1, PM2.5, PM10**
- **Carbon Dioxide with NDIR sensor**
- **Air Quality Index by EPA, based on 24h average PM2.5 particles**
- **Ambient light**
- **Total VOC (volatile organic compound)**
- **equivalent CO2 (not very correct compared with the NDIR sensor, but it's provided by the VOC sensor)**

On top of that:

- **At least one OLED display to show the data (can have one more on the top of the MCU board)**
- **three RGB wide angle LEDs with auto brightness. LED1 indicates PM2.5, LED2 - Air quality index, LED3 - CO2.**
- **auto night dimming of the displays and LEDs (can be disabled)**
- **MIN/MAX values of Temperature, PM2.5 and CO2, and 24h average PM2.5 value.**
- **multi function button for selection of the data to show on the display**

ESPHome Configuration
---------------------
Full documentation (PCB, Schematic, esphome yaml config) is published here: `https://github.com/nkitanov/iaq_board <https://github.com/nkitanov/iaq_board>`__

YAML configuration is about 700 lines and can be downloaded from here: `iaq_board.yaml <https://github.com/nkitanov/iaq_board/blob/master/firmware/iaq_board.yaml>`__

.. figure:: images/iaq_board1.jpg
    :align: center
    :width: 100.0%

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/X75OGs2TTT8" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

See Also
--------

- :doc:`/devices/nodemcu_esp8266`
- :doc:`/components/display/ssd1306`
- :doc:`/components/sensor/bme280`
- :doc:`/components/sensor/pmsx003`
- :doc:`/components/sensor/mhz19`
- :doc:`/components/sensor/sgp30`
- :doc:`/components/sensor/sgp40`
- :doc:`/components/sensor/tsl2561`
- :doc:`/components/binary_sensor/gpio`
- :doc:`/components/sensor/template`
- :doc:`/components/light/neopixelbus`
- :doc:`/guides/automations`
- :doc:`/components/i2c`
- :doc:`/components/uart`
- :ghedit:`Edit`
