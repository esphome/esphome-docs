Dual relay cover motor control
==============================

.. seo::
    :description: An example of how to integrate covers that are controlled by two relays into ESPHome.
    :image: sonoff_dual_r2.jpg
    :keywords: Relay, Sonoff Dual R2, Cover

The following is a possible configuration file for common covers that use a motor with 2 inputs.
Only one should be powered at a time (interlocking) to either move the cover up or down. For this
the `Sonoff Dual R2 <https://www.itead.cc/sonoff-dual.html>`__ can be used which has two independent
relays. Additionally this configuration allows the single button on the Sonoff to control the motion
by cycling between: open->stop->close->stop->...

These kind of motors automatically stop when the end of the cover movement is reached. However,
to be safe, this automation stops powering the motor after 1 minute of movement. In the rare case
of the end-stop switch in the motor failing this will reduce the risk for damage or fire.

Of the four main components (button sensor, 2 relays switches and the cover), only the cover will be
visible to the end-user. The other three are hidden by means of not including a ``name``. This is to
prevent accidentally switching on both relays simultaneously from Home Assistant as that might be harmful
for some motors.

.. note::

    Controlling the cover to quickly (sending new open/close commands within a minute of previous commands)
    might cause unexpected behaviour (eg: cover stopping halfway). This is because the delayed relay off
    feature is implemented using asynchronous automations. So every time a open/close command is sent a
    delayed relay off command is added and old ones are not removed.

.. code-block:: yaml

    esphome:
      name: cover
      platform: ESP8266
      board: esp01_1m

    wifi:
      ssid: '***'
      password: '***'

    api:

    logger:

    ota:

    binary_sensor:
    - platform: gpio
      pin:
        number: GPIO10
        inverted: true
      id: button
      on_press:
        then:
          # logic for cycling through movements: open->stop->close->stop->...
          - lambda: |
              if (id(cover).state == COVER_OPEN) {
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
      pin: GPIO12
      interlock: [open, close]
      id: open
    - platform: gpio
      pin: GPIO5
      interlock: [open, close]
      id: close

    cover:
    - platform: time_based
      name: "Cover"
      id: cover
      open_action:
        - switch.turn_on: open
      open_duration: 60s
      close_action:
        - switch.turn_on: close
      close_duration: 60s
      stop_action:
        - switch.turn_off: open
        - switch.turn_off: close

See Also
--------

- :doc:`/guides/automations`
- :doc:`/components/cover/time_based`
- :doc:`/devices/sonoff`
- :ghedit:`Edit`
