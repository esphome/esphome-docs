DIY Light switch using a Sonoff Dual
====================================

.. seo::
    :description: An example of how to integrate a dual light switch into Home Assistant using ESPHome
    :keywords: Relay, Sonoff Dual Dual R1, Light, HASS, Home Assistant, ESPHome

.. note::

    This is a DIY solution, and you will need to have some knowledge of electrical wiring and enough
    capabilities to do this work safely.

    The author, and the ESPHome team, take no responsibility for any actions, injuries or outcomes
    from following this guide.

    In some countries you may need specific qualifications before you can carry out such work in
    a residential property.

Please read up on :doc:`/cookbook/sonoff-basic-light-switch` to get the background and principals of
the this project. It's all basically the same, but with a double switch.

So we will be using GPIO4 and GPIO14 for the two retractive switches, again they will both short to 0V
when the switch is clicked.

R1
--

The R1 version of the Dual controls the relays via the UART, so the code gets a bit complex here.

.. code-block:: yaml

    esphome:
      name: dual_ls
      platform: ESP8266
      board: esp01_1m

    wifi:
      ssid: !secret wifi_ssid
      password: !secret wifi_password

    logger:
      baud_rate: 0

    # Enable Home Assistant API
    api:

    ota:

    uart:
      tx_pin: GPIO01
      rx_pin: GPIO03
      baud_rate: 19200

    switch:
      - platform: template
        id: relay_1
        turn_on_action:
          if:
            condition:
              switch.is_off: relay_2
            then:
              - uart.write: [0xA0, 0x04, 0x01, 0xA1]
            else:
              - uart.write: [0xA0, 0x04, 0x03, 0xA1]
        turn_off_action:
          if:
            condition:
              switch.is_off: relay_2
            then:
              - uart.write: [0xA0, 0x04, 0x00, 0xA1]
            else:
              - uart.write: [0xA0, 0x04, 0x02, 0xA1]
        optimistic: true

      - platform: template
        id: relay_2
        turn_on_action:
          if:
            condition:
              switch.is_off: relay_1
            then:
              - uart.write: [0xA0, 0x04, 0x02, 0xA1]
            else:
              - uart.write: [0xA0, 0x04, 0x03, 0xA1]
        turn_off_action:
          if:
            condition:
              switch.is_off: relay_1
            then:
              - uart.write: [0xA0, 0x04, 0x00, 0xA1]
            else:
              - uart.write: [0xA0, 0x04, 0x01, 0xA1]
        optimistic: true

    binary_sensor:
      - platform: gpio
        pin:
          number: GPIO4
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
          number: GPIO14
          mode:
            input: true
            pullup: true
          inverted: true
        id: button_2
        on_press:
          then:
            - light.toggle: light_2

      - platform: status
        name: "Dual LS Status"

    status_led:
      pin:
        number: GPIO13
        inverted: yes

    output:
      - platform: template
        type: binary
        id: out_1
        write_action:
          if:
            condition:
              light.is_on: light_1
            then:
              - switch.turn_on: relay_1
            else:
              - switch.turn_off: relay_1

      - platform: template
        type: binary
        id: out_2
        write_action:
          if:
            condition:
              light.is_on: light_2
            then:
              - switch.turn_on: relay_2
            else:
              - switch.turn_off: relay_2

    light:
      - platform: binary
        name: "Dual L1"
        id: light_1
        output: out_1

      - platform: binary
        name: "Dual L2"
        id: light_2
        output: out_2


In the above code block, there is a *secrets.yaml* file so that you have just one place to change WiFi
details for all your devices.

The logger baud_rate: 0 is required to make sure the logged does not send any data over the UART or it would
mess with the relays.

Although not visible day to day, there is also the status LED configured so that it can be used when setting
up / debugging. Also a configured binary sensor to give status in case you want to perform an action / alert
if the light switch disconnects for any reason.

R2
--

This one is a lot simpler as it uses real GPIO for its relays. Please note this is untested, but should work!
It's basically the same as the :doc:`T2 </cookbook/sonoff-t1-3>`

.. code-block:: yaml

    esphome:
      name: dual_ls
      platform: ESP8266
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
        id: button
        on_press:
          then:
            - light.toggle: light_1

      - platform: gpio
        pin:
          number: GPIO14
          mode:
            input: true
            pullup: true
          inverted: true
        id: button
        on_press:
          then:
            - light.toggle: light_2

      - platform: status
        name: "Dual LS Status"

    output:
      - platform: gpio
        pin: GPIO12
        id: relay_1

      - platform: gpio
        pin: GPIO5
        id: relay_2

    light:
      - platform: binary
        name: "Dual L1"
        id: light_1
        output: relay_1

      - platform: binary
        name: "Dual L2"
        id: light_2
        output: relay_2

    status_led:
      pin:
        number: GPIO13
        inverted: yes



See Also
--------

- :doc:`/cookbook/sonoff-light-switch`
- :doc:`/guides/automations`
- :doc:`/devices/sonoff_basic`
