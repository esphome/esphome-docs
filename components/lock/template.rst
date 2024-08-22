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
            return LOCK_STATE_LOCKED;
          } else {
            return LOCK_STATE_UNLOCKED;
          }
        lock_action:
          - switch.turn_on: switch1
        unlock_action:
          - switch.turn_off: switch1
        open_action:
          - button.press: button1


Possible return values for the optional lambda:

 - ``return LOCK_STATE_LOCKED;`` if the lock should be reported as LOCKED.
 - ``return LOCK_STATE_UNLOCKED;`` if the lock should be reported as UNLOCKED.
 - ``return LOCK_STATE_JAMMED;`` if the lock should be reported as JAMMED.
 - ``return LOCK_STATE_LOCKING;`` if the lock should be reported as LOCKING.
 - ``return LOCK_STATE_UNLOCKING;`` if the lock should be reported as UNLOCKING.
 - ``return {};`` if the last state should be repeated.

.. note::

    Only ``LOCK_STATE_LOCKED`` and ``LOCK_STATE_UNLOCKED`` are supported by the MQTT component in Home Assistant

Configuration variables:
------------------------

- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated repeatedly to get the current state of the lock.
- **lock_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests the lock to be locked.
- **unlock_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote (like Home Assistant's frontend) requests the lock to be unlocked.
- **optimistic** (*Optional*, boolean): Whether to operate in optimistic mode - when in this mode,
  any command sent to the template lock will immediately update the reported state.
  Defaults to ``false``.
- **assumed_state** (*Optional*, boolean): Whether the true state of the lock is not known.
  This will make the Home Assistant frontend show buttons for both LOCK and UNLOCK actions, instead
  of hiding one of them when the lock is LOCKED/UNLOCKED. Defaults to ``false``.
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
          state: LOCK_STATE_LOCKED

      # Templated
      - lock.template.publish:
          id: template_lock1
          state: !lambda 'return LOCK_STATE_LOCKED;'

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the template lock.
- **state** (**Required**, boolean, :ref:`templatable <config-templatable>`):
  The state to publish.

.. note::

    This action can also be written in lambdas, the parameter of the `publish_state` method denotes the state the
    lock should become:

    .. code-block:: cpp

        id(template_lock1).publish_state(lock::LOCK_STATE_LOCKED);

See Also
--------

- :doc:`/automations/index`
- :doc:`/components/lock/index`
- :doc:`/components/binary_sensor/index`
- :apiref:`template/lock/template_lock.h`
- :ghedit:`Edit`
