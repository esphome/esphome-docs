Template Lock
===============

.. seo::
    :description: Instructions for setting up template locks that can execute arbitrary actions when locked, unlocked, or opened
    :image: description.svg

The ``template`` lock platform allows you to create simple locks out of just actions and
an optional value lambda. Once defined, it will automatically appear in Home Assistant
as a lock and can be controlled through the frontend.

.. code-block:: yaml

    # Example configuration entry
    lock:
      - platform: template
        name: "Template Lock"
        lambda: |-
          if (id(some_binary_sensor).state) {
            return true;
          } else {
            return false;
          }
        lock_action:
          - switch.turn_on: switch1
        unlock_action:
          - switch.turn_off: switch1
        open_action:
          - button.press: button1


Possible return values for the optional lambda:

 - ``return true;`` if the lock should be reported as LOCKED.
 - ``return false;`` if the lock should be reported as UNLOCKED.
 - ``return {};`` if the last state should be repeated.

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the lock.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated repeatedly to get the current state of the lock.
- **lock_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests the lock to be locked.
- **unlock_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests the lock to be unlocked.
- **restore_state** (*Optional*, boolean): Sets whether ESPHome should attempt to restore the
  state on boot-up and call the lock/unlock actions with the recovered values. Defaults to ``no``.
- **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
  any command sent to the template lock will immediately update the reported state.
  Defaults to ``false``.
- **assumed_state** (*Optional*, boolean): Whether the true state of the lock is not known.
  This will make the Home Assistant frontend show buttons for both LOCK and UNLOCK actions, instead
  of hiding one of them when the lock is LOCKED/UNLOCKED. Defaults to ``false``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Lock <config-lock>`.

.. _lock-template-publish_action:

``lock.template.publish`` Action
----------------------------------

You can also publish a state to a template lock from elsewhere in your YAML file
with the ``lock.template.publish`` action.

.. code-block:: yaml

    # Example configuration entry
    lock:
      - platform: template
        name: "Template Lock"
        id: template_lock1

    # in some trigger
    on_...:
      - lock.template.publish:
          id: template_lock1
          state: ON

      # Templated
      - lock.template.publish:
          id: template_lock1
          state: !lambda 'return true;'

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the template lock.
- **state** (**Required**, boolean, :ref:`templatable <config-templatable>`):
  The state to publish.

.. note::

    This action can also be written in lambdas, the parameter of the `public_state` method denotes if
    the lock is currently locked or unlocked:

    .. code-block:: cpp

        id(template_lock1).publish_state(false);

See Also
--------

- :doc:`/guides/automations`
- :doc:`/components/lock/index`
- :doc:`/components/binary_sensor/index`
- :apiref:`template/lock/template_lock.h`
- :ghedit:`Edit`
