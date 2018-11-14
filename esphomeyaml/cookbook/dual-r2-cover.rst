Dual relay cover motor control
==============================

.. seo::
    :description: An example of how to integrate covers that are controlled by two relays into esphomelib.
    :image: sonoff_dual_r2.jpg
    :keywords: Relay, Sonoff Dual R2, Cover

The following is a possible configuration file for common covers that use a motor with 2 inputs.
Only one should be powered at a time (interlocking) to either move the cover up or down. For this
the `Sonoff Dual R2 <https://www.itead.cc/sonoff-dual.html>`__ can be used which has two independent
relays. Additionally this configuration allows the single button on the Sonoff to control the motion
by cycling between: open->stop->down->stop->...

These kind of motors automatically stop when the end of the cover movement is reached. However,
to be safe, this automation stops powering the motor after 1 minute of movement. In the rare case
of the end-stop switch in the motor failing this will reduce the risk for damage or fire.

Of the four main components (button sensor, 2 relays switches and the cover), only the cover will be
visible to the end-user. The other three are hidden by means of not including a ``name``. This is to
prevent accidentally switching on both relays simultaneously from MQTT/Home-assistant as that might be harmful
for some motors.

.. note::

    Controlling the cover to quickly (sending new open/close commands within a minute of previous commands)
    might cause unexpected behaviour (eg: cover stopping halfway). This is because the delayed relay off
    feature is implemented using asynchronous automations. So every time a open/close command is sent a
    delayed relay off command is added and old ones are not removed.

.. code:: yaml

  esphomeyaml:
    name: cover
    platform: ESP8266
    board: esp01_1m
    board_flash_mode: dout

  wifi:
    ssid: '***'
    password: '***'

  mqtt:
    broker: 'mqtt'
    username: ''
    password: ''

  logger:

  ota:

  binary_sensor:
    - platform: gpio
      pin:
        number: 10
        inverted: true
      id: button
      on_press:
        then:
          # logic for cycling through movements: open->stop->close->stop->...
          - lambda: |
              if (id(cover).state == cover::COVER_OPEN) {
                if (id(open).state){
                  // cover is in opening movement, stop it
                  id(cover).stop();
                } else {
                  // cover has finished opening, close it
                  id(cover).close();
                }
              } else {
                if (id(close).state){
                  // cover is in closing movement, stop it
                  id(cover).stop();
                } else {
                  // cover has finished closing, open it
                  id(cover).open();
                }
              }

  switch:
    - platform: gpio
      pin: 12
      id: open
    - platform: gpio
      pin: 5
      id: close

  cover:
    - platform: template
      name: "Cover"
      id: cover
      open_action:
        # cancel potential previous movement
        - switch.turn_off: close
        # perform movement
        - switch.turn_on: open
        # wait until cover is open
        - delay: 60s
        # turn of relay to prevent keeping the motor powered
        - switch.turn_off: open
      close_action:
        - switch.turn_off: open
        - switch.turn_on: close
        - delay: 60s
        - switch.turn_off: close
      stop_action:
        - switch.turn_off: open
        - switch.turn_off: close
      optimistic: true

See Also
--------

- :doc:`/esphomeyaml/guides/automations`
- :doc:`/esphomeyaml/components/cover/template`
- :doc:`/esphomeyaml/devices/sonoff`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/cookbook/dual-r2-cover.rst>`__

.. disqus::
