Sonoff Fish Pond Pump
=====================

.. seo::
    :description: Firmware for an Sonoff S2X smart switch 
    :image: images/sonoff-s2x.jpg
    :keywords: sonoff, esp8266, home assistant, smart socket

.. figure:: images/sonoff-s2x.jpg
    :align: center
    :width: 30.0%

This is a basic firmware for the Sonoff S2X smart switch series. The features are:
 
* The switch is automatically registered to HA via the api.
* A *single click* toggles the relay (works offline).
* A *double click*, a *triple click*, or a *longpress* triggers custom actions on HA. 

.. warning::

    Do NOT connect your device to the mains when programming it.
    Take care working with the mains voltage at all times!

1. Preparation
--------------
Prepare your socket according to these instructions 

- :doc:`Sonoff S20 </esphomeyaml/devices/sonoff_s20>`
- `Sonoff S26 <https://github.com/arendst/Sonoff-Tasmota/wiki/Sonoff-S26-Smart-Socket/>`

2. ESPHome Configuration
------------------------

Here is the configuration with the basic operations outlined above.

.. code-block:: yaml

    substitutions:
      devicename: sonoff1

    esphomeyaml:
      name: $devicename
      platform: ESP8266
      board: esp01_1m
      board_flash_mode: dout


    wifi:
      networks:
        - ssid: !secret wifi_ssid
          password: !secret wifi_password
        - ssid: !secret wifi_ssid2
          password: !secret wifi_password2
    
    api:

    logger:
      level: debug

    debug:

    ota:

    binary_sensor:
      - platform: gpio
        pin:
          number: GPIO0
          mode: INPUT_PULLUP
          inverted: True
        name: "Button"
        internal: True

        on_press:
          then:
            - light.turn_on:
                id: green_led_light
                transition_length: 0s
        
        on_release:
          then:
            - light.turn_off:
                id: green_led_light
                transition_length: 0s

        on_multi_click:
        - timing: # Double Clicked
            - ON for at most 1s
            - OFF for at most 1s
            - ON for at most 1s
            - OFF for at least 0.2s
          then:
            - logger.log: "Double Clicked"
            - lambda: |-  # turn our binary sensor on
                id(double_click).publish_state(true);
            - light.turn_on: # give visual feedback with the green led
                id: green_led_light
                transition_length: 0.5s
            - delay: 0.5s
            - light.turn_off:
                id: green_led_light
                transition_length: 0.5s
            - delay: 0.5s
            - light.turn_on:
                id: green_led_light
                transition_length: 0.5s
            - delay: 0.5s
            - light.turn_off:
                id: green_led_light
                transition_length: 0.5s
            - lambda: |-   # turn our binary sensor off again
                id(double_click).publish_state(false);

        - timing: # Triple Clicked
            - ON for at most 1s
            - OFF for at most 1s
            - ON for at most 1s
            - OFF for at most 1s
            - ON for at most 1s
            - OFF for at least 0.2s
          then:
            - logger.log: "Triple Clicked"
            - lambda: |-  # turn our binary sensor on
                id(triple_click).publish_state(true);
            - light.turn_on: # give visual feedback with the green led
                id: green_led_light
                transition_length: 0.5s
            - delay: 0.5s
            - light.turn_off:
                id: green_led_light
                transition_length: 0.5s
            - delay: 0.5s
            - light.turn_on:
                id: green_led_light
                transition_length: 0.5s
            - delay: 0.5s
            - light.turn_off:
                id: green_led_light
                transition_length: 0.5s
            - delay: 0.5s
            - light.turn_on:
                id: green_led_light
                transition_length: 0.5s
            - delay: 0.5s
            - light.turn_off:
                id: green_led_light
                transition_length: 0.5s
            - lambda: |-    # turn our binary sensor off again
                id(triple_click).publish_state(false);

        - timing: # Single Long Clicked
            - ON for 1s to 3s
            - OFF for at least 0.5s
          then:
            - logger.log: "Single Long Clicked"
            - lambda: |-  # turn our binary sensor on
                id(long_click).publish_state(true);
            - light.turn_on: # give visual feedback with the green led
                id: green_led_light
                transition_length: 0.5s
            - delay: 0.5s
            - light.turn_off:
                id: green_led_light
                transition_length: 0.5s
            - lambda: |-     # turn our binary sensor off again
                id(long_click).publish_state(false);

        - timing: # Single Short clicked --> toggle the relais
            - ON for at most 1s
            - OFF for at least 0.5s
          then:
            - logger.log: "Single Short Clicked"
            - switch.toggle: relais


      - platform: status
        name: "$devicename Status"

      - platform: template
        name: "$devicename Double Click"
        id: double_click
        lambda: |-
          return false;    

      - platform: template
        name: "$devicename Triple Click"
        id: triple_click
        lambda: |-
          return false;  

      - platform: template
        name: "$devicename Long Click"
        id: long_click
        lambda: |-
          return false;   

    sensor:
      - platform: wifi_signal
        name: "$devicename WiFi Signal"
        update_interval: 60s

    switch:        #relais
      - platform: gpio
        name: "$devicename"
        pin: GPIO12
        id: relais

    output:
      # Register the green LED as a dimmable output ....
      - platform: esp8266_pwm
        id: green_led
        pin:
          number: GPIO13
          inverted: True

    light:
      - platform: monochromatic
        name: "Green LED"
        output: green_led
        id: green_led_light
        internal: True



3. Home Assistant
*****************

An example for an automation that toggles a switch when another switch is double clicked:

.. code-block:: yaml

    - alias: on double click
      trigger:
      - entity_id: binary_sensor.sonoff1_double_click
        platform: state
        from: 'off'
        to: 'on'
      action:
      - entity_id: switch.sonoff2
        service: homeassistant.toggle


See Also
--------

- :doc:`/esphomeyaml/devices/sonoff_s20`
- `Adding ESPHome to Home Assistant <https://www.home-assistant.io/components/esphome/>`__.

.. disqus::
