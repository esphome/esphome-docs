Template Switch
===============

.. seo::
    :description: Instructions for setting up template switches that can execute arbitrary actions when turned on or off.
    :image: description.png

The ``template`` switch platform allows you to create simple switches out of just actions and
an optional value lambda. Once defined, it will automatically appear in Home Assistant
as a switch and can be controlled through the frontend.

.. code-block:: yaml

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


Possible return values for the optional lambda:

 - ``return true;`` if the switch should be reported as ON.
 - ``return false;`` if the switch should be reported as OFF.
 - ``return {};`` if the last state should be repeated.

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the switch.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated repeatedly to get the current state of the switch.
- **turn_on_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests the switch to be turned on.
- **turn_off_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests the switch to be turned off.
- **restore_state** (*Optional*, boolean): Sets whether ESPHome should attempt to restore the
  state on boot-up and call the turn on/off actions with the recovered values. Defaults to ``no``.
- **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
  any command sent to the template switch will immediately update the reported state.
  Defaults to ``false``.
- **assumed_state** (*Optional*, boolean): Whether the true state of the switch is not known.
  This will make the Home Assistant frontend show buttons for both ON and OFF actions, instead
  of hiding one of them when the switch is ON/OFF. Defaults to ``false``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Switch <config-switch>`.

.. _switch-template-publish_action:

``switch.template.publish`` Action
----------------------------------

You can also publish a state to a template switch from elsewhere in your YAML file
with the ``switch.template.publish`` action.

.. code-block:: yaml

    # Example configuration entry
    switch:
      - platform: template
        name: "Template Switch"
        id: template_swi

    # in some trigger
    on_...:
      - switch.template.publish:
          id: template_swi
          state: ON

      # Templated
      - switch.template.publish:
          id: template_swi
          state: !lambda 'return true;'

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the template switch.
- **state** (**Required**, boolean, :ref:`templatable <config-templatable>`):
  The state to publish.

.. note::

    This action can also be written in lambdas:

    .. code-block:: cpp

        id(template_swi).publish_state(42.0);

See Also
--------

- :doc:`/guides/automations`
- :doc:`/components/switch/index`
- :doc:`/components/binary_sensor/index`
- :apiref:`template/switch/template_switch.h`
- :ghedit:`Edit`
