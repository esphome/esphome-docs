Sonoff T1/T2/T3 UK
==================

.. seo::
    :description: An example of how to integrate a T1 T2 or T3 Sonoff light switch into Home Assistant
     using ESPHome
    :image: sonoff_1t_t3.png
    :keywords: Relay, Sonoff Basic, Sonoff Dual Dual R1, Light, HASS, Home Assistant, ESPHome

Please make sure you have read up about :doc:`the Sonoff T1 / T2 / T3 and how to flash it with ESPHome </devices/sonoff_t1_uk_3gang_v1.1>`.

So let's get straight on with the code!

T1
--

.. code-block:: yaml

    esphome:
      name: my_t1

    esp8266:
      board: esp01_1m

    wifi:
      ssid: !secret wifi_ssid
      password: !secret wifi_password

    logger:

    api:

    ota:

    binary_sensor:
      - platform: gpio
        pin:
          number: GPIO0
          mode:
            input: true
            pullup: true
          inverted: true
        id: button_1
        on_press:
          then:
            - light.toggle: light_1

      - platform: status
        name: "T1 Status"

    output:
      - platform: gpio
        pin: GPIO12
        id: relay_1

    light:
      - platform: binary
        name: "T1"
        id: light_1
        output: relay_1

    status_led:
      pin:
        number: GPIO13
        inverted: yes


In the above code block, there is a *secrets.yaml* file so that you have just one place to change WiFi
details for all your devices.

The use_address is required because the Sonoff T series don't work with mDNS properly. This means that it will
show as off line in the dashboard, and you will need to use the IP address to view the logs or upload new versions
of the firmware. You will also need to manually add the device in integrations by IP address. You will need to
assign a fixed IP in the above configuration, or use a fixed IP assigned by your DHCP server.

See `issue #810 <https://github.com/esphome/issues/issues/810>`__ for further details.


T2
--

.. code-block:: yaml

    esphome:
      name: my_t2

    esp8266:
      board: esp01_1m

    wifi:
      ssid: !secret wifi_ssid
      password: !secret wifi_password

    logger:

    api:

    ota:

    binary_sensor:
      - platform: gpio
        pin:
          number: GPIO0
          mode:
            input: true
            pullup: true
          inverted: true
        id: button_1
        on_press:
          then:
            - light.toggle: light_1

      - platform: gpio
        pin:
          number: GPIO9
          mode:
            input: true
            pullup: true
          inverted: true
        id: button_2
        on_press:
          then:
            - light.toggle: light_2

      - platform: status
        name: "T2 Status"

    output:
      - platform: gpio
        pin: GPIO12
        id: relay_1

      - platform: gpio
        pin: GPIO5
        id: relay_2

    light:
      - platform: binary
        name: "T2 L1"
        id: light_1
        output: relay_1

      - platform: binary
        name: "T2 L2"
        id: light_2
        output: relay_2

    status_led:
      pin:
        number: GPIO13
        inverted: yes


T3
--

.. code-block:: yaml

    esphome:
      name: my_t3

    esp8266:
      board: esp01_1m

    wifi:
      ssid: !secret wifi_ssid
      password: !secret wifi_password

    logger:

    api:

    ota:

    binary_sensor:
      - platform: gpio
        pin:
          number: GPIO0
          mode:
            input: true
            pullup: true
          inverted: true
        id: button_1
        on_press:
          then:
            - light.toggle: light_1

      - platform: gpio
        pin:
          number: GPIO9
          mode:
            input: true
            pullup: true
          inverted: true
        id: button_2
        on_press:
          then:
            - light.toggle: light_2

      - platform: gpio
        pin:
          number: GPIO10
          mode:
            input: true
            pullup: true
          inverted: true
        id: button_3
        on_press:
          then:
            - light.toggle: light_3

      - platform: status
        name: "T3 Status"

    output:
      - platform: gpio
        pin: GPIO12
        id: relay_1

      - platform: gpio
        pin: GPIO5
        id: relay_2

      - platform: gpio
        pin: GPIO4
        id: relay_3

    light:
      - platform: binary
        name: "T3 L1"
        id: light_1
        output: relay_1

      - platform: binary
        name: "T3 L2"
        id: light_2
        output: relay_2

      - platform: binary
        name: "T3 L3"
        id: light_3
        output: relay_3

    status_led:
      pin:
        number: GPIO13
        inverted: yes


See Also
--------

- :doc:`/cookbook/sonoff-light-switch`
- :doc:`/guides/automations`
- :doc:`/devices/sonoff_t1_uk_3gang_v1.1`
