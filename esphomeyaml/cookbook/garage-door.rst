Simple Garage Door
==================

.. seo::
    :description: Instructions for setting up a simple garage door in esphomelib.
    :image: window-open.png

The following is a possible configuration file for garage doors that are controlled by two relays:
One for opening and another one for closing the garage door. When either one of them is turned on
for a short period of time, the close/open action begins.



.. code-block:: yaml

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
        
        
Another configuration that uses a single relay to activate a remote control button. The button can only start or stop the motor of the gate. In itself, the button or remote can not know if it opens or closes the gate. The relay simulates the button press for 500ms.


.. code-block:: yaml

    switch:
      - platform: gpio
        pin: D6
        id: relay
      - platform: template
        name: "Gate Remote"
        icon: "mdi:gate"
        optimistic: no
        turn_on_action:
        - switch.turn_on: relay
        - delay: 500ms
        - switch.turn_off: relay


See Also
--------

- :doc:`/esphomeyaml/guides/automations`
- :doc:`/esphomeyaml/components/cover/template`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/cookbook/garage-door.rst>`__

.. disqus::
