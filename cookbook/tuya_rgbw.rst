Tuya RGBW LED controller
========================

The Tuya RGBW controller is inexpensive, available on ebay, and can be OTA flashed using `tuya-convert <https://github.com/ct-Open-Source/tuya-convert>`__, after which it can be OTA flashed via the ESPHome web interface (NOTE: a port must be explicitly set if using a Home Assistant add-on for this, and you need to connect directly to that port instead of using the proxied port via Home Assistant).

.. figure:: images/tuya_rgbw.jpg
    :align: center
    :width: 80.0%

The configuration below shows an example that can be compiled to a binary firmware file that works correctly for this device, and that cycles through three different brightnesses and an off state based on the number of button presses. The device can also be controlled via Home Assistant, of course, setting specific RGBW combinations and brightness levels.

.. code-block:: yaml

    # Example configuration entry
    output:
      - platform: esp8266_pwm
        id: output_red
        pin: GPIO14
      - platform: esp8266_pwm
        id: output_green
        pin: GPIO5
      - platform: esp8266_pwm
        id: output_blue
        pin: GPIO12
      - platform: esp8266_pwm
        id: output_white
        pin: GPIO15

    globals:
      - id: action_state
        type: int
        restore_value: no
        initial_value: '0'

    binary_sensor:
      - platform: gpio
        pin:   GPIO13
        name: "RGBW Controller Button"
        filters:
          - invert:
          - delayed_on_off: 20ms
        on_press:
          then:
            - lambda: id(action_state) = (id(action_state) + 1) % 4;
            - if:
                condition:
                  lambda: 'return id(action_state) == 0;'
                then:
                  - light.turn_off:  rgbw_lightstrip1
            - if:
                condition:
                  lambda: 'return id(action_state) == 1;'
                then:
                  - light.turn_on:
                      id: rgbw_lightstrip1
                      brightness: 60%
            - if:
                condition:
                  lambda: 'return id(action_state) == 2;'
                then:
                  - light.turn_on:
                      id: rgbw_lightstrip1
                      brightness: 40%
            - if:
                condition:
                  lambda: 'return id(action_state) == 3;'
                then:
                  - light.turn_on:
                      id: rgbw_lightstrip1
                      brightness: 15%
    light:
      - platform: rgbw
        name: "rgbw_strip_01"
        id: rgbw_lightstrip1
        red: output_red
        green: output_green
        blue: output_blue
        white: output_white

        # Ensure the light turns on by default if the physical switch is actuated.
        restore_mode: ALWAYS_OFF

See Also
--------

- :doc:`/components/light/rgbw`
- :doc:`/components/output/esp8266_pwm`
- :ghedit:`Edit`
