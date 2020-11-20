Current Based Cover
===================

.. seo::
    :description: Instructions for setting up current-based covers in ESPHome.
    :image: flash.png

The ``current_based`` cover platform allows you to create covers with position control by using current
sensors to detect the fully-open and fully-closed states. This is pretty useful when using motors with 
integrated mechanical endstops. During cover operation, the component monitors the current consumption 
to detect when the motor has stopped. 

When fully open or close is requested, the corresponding relay will stay on until the current the motor is 
consuming goes below a certain amount. The current amount needs to be specified in the configuration.

Open and close durations can be specified to allow ESPHome to approximate the current position of the cover.

This type of cover also provides current-based obstacle detection with automatic configurable rollback. 

.. warning::

    Take in mind that depending of the type of motor and cover you are controlling, current-based obstacle detection could
    not work and cover may be damaged if blocked. Use it at your own risk.

.. figure:: images/more-info-ui.png
    :align: center
    :width: 75.0%

.. code-block:: yaml

     # Example configuration entry
    cover:
      - platform: current_based
        name: "Current Based Cover"

        open_sensor: open_current_sensor
        open_moving_current_threshold: 0.5
        open_obstacle_current_threshold: 0.8
        open_duration: 12s
        open_action:
          - switch.turn_on: open_cover_switch

        close_sensor: close_current_sensor
        close_moving_current_threshold: 0.5
        close_obstacle_current_threshold: 0.8
        close_duration: 10s
        close_action:
          - switch.turn_on: close_cover_switch

        stop_action:
          - switch.turn_off: close_cover_switch
          - switch.turn_off: open_cover_switch

        obstacle_rollback: 30%
        start_sensing_delay: 0.8s
          


Configuration variables:
------------------------

- **name** (**Required**, string): The name of the cover.

- **open_sensor** (**Required**, :ref:`config-id`): The sensor to read the current drain 
  values when opening.
- **open_action** (**Required**, :ref:`Action <config-action>`): The action that should
  be performed when the remote requests the cover to be opened.
- **open_duration** (**Required**, :ref:`config-time`): The amount of time it takes the cover
  to open up from the fully-closed state.
- **open_moving_current_threshold** (*Required*, float): The amount of current in Amps the motor 
  should drain to consider the open motor is moving.
- **open_obstacle_current_threshold** (*Required*, float): The amount of current in Amps the motor 
  should drain to consider the open motor is blocked.

- **close_sensor** (**Required**, :ref:`config-id`): The sensor to read the current drain 
  values when closing.
- **close_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote requests the cover to be closed.
- **close_duration** (**Required**, :ref:`config-time`): The amount of time it takes the cover
  to close from the fully-open state.
- **close_moving_current_threshold** (*Required*, float): The amount of current in Amps the motor 
  should drain to consider the close motor is moving.
- **close_obstacle_current_threshold** (*Required*, float): The amount of current in Amps the motor 
  should drain to consider the open motor is blocked.

- **stop_action** (**Required**, :ref:`Action <config-action>`): The action that should
  be performed when the remote requests the cover to be closed or an endstop is reached.

- **max_duration** (*Optional*, :ref:`config-time`): The maximum duration the cover should be opening
  or closing. Useful for protecting from dysfunctional endstops.
- **start_sensing_delay** (*Optional*, :ref:`config-time`): The amount of time the current sensing will be 
  disabled when the movement starts. Motors can take some time before reaching their average consumption. 
  Low values can cause an immediate stop because of the first current reading occurring in the current-rising period. 
  Defaults to ``500ms``.
- **obstacle_rollback** (*Optional*, percentage): The percentage of rollback the cover will perform in case of 
  obstacle is detected. Defaults to ``10%``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Cover <config-cover>`.

See Also
--------

- :doc:`index`
- :ref:`automation`
- :apiref:`current_based/current_based_cover.h`
- :ghedit:`Edit`
