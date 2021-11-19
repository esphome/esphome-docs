MIDI Input Component
====================

.. seo::
    :description: Instructions for setting up a MIDI Input in ESPHome
    :image: midi.svg

The ``midi_in`` component allows connecting MIDI devices, such as MIDI Keyboards, drum pads, etc. to ESPHome and receive events, such as Key On/Off, Controller change, etc. Uses "Arduino MIDI Library" under the hood.

The MIDI communicates via :ref:`UART <uart>`.


.. code-block:: yaml

    # Example configuration entry
    uart:
      baud_rate: 31250

    midi_in:
      - channel: 1
        connected: # optional binary_sensor
          name: "MIDI Keyboard Connected"
          device_class: connectivity
          filters:
            - delayed_off: 5s
        playback: # optional binary_sensor
          name: "MIDI Keyboard Playback"
          device_class: occupancy
          icon: mdi:piano
          filters:
            - delayed_off: 60s

Configuration variables:
------------------------

- **channel** (*Optional*, int): MIDI channel to listen to events on (1-16). Defaults in `1`.
- **uart_id** (*Optional*, :ref:`config-id`): The ID of the :ref:`UART bus <uart>` you wish to use for this sensor.
  Use this if you want to use multiple UART buses at once.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID of the MIDI IN if you have multiple components.
- **connected** (*Optional*): Indicates if MIDI connection with the device is established.

  - **name** (**Required**, string): The name for the sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Binary Sensor <config-binary_sensor>`.

- **playback** (*Optional*): Indicates MIDI devices is "playing". This includes keys and pedals. 

  - **name** (**Required**, string): The name for the sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Binary Sensor <config-binary_sensor>`.

- **on_channel_message** (*Optional*, :ref:`Automation <automation>`): An automation to
  run when a channel message is received from the MIDI device. See :ref:`midi_in-on_channel_message`.
- **on_system_message** (*Optional*, :ref:`Automation <automation>`): An automation to
  run when a system message is received from the MIDI device. See :ref:`midi_in-on_system_message`.

.. _midi_in-on_channel_message:

``on_channel_message`` Trigger
******************************

This automation is triggered when a channel message is received from the MIDI device. The message type can be inspected to react to specific MIDI events, e.g. key presses:

.. code-block:: yaml

    midi_in:
      - ...
        on_channel_message:
          - lambda: |-
              if (x.type == midi::MidiType::NoteOn) {
                ESP_LOGD("midi_in", "Note ON: %#02x (channel %i)", x.data1, x.channel);
              }
          - logger.log:
              format: "%i: %#04x (%#04x %#04x)"
              args: [ 'x.channel', 'x.type', 'x.data1', 'x.data2' ]

A variable ``x`` of type :apistruct:`midi_in::MidiChannelMessage` is passed to the automation for use in lambdas.

Refer to `midi_Defs.h <https://github.com/FortySevenEffects/arduino_midi_library/blob/master/src/midi_Defs.h>`__ for possible values of ``MidiType``.

.. _midi_in-on_system_message:

``on_system_message`` Trigger
******************************

This automation is triggered when a system message is received from the MIDI device. The message type can be inspected to react to specific MIDI events, e.g:

.. code-block:: yaml

    midi_in:
      - ...
        on_system_message:
          - lambda: |-
              if (x.type == midi::MidiType::SystemReset) {
                ESP_LOGD("midi_in", "RESET");
              }

A variable ``x`` of type :apistruct:`midi_in::MidiSystemMessage` is passed to the automation for use in lambdas.

Refer to `midi_Defs.h <https://github.com/FortySevenEffects/arduino_midi_library/blob/master/src/midi_Defs.h>`__ for possible values of ``MidiType``.


UART Connection:
----------------

MIDI Output from our instrument should be connected to the RX pin on the ESP board. The baud rate needs to be set to 31250.


See Also
--------

- :ref:`uart`
- :apiref:`midi_in/midi_in.h`
- `Arduino MIDI Library <https://github.com/FortySevenEffects/arduino_midi_library>`__ by `FortySevenEffects <https://github.com/FortySevenEffects>`__
- :ghedit:`Edit`
