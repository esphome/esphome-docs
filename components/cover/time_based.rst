Time-Based Cover
================

.. seo::
    :description: Instructions for setting up time-based covers in ESPHome.
    :image: TODO.png

The ``time_based`` cover platform allows you to create covers with position control that do not
have any position feedback. The state of the cover is thus always an assumed one, the current
position is approximated with the time the cover has been moving in a direction.

.. figure:: images/more-info-ui.png
    :align: center
    :width: 75.0%

.. code-block:: yaml

    # Example configuration entry
    cover:
      - platform: time_based
        name: "Time-Based Cover"

        open_action:
          - switch.turn_on: open_cover_switch
        open_duration: 2.1min

        close_action:
          - switch.turn_on: close_cover_switch
        close_duration: 2min

        stop_action:
          - switch.turn_off: open_cover_switch
          - switch.turn_off: close_cover_switch


Configuration variables:
------------------------

- **name** (**Required**, string): The name of the cover.
- **open_action** (**Required**, :ref:`Action <config-action>`): The action that should
  be performed when the remote requests the cover to be opened.
- **open_duration** (**Required**, :ref:`config-time`): The amount of time it takes the cover
  to open up from the fully-closed state.
- **close_action** (*Optional*, :ref:`Action <config-action>`): The action that should
  be performed when the remote requests the cover to be closed.
- **close_duration** (**Required**, :ref:`config-time`): The amount of time it takes the cover
  to close from the fully-open state.
- **stop_action** (**Required**, :ref:`Action <config-action>`): The action that should
  be performed when the remote requests the cover to be closed or the cover has been opening/closing
  for the given durations.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Cover <config-cover>`.

See Also
--------

- :doc:`index`
- :ref:`automation`
- :apiref:`time_based/time_based_cover.h`
- :ghedit:`Edit`
