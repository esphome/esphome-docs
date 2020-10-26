Sonoff iFan03
=============

.. seo::
    :description: Instructions for using Sonoff iFan03 in ESPHome.
    :keywords: Fan, Sonoff, iFan03
    :image: fan.svg

Sonoff iFan03 is a driver for ceiling fans with lights.
By replacing the old driver with iFan03, your non-smart led ceiling fan will be converted to a smart ceiling fan.
For more information see `iFan03 <https://www.itead.cc/sonoff-ifan03-wifi-ceiling-fan-light-controller.html>`__

This configuration will expose a :doc:`/components/light/binary` and a :doc:`/components/fan/speed`.

To get this working in ESPHome you first need to create a :doc:`/components/output/custom` to control the iFan03.

Create a ifan03.h file:

.. code-block:: c++

    #include "esphome.h"
    using namespace esphome;

    class IFan03Output : public Component, public FloatOutput {
      public:
        void write_state(float state) override {
          if (state < 0.3) {
            // OFF
            digitalWrite(14, LOW);
            digitalWrite(12, LOW);
            digitalWrite(15, LOW);
          } else if (state < 0.6) {
            // low speed
            digitalWrite(14, HIGH);
            digitalWrite(12, LOW);
            digitalWrite(15, LOW);
          } else if (state < 0.9) {
            // medium speed
            digitalWrite(14, HIGH);
            digitalWrite(12, HIGH);
            digitalWrite(15, LOW);
          } else {
            // high speed
            digitalWrite(14, HIGH);
            digitalWrite(12, LOW);
            digitalWrite(15, HIGH);
          }
        }
    };

Then you need to set it up with yaml.

.. code-block:: yaml

    esphome:
      name: fan_ifan03
      platform: ESP8266
      board: esp8285
      includes:
        - ifan03.h
    wifi:
      ssid: <YOUR_SSID>
      password: <YOUR_PASSWORD>

    captive_portal:

    logger:

    api:

    ota:

    remote_receiver:
      pin: GPIO3

    binary_sensor:
      - platform: gpio
        id: button
        pin:
          number: GPIO0
        on_press:
          then:
            - light.toggle: ifan03_light

      - platform: remote_receiver
        name: "Fan 0"
        id: remote_0
        raw:
          code: [-207, 104, -103, 104, -104, 103, -104, 207, -104, 103, -104, 104, -103, 104, -104, 103, -104, 105, -102, 104, -725, 104, -311, 103, -518, 104, -933, 103, -104, 104, -725, 104, -932, 104, -207, 207, -519]
        on_release:
          then:
            - fan.turn_off: ifan03_fan
        internal: true
      - platform: remote_receiver
        id: remote_fan1
        raw:
          code: [-207, 104, -104, 103, -104, 104, -103, 207, -104, 104, -103, 104, -104, 103, -104, 104, -103, 104, -104, 103, -726, 103, -312, 103, -518, 104, -933, 103, -104, 104, -725, 104, -103, 104, -726, 103, -104, 311, -518]
        on_release:
          then:
            - fan.turn_on:
                  id: ifan03_fan
                  speed: LOW
        internal: true
      - platform: remote_receiver
        id: remote_fan2
        raw:
          code: [-208, 103, -104, 104, -103, 104, -103, 208, -103, 104, -104, 103, -104, 104, -103, 104, -104, 103, -104, 103, -726, 104, -310, 104, -518, 104, -933, 103, -104, 104, -725, 104, -207, 104, -622, 103, -416, 102, -415]
        on_release:
          then:
            - fan.turn_on:
                  id: ifan03_fan
                  speed: MEDIUM
        internal: true
      - platform: remote_receiver
        id: remote_fan3
        raw:
          code: [-207, 104, -104, 103, -104, 104, -103, 208, -103, 104, -104, 103, -104, 104, -103, 104, -104, 103, -104, 103, -726, 104, -311, 104, -518, 103, -934, 103, -103, 104, -726, 103, -104, 207, -622, 104, -103, 104, -207, 104, -415]
        on_release:
          then:
            - fan.turn_on:
                  id: ifan03_fan
                  speed: HIGH
        internal: true

      - platform: remote_receiver
        id: remote_light
        raw:
          code: [-207, 104, -103, 104, -104, 103, -104, 207, -104, 103, -104, 104, -103, 104, -103, 104, -104, 103, -104, 104, -725, 104, -311, 103, -518, 104, -933, 103, -104, 103, -726, 103, -311, 104, -518, 104, -207, 104, -103, 104, -414]
        on_release:
          then:
            - light.toggle: ifan03_light

    output:
      - platform: custom
        type: float
        outputs:
          id: fanoutput
        lambda: |-
          auto ifan03_fan = new IFan03Output();
          App.register_component(ifan03_fan);
          return {ifan03_fan};

      - platform: gpio
        pin: GPIO9
        id: relay_light
        inverted: true

    light:
      - platform: binary
        name: "iFan03 Light"
        output: relay_light
        id: ifan03_light

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
                    - switch.is_off: relay_fan1
                    - switch.is_off: relay_fan2
                    - switch.is_off: relay_fan3
                then:
                  - fan.turn_off: ifan03_fan
            - if:
                condition:
                  and:
                    - switch.is_on: relay_fan1
                    - switch.is_off: relay_fan2
                    - switch.is_off: relay_fan3
                then:
                  - fan.turn_on:
                      id: ifan03_fan
                      speed: LOW
            - if:
                condition:
                  and:
                    - switch.is_off: relay_fan1
                    - switch.is_on: relay_fan2
                    - switch.is_off: relay_fan3
                then:
                  - fan.turn_on:
                      id: ifan03_fan
                      speed: MEDIUM
            - if:
                condition:
                  and:
                    - switch.is_off: relay_fan1
                    - switch.is_off: relay_fan2
                    - switch.is_on: relay_fan3
                then:
                  - fan.turn_on:
                      id: ifan03_fan
                      speed: HIGH
            - switch.turn_off: update_fan_speed

      - platform: gpio
        pin: GPIO14
        id: relay_fan1

      - platform: gpio
        pin: GPIO12
        id: relay_fan2

      - platform: gpio
        pin: GPIO15
        id: relay_fan3

    fan:
      - platform: speed
        output: fanoutput
        id: ifan03_fan
        name: "iFan03 Fan"

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
