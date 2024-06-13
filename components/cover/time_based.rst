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
- **manual_control** (*Optional*, boolean): For covers with manual external controls. With this 
  configuration if the cover is commanded to open or close the corresponding actions will be 
  performed even if the current state fully open or fully closed matches desired state, then 
  ``stop_action`` will be called after the full duration of the action elapses. 
  The current state will then be relearned upon completion.
  It's recommended to  set ``assumed_state`` to true so the cover control button aren't disabled 
  in the interface. Defaults to ``false``. 
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

Handle stop_action:
------------------------
For some cover controllers, separate switches for UP and DOWN action are used while a stop is issued when sending a counter command.
This can be handled at the **stop_action** by using the following lambda function:

.. code-block:: yaml

    stop_action: 
      - lambda: !lambda |-
          if (id(cover).get_last_operation() == CoverOperation::COVER_OPERATION_OPENING) {
            // Cover is currently opening
            id(cover_button_down).press();
          } else if (id(cover).get_last_operation() == CoverOperation::COVER_OPERATION_CLOSING) {
            // Cover is currently closing
            id(cover_button_up).press();
          }

Be aware that ``get_last_operation`` will only return the last opening or closing operation, but not the last idle operation. 
This issue is tracked `here <https://github.com/esphome/issues/issues/4252#issuecomment-2132727377>`_.

See Also
--------

- :doc:`index`
- :ref:`automation`
- :apiref:`time_based/time_based_cover.h`
- :ghedit:`Edit`
