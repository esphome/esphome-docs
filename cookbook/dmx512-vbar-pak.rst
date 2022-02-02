ADJ VBar Pak with DMX Component
===============================

.. seo::
    :description: An example of how to integrate four [ADJ VBar Pak](https://d295jznhem2tn9.cloudfront.net/ItemRelatedFiles/8659/vbar_pak.pdf) DMX lights with ESPHome in Home Assistant
    :keywords: DMX, DMX512, RGB, RGBW, VBar, VPar, Par, Light

In the example below we use the DMX Component of ESPHome to control an ADJ VBar Pak DMX light in Home Assistant.
The lights will appear as RGBW (using the Amber channel as a kind of warm white). Since Home Assistant allows
direct setting of the light brightness, the hardware dimmers of the lights are grouped together and implemented 
as a separate light to simultaneously dim all of them.

Similarly with the hardware effects and their settings, these are handled simultaneously for all the 4 VBars. 
There's a dropdown select for the effect type, another one for the effect modes, and a number to adjust intensity/speed of the effect.

There's also a ``partition`` light, which groups the lights into one, thus allowing a selection of native ESPHome software effects on them. 

Hardware setup
--------------

This example runs on a Wemos D1 Mini (ESP8266) with an MAX485 transceiver connected as below:

.. code-block:: yaml

    MAX485-M VCC     -> ESP8266 +3.3V
    MAX485-M GND     -> ESP8266 GND
    MAX485-M DE      -> ESP8266 +3.3V
    MAX485-M RE      -> ESP8266 +3.3V
    MAX485-M DI      -> ESP8266 GPIO2
    MAX485-M A       -> XLR 3 (DMX +)
    MAX485-M B       -> XLR 2 (DMX -)
    MAX485-M GND     -> XLR 1 (DMX GND)



DMX Addressing
--------------

Lights are daisy chained with XLR cables. The last light in the chain has on the output a 120Ohm resistor placed between XLR pins 2 and 3.

In this example they have to be set up to 8-channel mode (to access all the effects, see 
[the manual](https://d295jznhem2tn9.cloudfront.net/ItemRelatedFiles/8659/vbar_pak.pdf)). The address of the first one is 1 (``d.001``), the 
next one is 9 (``d.009``), the third one is 17 (``d.017``), and the forth one is 25 (``d.025``), using the buttons on each fixture. 

In the output config the channels will be for the first one from 1 to 8, the second one from 9 to 16, third one from 17 to 24, 
and forth one from 25 to 32. 


.. code-block:: yaml

    substitutions:
      device_name: multiple-dmx-vbar
      friendly_name: "DMX VBar"
      device_ip: 192.168.1.11
      device_description: "DMX control of 4 ADJ VBar Pak lights"

    esphome:
      name: ${device_name}
      comment: "${device_description}"
      platform: ESP8266
      board: d1_mini
      esp8266_restore_from_flash: true

    logger:
      baud_rate: 0
      level: INFO

    api:
      reboot_timeout: 15min

    ota:
      password: !secret ota_password

    wifi:
      ssid: !secret wifi_ssid
      password: !secret wifi_password
      manual_ip:
        static_ip: ${device_ip}
        gateway: 192.168.1.1
        subnet: 255.255.255.0
      use_address: ${device_ip}

    button:
    - platform: restart
      name: ${friendly_name} restart

    switch:
    - platform: gpio
      name: ${friendly_name} MUTE
      icon: mdi:lightbulb-off
      restore_mode: ALWAYS_OFF
      pin:
        number: GPIO13 #ESP8266, Wemos D1 Mini D7
        inverted: true

    binary_sensor:
    - platform: status
      name: ${friendly_name} network status

    sensor:
    - platform: wifi_signal
      name: ${friendly_name} WiFi signal
      update_interval: 60s
      disabled_by_default: true
    - platform: uptime
      name: ${friendly_name} uptime
      disabled_by_default: true

    uart:
      id: uart_bus
      baud_rate: 250000
      tx_pin: GPIO2 #ESP8266, Wemos D1 Mini D4
      stop_bits: 2

    dmx512:
      id: dmx
      uart_id: uart_bus
      tx_pin: GPIO2 #ESP8266, Wemos D1 Mini D4
      uart_num: 1

    output:
    # d.001
    - platform: dmx512
      channel: 1
      universe: dmx
      id: vbar1_red
    - platform: dmx512
      channel: 2
      universe: dmx
      id: vbar1_green
    - platform: dmx512
      channel: 3
      universe: dmx
      id: vbar1_blue
    - platform: dmx512
      channel: 4
      universe: dmx
      id: vbar1_amber
    - platform: dmx512
      channel: 5
      universe: dmx
      id: vbar1_master
    - platform: dmx512
      channel: 6
      universe: dmx
      id: vbar1_effect_level
    - platform: dmx512
      channel: 7
      universe: dmx
      id: vbar1_effect_select
    - platform: dmx512
      channel: 8
      universe: dmx
      id: vbar1_effect_mode

    # d.009
    - platform: dmx512
      channel: 9
      universe: dmx
      id: vbar2_red
    - platform: dmx512
      channel: 10
      universe: dmx
      id: vbar2_green
    - platform: dmx512
      channel: 11
      universe: dmx
      id: vbar2_blue
    - platform: dmx512
      channel: 12
      universe: dmx
      id: vbar2_amber
    - platform: dmx512
      channel: 13
      universe: dmx
      id: vbar2_master
    - platform: dmx512
      channel: 14
      universe: dmx
      id: vbar2_effect_level
    - platform: dmx512
      channel: 15
      universe: dmx
      id: vbar2_effect_select
    - platform: dmx512
      channel: 16
      universe: dmx
      id: vbar2_effect_mode

    # d.017
    - platform: dmx512
      channel: 17
      universe: dmx
      id: vbar3_red
    - platform: dmx512
      channel: 18
      universe: dmx
      id: vbar3_green
    - platform: dmx512
      channel: 19
      universe: dmx
      id: vbar3_blue
    - platform: dmx512
      channel: 20
      universe: dmx
      id: vbar3_amber
    - platform: dmx512
      channel: 21
      universe: dmx
      id: vbar3_master
    - platform: dmx512
      channel: 22
      universe: dmx
      id: vbar3_effect_level
    - platform: dmx512
      channel: 23
      universe: dmx
      id: vbar3_effect_select
    - platform: dmx512
      channel: 24
      universe: dmx
      id: vbar3_effect_mode

    # d.025
    - platform: dmx512
      channel: 25
      universe: dmx
      id: vbar4_red
    - platform: dmx512
      channel: 26
      universe: dmx
      id: vbar4_green
    - platform: dmx512
      channel: 27
      universe: dmx
      id: vbar4_blue
    - platform: dmx512
      channel: 28
      universe: dmx
      id: vbar4_amber
    - platform: dmx512
      channel: 29
      universe: dmx
      id: vbar4_master
    - platform: dmx512
      channel: 30
      universe: dmx
      id: vbar4_effect_level
    - platform: dmx512
      channel: 31
      universe: dmx
      id: vbar4_effect_select
    - platform: dmx512
      channel: 32
      universe: dmx
      id: vbar4_effect_mode

    - platform: template
      id: vbar_groupdim
      type: float
      write_action:
        - lambda: |-
            id(vbar1_master).set_level(state);
            id(vbar2_master).set_level(state);
            id(vbar3_master).set_level(state);
            id(vbar4_master).set_level(state);

    number:
    - platform: template
      name: ${friendly_name} Effect Level
      icon: mdi:flower-pollen-outline
      id: vbar_effect_level_num
      optimistic: true
      min_value: 0
      max_value: 255
      step: 1
      restore_value: true
      set_action:
        - lambda: |-
            id(vbar1_effect_level).set_level(x / 255);
            id(vbar2_effect_level).set_level(x / 255);
            id(vbar3_effect_level).set_level(x / 255);
            id(vbar4_effect_level).set_level(x / 255);

    select:
    - platform: template
      name: ${friendly_name} Effect
      optimistic: true
      restore_value: true
      icon: mdi:pan
      id: vbar1_effect_select_dropdown
      options:
        - "None"
        - "Color Macro"
        - "Color Change"
        - "Color Fade"
        - "Sound Active"
        - "Strobing"
      set_action:
        - lambda: |-
              if (x.compare(std::string{"None"}) == 0) {
                id(vbar1_effect_select).set_level(0);
                id(vbar2_effect_select).set_level(0);
                id(vbar3_effect_select).set_level(0);
                id(vbar4_effect_select).set_level(0);
                auto call = id(vbar_effect_level_num).make_call();
                call.set_value(0);
                call.perform();
              }
              if (x.compare(std::string{"Strobing"}) == 0) {
                id(vbar1_effect_select).set_level(0.04);
                id(vbar2_effect_select).set_level(0.04);
                id(vbar3_effect_select).set_level(0.04);
                id(vbar4_effect_select).set_level(0.04);
              }
              if (x.compare(std::string{"Color Macro"}) == 0) {
                id(vbar1_effect_select).set_level(0.3);
                id(vbar2_effect_select).set_level(0.3);
                id(vbar3_effect_select).set_level(0.3);
                id(vbar4_effect_select).set_level(0.3);
              }
              if (x.compare(std::string{"Color Change"}) == 0) {
                id(vbar1_effect_select).set_level(0.5);
                id(vbar2_effect_select).set_level(0.5);
                id(vbar3_effect_select).set_level(0.5);
                id(vbar4_effect_select).set_level(0.5);
              }
              if (x.compare(std::string{"Color Fade"}) == 0) {
                id(vbar1_effect_select).set_level(0.66);
                id(vbar2_effect_select).set_level(0.66);
                id(vbar3_effect_select).set_level(0.66);
                id(vbar4_effect_select).set_level(0.66);
              }
              if (x.compare(std::string{"Sound Active"}) == 0) {
                id(vbar1_effect_select).set_level(0.9);
                id(vbar2_effect_select).set_level(0.9);
                id(vbar3_effect_select).set_level(0.9);
                id(vbar4_effect_select).set_level(0.9);
                auto call = id(vbar_effect_level_num).make_call();
                call.set_value(200);
                call.perform();
              }

    - platform: template
      name: ${friendly_name} Effect Mode
      icon: mdi:dots-hexagon
      optimistic: true
      restore_value: true
      id: vbar_effect_mode_dropdown
      options:
        - Change-Fade-Sound-1-Macro-OFF
        - Change-Fade-Sound-2-Macro-R
        - Change-Fade-Sound-3-Macro-G
        - Change-Fade-Sound-4-Macro-B
        - Change-Fade-Sound-5-Macro-A
        - Change-Fade-Sound-6-Macro-RG
        - Change-Fade-Sound-7-Macro-RB
        - Change-Fade-Sound-8-Macro-RA
        - Change-Fade-Sound-9-Macro-GB
        - Change-Fade-Sound-10-Macro-GA
        - Change-Fade-Sound-11-Macro-BA
        - Change-Fade-Sound-12-Macro-RGB
        - Change-Fade-Sound-13-Macro-RGA
        - Change-Fade-Sound-14-Macro-RBA
        - Change-Fade-Sound-15-Macro-GBA
        - Change-Fade-Sound-16-Macro-RGBA
      set_action:
        - lambda: |-
              if (x.compare(std::string{"Change-Fade-Sound-1-Macro-OFF"}) == 0) {
                id(vbar1_effect_mode).set_level(0.03);
                id(vbar2_effect_mode).set_level(0.03);
                id(vbar3_effect_mode).set_level(0.03);
                id(vbar4_effect_mode).set_level(0.03);
              }
              if (x.compare(std::string{"Change-Fade-Sound-2-Macro-R"}) == 0) {
                id(vbar1_effect_mode).set_level(0.09);
                id(vbar2_effect_mode).set_level(0.09);
                id(vbar3_effect_mode).set_level(0.09);
                id(vbar4_effect_mode).set_level(0.09);
              }
              if (x.compare(std::string{"Change-Fade-Sound-3-Macro-G"}) == 0) {
                id(vbar1_effect_mode).set_level(0.16);
                id(vbar2_effect_mode).set_level(0.16);
                id(vbar3_effect_mode).set_level(0.16);
                id(vbar4_effect_mode).set_level(0.16);
              }
              if (x.compare(std::string{"Change-Fade-Sound-4-Macro-B"}) == 0) {
                id(vbar1_effect_mode).set_level(0.22);
                id(vbar2_effect_mode).set_level(0.22);
                id(vbar3_effect_mode).set_level(0.22);
                id(vbar4_effect_mode).set_level(0.22);
              }
              if (x.compare(std::string{"Change-Fade-Sound-5-Macro-A"}) == 0) {
                id(vbar1_effect_mode).set_level(0.28);
                id(vbar2_effect_mode).set_level(0.28);
                id(vbar3_effect_mode).set_level(0.28);
                id(vbar4_effect_mode).set_level(0.28);
              }
              if (x.compare(std::string{"Change-Fade-Sound-6-Macro-RG"}) == 0) {
                id(vbar1_effect_mode).set_level(0.35);
                id(vbar2_effect_mode).set_level(0.35);
                id(vbar3_effect_mode).set_level(0.35);
                id(vbar4_effect_mode).set_level(0.35);
              }
              if (x.compare(std::string{"Change-Fade-Sound-7-Macro-RB"}) == 0) {
                id(vbar1_effect_mode).set_level(0.41);
                id(vbar2_effect_mode).set_level(0.41);
                id(vbar3_effect_mode).set_level(0.41);
                id(vbar4_effect_mode).set_level(0.41);
              }
              if (x.compare(std::string{"Change-Fade-Sound-8-Macro-RA"}) == 0) {
                id(vbar1_effect_mode).set_level(0.47);
                id(vbar2_effect_mode).set_level(0.47);
                id(vbar3_effect_mode).set_level(0.47);
                id(vbar4_effect_mode).set_level(0.47);
              }
              if (x.compare(std::string{"Change-Fade-Sound-9-Macro-GB"}) == 0) {
                id(vbar1_effect_mode).set_level(0.53);
                id(vbar2_effect_mode).set_level(0.53);
                id(vbar3_effect_mode).set_level(0.53);
                id(vbar4_effect_mode).set_level(0.53);
              }
              if (x.compare(std::string{"Change-Fade-Sound-10-Macro-GA"}) == 0) {
                id(vbar1_effect_mode).set_level(0.6);
                id(vbar2_effect_mode).set_level(0.6);
                id(vbar3_effect_mode).set_level(0.6);
                id(vbar4_effect_mode).set_level(0.6);
              }
              if (x.compare(std::string{"Change-Fade-Sound-11-Macro-BA"}) == 0) {
                id(vbar1_effect_mode).set_level(0.66);
                id(vbar2_effect_mode).set_level(0.66);
                id(vbar3_effect_mode).set_level(0.66);
                id(vbar4_effect_mode).set_level(0.66);
              }
              if (x.compare(std::string{"Change-Fade-Sound-12-Macro-RGB"}) == 0) {
                id(vbar1_effect_mode).set_level(0.72);
                id(vbar2_effect_mode).set_level(0.72);
                id(vbar3_effect_mode).set_level(0.72);
                id(vbar4_effect_mode).set_level(0.72);
              }
              if (x.compare(std::string{"Change-Fade-Sound-13-Macro-RGA"}) == 0) {
                id(vbar1_effect_mode).set_level(0.78);
                id(vbar2_effect_mode).set_level(0.78);
                id(vbar3_effect_mode).set_level(0.78);
                id(vbar4_effect_mode).set_level(0.78);
              }
              if (x.compare(std::string{"Change-Fade-Sound-14-Macro-RBA"}) == 0) {
                id(vbar1_effect_mode).set_level(0.85);
                id(vbar2_effect_mode).set_level(0.85);
                id(vbar3_effect_mode).set_level(0.85);
                id(vbar4_effect_mode).set_level(0.85);
              }
              if (x.compare(std::string{"Change-Fade-Sound-15-Macro-GBA"}) == 0) {
                id(vbar1_effect_mode).set_level(0.91);
                id(vbar2_effect_mode).set_level(0.91);
                id(vbar3_effect_mode).set_level(0.91);
                id(vbar4_effect_mode).set_level(0.91);
              }
              if (x.compare(std::string{"Change-Fade-Sound-16-Macro-RGBA"}) == 0) {
                id(vbar1_effect_mode).set_level(0.97);
                id(vbar2_effect_mode).set_level(0.97);
                id(vbar3_effect_mode).set_level(0.97);
                id(vbar4_effect_mode).set_level(0.97);
              }

    light:
    - platform: monochromatic
      name: ${friendly_name} Dimmer
      output: vbar_groupdim
      icon: mdi:blur
      default_transition_length: 1s
      gamma_correct: 0
      restore_mode: RESTORE_DEFAULT_ON

    - platform: rgbw
      name: ${friendly_name} 1
      id: dmx_bar_1
      red: vbar1_red
      green: vbar1_green
      blue: vbar1_blue
      white: vbar1_amber
      icon: mdi:spotlight
      default_transition_length: 0.3s
      color_interlock: false
      gamma_correct: 0
      restore_mode: RESTORE_DEFAULT_ON
    - platform: monochromatic
      name: ${friendly_name} 1 Dimmer
      output: vbar1_master
      icon: mdi:blur
      disabled_by_default: true
      default_transition_length: 2s
      gamma_correct: 0
      restore_mode: RESTORE_DEFAULT_ON

    - platform: rgbw
      name: ${friendly_name} 2
      id: dmx_bar_2
      red: vbar2_red
      green: vbar2_green
      blue: vbar2_blue
      white: vbar2_amber
      icon: mdi:spotlight
      default_transition_length: 0.3s
      color_interlock: false
      gamma_correct: 0
      restore_mode: RESTORE_DEFAULT_ON
    - platform: monochromatic
      name: ${friendly_name} 2 Dimmer
      output: vbar2_master
      icon: mdi:blur
      disabled_by_default: true
      default_transition_length: 2s
      gamma_correct: 0
      restore_mode: RESTORE_DEFAULT_ON

    - platform: rgbw
      name: ${friendly_name} 3
      id: dmx_bar_3
      red: vbar3_red
      green: vbar3_green
      blue: vbar3_blue
      white: vbar3_amber
      icon: mdi:spotlight
      default_transition_length: 0.3s
      color_interlock: false
      gamma_correct: 0
      restore_mode: RESTORE_DEFAULT_ON
    - platform: monochromatic
      name: ${friendly_name} 3 Dimmer
      output: vbar3_master
      icon: mdi:blur
      disabled_by_default: true
      default_transition_length: 2s
      gamma_correct: 0
      restore_mode: RESTORE_DEFAULT_ON

    - platform: rgbw
      name: ${friendly_name} 4
      id: dmx_bar_4
      red: vbar4_red
      green: vbar4_green
      blue: vbar4_blue
      white: vbar4_amber
      icon: mdi:spotlight
      default_transition_length: 0.3s
      color_interlock: false
      gamma_correct: 0
      restore_mode: RESTORE_DEFAULT_ON
    - platform: monochromatic
      name: ${friendly_name} 4 Dimmer
      output: vbar4_master
      icon: mdi:blur
      disabled_by_default: true
      default_transition_length: 2s
      gamma_correct: 0
      restore_mode: RESTORE_DEFAULT_ON


    - platform: partition
      name: ${friendly_name} Group
      default_transition_length: 0.3s
      icon: mdi:spotlight
      restore_mode: RESTORE_DEFAULT_OFF
      segments:
        - single_light_id: dmx_bar_1
        - single_light_id: dmx_bar_2
        - single_light_id: dmx_bar_3
        - single_light_id: dmx_bar_4
      effects:
        - addressable_rainbow:
        - addressable_color_wipe:
        - addressable_scan:
        - addressable_twinkle:
        - addressable_random_twinkle:
      on_turn_on:
        then:
          - light.turn_off: dmx_bar_1
          - light.turn_off: dmx_bar_2
          - light.turn_off: dmx_bar_3
          - light.turn_off: dmx_bar_4
      on_turn_off:
        then:
          - light.turn_on: dmx_bar_1
          - light.turn_on: dmx_bar_2
          - light.turn_on: dmx_bar_3
          - light.turn_on: dmx_bar_4
