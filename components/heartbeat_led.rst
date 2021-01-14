Heartbeat LED
==========

.. seo::
    :description: Instructions for setting up heartbeat LEDs in ESPHome to monitor an ESP.
    :image: led-on.png

The ``heartbeat_led`` component slowly blinks an LED to indicate the status of
the device. If it is blinking, it means the base loop is running.

.. code-block:: yaml

    # Example configuration entry
    heartbeat_led:
      pin: GPIO2

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The
  GPIO pin to operate the status LED on.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. note::

    If your LED is in an active-LOW mode (when it's on if the output is enabled), use the
    ``inverted`` option of the :ref:`Pin Schema <config-pin_schema>`:

    .. code-block:: yaml

        status_led:
          pin:
            number: D0
            inverted: True

See Also
--------

- :apiref:`heartbeat_led/heartbeat_led.h`
- :ghedit:`Edit`
