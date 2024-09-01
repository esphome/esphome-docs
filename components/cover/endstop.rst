Endstop Cover
=============

.. seo::
    :description: Instructions for setting up time-based covers in ESPHome.
    :image: electric-switch.svg

The ``endstop`` cover platform allows you to create covers with position control that have
endstops at both ends of the cover to detect the fully-open and fully-closed states.
When any of these endstops are reached, the cover is stopped (via ``stop_action``)
and the corresponding state is sent out.

This cover platform is mainly intended for DIY cover setups: Two endstops at either end and a motor
controlling the cover. The user just needs to enter what to do when the platform wants to move the
cover in either direction, or stop it, as well as information about open and close information so that
the current position can be approximated.

Additionally, open and close durations must be specified to allow ESPHome to approximate the
current position of the cover.

.. figure:: images/more-info-ui.png
    :align: center
    :width: 75.0%

.. code-block:: yaml

    # Example configuration entry
    cover:
      - platform: endstop
        name: "Endstop Cover"

        open_action:
          - switch.turn_on: open_cover_switch
        open_duration: 2.1min
        open_endstop: open_endstop_binary_sensor

        close_action:
          - switch.turn_on: close_cover_switch
        close_duration: 2min
        close_endstop: close_endstop_binary_sensor

        stop_action:
          - switch.turn_off: open_cover_switch
          - switch.turn_off: close_cover_switch


Configuration variables:
------------------------

- **open_action** (**Required**, :ref:`Action <config-action>`): The action that should
  be performed when the remote requests the cover to be opened.
- **open_duration** (**Required**, :ref:`config-time`): The amount of time it takes the cover
  to open up from the fully-closed state.
- **open_endstop** (**Required**, :ref:`config-id`): The ID of the
  :ref:`Binary Sensor <config-binary_sensor>` that turns on when the open position is reached.

- **close_action** (**Required**, :ref:`Action <config-action>`): The action that should
  be performed when the remote requests the cover to be closed.
- **close_duration** (**Required**, :ref:`config-time`): The amount of time it takes the cover
  to close from the fully-open state.
- **close_endstop** (**Required**, :ref:`config-id`): The ID of the
  :ref:`Binary Sensor <config-binary_sensor>` that turns on when the closed position is reached.

- **stop_action** (**Required**, :ref:`Action <config-action>`): The action that should
  be performed when the remote requests the cover to be closed or an endstop is reached.
- **max_duration** (*Optional*, :ref:`config-time`): The maximum duration the cover should be opening
  or closing. Useful for protecting from dysfunctional endstops.
- All other options from :ref:`Cover <config-cover>`.

See Also
--------

- :doc:`index`
- :ref:`automation`
- :apiref:`endstop/endstop_cover.h`
- :ghedit:`Edit`
