Deep Sleep Component
====================

The ``deep_sleep`` component can be used to automatically enter a deep sleep mode on the
ESP8266/ESP32 after a certain amount of time. This is especially useful with nodes that operate
on batteries and therefore need to conserve as much energy as possible.

To use ``deep_sleep`` first specify how long the node should be active, i.e. how long it should
check sensor values and report them, using the ``run_duration`` and ``run_cycles`` options. If you
use both in your configuration, any time either one of them is finished, the node will go into deep
sleep mode.

Next, tell the node how it should wakeup. On the ESP8266, you can only put the node into deep sleep
for a duration using ``sleep_duration``, note that on the ESP8266 ``GPIO16`` must be connected to
the ``RST`` pin so that it will wake up again. On the ESP32, you additionally have the option
to wake up on any RTC pin (0, 2, 4, 12, 13, 14, 15, 25, 26, 27, 32, 39).

While in deep sleep mode, the node will not do any work and not respond to any network traffic,
even Over The Air updates.

.. code:: yaml

    # Example configuration entry
    deep_sleep:
      run_duration: 10s
      sleep_duration: 10min

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

-  **run_duration** (*Optional*, :ref:`config-time`):
   The time duration the node should be active, i.e. run code.
-  **run_cycles** (*Optional*, int): The number of ``loop()`` cycles to go through before
   entering deep sleep mode. Note: for advanced use-cases with custom code only.
-  **sleep_duration** (*Optional*, :ref:`config-time`): The time duration to stay in deep sleep mode.
-  **wakeup_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`):
   Only on ESP32. A pin to wake up to once in deep sleep mode. Use the inverted property to wake up
   to LOW signals.
-  **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

See Also
^^^^^^^^

- :doc:`switch/shutdown`
- :ref:`automation`
- :doc:`API Reference </api/core/deep-sleep>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/deep_sleep.rst>`__
