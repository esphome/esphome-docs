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
to wake up on any RTC pin (``GPIO0``, ``GPIO2``, ``GPIO4``, ``GPIO12``, ``GPIO13``, ``GPIO14``,
``GPIO15``, ``GPIO25``, ``GPIO26``, ``GPIO27``, ``GPIO32``, ``GPIO39``).

While in deep sleep mode, the node will not do any work and not respond to any network traffic,
even Over The Air updates.

.. code:: yaml

    # Example configuration entry
    deep_sleep:
      run_duration: 10s
      sleep_duration: 10min

Configuration variables:
------------------------

- **run_duration** (*Optional*, :ref:`config-time`): The time duration the node should be active, i.e. run code.
- **run_cycles** (*Optional*, int): The number of ``loop()`` cycles to go through before
  entering deep sleep mode. Note: for advanced use-cases with custom code only.
- **sleep_duration** (*Optional*, :ref:`config-time`): The time duration to stay in deep sleep mode.
- **wakeup_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`):
  Only on ESP32. A pin to wake up to once in deep sleep mode. Use the inverted property to wake up
  to LOW signals.
- **wakeup_pin_mode** (*Optional*): Only on ESP32. Specify how to handle waking up from a ``wakeup_pin`` if
  the wakeup pin is already in the state with which it would wake up when attempting to enter deep sleep.
  See :ref:`deep_sleep-esp32_wakeup_pin_mode`. Defaults to ``IGNORE``
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. note::

    The :ref:`availability feature <mqtt-last_will_birth>` of the MQTT client will cause all values
    from the node to be displayed as "unavailable" while the node is in deep sleep mode. To disable availability
    reporting and not have any "unavailable" values, set ``birth_message`` and ``will_message`` to empty values:

    .. code:: yaml

        mqtt:
          # ...
          birth_message:
          will_message:

.. _deep_sleep-esp32_wakeup_pin_mode:

ESP32 Wakeup Pin Mode
---------------------

On the ESP32, you have the option of waking up on any RTC pin. However, there's one scenario that you need
to tell esphomelib how to handle: What if the wakeup pin is already in the state with which it would wake up
when the deep sleep should start? There are three ways of handling this using the ``wakeup_pin_mode`` option:

- ``IGNORE`` (Default): Ignore the fact that we will immediately exit the deep sleep mode because the wakeup
  pin is already active.
- ``KEEP_AWAKE``: Keep the ESP32 awake while the wakeup pin is still active. Or in other words: defer the
  activation of the deep sleep until the wakeup pin is no longer active.
- ``INVERT_WAKEUP``: When deep sleep was set up to wake up on a HIGH signal, but the wakeup pin is already HIGH,
  then re-configure deep sleep to wake up on a LOW signal and vice versa. Useful in situations when you want to
  use observe the state changes of a pin using deep sleep and the ON/OFF values last longer.


.. _deep_sleep-enter_action:

``deep_sleep.enter`` Action
---------------------------

This action makes the given deep sleep component enter deep sleep immediately.

.. code:: yaml

    on_...:
      then:
        - deep_sleep.enter: deep_sleep_1


.. _deep_sleep-prevent_action:

``deep_sleep.prevent`` Action
-----------------------------

This action prevents the given deep sleep component from entering deep sleep.
Useful for

.. code:: yaml

    on_...:
      then:
        - deep_sleep.prevent: deep_sleep_1

.. note::

    For example, if you want to upload a binary via OTA with deep sleep mode it can be difficult to
    catch the ESP being active.

    You can use this automation to automatically prevent deep sleep when a MQTT message on the topic
    ``livingroom/ota_mode`` with the payload ``ON`` is received. Then, to do the OTA update, just
    use a MQTT client to publish a retained MQTT message described above. When the node wakes up again
    it will no longer enter deep sleep mode and you can upload your OTA update.

    Remember to turn "OTA mode" off again after the OTA update by sending a MQTT message with the payload
    ``OFF``.

    .. code:: yaml

        deep_sleep:
          # ...
          id: deep_sleep_1
        mqtt:
          # ...
          on_message:
            topic: livingroom/ota_mode
            payload: ON
            then:
              - deep_sleep.prevent:
                  id: deep_sleep_1

See Also
--------

- :doc:`switch/shutdown`
- :ref:`automation`
- :doc:`API Reference </api/core/deep-sleep>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/deep_sleep.rst>`__

.. disqus::
