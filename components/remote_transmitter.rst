Remote Transmitter
==================

.. seo::
    :description: Instructions for setting up configurations that send out pre-defined sequences of IR or RF signals
    :image: remote.svg
    :keywords: Infrared, IR, RF, Remote, TX, 433, Blaster

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
      pin: GPIOXX
      carrier_duty_percent: 50%

Configuration variables:
------------------------

-  **pin** (**Required**, :ref:`config-pin`): The pin to transmit the remote signal on.
-  **carrier_duty_percent** (*Optional*, int): How much of the time the remote is on. For example, infrared
   protocols modulate the signal using a carrier signal. Set this to ``50%`` if you're working with IR LEDs and to
   ``100%`` if working with other things like 433MHz transmitters.
- **rmt_channel** (*Optional*, int): The RMT channel to use. Only on **esp32**.
  The following ESP32 variants have these channels available:

  .. csv-table::
      :header: "ESP32 Variant", "Channels"

      "ESP32", "0, 1, 2, 3, 4, 5, 6, 7"
      "ESP32-S2", "0, 1, 2, 3"
      "ESP32-S3", "0, 1, 2, 3"
      "ESP32-C3", "0, 1"

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

  - **times** (:ref:`templatable <config-templatable>`, int): The number of times to repeat the code.
  - **wait_time** (:ref:`templatable <config-templatable>`, :ref:`config-time`): The time to wait between repeats (in µs as a result of a :ref:`lambda <config-lambda>`).

- **transmitter_id** (*Optional*, :ref:`config-id`): The remote transmitter to send the
  remote code with. Defaults to the first one defined in the configuration.

If you're looking for the same functionality as is default in the ``rpi_rf`` integration in
Home Assistant, you'll want to set the **times** to 10 and the **wait_time** to 0s.

.. _remote_transmitter-transmit_abbwelcome:

``remote_transmitter.transmit_abbwelcome`` **Action**

This :ref:`action <config-action>` sends a ABB-Welcome message to the intercom bus. The
message type, addresses, address length and data can vary a lot between ABB-Welcome
systems. Please refer to the received messages while performing actions like ringing a
doorbell or opening a door.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_abbwelcome:
          source_address: 0x1001 # your indoor station address
          destination_address: 0x4001 # door address
          three_byte_address: false # address length of your system
          message_type: 0x0d # unlock door, on some systems 0x0e is used instead
          data: [0xab, 0xcd, 0xef]  # message data, see receiver dump

Configuration variables:

- **source_address** (**Required**, int):The source address to send the command from,
  see received messages for more info. For indoor stations the last byte of the address
  represents the apartment number set by the dials on the back of the indoor station and is
  transmitted in hexadecimal format.
- **destination_address** (**Required**, int): The destination address to send the command to,
  see received messages for more info.
- **three_byte_address** (**Required**, int): The destination address to send the command to,
  see received messages for more info.
- **three_byte_address** (**Optional**, boolean): The length of the source and destination address. ``false``
  means two bytes and ``true`` means three bytes. Please check the received messages to see which address length
  is used by your system. For example, ``[XXXX > XXXX]`` appears in the receiver log for two byte addresses and
  ``[XXXXXX > XXXXXX]`` for three byte addresses. Defaults to ``false``.
- **retransmission** (**Optional**, boolean): Should only be ``true`` if this message has been transmitted
  before with the same ``message_id``. Typically, messages are transmitted up to three times with a 1 second
  interval if no reply is received. Defaults to ``false``.
- **message_type** (**Required**, int): The message type, see dumper output for more info.
  The highest bit indicates a reply.
- **message_id** (**Optional**, int): The message ID, see dumper output for more info.
  Defaults to a randomly generated ID if this message is not a reply or retransmission.
- **data** (**Optional**, 0-7 bytes list): The code to send.
  Usually you only need to copy this directly from the dumper output. Defaults to ``[]``
- All other options from :ref:`remote_transmitter-transmit_action`.

.. note::

    ABB-Welcome messages are sent over the two-wire bus of your intercom system.
    A custom receiver and transmitter circuit is required.
    `More info <https://github.com/Mat931/esp32-doorbell-bus-interface>`__

.. _remote_transmitter-transmit_aeha:

``remote_transmitter.transmit_aeha`` **Action**

This :ref:`action <config-action>` sends a AEHA code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_aeha:
          address: 0x1FEF
          data: [0x1F, 0x3E, 0x06, 0x5F]

Configuration variables:

- **address** (**Required**, int): The address to send the command to, see dumper output for more details.
- **data** (**Required**, list): The command to send, A length of 2-35 bytes can be specified for one packet.
- **carrier_frequency** (*Optional*, float): Set a frequency to send the signal
  with for infrared signals. Defaults to ``38000Hz``.
- All other options from :ref:`remote_transmitter-transmit_action`.

AEHA refers to the Association for Electric Home Appliances in Japan, a format used by Panasonic and many other companies.

.. _remote_transmitter-transmit_byronsx:

``remote_transmitter.transmit_byronsx`` **Action**

This :ref:`action <config-action>` sends a Byron Doorbell RF protocol code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_byronsx:
          address: '0x4f'
          command: '0x2'

Configuration variables:

- **address** (**Required**, int): The 8-bit ID to send, see dumper output for more info.
- **command** (**Required**, int): The command to send, see dumper output for more info.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_canalsat:

``remote_transmitter.transmit_canalsat`` **Action**

This :ref:`action <config-action>` sends a CanalSat infrared remote code to a remote transmitter.

.. note::

    The CanalSat and CanalSatLD protocols use a higher carrier frequency (56khz) and are very similar.
    Depending on the hardware used they may interfere with each other when enabled simultaneously.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_canalsat:
          device: 0x25
          address: 0x00
          command: 0x02

Configuration variables:

- **device** (**Required**, int): The device to send to, see dumper output for more details.
- **address** (*Optional*, int): The address (or subdevice) to send to, see dumper output for more details. Defaults to ``0``
- **command** (**Required**, int): The command to send.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_canalsatld:

``remote_transmitter.transmit_canalsatld`` **Action**

This :ref:`action <config-action>` sends a CanalSatLD infrared remote code to a remote transmitter.

.. note::

    The CanalSat and CanalSatLD protocols use a higher carrier frequency (56khz) and are very similar.
    Depending on the hardware used they may interfere with each other when enabled simultaneously.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_canalsatld:
          device: 0x25
          address: 0x00
          command: 0x02

Configuration variables:

- **device** (**Required**, int): The device to send to, see dumper output for more details.
- **address** (*Optional*, int): The address (or subdevice) to send to, see dumper output for more details. Defaults to ``0``
- **command** (**Required**, int): The command to send.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_coolix:

``remote_transmitter.transmit_coolix`` **Action**

This :ref:`action <config-action>` sends one or two (stricted or not) 24-bit Coolix infrared remote codes to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_coolix:
          first: 0xB23FE4
          second: 0xB23FE4

Configuration variables:

- **first** (**Required**, :ref:`templatable <config-templatable>`, uint32_t): The first 24-bit Coolix code to send, see dumper output for more info.
- **second** (*Optional*, :ref:`templatable <config-templatable>`, uint32_t): The second 24-bit Coolix code to send, see dumper output for more info.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_dish:

``remote_transmitter.transmit_dish`` **Action**

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

.. _remote_transmitter-transmit_dooya:

``remote_transmitter.transmit_dooya`` **Action**

This :ref:`action <config-action>` sends a Dooya RF remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_dooya:
          id: 0x001612E5
          channel: 142
          button: 12
          check: 3

Configuration variables:

- **id** (**Required**, int): The 24-bit ID to send. Each remote has a unique one.
- **channel** (**Required**, int): The 8-bit channel to send, between 0 and 255 inclusive.
- **button** (**Required**, int): The 4-bit button to send, between 0 and 15 inclusive.
- **check** (**Required**, int): The 4-bit check to send. Includes an indication that a button is being held down. See dumper output for more info.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_drayton:

``remote_transmitter.transmit_drayton`` **Action**

This :ref:`action <config-action>` sends a Draton Digistat RF remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_drayton:
          address: '0x6180'
          channel: '0x12'
          command: '0x02'

Configuration variables:

- **address** (**Required**, int): The 16-bit ID to send, see dumper output for more info.
- **channel** (**Required**, int): The switch/channel to send, between 0 and 127 inclusive.
- **command** (**Required**, int): The command to send, between 0 and 63 inclusive.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_jvc:

``remote_transmitter.transmit_jvc`` **Action**

This :ref:`action <config-action>` sends a JVC infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_jvc:
          data: 0x1234

Configuration variables:

- **data** (**Required**, int): The JVC code to send, see dumper output for more info.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_keeloq:

``remote_transmitter.transmit_keeloq`` **Action**

This :ref:`action <config-action>` sends KeeLoq RF remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_keeloq:
          address: '0x57ffe7b'
          command: '0x02'
          code: '0xd19ef0a9'
          repeat:
            times: 3
            wait_time: 15ms

Configuration variables:

- **address** (**Required**, int): The 32-bit address to send, see dumper output for more info.
- **command** (**Required**, int): The 4 bit command/button code to send, see dumper output for more info.
- **code** (**Optional**, int): The 32 bit encrypted field to send. Defaults to all zeros.
- **level** (**Optional**, boolean): Low battery level status bit. Defaults to false.
- All other options from :ref:`remote_transmitter-transmit_action`.
- A repeat **wait_time** of 15ms as shown replicates the repetition of an HCS301.

.. _remote_transmitter-transmit_haier:

``remote_transmitter.transmit_haier`` **Action**

This :ref:`action <config-action>` sends a 104-bit Haier code to a remote transmitter. 8-bits of checksum added automatically.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_haier:
          code: [0xA6, 0xDA, 0x00, 0x00, 0x40, 0x40, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x05]

Configuration variables:

- **code** (**Required**, list): The 13 byte Haier code to send.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_lg:

``remote_transmitter.transmit_lg`` **Action**

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

.. _remote_transmitter-transmit_magiquest:

``remote_transmitter.transmit_magiquest`` **Action**

This :ref:`action <config-action>` sends a MagiQuest wand code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_magiquest:
          wand_id: 0x01234567
          magnitude: 0x080C

Configuration variables:

- **wand_id** (**Required**, int): The wand ID to send, as a hex integer.  See the dumper output for your wand ID.
- **magnitude** (*Optional*, int): The magnitude of swishes and swirls of the want to transmit.  See the dumper output for examples.  If omitted, sends 0xFFFF (which the real wand never uses).
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_midea:

``remote_transmitter.transmit_midea`` **Action**

This :ref:`action <config-action>` sends a 40-bit Midea code to a remote transmitter. 8-bits of checksum added automatically.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_midea:
          code: [0xA2, 0x08, 0xFF, 0xFF, 0xFF]

    on_...:
      - remote_transmitter.transmit_midea:
          code: !lambda |-
            // Send a FollowMe code with the current temperature.
            return {0xA4, 0x82, 0x48, 0x7F, (uint8_t)(id(temp_sensor).state + 1)};

Configuration variables:

- **code** (**Required**, list, :ref:`templatable <config-templatable>`): The 40-bit Midea code to send as a list of hex or integers.
- All other options from :ref:`remote_transmitter-transmit_action`.

``remote_transmitter.transmit_nec`` **Action**

This :ref:`action <config-action>` sends an NEC infrared remote code to a remote transmitter.

.. note::

    In version 2021.12, the order of transferring bits was corrected from MSB to LSB in accordance with the NEC standard.
    Therefore, if the configuration file has come from an earlier version of ESPhome, it is necessary to reverse the order of the address and command bits when moving to 2021.12 or above.
    For example, address: 0x84ED, command: 0x13EC becomes 0xB721 and 0x37C8 respectively.
    Additionally, ESPHome does not automatically generate parity bits or pad values to 2 bytes.
    So, in order to send command 0x0, you need to use 0xFF00 (0x00 being the command and 0xFF being the logical inverse).

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_nec:
          address: 0x1234
          command: 0x78AB
          command_repeats: 1

Configuration variables:

- **address** (**Required**, int): The 16-bit address to send, see dumper output for more details.
- **command** (**Required**, int): The 16-bit NEC command to send.
- **command_repeats** (*Optional*, int): The number of times the command bytes are sent in one transmission. Defaults to `1`.
- All other options from :ref:`remote_transmitter-transmit_action`.

``remote_transmitter.transmit_nexa`` **Action**

This :ref:`action <config-action>` a Nexa RF remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_nexa:
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

``remote_transmitter.transmit_panasonic`` **Action**

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

``remote_transmitter.transmit_pioneer`` **Action**

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

``remote_transmitter.transmit_pronto`` **Action**

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

``remote_transmitter.transmit_raw`` **Action**

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

``remote_transmitter.transmit_rc5`` **Action**

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

.. _remote_transmitter-transmit_rc6:

``remote_transmitter.transmit_rc6`` **Action**

This :ref:`action <config-action>` sends an RC6 infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_rc6:
          address: 0x1F
          command: 0x3F

Configuration variables:

- **address** (**Required**, int): The address to send, see dumper output for more details.
- **command** (**Required**, int): The RC6 command to send.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_rc_switch_raw:

``remote_transmitter.transmit_rc_switch_raw`` **Action**

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

.. _remote_transmitter-transmit_rc_switch_type_a:

``remote_transmitter.transmit_rc_switch_type_a`` **Action**

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

``remote_transmitter.transmit_rc_switch_type_b`` **Action**

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

``remote_transmitter.transmit_rc_switch_type_c`` **Action**

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

``remote_transmitter.transmit_rc_switch_type_d`` **Action**

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

.. _remote_transmitter-transmit_roomba:

``remote_transmitter.transmit_roomba`` **Action**

This :ref:`action <config-action>` sends a Roomba infrared remote code to a remote transmitter.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_roomba:
          data: 0x88  # clean
          repeat:
            times: 3
            wait_time: 17ms

Configuration variables:

- **data** (**Required**, int): The Roomba code to send, see dumper output for more info.
- Note that ``repeat`` is still optional, however **Roomba vacuums require that a given code is received at least three times before they will act on it.** If your Roomba still does not respond to sent command increase this value.
- Note that ``wait_time`` is still optional; it will even work without this parameter, but Roomba Remote uses this 17 ms wait time between sent commands.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_samsung:

``remote_transmitter.transmit_samsung`` **Action**

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

``remote_transmitter.transmit_samsung36`` **Action**

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

``remote_transmitter.transmit_sony`` **Action**

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

``remote_transmitter.transmit_toshiba_ac`` **Action**

This :ref:`action <config-action>` sends a Toshiba AC infrared remote code to a remote transmitter.

.. note::

    This action transmits codes using the new(er) Toshiba AC protocol and likely will not work with older units.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_toshiba_ac:
          rc_code_1: 0xB24DBF4040BF
          rc_code_2: 0xD5660001003C

Configuration variables:

- **rc_code_1** (**Required**, int): The remote control code to send, see dumper output for more details.
- **rc_code_2** (*Optional*, int): The secondary remote control code to send; some codes are sent in
  two parts.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-transmit_mirage:

``remote_transmitter.transmit_mirage`` **Action**

This :ref:`action <config-action>` sends a 112-bit Mirage code to a remote transmitter. 8-bits of checksum added automatically.

.. code-block:: yaml

    on_...:
      - remote_transmitter.transmit_mirage:
          code: [0x56, 0x77, 0x00, 0x00, 0x22, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

Configuration variables:

- **code** (**Required**, list): The 14 byte Mirage code to send.
- All other options from :ref:`remote_transmitter-transmit_action`.

.. _remote_transmitter-rc_switch-protocol:

RC Switch Protocol
******************

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

See Also
--------

- :doc:`index`
- :doc:`/components/remote_receiver`
- :ref:`remote-setting-up-infrared`
- :ref:`remote-setting-up-rf`
- :doc:`/components/rf_bridge`
- :ref:`lambda_magic_rf_queues`
- `RCSwitch <https://github.com/sui77/rc-switch>`__ by `Suat Özgür <https://github.com/sui77>`__
- :apiref:`remote_transmitter/remote_transmitter.h`
- :ghedit:`Edit`
