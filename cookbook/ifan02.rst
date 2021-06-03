Sonoff iFan02
=============

.. seo::
    :description: Instructions for using Sonoff ifan02 in ESPHome.
    :keywords: Fan, Sonoff, ifan02
    :image: fan.svg

Sonoff iFan02 is a driver for ceiling fans with lights.
By replacing the old driver with iFan02, your non-smart led ceiling fan will be converted to a smart ceiling fan.
For more information see `iFan02 <https://www.itead.cc/sonoff-ifan02-wifi-smart-ceiling-fan-with-light.html>`__

This configuration will expose a :doc:`/components/light/binary` and a :doc:`/components/fan/speed`.

To get this working in ESPHome you first need to create a :doc:`/components/output/custom` to control the iFan02.

Create an ifan02.h file:

.. code-block:: c++

    #include "esphome.h"
    using namespace esphome;

    class IFan02Output : public Component, public FloatOutput {
      public:
        void write_state(float state) override {
          if (state < 0.3) {
            // OFF
            digitalWrite(5, LOW);
            digitalWrite(4, LOW);
            digitalWrite(15, LOW);
          } else if (state < 0.6) {
            // low speed
            digitalWrite(5, HIGH);
            digitalWrite(4, LOW);
            digitalWrite(15, LOW);
          } else if (state < 0.9) {
            // medium speed
            digitalWrite(5, HIGH);
            digitalWrite(4, HIGH);
            digitalWrite(15, LOW);
          } else {
            // high speed
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
      on_boot:
        priority: 225
        # turn off the light as early as possible
        then:
          - light.turn_off: ifan02_light

    wifi:
      ssid: <YOUR_SSID>
      password: <YOUR_PASSWORD>

    api:

    logger:

    ota:

    binary_sensor:
      - platform: gpio
        id: vbutton_light
        pin:
          number: GPIO0
          inverted: True
        on_press:
          then:
            - light.toggle: ifan02_light

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
          auto ifan02_fan = new IFan02Output();
          App.register_component(ifan02_fan);
          return {ifan02_fan};

      - platform: gpio
        pin: GPIO12
        id: light_output

    light:
      - platform: binary
        name: "iFan02 Light"
        output: light_output
        id: ifan02_light

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
                  - fan.turn_off: ifan02_fan
            - if:
                condition:
                  and:
                    - switch.is_on: fan_relay1
                    - switch.is_off: fan_relay2
                    - switch.is_off: fan_relay3
                then:
                  - fan.turn_on:
                      id: ifan02_fan
                      speed: 1
            - if:
                condition:
                  and:
                    - switch.is_on: fan_relay1
                    - switch.is_on: fan_relay2
                    - switch.is_off: fan_relay3
                then:
                  - fan.turn_on:
                      id: ifan02_fan
                      speed: 2
            - if:
                condition:
                  and:
                    - switch.is_on: fan_relay1
                    - switch.is_off: fan_relay2
                    - switch.is_on: fan_relay3
                then:
                  - fan.turn_on:
                      id: ifan02_fan
                      speed: 3
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
        id: ifan02_fan
        speed_count: 3
        name: "iFan02 Fan"

See Also
--------

- :doc:`/components/light/index`
- :doc:`/components/light/binary`
- :doc:`/components/fan/index`
- :doc:`/components/fan/speed`
- :doc:`/components/output/index`
- :doc:`/components/output/custom`
- :doc:`/guides/automations`
- :ghedit:`Edit`
