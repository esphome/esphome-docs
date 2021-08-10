Template Cover with Endstops
============================

.. seo::
    :description: An example of how to integrate covers with endstops in ESPHome.
    :image: window-open.svg

The following is an example configuration for controlling covers (like window blinds etc)
with ESPHome. This guide assumes that the cover is set up with two endstops at the top
and the bottom. When these endstops are reached, the cover will automatically stop.

To protect the motors from spinning indefinitely (in case an endstop fails) the motors
also have a maximum run time - after 3 minutes they will automatically turn off even if the
endstop is not reached.

ESPHome uses Home Assistant's cover architecture model which has two states: "OPEN" or
"CLOSED". We will map OPEN to "cover is at the top endstop" and CLOSE to "cover is at the bottom".

.. code-block:: yaml

    switch:
      # The switch that turns the UP direction on
      - platform: gpio
        pin: D1
        id: up_pin
        # Use interlocking to keep at most one of the two directions on
        interlock: &interlock_group [up_pin, down_pin]
        # If ESP reboots, do not attempt to restore switch state
        restore_mode: always off

      # The switch that turns the DOWN direction on
      - platform: gpio
        pin: D2
        id: down_pin
        interlock: *interlock_group
        restore_mode: always off


    binary_sensor:
      - platform: gpio
        pin: D4
        id: top_endstop
      - platform: gpio
        pin: D5
        id: bottom_endstop

    cover:
      - platform: endstop
        name: "My Endstop Cover"
        id: my_cover
        open_action:
          - switch.turn_on: up_pin
        open_duration: 2min
        open_endstop: top_endstop

        close_action:
          - switch.turn_on: down_pin
        close_duration: 2min
        close_endstop: bottom_endstop
        stop_action:
          - switch.turn_off: up_pin
          - switch.turn_off: down_pin
        max_duration: 3min

You can then optionally also add manual controls to the cover with three buttons:
open, close, and stop.

.. code-block:: yaml

    binary_sensor:
      # [...] - Previous binary sensors
      - platform: gpio
        id: open_button
        pin: D3
        on_press:
          - cover.open: my_cover
      - platform: gpio
        id: close_button
        pin: D6
        on_press:
          - cover.close: my_cover
      - platform: gpio
        id: stop_button
        pin: D7
        on_press:
          - cover.stop: my_cover

See Also
--------

- :doc:`/guides/automations`
- :doc:`/components/cover/template`
- :doc:`dual-r2-cover`
- :ghedit:`Edit`
