Ifan02
======

.. seo::
    :description: Instructions for using Sonoff ifan02 in ESPHome.
    :keywords: Fan, Sonoff, ifan02


Configuration for `Sonoff ifan02 <https://www.itead.cc/sonoff-ifan02-wifi-smart-ceiling-fan-with-light.html>`__.

First you need a :doc:`components/output/custom.html` to control the ifan02.

Create a ifan02.h file:

.. code-block:: c++

  #include "esphome.h"
  using namespace esphome;

  class IFan02Output : public Component, public output::FloatOutput {
    public:
      void write_state(float state) override {
          if (state < 0.3) {
            digitalWrite(5, LOW);
            digitalWrite(4, LOW);
            digitalWrite(15, LOW);
          }

          if (state >= 0.32 && state <= 0.34) {
            digitalWrite(5, HIGH);
            digitalWrite(4, LOW);
            digitalWrite(15, LOW);
          }
          if (state >= 0.65 && state <= 0.67) {
            digitalWrite(5, HIGH);
            digitalWrite(4, HIGH);
            digitalWrite(15, LOW);
          }
          if (state >= 0.9) {
            digitalWrite(5, HIGH);
            digitalWrite(4, LOW);
            digitalWrite(15, HIGH);
          }
      }
  };

Then you need to set it up with yaml.

.. code-block:: yaml

    esphome:
      name: ifan02
      platform: ESP8266
      board: esp8285
      includes:
        - ifan02.h

    binary_sensor:
      - platform: gpio
        id: vbutton_light
        pin:
          number: GPIO0
          inverted: True
        on_press:
          then:
            - light.toggle: light

      - platform: gpio
        id: vbutton_relay_1
        pin:
          number: GPIO9
          inverted: True
        on_press:
          then:
            - switch.toggle: fan_relay1
            - switch.turn_on: update_fan_speed

      - platform: gpio
        id: vbutton_relay_2
        pin:
          number: GPIO10
          inverted: True
        on_press:
          then:
            - switch.toggle: fan_relay2
            - switch.turn_on: update_fan_speed

      - platform: gpio
        id: vbutton_relay_3
        pin:
          number: GPIO14
          inverted: True
        on_press:
          then:
            - switch.toggle: fan_relay3
            - switch.turn_on: update_fan_speed

    output:
      - platform: custom
        type: float
        outputs:
          id: fanoutput
        lambda: |-
          auto ifan02 = new IFan02Output();
          App.register_component(ifan02);
          return {ifan02};

      - platform: gpio
        pin: GPIO12
        id: light_output

    light:
      - platform: binary
        name: ifan02_light
        output: light_output
        id: light

    switch:
      - platform: template
        id: update_fan_speed
        optimistic: True
        turn_on_action:
          then:
            - delay: 200ms
            - if:
                condition:
                  and:
                    - switch.is_off: fan_relay1
                    - switch.is_off: fan_relay2
                    - switch.is_off: fan_relay3
                then:
                  - fan.turn_off: ifan02
            - if:
                condition:
                  and:
                    - switch.is_on: fan_relay1
                    - switch.is_off: fan_relay2
                    - switch.is_off: fan_relay3
                then:
                  - fan.turn_on:
                      id: ifan02
                      speed: LOW
            - if:
                condition:
                  and:
                    - switch.is_on: fan_relay1
                    - switch.is_on: fan_relay2
                    - switch.is_off: fan_relay3
                then:
                  - fan.turn_on:
                      id: ifan02
                      speed: MEDIUM
            - if:
                condition:
                  and:
                    - switch.is_on: fan_relay1
                    - switch.is_off: fan_relay2
                    - switch.is_on: fan_relay3
                then:
                  - fan.turn_on:
                      id: ifan02
                      speed: HIGH
            - switch.turn_off: update_fan_speed

      - platform: gpio
        pin: GPIO5
        id: fan_relay1

      - platform: gpio
        pin: GPIO4
        id: fan_relay2

      - platform: gpio
        pin: GPIO15
        id: fan_relay3

    fan:
      - platform: speed
        output: fanoutput
        id: ifan02
        name: ifan02_fan