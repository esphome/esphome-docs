Sprinkler Controller
====================

.. seo::
    :description: Instructions for setting up the sprinkler controller component in ESPHome to control sprinkler valves.
    :image: sprinkler.png

The ``sprinkler`` controller component aims to behave like a sprinkler system/valve controller, much
like those made by companies such as Rain Bird or Hunter. It does so by automating control of a
number of :ref:`switch <config-switch>` components, each of which would typically be used to control
an individual electric valve via a relay or other switching device. It offers support for:

- Up to 256 valves/zones per controller instance
- Multiple controller instances on a single device
- Multiple pumps, which may be shared across controller instances
- Running only a single valve/zone for its configured run duration
- Pausing and resuming a cycle
- Iterating through valves/zones in forward or reverse order

In addition, it provides:

- Enable/disable for each individual valve, allowing valves to be omitted from a full cycle of the system
- A multiplier value to proportionally increase or decrease the run duration for all valves/zones
  within a given controller instance
- Valve management strategies to accommodate varying types of hardware:

  - Adjustable "valve open delay" to help ensure valves are fully closed before the next one is opened
  - Adjustable "valve overlap" to help minimize banging of pipes due to water hammer

.. note::

    While the term "pump" is used throughout this document, the device controlled need not be a
    physical pump. Instead, it may simply be another electric valve located upstream of distribution
    valves (often known in the industry as a "main" or "master" valve). The pump or upstream valve
    simply controls the water supply to other downstream valves.

.. code-block:: yaml

    # Example minimal configuration entry
    sprinkler:
      - id: sprinkler_ctrlr
        name: "Sprinklers"
        auto_advance_switch_name: "Sprinklers Auto Advance"
        valves:
          - valve_switch_name: "Front Lawn"
            enable_switch_name: "Enable Front Lawn"
            run_duration: 1800s
            valve_switch: lawn_sprinkler_valve_sw0
          - valve_switch_name: "Back Lawn"
            enable_switch_name: "Enable Back Lawn"
            run_duration: 900s
            valve_switch: lawn_sprinkler_valve_sw1

Configuration variables:
------------------------

- **name** (**Required** with more than one valve, *string*): The name for the sprinkler controller's 
  main switch as it will appear in the front end. This switch, when turned on, calls the
  ``sprinkler.resume_or_start_full_cycle`` action; when turned off, it calls the ``sprinkler.shutdown``
  action (see below). It will appear to be "on" when any valve on the controller is active. This switch
  will not appear in the front end if the controller is configured with only one valve.
- **auto_advance_switch_name** (**Required** with more than one valve, *string*): The name for the
  sprinkler controller's "auto-advance" switch as it will appear in the front end. When this switch is
  turned on while a valve is active, when the valve's ``run_duration`` is reached, the sprinkler
  controller will automatically advance to the next enabled valve as a part of a "full cycle" of the
  system. When turned off, the sprinkler controller will shut down after the active valve's
  ``run_duration`` is reached. This switch will not appear in the front end if the controller is
  configured with only one valve.
- **reverse_switch_name** (*Optional*, *string*): The name for the sprinkler controller's reverse switch
  as it will appear in the front end. When this switch is turned on, the controller will iterate through
  the valves in reverse order (last-to-first as they appear in the controller's configuration). When
  this switch is turned off or not provided, the controller will iterate through the valves first-to-last.
  This switch will not appear in the front end if the controller is configured with only one valve.
- **valve_open_delay** (*Optional*, :ref:`config-time`): The delay in seconds from when a valve/zone
  is activated to when the switch component is turned on. Useful for systems with valves which depend
  on sufficient water pressure to close. May not be used with *valve_overlap*.
- **valve_overlap** (*Optional*, :ref:`config-time`): The delay in seconds from when a valve/zone
  is activated to when the previous valve/switch will be turned off. This may help prevent pipes from
  banging as the valves close. May not be used with *valve_open_delay*.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation. While optional,
  this is necessary to call controller actions (see below) such as ``start_full_cycle`` or ``shutdown``.
- **valves** (**Required**, *list*): A list of valves the controller should use. Each valve consists of:

  - **enable_switch_name** (*Optional*, *string*): The name for the switch component to be used to enable
    this valve to be run as a part of a full cycle of the system. When this switch is turned off, the valve
    will be excluded from a full cycle of the system. When this switch is turned on or not provided, the
    controller will include the valve in a full cycle of the system.
  - **valve_switch_name** (**Required**, *string*): The name for the switch component to be used to control
    the valve for this part of the sprinkler system (often referred to as a "zone"). When this switch is
    turned on, the controller's "auto-advance" feature is disabled and it will activate the associated
    valve for its ``run_duration`` multiplied by the controller's multiplier value. When this switch is
    turned off, the ``sprinkler.shutdown`` action is called (see below).
  - **pump_switch** (*Optional*, :ref:`Switch <config-switch>`): This is the :ref:`switch <config-switch>`
    component to be used to control the valve's pump or other upstream electric valve.
  - **run_duration** (**Required**, :ref:`config-time`): The duration in seconds this valve should
    remain on/open after it is activated. Note that ``valve_open_delay`` cuts into this interval while
    ``valve_overlap`` extends it. When a given valve is activated, the controller's multiplier value is
    multiplied by this value to determine the run duration for the valve, thus allowing the run duration for
    all valves/zones to be proportionally increased or decreased as desired.
  - **valve_switch** (**Required**, :ref:`Switch <config-switch>`): This is the :ref:`switch <config-switch>`
    component to be used to control the valve that operates the given section or zone of the sprinkler
    system. Typically this would be a :doc:`GPIO switch <switch/gpio>` wired to control a relay
    or other switching device which in turn would activate the respective valve. *It is not recommended
    to expose this switch to the front end.*

.. _sprinkler-controller-actions:

Controller Actions
------------------

.. _sprinkler-controller-action_start_full_cycle:

``sprinkler.start_full_cycle`` action
*************************************

Starts a full cycle of the system. This enables the controller's "auto-advance" feature and the
controller will iterate through all enabled valves/zones. They will each run for their configured
``run_duration`` multiplied by the controller's multiplier value. *Note that if NO valves are enabled
when this action is called, the controller will automatically enable all valves.*

.. code-block:: yaml

    on_...:
      then:
        - sprinkler.start_full_cycle: sprinkler_ctrlr

.. _sprinkler-controller-action_start_single_valve:

``sprinkler.start_single_valve`` action
***************************************

Starts a single valve. This disables the controller's "auto-advance" feature so that only this
valve/zone will run. The valve will remain on for its configured ``run_duration`` multiplied by
the controller's multiplier value. *Note that this action ignores whether the valve is enabled;
that is, when called, the specified valve will always run.* Valves are numbered in the order they
appear in the sprinkler controller's configuration starting at zero (0).

.. code-block:: yaml

    on_...:
      then:
        - sprinkler.start_single_valve:
            id: sprinkler_ctrlr
            valve_number: 0

.. _sprinkler-controller-action_shutdown:

``sprinkler.shutdown`` action
*****************************

Immediately turns off all valves, effectively shutting down the system.

.. code-block:: yaml

    on_...:
      then:
        - sprinkler.shutdown: sprinkler_ctrlr

.. _sprinkler-controller-action_next_valve:

``sprinkler.next_valve`` action
*******************************

Immediately advances to the next valve (numerically). If no valve is active, the first valve (as
they appear in the controller's configuration) will be started.

.. code-block:: yaml

    on_...:
      then:
        - sprinkler.next_valve: sprinkler_ctrlr

.. _sprinkler-controller-action_previous_valve:

``sprinkler.previous_valve`` action
***********************************

Immediately advances to the previous valve (numerically). If no valve is active, the last valve (as
they appear in the controller's configuration) will be started.

.. code-block:: yaml

    on_...:
      then:
        - sprinkler.previous_valve: sprinkler_ctrlr

.. _sprinkler-controller-action_pause:

``sprinkler.pause`` action
**************************

Immediately turns off all valves, saving the active valve and the amount of time remaining so that
the cycle may be resumed later on.

.. code-block:: yaml

    on_...:
      then:
        - sprinkler.pause: sprinkler_ctrlr

.. _sprinkler-controller-action_resume:

``sprinkler.resume`` action
***************************

Resumes a cycle placed on hold with ``sprinkler.pause``. If there is no paused cycle, this action
will do nothing.

.. code-block:: yaml

    on_...:
      then:
        - sprinkler.resume: sprinkler_ctrlr

.. _sprinkler-controller-action_resume_or_start_full_cycle:

``sprinkler.resume_or_start_full_cycle`` action
***********************************************

Resumes a cycle placed on hold with ``sprinkler.pause``, but if no cycle was paused, starts a full
cycle (equivalent to ``sprinkler.start_full_cycle``).

.. code-block:: yaml

    on_...:
      then:
        - sprinkler.resume_or_start_full_cycle: sprinkler_ctrlr

.. _sprinkler-controller-action_set_multiplier:

``sprinkler.set_multiplier`` action
***********************************

Sets the multiplier value used to proportionally increase or decrease the run duration for all valves/zones.
When a given valve is activated, this value is multiplied by the valve's run duration (see below) to determine
the valve's actual run duration.

.. code-block:: yaml

    on_...:
      then:
        - sprinkler.set_multiplier:
            id: sprinkler_ctrlr
            multiplier: 1.5

.. _sprinkler-controller-action_set_valve_run_duration:

``sprinkler.set_valve_run_duration`` action
*******************************************

Sets the run duration for the specified valve. When the valve is activated, this value is multiplied by the
multiplier value (see above) to determine the valve's actual run duration.

.. code-block:: yaml

    on_...:
      then:
        - sprinkler.set_valve_run_duration:
            id: sprinkler_ctrlr
            valve_number: 0
            run_duration: 600s

.. note::

    The ``next_valve``, ``previous_valve`` and ``start_single_valve`` actions ignore whether a valve
    is enabled via its enable switch.

Controller Examples
-------------------

Single Controller, Single Valve, No Pump
****************************************

This first example illustrates a complete, single-valve system with no pump/upstream valve(s). It
could be useful for controlling a single valve independent of any other sprinkler controllers. A pump
could easily be added by adding the ``pump_switch`` parameter and a :ref:`switch <config-switch>`.

.. code-block:: yaml

    esphome:
        name: esp-sprinkler-controller
        platform: ESP32
        board: featheresp32

    wifi:
        ssid: "wifi_ssid"
        password: "wifi_password"

    logger:

    sprinkler:
      - id: garden_sprinkler_ctrlr
        valves:
          - valve_switch_name: "Flower Garden"
            run_duration: 300s
            valve_switch: garden_sprinkler_valve

    switch:
      - platform: gpio
        id: garden_sprinkler_valve
        pin: 5

Single Controller, Three Valves, No Pump
****************************************

This example illustrates a complete, simple three-valve system with no pump/upstream valve(s):

.. code-block:: yaml

    esphome:
        name: esp-sprinkler-controller
        platform: ESP32
        board: featheresp32

    wifi:
        ssid: "wifi_ssid"
        password: "wifi_password"

    logger:

    sprinkler:
      - id: lawn_sprinkler_ctrlr
        name: "Lawn Sprinklers"
        auto_advance_switch_name: "Lawn Sprinklers Auto Advance"
        reverse_switch_name: "Lawn Sprinklers Reverse"
        valve_overlap: 5s
        valves:
          - valve_switch_name: "Front Lawn"
            enable_switch_name: "Enable Front Lawn"
            run_duration: 900s
            valve_switch: lawn_sprinkler_valve_sw0
          - valve_switch_name: "Side Lawn"
            enable_switch_name: "Enable Side Lawn"
            run_duration: 900s
            valve_switch: lawn_sprinkler_valve_sw1
          - valve_switch_name: "Back Lawn"
            enable_switch_name: "Enable Back Lawn"
            run_duration: 900s
            valve_switch: lawn_sprinkler_valve_sw2

    switch:
      - platform: gpio
        id: lawn_sprinkler_valve_sw0
        pin: 0
      - platform: gpio
        id: lawn_sprinkler_valve_sw1
        pin: 2
      - platform: gpio
        id: lawn_sprinkler_valve_sw2
        pin: 4

Single Controller, Three Valves, Single Pump
********************************************

This example illustrates a complete three-valve system with a single pump/upstream valve:

.. code-block:: yaml

    esphome:
        name: esp-sprinkler-controller
        platform: ESP32
        board: featheresp32

    wifi:
        ssid: "wifi_ssid"
        password: "wifi_password"

    logger:

    sprinkler:
      - id: lawn_sprinkler_ctrlr
        name: "Lawn Sprinklers"
        auto_advance_switch_name: "Lawn Sprinklers Auto Advance"
        reverse_switch_name: "Lawn Sprinklers Reverse"
        valve_open_delay: 5s
        valves:
          - valve_switch_name: "Front Lawn"
            enable_switch_name: "Enable Front Lawn"
            pump_switch: sprinkler_pump_sw
            run_duration: 900s
            valve_switch: lawn_sprinkler_valve_sw0
          - valve_switch_name: "Side Lawn"
            enable_switch_name: "Enable Side Lawn"
            pump_switch: sprinkler_pump_sw
            run_duration: 900s
            valve_switch: lawn_sprinkler_valve_sw1
          - valve_switch_name: "Back Lawn"
            enable_switch_name: "Enable Back Lawn"
            pump_switch: sprinkler_pump_sw
            run_duration: 900s
            valve_switch: lawn_sprinkler_valve_sw2

    switch:
      - platform: gpio
        id: sprinkler_pump_sw
        pin: 12
      - platform: gpio
        id: lawn_sprinkler_valve_sw0
        pin: 0
      - platform: gpio
        id: lawn_sprinkler_valve_sw1
        pin: 2
      - platform: gpio
        id: lawn_sprinkler_valve_sw2
        pin: 4

Dual Controller, Five Valves, Two Pumps
***************************************

This example illustrates a complete and more complex dual-controller system with a total of five
valves (three on the first controller and two on the second controller) and two pumps/upstream
valves, each of which are shared between the two controllers:

.. code-block:: yaml

    esphome:
        name: esp-sprinkler-controller
        platform: ESP32
        board: featheresp32

    wifi:
        ssid: "wifi_ssid"
        password: "wifi_password"

    logger:

    sprinkler:
      - id: lawn_sprinkler_ctrlr
        name: "Lawn Sprinklers"
        auto_advance_switch_name: "Lawn Sprinklers Auto Advance"
        reverse_switch_name: "Lawn Sprinklers Reverse"
        valve_overlap: 5s
        valves:
          - valve_switch_name: "Front Lawn"
            enable_switch_name: "Enable Front Lawn"
            pump_switch: sprinkler_pump_sw0
            run_duration: 900s
            valve_switch: lawn_sprinkler_valve_sw0
          - valve_switch_name: "Side Lawn"
            enable_switch_name: "Enable Side Lawn"
            pump_switch: sprinkler_pump_sw0
            run_duration: 900s
            valve_switch: lawn_sprinkler_valve_sw1
          - valve_switch_name: "Back Lawn"
            enable_switch_name: "Enable Back Lawn"
            pump_switch: sprinkler_pump_sw1
            run_duration: 900s
            valve_switch: lawn_sprinkler_valve_sw2
      - id: garden_sprinkler_ctrlr
        name: "Garden Sprinklers"
        auto_advance_switch_name: "Garden Sprinklers Auto Advance"
        reverse_switch_name: "Garden Sprinklers Reverse"
        valve_open_delay: 5s
        valves:
          - valve_switch_name: "Front Garden"
            enable_switch_name: "Enable Front Garden"
            pump_switch: sprinkler_pump_sw0
            run_duration: 900s
            valve_switch: garden_sprinkler_valve_sw0
          - valve_switch_name: "Back Garden"
            enable_switch_name: "Enable Back Garden"
            pump_switch: sprinkler_pump_sw1
            run_duration: 900s
            valve_switch: garden_sprinkler_valve_sw1

    switch:
      - platform: gpio
        id: sprinkler_pump_sw0
        pin: 12
      - platform: gpio
        id: sprinkler_pump_sw1
        pin: 13
      - platform: gpio
        id: lawn_sprinkler_valve_sw0
        pin: 0
      - platform: gpio
        id: lawn_sprinkler_valve_sw1
        pin: 2
      - platform: gpio
        id: lawn_sprinkler_valve_sw2
        pin: 4
      - platform: gpio
        id: garden_sprinkler_valve_sw0
        pin: 14
      - platform: gpio
        id: garden_sprinkler_valve_sw1
        pin: 15

.. note::

    In this final complete configuration example, pump control is split among the two sprinkler
    controller instances. This will behave as expected; multiple instances of the controller will
    communicate to ensure any given pump is activated and deactivated only as necessary, even when
    the controllers are operating simultaneously.

Expose Sprinkler Controller Actions via user-API
************************************************

This configuration snippet illustrates how user-defined ESPHome API services may be used to expose
various sprinkler controller actions to the front end. This could be useful to change settings
and/or trigger sprinkler controller actions using automations.

.. code-block:: yaml

    api:
      services:
        - service: set_multiplier
          variables:
            multiplier: float
          then:
            - sprinkler.set_multiplier:
                id: lawn_sprinkler_ctrlr
                multiplier: !lambda 'return multiplier;'
        - service: start_full_cycle
          then:
            - sprinkler.start_full_cycle: lawn_sprinkler_ctrlr
        - service: start_single_valve
          variables:
            valve: int
          then:
            - sprinkler.start_single_valve:
                id: lawn_sprinkler_ctrlr
                valve_number: !lambda 'return valve;'
        - service: next_valve
          then:
            - sprinkler.next_valve: lawn_sprinkler_ctrlr
        - service: previous_valve
          then:
            - sprinkler.previous_valve: lawn_sprinkler_ctrlr
        - service: shutdown
          then:
            - sprinkler.shutdown: lawn_sprinkler_ctrlr

Additional Tricks
*****************

Beyond what is shown in the configuration examples above, other ESPHome elements may be called into
play to help build out an extensive interface for the controller in the front end (Home Assistant).
For example, the :ref:`number <config-number>` component may be used to set valve run durations or
the controller's multiplier value:

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
          - sprinkler.set_multiplier:
              id: lawn_sprinkler_ctrlr
              multiplier: !lambda 'return x;'

See Also
--------

- :apiref:`sprinkler/sprinkler.h`
- :apiref:`switch/switch.h`
- :ghedit:`Edit`
