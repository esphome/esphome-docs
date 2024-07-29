Absolute Humidity
=================

.. seo::
    :description: Instructions for setting up absolute humidity calculation
    :image: water-drop.svg

The ``absolute_humidity`` platform allows you to calculate absolute humidity from air temperature and relative humidity.

See the links at the bottom of the page for details on absolute humidity and the different saturated vapor pressure equations.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: absolute_humidity
        name: Absolute Humidity
        temperature: air_temperature
        humidity: relative_humidity

      # Use any temperature and relative humidity source, e.g. a BME280:
      - platform: ...
        temperature:
          name: Temperature
          id: air_temperature
        humidity:
          name: Relative Humidity
          id: relative_humidity
    
    # Complete  yaml example with a HDC3020 temperature humidity sensor 
    # Added and Id (abHumidity4) to display the absolute humidity on an OLED display 
    esphome:
  name: sensor1
  friendly_name: Demo

esp32:
  board: esp32-c3-devkitm-1
  framework:
    type: arduino

# Enable logging
logger:

# Enable Home Assistant API
api:
  encryption:
    key: "da5j6DRLuSO3mjiS6ihVwxqu5kVsu0Q6QoNm0/ME1O4="

ota:
  - platform: esphome
    password: "75b695ebdd1cb8b4aa4ff39654a4b0ed"

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  # Enable fallback hotspot (captive portal) in case wifi connection fails
  ap:
    ssid: "Sensor1 Fallback Hotspot"
    password: "VbWEDXbmtuRk"

captive_portal:


external_components:
  - source: config/my_components
    components: hdc3020

i2c:
  sda: GPIO5
  scl: GPIO6
  scan: false

sensor:
  - platform: hdc3020
    address: 0x44
    temperature:
      name: "Outside Temperature"
      id: temperature4
    humidity:
      name: "Outside Humidity"
      id: humidity4
    update_interval: 10s
  - platform: absolute_humidity
    name: Absolute Humidity
    id:   abHumidity4
    temperature: temperature4
    humidity: humidity4


font:
  - file: "config/arial.ttf"
    id: my_font
    size: 26

display:
  - platform: ssd1306_i2c
    model: "SSD1306 128x64"
    address: 0x3c
    lambda: |-
      it.printf(12,8,id(my_font),TextAlign::LEFT,"%.1f°C", id(temperature4).state);
      it.printf(12,36,id(my_font),TextAlign::LEFT,"%.1f g/m3", id(abHumidity4).state);

deep_sleep:
  id: deep_sleep_1
  run_duration: 18s  # must be long enough to wirelessly update after a rest or power up
  sleep_duration: 5min # must be long enough to cool down board for accurate temperature
----------------------------------

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the absolute humidity sensor.
- **temperature** (**Required**, :ref:`config-id`): The sensor that is used to measure the current temperature, in °C.
- **humidity** (**Required**, :ref:`config-id`): The sensor that is used to measure the current relative humidity, in %.
- **equation** (*Optional*): The saturated vapor pressure equation to use (see below).
- All other options from :ref:`Sensor <config-sensor>`.

Saturated vapor pressure equations
----------------------------------

There are several different equations for calculating saturated vapor pressure.
``Wobus`` is used by default, as it is notionally the most accurate, but any of the following can be used:

- ``Buck``: `Arden Buck equation <https://en.wikipedia.org/wiki/Arden_Buck_equation>`__
- ``Tetens``: `Tetens equation <https://en.wikipedia.org/wiki/Tetens_equation>`__
- ``Wobus``: `Wobus equation <https://wahiduddin.net/calc/density_altitude.htm>`__

See Also
--------

- :ref:`sensor-filters`
- :apiref:`absolute_humidity/absolute_humidity.h`
- `NOAA Discussion on Humidity <https://www.weather.gov/lmk/humidity>`__
- `Absolute humidity on Wikipedia <https://en.wikipedia.org/wiki/Humidity#Absolute_humidity>`__
- `How to calculate absolute humidity <https://www.environmentalbiophysics.org/chalk-talk-how-to-calculate-absolute-humidity/>`__
- `How to convert relative humidity to absolute humidity <https://carnotcycle.wordpress.com/2012/08/04/how-to-convert-relative-humidity-to-absolute-humidity/>`__
- :ghedit:`Edit`
