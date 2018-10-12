Simple Garage Door
==================

The following is a possible configuration file for garage doors that are controlled by two relays:
One for opening and another one for closing the garage door. When either one of them is turned on
for a short period of time, the close/open action begins.



.. code:: yaml

    switch:
      - platform: gpio
        pin: D3
        name: "Garage Door Open Switch"
        id: open_switch
      - platform: gpio
        pin: D4
        name: "Garage Door Close Switch"
        id: close_switch
    cover:
      - platform: template
        name: "Garage Door"
        open_action:
          # Cancel any previous action
          - switch.turn_off:
              id: close_switch
          # Turn the OPEN switch on briefly
          - switch.turn_on:
              id: open_switch
          - delay: 0.1s
          - switch.turn_off:
              id: open_switch
        close_action:
          - switch.turn_off:
              id: open_switch
          - switch.turn_on:
              id: close_switch
          - delay: 0.1s
          - switch.turn_off:
              id: close_switch
        stop_action:
          - switch.turn_off:
              id: close_switch
          - switch.turn_off:
              id: open_switch
        optimistic: true

See Also
--------

- :doc:`/esphomeyaml/guides/automations`
- :doc:`/esphomeyaml/components/cover/template`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/cookbook/garage-door.rst>`__

.. disqus::
