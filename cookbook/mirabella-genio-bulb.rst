Mirabella Genio Bulbs
=====================

The Mirabella Genio is a Tuya based smart bulb sold by Kmart in Australia. 

.. figure:: images/mirabella-genio-b22-rgbw.jpg
    :align: center
    :width: 50.0%

Originally intended to be used with their companion app once flashed using `tuya-convert <https://github.com/ct-Open-Source/tuya-convert>`__ ESPHome generated firmware can be uploaded allowing you to control the bulbs via Home Assistant.

Thanks to the `existing work <https://github.com/arendst/Sonoff-tasmota/wiki/Mirabella-Genio-Bulb>`__ by `@so3n <https://github.com/arendst/Sonoff-tasmota/wiki/Mirabella-Genio-Bulb>`__ which these adaptions created by `@cryptelli <https://community.home-assistant.io/u/cryptelli>`__ and `@bircoe <https://community.home-assistant.io/u/bircoe>`__ are based on.

Dimmable Warm/Cool White Bulbs
------------------------------

.. code-block:: yaml

    esphome:
      name: mirabella_genio_cw_1
      platform: ESP8266
      board: esp01_1m

      # Ensure the light turns on by default if the physical switch is actuated.
      # https://esphome.io/components/esphome#esphome-on-boot
      on_boot:
        priority: 100 # Highest priority, ensures light turns on without delay.
        then:
          - light.turn_on: light

    wifi:
      ssid: 'WIFI'
      password: 'WIFIPASS'

    logger:

    web_server:
      port: 80

    api:

    ota:

    light:
      - platform: monochromatic
        name: "Mirabella Genio Smart Bulb"
        id: light
        output: output_component1

    output:
      - platform: esp8266_pwm
        id: output_component1
        pin: GPIO13

Tunable Warm/Cool White Bulbs
-----------------------------

.. code-block:: yaml

    esphome:
      name: mirabella_genio_cwww_1
      platform: ESP8266
      board: esp01_1m

      # Ensure the light turns on by default if the physical switch is actuated.
      # https://esphome.io/components/esphome#esphome-on-boot
      on_boot:
        priority: 100 # Highest priority, ensures light turns on without delay.
        then:
          - light.turn_on: light
      
    wifi:
      ssid: 'WIFI'
      password: 'WIFIPASS'

    logger:

    web_server:
      port: 80

    api:

    ota:

    output:
      - platform: esp8266_pwm
        id: output_warm_white
        pin: GPIO14
      - platform: esp8266_pwm
        id: output_daylight
        pin: GPIO5

    light:
      - platform: cwww
        name: "Mirabella Genio Smart Bulb"
        id: light
        cold_white: output_daylight
        warm_white: output_warm_white
        cold_white_color_temperature: 6500 K
        warm_white_color_temperature: 2700 K

RGBW Colour Bulbs
-----------------

.. code-block:: yaml

    esphome:
      name: rgbw_e27_01
      platform: ESP8266
      board: esp01_1m

      # Ensure the light turns on by default if the physical switch is actuated.
      # https://esphome.io/components/esphome#esphome-on-boot
      on_boot:
        priority: 100 # Highest priority, ensures light turns on without delay.
        then:
          - light.turn_on: light

    wifi:
      ssid: 'WIFI'
      password: 'WIFIPASS'

    logger:

    web_server:
      port: 80

    api:

    ota:

    output:
      - platform: esp8266_pwm
        id: output_red
        pin: GPIO4
      - platform: esp8266_pwm
        id: output_green
        pin: GPIO12
      - platform: esp8266_pwm
        id: output_blue
        pin: GPIO14
      - platform: esp8266_pwm
        id: output_white
        pin: GPIO5

    light:
      - platform: rgbw
        name: "rgbw_e27_01"
        id: light
        red: output_red
        green: output_green
        blue: output_blue
        white: output_white


Addding to Home Assistant
-------------------------

You can now add your bulb to home assistant via the configurations page, look for 'ESPHome' under the Integrations option and click 'Configure'.


See Also
--------

- `Flashing using tuya-convert <http://www.thesmarthomehookup.com/tuya-convert-walk-through-february-2019/>`__
- :doc:`/components/light/index`
- :doc:`/components/light/monochromatic`
- :doc:`/components/light/cwww`
- :doc:`/components/light/rgbw`
- :doc:`/components/output/index`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/guides/automations`
- :ghedit:`Edit`

.. disqus::
