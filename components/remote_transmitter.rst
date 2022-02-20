Remote Transmitter
==================

.. seo::
    :description: Instructions for setting up switches that send out pre-defined sequences of IR or RF signals
    :image: remote.svg
    :keywords: Infrared, IR, RF, Remote, TX

The ``remote_transmitter`` component lets you send digital packets to control
devices in your home. For example this includes infrared data or 433MHz RF signals.

First, you need to setup a global hub that specifies which pin your remote
sender is connected to. Then you can use the available actions to send encoded
remote signals.

**See** :ref:`remote-setting-up-infrared` **and** :ref:`remote-setting-up-rf` **for set up guides.**

.. note::

    This component is more accurate on the ESP32, since that chipset has a dedicated
    peripheral for sending exact signal sequences.

.. code-block:: yaml

    # Example configuration entry
    remote_transmitter:
      pin: GPIO32
      carrier_duty_percent: 50%

    # Individual switches
    switch:
      - platform: template
        name: "Panasonic TV Off"
        turn_on_action:
          remote_transmitter.transmit_panasonic:
            address: 0x4004
            command: 0x100BCBD

Configuration variables:
------------------------

-  **pin** (**Required**, :ref:`config-pin`): The pin to transmit the remote signal on.
-  **carrier_duty_percent** (*Optional*, int): How much of the time the remote is on. For example, infrared
   protocols modulate the signal using a carrier signal. Set this is ``50%`` if you're working with IR LEDs and to
   ``100%`` if working with other things like 433MHz transmitters.
-  **id** (*Optional*, :ref:`config-id`): Manually specify
   the ID used for code generation. Use this if you have multiple remote transmitters.

.. _remote_transmitter-transmit_action:

Remote Transmitter Actions
--------------------------

Remote transmitters support a number of :ref:`actions <config-action>` that can be used
to send remote codes. All supported protocols are listed below. All actions additionally
have these configuration variables:

.. code-block::yaml

    on_...:
      - remote_transmitter.transmit_x:
          # ...
          repeat:
            times: 5
            wait_time: 10ms

Configuration variables:

- **repeat** (*Optional*): Optionally set the code to be repeated a number of times.
  Defaults to sending the code only once.

  - **times** (int): The number of times to repeat the code.
  - **wait_time** (:ref:`config-time`): The time to wait between repeats.

- **transmitter_id** (*Optional*, :ref:`config-id`): The remote transmitter to send the
  remote code with. Defaults to the first one defined in the configuration.

If you're looking for the same functionality as is default in the ``rpi_rf`` integration in
Home Assistant, you'll want to set the **times** to 10 and the **wait_time** to 0s.

.. _remote_transmitter-transmit_coolix:

``remote_transmitter.transmit_coolix`` Action
*********************************************

This :ref:`action <config-action>` sends a 24-bit Coolix infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_coolix:
          data: 0xB23FE4

Configuration variables:

- **data** (**Required**, int): The Coolix code to send, see dumper output for more info.

.. _remote_transmitter-transmit_dish:

``remote_transmitter.transmit_dish`` Action
*******************************************

This :ref:`action <config-action>` sends a Dish Network infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_dish:
          address: 1
          command: 16

Configuration variables:

- **address** (*Optional*, int): The number of the receiver to target, between 1 and 16 inclusive. Defaults to ``1``.
- **command** (**Required**, int): The command to send, between 0 and 63 inclusive.
- All other options from :ref:`remote_transmitter-transmit_action`.

You can find a list of commands in the `LIRC project <https://sourceforge.net/p/lirc-remotes/code/ci/master/tree/remotes/dishnet/Dish_Network.lircd.conf>`__.

.. _remote_transmitter-transmit_jvc:

``remote_transmitter.transmit_jvc`` Action
******************************************

This :ref:`action <config-action>` sends a JVC infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_jvc:
          data: 0x1234

Configuration variables:

- **data** (**Required**, int): The JVC code to send, see dumper output for more info.

.. _remote_transmitter-transmit_lg:

``remote_transmitter.transmit_lg`` Action
*****************************************

This :ref:`action <config-action>` sends an LG infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_lg:
          data: 0x20DF10EF # power on/off
          nbits: 32

Configuration variables:

- **data** (**Required**, int): The LG code to send, see dumper output for more info.
- **nbits** (*Optional*, int): The number of bits to send. Defaults to ``28``.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_midea:

``remote_transmitter.transmit_midea`` Action
********************************************

This :ref:`action <config-action>` sends a 40-bit Midea code to a remote transmitter. 8-bits of checksum added automatically.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_midea:
          code: [0xA2, 0x08, 0xFF, 0xFF, 0xFF]

Configuration variables:

- **code** (**Required**, list): The 40-bit Midea code to send as a list of hex or integers.
- All other options from :ref:`remote_transmitter-transmit_action`.

``remote_transmitter.transmit_nec`` Action
******************************************

This :ref:`action <config-action>` sends an NEC infrared remote code to a remote transmitter.

.. note::

    In version 2021.12, the order of transferring bits was corrected from MSB to LSB in accordance with the NEC standard.
    Therefore, if the the configuration file has come from an earlier version of ESPhome, it is necessary to reverse the order of the address and command bits when moving to 2021.12 or above.
    For example, address: 0x84ED, command: 0x13EC becomes 0xB721 and 0x37C8 respectively.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_nec:
          address: 0x1234
          command: 0x78AB

Configuration variables:

- **address** (**Required**, int): The address to send, see dumper output for more details.
- **command** (**Required**, int): The NEC command to send.
- All other options from :ref:`remote_transmitter-transmit_action`.

``remote_transmitter.transmit_nexa`` Action
*******************************************

This :ref:`action <config-action>` a Nexa RF remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.nexa:
          device: 0x38DDB4A
          state: 1
          group: 0
          channel: 15
          level: 0

Configuration variables:

- **device** (**Required**, int): The Nexa device code to send, see dumper output for more info.
- **state** (**Required**, int): The Nexa state code to send (0-OFF, 1-ON, 2-DIMMER LEVEL), see dumper output for more info.
- **group** (**Required**, int): The Nexa group code to send, see dumper output for more info.
- **channel** (**Required**, int): The Nexa channel code to send, see dumper output for more info.
- **level** (**Required**, int): The Nexa level code to send, see dumper output for more info.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_panasonic:

``remote_transmitter.transmit_panasonic`` Action
************************************************

This :ref:`action <config-action>` sends a Panasonic infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_panasonic:
          address: 0x1FEF
          command: 0x1F3E065F

Configuration variables:

- **address** (**Required**, int): The address to send the command to, see dumper output for more details.
- **command** (**Required**, int): The command to send.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_pioneer:

``remote_transmitter.transmit_pioneer`` Action
**********************************************

This :ref:`action <config-action>` sends a Pioneer infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_pioneer:
          rc_code_1: 0xA556
          rc_code_2: 0xA506
          repeat:
            times: 2

Configuration variables:

- **rc_code_1** (**Required**, int): The remote control code to send, see dumper output for more details.
- **rc_code_2** (*Optional*, int): The secondary remote control code to send; some codes are sent in
  two parts.
- Note that ``repeat`` is still optional, however **Pioneer devices may require that a given code is
  received multiple times before they will act on it.** Add this if your device does not respond to
  commands sent with this action.
- All other options from :ref:`remote_transmitter-transmit_action`.

At the time this action was created, Pioneer maintained listings of IR codes used for their devices
`here <https://www.pioneerelectronics.com/PUSA/Support/Home-Entertainment-Custom-Install/IR+Codes>`__.
If unable to find your specific device in the documentation, find a device in the same class; the codes
are largely shared among devices within a given class.

.. _remote_transmitter-transmit_pronto:

``remote_transmitter.transmit_pronto`` Action
*********************************************

This :ref:`action <config-action>` sends a raw code to a remote transmitter specified in Pronto format.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_pronto:
          data: "0000 006D 0010 0000 0008 0020 0008 0046 000A 0020 0008 0020 0008 001E 000A 001E 000A 0046 000A 001E 0008 0020 0008 0020 0008 0046 000A 0046 000A 0046 000A 001E 000A 001E 0008 06C3"

Configuration variables:

- **data** (**Required**, string): The raw code to send specified as a string.
  A lot of remote control Pronto codes can be found on http://remotecentral.com
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_raw:

``remote_transmitter.transmit_raw`` Action
******************************************

This :ref:`action <config-action>` sends a raw code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_raw:
          code: [4088, -1542, 1019, -510, 513, -1019, 510, -509, 511, -510, 1020,
                 -1020, 1022, -1019, 510, -509, 511, -510, 511, -509, 511, -510,
                 1020, -1019, 510, -511, 1020, -510, 512, -508, 510, -1020, 1022,
                 -1021, 1019, -1019, 511, -510, 510, -510, 1022, -1020, 1019,
                 -1020, 511, -511, 1018, -1022, 1020, -1019, 1021, -1019, 1020,
                 -511, 510, -1019, 1023, -1019, 1019, -510, 512, -508, 510, -511,
                 512, -1019, 510, -509]

Configuration variables:

- **code** (**Required**, list): The raw code to send as a list of integers.
  Positive numbers represent a digital high signal and negative numbers a digital low signal.
  The number itself encodes how long the signal should last (in microseconds).
- **carrier_frequency** (*Optional*, float): Optionally set a frequency to send the signal
  with for infrared signals. Defaults to ``0Hz``.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_rc5:

``remote_transmitter.transmit_rc5`` Action
******************************************

This :ref:`action <config-action>` sends an RC5 infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_rc5:
          address: 0x1F
          command: 0x3F

Configuration variables:

- **address** (**Required**, int): The address to send, see dumper output for more details.
- **command** (**Required**, int): The RC5 command to send.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_rc_switch_raw:

``remote_transmitter.transmit_rc_switch_raw`` Action
****************************************************

This :ref:`action <config-action>` sends a raw RC-Switch code to a
remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_rc_switch_raw:
          code: '001010011001111101011011'
          protocol: 1

Configuration variables:

- **code** (**Required**, string): The raw code to send, copy this from the dump output.
- **protocol** (*Optional*): The RC Switch protocol to use, see :ref:`remote_transmitter-rc_switch-protocol`
  for more information.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-rc_switch-protocol:

RC Switch Protocol
^^^^^^^^^^^^^^^^^^

All RC Switch ``protocol`` settings have these settings:

- Either the value is an integer, then the inbuilt protocol definition with the given number
  is used.
- Or a key-value mapping is given, then there are these settings:

  - **pulse_length** (**Required**, int): The pulse length of the protocol - how many microseconds
    one pulse should last for.
  - **sync** (*Optional*): The number of high/low pulses for the sync header, defaults to ``[1, 31]``
  - **zero** (*Optional*): The number of high/low pulses for a zero bit, defaults to ``[1, 3]``
  - **one** (*Optional*): The number of high/low pulses for a one bit, defaults to ``[3, 1]``
  - **inverted** (*Optional*, boolean): If this protocol is inverted. Defaults to ``false``.

.. _remote_transmitter-transmit_rc_switch_type_a:

``remote_transmitter.transmit_rc_switch_type_a`` Action
*******************************************************

This :ref:`action <config-action>` sends a type A RC-Switch code to a
remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_rc_switch_type_a:
          group: '01001'
          device: '10110'
          state: off
          protocol: 1

Configuration variables:

- **group** (**Required**, string): The group to send the command to.
- **device** (**Required**, string): The device in the group to send the command to.
- **state** (**Required**, boolean): The on/off state to send.
- **protocol** (*Optional*): The RC Switch protocol to use, see :ref:`remote_transmitter-rc_switch-protocol`
  for more information.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_rc_switch_type_b:

``remote_transmitter.transmit_rc_switch_type_b`` Action
*******************************************************

This :ref:`action <config-action>` sends a type B RC-Switch code to a
remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_rc_switch_type_b:
          address: '0100'
          channel: '1011'
          state: off
          protocol: 1

Configuration variables:

- **address** (**Required**, int): The address to send the command to.
- **channel** (**Required**, int): The channel to send the command to.
- **state** (**Required**, boolean): The on/off state to send.
- **protocol** (*Optional*): The RC Switch protocol to use, see :ref:`remote_transmitter-rc_switch-protocol`
  for more information.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_rc_switch_type_c:

``remote_transmitter.transmit_rc_switch_type_c`` Action
*******************************************************

This :ref:`action <config-action>` sends a type C RC-Switch code to a
remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_rc_switch_type_c:
          family: 'C'
          group: 3
          device: 1
          state: off
          protocol: 1

Configuration variables:

- **family** (**Required**, string): The family to send the command to. Range is ``a`` to ``p``.
- **group** (**Required**, int): The group to send the command to. Range is 1 to 4.
- **device** (**Required**, int): The device to send the command to. Range is 1 to 4.
- **state** (**Required**, boolean): The on/off state to send.
- **protocol** (*Optional*): The RC Switch protocol to use, see :ref:`remote_transmitter-rc_switch-protocol`
  for more information.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_rc_switch_type_d:

``remote_transmitter.transmit_rc_switch_type_d`` Action
*******************************************************

This :ref:`action <config-action>` sends a type D RC-Switch code to a
remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_rc_switch_type_d:
          group: 'c'
          device: 1
          state: off
          protocol: 1

Configuration variables:

- **group** (**Required**, int): The group to send the command to. Range is 1 to 4.
- **device** (**Required**, int): The device to send the command to. Range is 1 to 3.
- **state** (**Required**, boolean): The on/off state to send.
- **protocol** (*Optional*): The RC Switch protocol to use, see :ref:`remote_transmitter-rc_switch-protocol`
  for more information.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_samsung:

``remote_transmitter.transmit_samsung`` Action
**********************************************

This :ref:`action <config-action>` sends a Samsung infrared remote code to a remote transmitter.
It transmits codes up to 64 bits in length in a single packet.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_samsung:
          data: 0x1FEF05E4
      # additional example for 48-bit codes:
      - remote_transmitter.transmit_samsung:
          data: 0xB946F50A09F6
          nbits: 48

Configuration variables:

- **data** (**Required**, int): The data to send, see dumper output for more details.
- **nbits** (*Optional*, int): The number of bits to send. Defaults to ``32``.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_samsung36:

``remote_transmitter.transmit_samsung36`` Action
************************************************

This :ref:`action <config-action>` sends a Samsung36 infrared remote code to a remote transmitter.
It transmits the ``address`` and ``command`` in two packets separated by a "space".

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_samsung36:
          address: 0x0400
          command: 0x000E00FF

Configuration variables:

- **address** (**Required**, int): The address to send, see dumper output for more details.
- **command** (**Required**, int): The Samsung36 command to send, see dumper output for more details.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_sony:

``remote_transmitter.transmit_sony`` Action
*******************************************

This :ref:`action <config-action>` a Sony infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_sony:
          data: 0x123
          nbits: 12

Configuration variables:

- **data** (**Required**, int): The Sony code to send, see dumper output for more info.
- **nbits** (*Optional*, int): The number of bits to send. Defaults to ``12``.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_toshiba_ac:

``remote_transmitter.transmit_toshiba_ac`` Action
*************************************************

This :ref:`action <config-action>` sends a Toshiba AC infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_toshiba_ac:
          rc_code_1: 0xB24DBF4040BF
          rc_code_2: 0xD5660001003C

Configuration variables:

- **rc_code_1** (**Required**, int): The remote control code to send, see dumper output for more details.
- **rc_code_2** (*Optional*, int): The secondary remote control code to send; some codes are sent in
  two parts.
- **Note:** this action transmits codes using the new(er) Toshiba AC protocol and likely will not work with older units.
- All other options from :ref:`remote_transmitter-transmit_action`.


Lambda calls
************

Actions may also be called from :ref:`lambdas <config-lambda>`. The ``.transmit()`` call can be populated with
encoded data for a specific protocol by following the example below.
See the full API Reference for more info.

- ``.transmit()``: Transmit an IR code using the remote transmitter.

  .. code-block:: cpp

      // Example - transmit using the Pioneer protocol
      auto call = id(my_transmitter).transmit();
      esphome::remote_base::PioneerData data = { rc_code_1, rc_code_2 };
      esphome::remote_base::PioneerProtocol().encode(call.get_data(), data);
      call.set_send_times(2);
      call.perform();


.. _remote-setting-up-infrared:

Setting up Infrared Devices
---------------------------

In this guide an infrared device will be set up with ESPHome. First, the remote code
will be captured with an IR receiver module (like `this one <https://www.sparkfun.com/products/10266>`__).
We will use ESPHome's dumping ability to output the decoded remote code directly.

Then we will set up a new remote transmitter with an infrared LED (like
`this one <https://learn.sparkfun.com/tutorials/ir-communication/all>`__) to transmit the
code when a switch is triggered.

First, connect the infrared receiver module to a pin on your board and set up a
remote_receiver instance:

.. code-block:: yaml

    remote_receiver:
      pin: D0
      dump: all

Compile and upload the code. While viewing the log output from the ESP,
press a button on an infrared remote you want to capture (one at a time).

You should see log output like below:

.. code-block:: text

    # If the codec is known:
    [D][remote.panasonic] Received Panasonic: address=0x4004 command=0x8140DFA2

    # Or raw output if it's not known yet
    # The values may fluctuate a bit, but as long as they're similar it's ok
    [D][remote.raw] Received Raw: 4088, -1542, 1019, -510, 513, -1019, 510, -509, 511, -510, 1020,
    [D][remote.raw]   -1020, 1022, -1019, 510, -509, 511, -510, 511, -509, 511, -510,
    [D][remote.raw]   1020, -1019, 510, -511, 1020, -510, 512, -508, 510, -1020, 1022

If the codec is already implemented in ESPHome, you will see the decoded value directly -
otherwise you will see the raw data dump (which you can use just as well). You have
just successfully captured your first infrared code.

Now let's use this information to emulate a button press from the ESP. First, wire up the
IR diode to a new pin on the ESP and configure a global ``remote_transmitter`` instance:

.. code-block:: yaml

    remote_transmitter:
      pin: D1
      # Infrared remotes use a 50% carrier signal
      carrier_duty_percent: 50%

This will allow us to send any data we want via the IR LED. To replicate the codes we decoded
earlier, create a new template switch that sends the infrared code when triggered:

.. code-block:: yaml

    switch:
      - platform: template
        name: Panasonic Power Button
        turn_on_action:
          - remote_transmitter.transmit_panasonic:
              address: 0x4004
              command: 0x8140DFA2

    # Or for raw code
    switch:
      - platform: template
        name: Raw Code Power Button
        turn_on_action:
          - remote_transmitter.transmit_raw:
              carrier_frequency: 38kHz
              code: [4088, -1542, 1019, -510, 513, -1019, 510, -509, 511, -510, 1020,
                     -1020, 1022, -1019, 510, -509, 511, -510, 511, -509, 511, -510,
                     1020, -1019, 510, -511, 1020, -510, 512, -508, 510, -1020, 1022]

Recompile again, when you power up the device the next time you will see a new switch
in the frontend. Click on it and you should see the remote signal being transmitted. Done!

.. _remote-setting-up-rf:

Setting Up RF Devices
---------------------

The ``remote_transmitter`` and ``remote_receiver`` components can also be used to send
and receive 433MHz RF signals. This guide will discuss setting up a 433MHz receiver to
capture a device's remote codes. After that we will set up a 433MHz transmitter to replicate
the remote code with the press of a switch in the frontend.

First, connect the RF module to a pin on the ESP and set up a remote_receiver instance:

.. code-block:: yaml

    remote_receiver:
      pin: D0
      dump: all
      # Settings to optimize recognition of RF devices
      tolerance: 50%
      filter: 250us
      idle: 4ms
      buffer_size: 2kb

Compile and upload the code. While viewing the log output from the ESP,
press a button on an RF remote you want to capture (one at a time).

You should see log output like below:

.. code-block:: text

    # If the codec is known:
    [D][remote.rc_switch] Received RCSwitch: protocol=2 data='100010000000000010111110'

    # Or raw output if it's not known yet
    # The values may fluctuate a bit, but as long as they're similar it's ok
    [D][remote.raw] Received Raw: 4088, -1542, 1019, -510, 513, -1019, 510, -509, 511, -510, 1020,
    [D][remote.raw]   -1020, 1022, -1019, 510, -509, 511, -510, 511, -509, 511, -510,
    [D][remote.raw]   1020, -1019, 510, -511, 1020, -510, 512, -508, 510, -1020, 1022

.. note::

    If the log output is flooded with "Received Raw" messages, you can also disable raw
    remote code reporting and rely on rc_switch to decode the values.

    .. code-block:: yaml

        remote_receiver:
          pin: D0
          dump:
            - rc_switch
          tolerance: 50%
          filter: 250us
          idle: 4ms
          buffer_size: 2kb

If the codec is already implemented in ESPHome, you will see the decoded value directly -
otherwise you will see the raw data dump (which you can use just as well). You have
just successfully captured your first RF code.

Now let's use this information to emulate a button press from the ESP. First, wire up the
RF transmitter to a new pin on the ESP and configure a global ``remote_transmitter`` instance:

.. code-block:: yaml

    remote_transmitter:
      pin: D1
      # RF uses a 100% carrier signal
      carrier_duty_percent: 100%

This will allow us to send any data we want via the RF transmitter. To replicate the codes we decoded
earlier, create a new template switch that sends the RF code when triggered:

.. code-block:: yaml

    switch:
      - platform: template
        name: RF Power Button
        turn_on_action:
          - remote_transmitter.transmit_rc_switch_raw:
              code: '100010000000000010111110'
              protocol: 2

    # Or for raw code
    switch:
      - platform: template
        name: Raw Code Power Button
        turn_on_action:
          - remote_transmitter.transmit_raw:
              code: [4088, -1542, 1019, -510, 513, -1019, 510, -509, 511, -510, 1020,
                     -1020, 1022, -1019, 510, -509, 511, -510, 511, -509, 511, -510,
                     1020, -1019, 510, -511, 1020, -510, 512, -508, 510, -1020, 1022]

Recompile again, when you power up the device the next time you will see a new switch
in the frontend. Click on it and you should see the remote signal being transmitted. Done!

See Also
--------

- :doc:`index`
- :doc:`/components/remote_receiver`
- `RCSwitch <https://github.com/sui77/rc-switch>`__ by `Suat Özgür <https://github.com/sui77>`__
- `IRRemoteESP8266 <https://github.com/markszabo/IRremoteESP8266/>`__ by `Mark Szabo-Simon <https://github.com/markszabo>`__
- :ghsources:`esphome/components/remote_transmitter`
- :ghedit:`Edit`
