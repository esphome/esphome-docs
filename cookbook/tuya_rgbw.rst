Tuya RGBW LED controller
========================

The Tuya RGBW controller is inexpensive, available on ebay, and can be OTA flashed using `tuya-convert <https://github.com/ct-Open-Source/tuya-convert>`__, after which it can be OTA flashed via the ESPHome web interface (NOTE: a port must be explicitly set if using a Home Assistant add-on for this, and you need to connect directly to that port instead of using the proxied port via Home Assistant).

.. figure:: images/tuya_rgbw.jpg
    :align: center
    :width: 80.0%

The configuration below shows an example that can be compiled to a binary firmware file that works correctly for this device, and that cycles through three different brightnesses and an off state based on the number of button presses.  The device can also be controlled via Home Assistant, of course, setting specific RGBW combinations and brightness levels. Here is the configuration:

.. code-block:: yaml

    esphome:
      name: rgbw_controller
      platform: ESP8266
      board: esp01_1m
    
    wifi:
      ssid: "MY-SSID"
      password: "mypassword"
    
      # Enable fallback hotspot (captive portal) in case wifi connection fails
      ap:
        ssid: "Rgbw Controller"
        password: "some_password"
    
    captive_portal:
    
    # Enable logging
    logger:
    
    # Enable Home Assistant API
    api:
    
    ota:
    
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
            - lambda: |-
                // cycle between state in [0, 1, 2, 3]
                id(action_state) += 1;
                if (id(action_state) > 3) {
                  id(action_state) = 0;
                }
                
                //ESP_LOGD("ButtonPress", "Global value is: %d", id(action_state));
        
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


Make your node in the ESPHome dashboard and compile/upload it.


See Also
--------

- :doc:`/components/light/rgbw`
- :doc:`/components/output/esp8266_pwm`
- :ghedit:`Edit`
