Simple Garage Door
==================

.. seo::
    :description: Instructions for setting up a simple garage door in ESPHome.
    :image: window-open.svg

The following is a possible configuration file for garage doors that are controlled by two relays:
One for opening and another one for closing the garage door. When either one of them is turned on
for a short period of time, the close/open action begins.

.. code-block:: yaml

    switch:
      - platform: gpio
        pin: GPIOXX
        name: "Garage Door Open Switch"
        id: open_switch
      - platform: gpio
        pin: GPIOXX
        name: "Garage Door Close Switch"
        id: close_switch
    cover:
      - platform: template
        name: "Garage Door"
        open_action:
          # Cancel any previous action
          - switch.turn_off: close_switch
          # Turn the OPEN switch on briefly
          - switch.turn_on: open_switch
          - delay: 0.1s
          - switch.turn_off: open_switch
        close_action:
          - switch.turn_off: open_switch
          - switch.turn_on: close_switch
          - delay: 0.1s
          - switch.turn_off: close_switch
        stop_action:
          - switch.turn_off: close_switch
          - switch.turn_off: open_switch
        optimistic: true
        assumed_state: true

See Also
--------

- :doc:`/automations/index`
- :doc:`/components/switch/gpio`
- :doc:`/components/cover/template`
- :ghedit:`Edit`
