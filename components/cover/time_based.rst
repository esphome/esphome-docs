Time Based Cover
================

.. seo::
    :description: Instructions for setting up time-based covers in ESPHome.
    :image: timer.svg

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
  be performed to stop the cover when the remote requests the cover to be stopped or
  when the cover has been opening/closing for the given durations.
- **has_built_in_endstop** (*Optional*, boolean): Indicates that the cover has built in end stop
  detectors. In this configuration the ``stop_action`` is not performed when the open or close
  time is completed and if the cover is commanded to open or close the corresponding actions
  will be performed without checking current state. Defaults to ``false``.
- **manual_control** (*Optional*, boolean): If your cover has a manual control switch, it's not 
  possible for the system to be sure of its current position. Thus, the cover state is unsure. 
  So whenever the cover is commanded to open or close, the command will be performed completely 
  (including any defined ``stop_action``) and the current state will be relearned from this. 
  Defaults to ``false``. 
- **assumed_state** (*Optional*, boolean): Whether the true state of the cover is not known.
  This will make the Home Assistant frontend show buttons for both OPEN and CLOSE actions, instead
  of hiding or disabling one of them. Defaults to ``true``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Cover <config-cover>`.


.. note::

    The stop button on the UI is always enabled even when the cover is stopped and each press
    on the button will cause the ``stop_action`` to be performed.

.. note::

    The state of the cover can be restored from flash after a node reboot, with 
    ``esp8266_restore_from_flash: true`` option set. 
    See :doc:`esp8266_restore_from_flash </components/esphome>` for details.



See Also
--------

- :doc:`index`
- :ref:`automation`
- :apiref:`time_based/time_based_cover.h`
- :ghedit:`Edit`
