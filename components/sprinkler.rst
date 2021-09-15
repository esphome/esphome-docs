Sprinkler Controller
====================

.. seo::
    :description: Instructions for setting up the sprinkler controller component in ESPHome to control sprinkler valves.
    :image: sprinkler.png

The ``sprinkler`` controller component aims to behave like a sprinkler system/valve controller, much
like those made by companies such as Rain Bird or Hunter. It does so by automating control of a
number of :ref:`switch <config-switch>` components, each of which would typically be used to control
an individual electric valve via a relay or other switching device. It offers a number of features:

- Support for up to 127 valves/zones
- Support for a pump or "master" electric valve
- Adjustable "valve open delay" to help ensure valves are fully closed before the next one is opened
- Enable/disable for each individual valve, allowing valves to be omitted from a full cycle of the system
- A multiplier value to proportionally increase or decrease the run duration for all valves/zones
- Ability to:
  - Run only a single valve/zone for its configured run duration
  - Pause and resume a cycle
  - Iterate through valves/zones in forward or reverse order

.. code-block:: yaml

    # Example configuration entry
    sprinkler:
      id: sprinkler_ctrlr
      pump: sprinkler_pump_sw
      valve_open_delay: 5s
      valves:
        - name: "Front Yard"
          run_duration: 2700s
          enable_switch: front_yard_valve_enable_sw
          valve_switch: front_yard_valve_sw
        - name: "Back Yard"
          run_duration: 1800s
          enable_switch: back_yard_valve_enable_sw
          valve_switch: back_yard_valve_sw
  
Configuration variables:
------------------------

- **pump** (*Optional*, :ref:`Switch <config-switch>`): This is the :ref:`switch <config-switch>`
  component to be used to control the system's pump or "master" electric valve.
- **valve_open_delay** (**Required**, :ref:`config-time`): The delay in seconds from when a valve/zone
  is activated to when the switch component is turned on. Useful for systems with valves which depend
  on sufficient water pressure to close.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation. While optional,
  this is necessary to call controller actions (see below) such as ``start_full_cycle`` or ``shutdown``.
- **valves** (**Required**, *list*): A list of valves the controller should use. Each valve consists of:

  - **name** (*Optional*, *string*): The "friendly" name for the valve. This may be accessed in
    :ref:`lambdas <config-lambda>` by calling ``valve_name()``. This could be used, for example, to
    recall the valve/zone name to be shown on a display.
  - **run_duration** (**Required**, :ref:`config-time`): The duration in seconds this valve should
    remain open after it is activated. Note that ``valve_open_delay`` cuts into this interval. The
    controller's multiplier value is multiplied by this value to determine the run duration for a given
    valve/zone when it is activated, thus allowing the run duration for all valves/zones to be
    proportionally increased or decreased as desired.
  - **enable_switch** (*Optional*, :ref:`Switch <config-switch>`): This is the
    :ref:`switch <config-switch>` component to be used to enable this valve to be run as a part of a
    full cycle of the system. If it is not specified, the controller will assume that the valve is
    always enabled.
  - **valve_switch** (**Required**, :ref:`Switch <config-switch>`): This is the
    :ref:`switch <config-switch>` component to be used to control the valve for this part of the
    sprinkler system (often referred to as a "zone").

.. _sprinkler-controller_actions:

Controller Actions
------------------

- **sprinkler.start_full_cycle**: Starts a full cycle of the system. This enables the controller's
  ``auto_advance`` feature and the controller will iterate through all enabled valves/zones. They
  will each run for their configured ``run_duration`` multiplied by the controller's multiplier
  value. *Note that if NO valves are enabled when this action is called, the controller will
  automatically enable all valves.*
- **sprinkler.shutdown**: Immediately turns off all valves, effectively shutting down the system.
- **sprinkler.next_valve**: Immediately advances to the next valve (numerically).
- **sprinkler.previous_valve**: Immediately advances to the previous valve (numerically).
- **sprinkler.pause**: Immediately turns off all valves, saving the active valve and the amount of
  time remaining so that the cycle may be resumed later on.
- **sprinkler.resume**: Resumes a cycle placed on hold with ``sprinkler.pause``.
- **sprinkler.resume_or_start_full_cycle**: Resumes a cycle placed on hold with ``sprinkler.pause``,
  but if no cycle was paused, starts a full cycle (same as ``sprinkler.start_full_cycle``).

.. note::

    The ``next_valve`` and ``previous_valve`` actions ignore whether a valve is enabled via its
    ``enable_switch`` (if configured).

Controller Examples
-------------------

Beyond the basic example configuration above, other ESPHome elements may be called into play to help
build out a nice interface for the controller in the front end (Home Assistant). For example, the
:ref:`number <config-number>` component may be used to set valve run durations or the controller's
multiplier value:


.. code-block:: yaml

    # Example configuration to set multiplier via number
    number:
      - platform: template
        id: sprinkler_ctrlr_multiplier
        name: "Sprinkler Controller Multiplier"
        optimistic: true
        min_value: 0.1
        max_value: 10.0
        step: 0.1
        initial_value: 1.0
        set_action:
          lambda: "id(sprinkler_ctrlr).set_multiplier(x);"

A similar arrangement may also be used to set valve run durations using the
``set_valve_run_duration(x)`` method. Whole numbers must be used in this case, however, as valve
run durations are specified in seconds.

A couple of other noteworthy functions are ``set_auto_advance()`` and ``set_reverse()``. These set
the controller to run a full cycle (as opposed to a single valve/zone) and the order
(ascending/descending) in which the controller will iterate through the valves/zones (respectively).
Template :ref:`switches <config-switch>` are useful for these:

.. code-block:: yaml

    # Example configuration to enable/disable auto-advance and reverse
    switch:
      # zone auto-advance -- enables automatic advancing to the next (enabled) zone
      - platform: template
        id: sprinkler_auto_adv
        name: "Sprinkler Controller Auto Advance"
        turn_on_action:
          - lambda: "id(sprinkler_ctrlr).set_auto_advance(true);"
        turn_off_action:
          - lambda: "id(sprinkler_ctrlr).set_auto_advance(false);"
        lambda: 'return id(sprinkler_ctrlr).auto_advance();'
      # zone reverse -- iterates through zones in reverse/descending order when enabled
      - platform: template
        id: sprinkler_reverse
        name: "Sprinkler Controller Reverse"
        turn_on_action:
          - lambda: "id(sprinkler_ctrlr).set_reverse(true);"
        turn_off_action:
          - lambda: "id(sprinkler_ctrlr).set_reverse(false);"
        lambda: 'return id(sprinkler_ctrlr).reverse();'

Similarly, the ``start_single_valve(x)`` method (where ``x`` is the number of the valve to
activate) could be called from a template :ref:`switch's <config-switch>` ``turn_on`` action to
activate a single specific valve.

.. note::

    Exposing the individual valve switches directly to the front end (Home Assistant) is not
    recommended. Doing so will allow the sprinkler controller's mechanism/behavior to be easily
    circumvented which is likely not desirable other than for testing, debugging or troubleshooting.

Finally, another template switch may be used to start or stop the system:

.. code-block:: yaml

    # Example configuration to start/stop the system
    switch:
      - platform: template
        id: sprinkler_activate
        name: "Sprinkler Controller Activate"
        turn_on_action:
          - sprinkler.start_full_cycle: sprinkler_ctrlr
        turn_off_action:
          - sprinkler.shutdown: sprinkler_ctrlr
        lambda: 'return id(sprinkler_ctrlr).is_a_valid_valve(id(sprinkler_ctrlr).active_valve());'

See Also
--------

- :apiref:`sprinkler/sprinkler.h`
- :apiref:`switch/switch.h`
- :ghedit:`Edit`
