Remote Transmitter Switch
=========================

The ``remote_transmitter`` switch platform allows you to create switches
that send a pre-defined remote control sequence
using the :doc:`/esphomeyaml/components/remote_transmitter`. Every time
the switch is turned on, the configured remote signal is sent.

Use cases include, but are not limited to, infrared remotes, 433MHz signals and so on.

.. figure:: images/remote_transmitter-ui.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    remote_transmitter:
      pin: 32

    # Individual switches
    switch:
      - platform: remote_transmitter
        name: "Panasonic TV Off"
        panasonic:
          address: 0x4004
          command: 0x100BCBD
        repeat: 25

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the switch.
- The remote code, see :ref:`remote_transmitter-codes`. Only one
  of them can be specified per switch.
- **repeat** (*Optional*, int): How often the command should be sent.

  - **times** (int): The number of times the code should be sent. Defaults to ``1``.
  - **wait_time** (:ref:`time <config-time>`): The time to wait between repeats.

- **remote_transmitter_id** (*Optional*, :ref:`config-id`): The id of the :doc:`/esphomeyaml/components/remote_transmitter`.
  Defaults to the first hub specified.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Switch <config-switch>` and :ref:`MQTT Component <config-mqtt-component>`.

.. note::

    For the Sonoff RF Bridge you can use `this hack <https://github.com/xoseperez/espurna/wiki/Hardware-Itead-Sonoff-RF-Bridge---Direct-Hack>`__
    created by the Github user wildwiz. Then use this configuration for the remote receiver/transmitter hubs:

    .. code:: yaml

        remote_receiver:
          pin: 4
          dump: all

        remote_transmitter:
          pin: 5
          carrier_duty_percent: 100%

    Supporting the RF Bridge chip directly is currently only a long-term goal for esphomelib.

.. _remote_transmitter-codes:

Remote Codes
------------

Supported remote codes:

.. code:: yaml

    switch:
    - platform: remote_transmitter
      # ... - Only one of these is allowed for one remote transmitter at a time
      nec:
        address: 0x4242
        command: 0x8484
      lg:
        data: 0x01234567890ABC
        nbits: 28
      sony:
        data: 0xABCDEF
        nbits: 12
      panasonic:
        address: 0x4004
        command: 0x1000BCD
      rc_switch_raw:
        code: '001010011001111101011011'
        protocol: 1
      rc_switch_type_a:
        group: '11001'
        device: '01000'
        state: True
      rc_switch_type_b:
        address: 4
        channel: 2
        state: True
      rc_switch_type_c:
        family: 'a'
        group: 1
        device: 2
        state: True
      rc_switch_type_d:
        group: 'a'
        device: 2
        state: True
      raw:
        carrier_frequency: 35kHz
        data:
          - 1000
          - -1000

Configuration variables:

- **nec**: Send a NEC IR code.

  - **address**: The address of the device.
  - **command**: The command to send.

- **lg**: Send an LG IR code.

  - **data**: The data bytes to send.
  - **nbits**: The number of bits to send, defaults to 28.

- **sony**: Send an Sony IR code.

  - **data**: The data bytes to send.
  - **nbits**: The number of bits to send, defaults to 12.

- **panasonic**: Send an Panasonic IR code.

  - **address**: The address of the device.
  - **command**: The command to send.

- **rc_switch_raw**: Send an RCSwitch raw code.

  - **code** (**Required**, string): The code to send. Must be a string of 0s and 1s.
    `For example <https://github.com/sui77/rc-switch/wiki/HowTo_OperateLowCostOutlets#type-d-status>`__ ``'001010011001111101011011'``.
  - **protocol** (*Optional*, :ref:`RCSwitch protocol <rc_switch-protocol>`): The RCSwitch protocol to use. Defaults to ``1``.

- **rc_switch_type_a**: Send an RCSwitch `type A code <https://github.com/sui77/rc-switch/wiki/HowTo_OperateLowCostOutlets#type-a-10-pole-dip-switches>`__.

  - **group** (**Required**, string): The group to address, usually the state of the first 5 DIP switches.
    Must be a string of 0s and 1s. For example ``'11001``.
  - **device** (**Required**, string): The device within the group, usually the state of the last 5 DIP switches.
    Must be a string of 0s and 1s. For example ``'01000``.
  - **state** (**Required**, boolean): Whether to send a "turn on" or "turn off" signal when this switch is triggered. See :ref:`remote_transmitter-on_off_template`.
  - **protocol** (*Optional*, :ref:`RCSwitch protocol <rc_switch-protocol>`): The RCSwitch protocol to use. Defaults to ``1``.

- **rc_switch_type_b**: Send an RCSwitch `type B code <https://github.com/sui77/rc-switch/wiki/HowTo_OperateLowCostOutlets#type-b-two-rotarysliding-switches>`__.

  - **address** (**Required**, int): The number of the first rotary switch. For example ``4``.
  - **channel** (**Required**, int): The number of the first rotary switch. For example ``2``.
  - **state** (**Required**, boolean): Whether to send a "turn on" or "turn off" signal when this switch is triggered. See :ref:`remote_transmitter-on_off_template`.
  - **protocol** (*Optional*, :ref:`RCSwitch protocol <rc_switch-protocol>`): The RCSwitch protocol to use. Defaults to ``1``.

- **rc_switch_type_c**: Send an RCSwitch `type C code <https://github.com/sui77/rc-switch/wiki/HowTo_OperateLowCostOutlets#type-c-intertechno>`__.

  - **family** (**Required**, string): The family of the device. Must be a character from ``a`` to ``p``.
  - **group** (**Required**, int): The group of the device. For example ``4``.
  - **address** (**Required**, int): The address of the device. For example ``2``.
  - **state** (**Required**, boolean): Whether to send a "turn on" or "turn off" signal when this switch is triggered. See :ref:`remote_transmitter-on_off_template`.
  - **protocol** (*Optional*, :ref:`RCSwitch protocol <rc_switch-protocol>`): The RCSwitch protocol to use. Defaults to ``1``.

- **rc_switch_type_d**: Send an RCSwitch type D code.

  - **group** (**Required**, string): The group of the device. Must be a character from ``a`` to ``d``.
  - **device** (**Required**, int): The address of the device. For example ``3``.
  - **state** (**Required**, boolean): Whether to send a "turn on" or "turn off" signal when this switch is triggered. See :ref:`remote_transmitter-on_off_template`.
  - **protocol** (*Optional*, :ref:`RCSwitch protocol <rc_switch-protocol>`): The RCSwitch protocol to use. Defaults to ``1``.

- **raw**: Send an arbitrary signal.

  - **carrier_frequency**: The frequency to use for the carrier. A lot
    of IR sensors only respond to a very specific frequency.
  - **data**: List containing integers describing the signal to send.
    Each value is a time in µs declaring how long the carrier should
    be switched on or off. Positive values mean ON, negative values
    mean OFF.

.. _finding_remote_codes:

Finding Remote Codes
--------------------

Each remote transmitter uses a different protocol to send its information. So to replicate an infrared or 433MHz
remote you will first need to "learn" these codes. You will first need to hook up a receiver and sniff the codes
using the :doc:`remote receiver component </esphomeyaml/components/remote_receiver>` like this:

.. code:: yaml

    remote_receiver:
      pin: GPIO34
      # dump all signals we find
      dump: all

And then activate the remote control you want to have in esphomelib. you will see a log output like this:

.. figure:: images/rf_receiver-log_raw.png
    :align: center

    Example log output for a 433MHz proprietary remote control.

Raw Remote Codes
****************

If esphomelib has a decoder set up for the code, it will spit out the decoded code in the logs. In this case,
it's a proprietary protocol which would be difficult to reverse engineer. Fortunately, we can just
do a "replay attack" by repeating the signal we just saw for our own purposes. The output you see in above image
is encoded in microseconds: A negative value represents the output being LOW for x microseconds and a positive
value denotes the output being HIGH for the specified number of microseconds.

Now you only need to set up the remote transmitter (which well *send* the code) like this:

.. code:: yaml

    remote_transmitter:
       pin: GPIO23
       # Set to 100% when working with RF signals, and 50% if working with IR leds
       carrier_duty_percent: 100%

And lastly, we need to set up the switch that, when turned on, will send our pre-defined remote code:

.. code:: yaml

    switch:
      - platform: remote_transmitter
        name: "My awesome RF switch"
        raw: [4088, -1542, 1019, -510, 513, -1019, 510, -509, 511, -510, 1020,
              -1020, 1022, -1019, 510, -509, 511, -510, 511, -509, 511, -510,
              1020, -1019, 510, -511, 1020, -510, 512, -508, 510, -1020, 1022,
              -1021, 1019, -1019, 511, -510, 510, -510, 1022, -1020, 1019,
              -1020, 511, -511, 1018, -1022, 1020, -1019, 1021, -1019, 1020,
              -511, 510, -1019, 1023, -1019, 1019, -510, 512, -508, 510, -511,
              512, -1019, 510, -509]

Note that you don't need to include the leading ``32519`` here, as it denotes a final space at the end of
a transmission.

RCSwitch Remote Codes
*********************

Starting with version 1.8.0 esphomelib can also recognize a bunch of 433MHz RF codes directly using `RCSwitch's <https://github.com/sui77/rc-switch>`__
remote protocol. If you have RF code dumping enabled for the receiver, you will then see log outputs like this one:

.. code::

    Received RCSwitch: protocol=1 data='0100010101'

Like before with raw codes, you can then use this code to create switches:

.. code:: yaml

    switch:
      - platform: remote_transmitter
        name: "Living Room Lights On"
        rc_switch_raw:
          code: '0100010101'
          protocol: 1

Alternatively, you can use the information on `this page <https://github.com/sui77/rc-switch/wiki/HowTo_OperateLowCostOutlets>`__
to manually find the RCSwitch codes without having to first find them using the remote receiver. For example, this would
be the esphomelib equivalent of the first Type-A switch on that site:

.. code:: yaml

    switch:
      - platform: remote_transmitter
        name: "Living Room Lights On"
        rc_switch_type_a:
          group: '1101'
          device: '0100'
          state: True

.. _remote_transmitter-on_off_template:

On/Off template
---------------

Each switch of the ``remote_transmitter`` platform only sends a pre-defined remote code when switched on.
For example the RCSwitch example above always **sends the turn on** RF code to the wall plug. In some cases
you might want to have switches that can do both things, i.e. turn a light on when switched on and turn a light off
when switched off. To do this, use the :doc:`/esphomeyaml/components/switch/template` like this:

.. code:: yaml

    switch:
      - platform: remote_transmitter
        id: living_room_lights_on
        rc_switch_type_a:
          group: '1101'
          device: '0100'
          state: True
      - platform: remote_transmitter
        id: living_room_lights_off
        rc_switch_type_a:
          group: '1101'
          device: '0100'
          state: False
      - platform: template
        name: Living Room Lights
        optimistic: True
        turn_on_action:
          - switch.turn_on: living_room_lights_on
        turn_off_action:
          - switch.turn_on: living_room_lights_off


.. _rc_switch-protocol:

RCSwitch Protocol
-----------------

RCSwitch transmitters/receivers all have a ``protocol:`` option that can be used to tell esphomelib what timings to use
for the transmission. This is necessary as many remotes use different timings to encode a logic zero or one.

RCSwitch has 7 built-in protocols that cover most use cases. You can however also choose to use custom parameters
for the protocol like so

.. code:: yaml

    # Use one of RCSwitch's pre-defined protocols (1-7)
    protocol: 1

    # Use a custom protocol:
    protocol:
      pulse_length: 175
      sync: [1, 31]
      zero: [1, 3]
      one: [3, 1]
      inverted: False

Configuration options for the custom variant:

- **pulse_length** (**Required**, int): The length of each pulse in microseconds.
- **sync** (*Optional*): The number of on and off pulses for a sync bit. Defaults to 1 pulse on and 31 pulses off.
- **zero** (*Optional*): The number of on and off pulses to encode a logic zero. Defaults to 1 pulse on and 3 pulses off.
- **one** (*Optional*): The number of on and off pulses to encode a logic one. Defaults to 3 pulses on and 1 pulse off.
- **inverted** (*Optional*, boolean): Whether to treat this protocol as inverted, i.e. encode all on pulses by logic LOWs
  and vice versa.


See Also
--------

- :doc:`index`
- :doc:`/esphomeyaml/components/remote_transmitter`
- :doc:`/esphomeyaml/components/remote_receiver`
- `RCSwitch <https://github.com/sui77/rc-switch>`__ by `Suat Özgür <https://github.com/sui77>`__
- `IRRemoteESP8266 <https://github.com/markszabo/IRremoteESP8266/>`__ by `Mark Szabo-Simon <https://github.com/markszabo>`__
- :doc:`API Reference </api/switch/remote_transmitter>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/switch/remote_transmitter.rst>`__

.. disqus::
