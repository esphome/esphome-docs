Interval Component
------------------

This component allows you to run actions at fixed time intervals. For example, if you want to toggle a switch every
minute, you can use this component. Please note that it's possible to achieve the same thing with the
:ref:`time.on_time <time-on_time>` trigger, but this technique is more light-weight and user-friendly.

.. code-block:: yaml

    # Example configuration entry
    interval:
      - interval: 1min
        then:
          - switch.toggle: relay_1


If a startup delay is configured, the first execution of the actions will not occur before at least that time after boot.

Configuration variables:
************************

- **interval** (**Required**, :ref:`config-time`): The interval to execute the action with.
- **startup_delay** (*Optional*, :ref:`config-time`): An optional startup delay - defaults to zero.
- **autostart** (*Optional*, boolean): Whether the interval should start on boot, or wait until ``interval.start`` is called.
- defaults to ``true``
- **then** (**Required**, :ref:`Action <config-action>`): The action to perform.


.. note::

    ``startup_delay`` and ``autostart`` cannot be used together.

Actions:
********

``interval.start`` Action
-------------------------

This action can be called on some trigger when the interval needs to be (re-)started, either because ``autostart`` was set to false, or because ``interval.stop`` was called before.

.. code-block:: yaml

    # Example configuration entry
    interval:
      - interval: 5s
        id: my_interval
        then:
          - logger.log: Tick

    # in some trigger
    on_...:
      - interval.start: my_interval

Configuration options:
- **id** (**Required**, :ref:`config-id`): The ID of the interval to start.

``interval.stop`` Action
-------------------------

This action can be called on some trigger when the interval needs to be stopped.

.. code-block:: yaml

    # Example configuration entry
    interval:
      - interval: 5s
        id: my_interval
        then:
          - logger.log: Tick

    # in some trigger
    on_...:
      - interval.stop: my_interval

Configuration options:
- **id** (**Required**, :ref:`config-id`): The ID of the interval to stop.

See Also
--------

- :doc:`index`
- :doc:`/automations/actions`
- :doc:`/automations/templates`
- :ghedit:`Edit`
