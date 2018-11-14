Template Switch
===============

.. seo::
    :description: Instructions for setting up template switches that can execute arbitrary actions when turned on or off.
    :image: description.svg

The ``template`` switch platform allows you to create simple switches out of just actions and
an optional value lambda. Once defined, it will automatically appear in Home Assistant
as a switch and can be controlled through the frontend.

.. code:: yaml

    # Example configuration entry
    switch:
      - platform: template
        name: "Template Switch"
        lambda: |-
          if (id(some_binary_sensor).state) {
            return true;
          } else {
            return false;
          }
        turn_on_action:
          - switch.turn_on: switch2
        turn_off_action:
          - switch.turn_on: switch1
        optimistic: true


Possible return values for the optional lambda:

 - ``return true;`` if the switch should be reported as ON.
 - ``return false;`` if the switch should be reported as OFF.
 - ``return {};`` if the last state should be repeated.

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the switch.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated repeatedly to get the current state of the switch.
  Only state *changes* will be published to MQTT.
- **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
  any command sent to the template cover will immediately update the reported state and no lambda
  needs to be used. Defaults to ``false``.
- **turn_on_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests the switch to be turned on.
- **turn_off_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests the switch to be turned on.
- **restore_state** (*Optional*, boolean): Sets whether esphomelib should attempt to restore the
  state on boot-up and call the turn on/off actions with the recovered values. Defaults to ``yes``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-binary_sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

See Also
--------

- :doc:`/esphomeyaml/guides/automations`
- :doc:`/esphomeyaml/components/switch/index`
- :doc:`/esphomeyaml/components/binary_sensor/index`
- :doc:`API Reference </api/switch/template>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/switch/template.rst>`__

.. disqus::
