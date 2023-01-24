.. _deep_sleep-component:

Deep Sleep Component
====================

.. seo::
    :description: Instructions for setting up the deep sleep support for minimizing power consumption on ESPs.
    :image: hotel.svg

The ``deep_sleep`` component can be used to automatically enter a deep sleep mode on the
ESP8266/ESP32 after a certain amount of time. This is especially useful with nodes that operate
on batteries and therefore need to conserve as much energy as possible.

To use ``deep_sleep`` first specify how long the node should be active, i.e. how long it should
check sensor values and report them, using the ``run_duration`` option.

Next, tell the node how it should wakeup. On the ESP8266, you can only put the node into deep sleep
for a duration using ``sleep_duration``, note that on the ESP8266 ``GPIO16`` must be connected to
the ``RST`` pin so that it will wake up again. On the ESP32, you additionally have the option
to wake up on any RTC pin (``GPIO0``, ``GPIO2``, ``GPIO4``, ``GPIO12``, ``GPIO13``, ``GPIO14``,
``GPIO15``, ``GPIO25``, ``GPIO26``, ``GPIO27``, ``GPIO32``, ``GPIO39``).

While in deep sleep mode, the node will not do any work and not respond to any network traffic,
even Over The Air updates.

.. code-block:: yaml

    # Example configuration entry
    deep_sleep:
      run_duration: 10s
      sleep_duration: 10min

.. note::

    On ESPs that have onboard USB chips one the chip's control lines is connected to the RST pin so that the flasher can reboot the ESP when necessary. On some devices this may interfere with deep sleep and prevent the ESP from waking. This can happen when your ESP is powered through the onboard USB connector, even if you are only using a USB power supply. Powering the ESP from a separate 3.3V source connected to the 3.3V pin and GND will solve this issue. 
    
Configuration variables:
------------------------

- **run_duration** (*Optional*, :ref:`config-time`): The time duration the node should be active, i.e. run code.

  Only on ESP32, instead of time, it is possible to specify run duration according to the wakeup reason from deep-sleep:

  - **default** (**Required**, :ref:`config-time`): default run duration for timer wakeup and any unspecified wakeup reason.
  - **gpio_wakeup_reason** (*Optional*, :ref:`config-time`): run duration if woken up by GPIO.
  - **touch_wakeup_reason** (*Optional*, :ref:`config-time`): run duration if woken up by touch.

- **sleep_duration** (*Optional*, :ref:`config-time`): The time duration to stay in deep sleep mode.
- **touch_wakeup** (*Optional*, boolean): Only on ESP32. Use a touch event to wakeup from deep sleep. To be able
  to wakeup from a touch event, :ref:`esp32-touch-binary-sensor` must be configured properly.
- **wakeup_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): Only on ESP32. A pin to wake up to once
  in deep sleep mode. Use the inverted property to wake up to LOW signals.
- **wakeup_pin_mode** (*Optional*): Only on ESP32. Specify how to handle waking up from a ``wakeup_pin`` if
  the wakeup pin is already in the state with which it would wake up when attempting to enter deep sleep.
  See :ref:`deep_sleep-esp32_wakeup_pin_mode`. Defaults to ``IGNORE``
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

Advanced features:

- **esp32_ext1_wakeup** (*Optional*): Use the EXT1 wakeup source of the ESP32 to wake from deep sleep to
  wake up on multiple pins. This cannot be used together with wakeup pin.

  - **pins** (**Required**, list of pin numbers): The pins to wake up on.
  - **mode** (**Required**): The mode to use for the wakeup source. Must be one of ``ALL_LOW`` (wake up when
    all pins go LOW) or ``ANY_HIGH`` (wake up when any pin goes HIGH).

.. note::

    Only one deep sleep component may be configured.

.. _deep_sleep-esp32_wakeup_pin_mode:

ESP32 Wakeup Pin Mode
---------------------

On the ESP32, you have the option of waking up on any RTC pin. However, there's one scenario that you need
to tell ESPHome how to handle: What if the wakeup pin is already in the state with which it would wake up
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

.. code-block:: yaml

    on_...:
      then:
        - deep_sleep.enter:
            id: deep_sleep_1
            sleep_duration: 20min


    # ESP32 can sleep until a specific time of day.
    on_...:
      then:
        - deep_sleep.enter:
            id: deep_sleep_1
            until: "16:00:00"
            time_id: sntp_id

Configuration options:

- **sleep_duration** (*Optional*, :ref:`templatable <config-templatable>`, :ref:`config-time`): The time duration to stay in deep sleep mode.
- **until** (*Optional*, string): The time of day to wake up. Only on ESP32.
- **time_id** (*Optional*, :ref:`config-id`): The ID of the time component to use for the ``until`` option. Only on ESP32.


.. _deep_sleep-prevent_action:

``deep_sleep.prevent`` Action
-----------------------------

This action prevents the given deep sleep component from entering deep sleep.
Useful for keeping the ESP active during data transfer or OTA updating (See note below for more information).

.. code-block:: yaml

    on_...:
      then:
        - deep_sleep.prevent: deep_sleep_1

.. note::

    For example, if you want to upload a binary via OTA with deep sleep mode it can be difficult to
    catch the ESP being active.

    You can use this automation to automatically prevent deep sleep when a MQTT message on the topic
    ``livingroom/ota_mode`` is received. Then, to do the OTA update, just
    use a MQTT client to publish a retained MQTT message described below. When the node wakes up again
    it will no longer enter deep sleep mode and you can upload your OTA update.

    Remember to turn "OTA mode" off again after the OTA update by sending a MQTT message with the payload
    ``OFF``. To enter the deep sleep again after the OTA update send a message on the topic ``livingroom/sleep_mode``
    with payload ``ON``. Deep sleep will start immediately. Don't forget to delete the payload before the node
    wakes up again.

    .. code-block:: yaml

        deep_sleep:
          # ...
          id: deep_sleep_1
        mqtt:
          # ...
          on_message:
            - topic: livingroom/ota_mode
              payload: 'ON'
              then:
                - deep_sleep.prevent: deep_sleep_1
            - topic: livingroom/sleep_mode
              payload: 'ON'
              then:
                - deep_sleep.enter: deep_sleep_1

.. _deep_sleep-allow_action:

``deep_sleep.allow`` Action
-----------------------------

This action allows the given deep sleep component to enter deep sleep, after previously being prevented.

.. code-block:: yaml

    on_...:
      then:
        - deep_sleep.allow: deep_sleep_1

See Also
--------

- :doc:`switch/shutdown`
- :ref:`automation`
- :apiref:`deep_sleep/deep_sleep_component.h`
- :ghedit:`Edit`
