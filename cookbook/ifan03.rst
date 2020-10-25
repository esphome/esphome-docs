Sonoff iFan03
=============

.. seo::
    :description: Instructions for using Sonoff iFan03 in ESPHome.
    :keywords: Fan, Sonoff, iFan02
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
  - platform: remote_receiver
    id: remote_0
    raw:
      code: [-207, 104, -103, 104, -104, 103, -104, 207, -104, 103, -104, 104, -103, 104, -104, 103, -104, 105, -102, 104, -725, 104, -311, 103, -518, 104, -933, 103, -104, 104, -725, 104, -932, 104, -207, 207, -519]
    on_release:
      then:
        - fan.turn_off: ifan03_fan
    internal: true
  - platform: remote_receiver
    id: remote_1
    raw:
      code: [-207, 104, -104, 103, -104, 104, -103, 207, -104, 104, -103, 104, -104, 103, -104, 104, -103, 104, -104, 103, -726, 103, -312, 103, -518, 104, -933, 103, -104, 104, -725, 104, -103, 104, -726, 103, -104, 311, -518]
    on_release:
      then:
        - fan.turn_on:
              id: ifan03_fan
              speed: LOW
    internal: true
  - platform: remote_receiver
    id: remote_2
    raw:
      code: [-208, 103, -104, 104, -103, 104, -103, 208, -103, 104, -104, 103, -104, 104, -103, 104, -104, 103, -104, 103, -726, 104, -310, 104, -518, 104, -933, 103, -104, 104, -725, 104, -207, 104, -622, 103, -416, 102, -415]
    on_release:
      then:
        - fan.turn_on:
              id: ifan03_fan
              speed: MEDIUM
    internal: true
  - platform: remote_receiver
    id: remote_3
    raw:
      code: [-207, 104, -104, 103, -104, 104, -103, 208, -103, 104, -104, 103, -104, 104, -103, 104, -104, 103, -104, 103, -726, 104, -311, 104, -518, 103, -934, 103, -103, 104, -726, 103, -104, 207, -622, 104, -103, 104, -207, 104, -415]
    on_release:
      then:
        - fan.turn_on:
              id: ifan03_fan
              speed: HIGH
    internal: true

output:
  - platform: custom
    type: float
    outputs:
      id: fanoutput
    lambda: |-
      auto ifan03_fan = new IFan03Output();
      App.register_component(ifan03_fan);
      return {ifan03_fan};

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
              - fan.turn_off: ifan03_fan
        - if:
            condition:
              and:
                - switch.is_on: fan_relay1
                - switch.is_off: fan_relay2
                - switch.is_off: fan_relay3
            then:
              - fan.turn_on:
                  id: ifan03_fan
                  speed: LOW
        - if:
            condition:
              and:
                - switch.is_off: fan_relay1
                - switch.is_on: fan_relay2
                - switch.is_off: fan_relay3
            then:
              - fan.turn_on:
                  id: ifan03_fan
                  speed: MEDIUM
        - if:
            condition:
              and:
                - switch.is_off: fan_relay1
                - switch.is_off: fan_relay2
                - switch.is_on: fan_relay3
            then:
              - fan.turn_on:
                  id: ifan03_fan
                  speed: HIGH
        - switch.turn_off: update_fan_speed

  - platform: gpio
    pin: GPIO14
    id: fan_relay1

  - platform: gpio
    pin: GPIO12
    id: fan_relay2

  - platform: gpio
    pin: GPIO15
    id: fan_relay3

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
