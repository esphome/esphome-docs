Remote Receiver
===============

.. seo::
    :description: Instructions for setting up remote receiver binary sensors for infrared and RF codes.
    :image: remote.png
    :keywords: RF, infrared

The ``remote_receiver`` component lets you receive and decode any remote signal, these can
for example be infrared remotes or 433MHz signals.

The component is split up into two parts: the remote receiver hub which
handles setting the pin and some other settings, and individual
:ref:`remote receiver binary sensors <remote-receiver-binary-sensor>`
which will trigger when they hear their own configured signal.

**See** :ref:`remote-setting-up-infrared` **and** :ref:`remote-setting-up-rf` **for set up guides.**

.. code-block:: yaml

    # Example configuration entry
    remote_receiver:
      pin: GPIO32
      dump: all

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`config-pin`): The pin to receive the remote signal on.
- **dump** (*Optional*, list): Decode and dump these remote codes in the logs (at log.level=DEBUG).
  Set to ``all`` to dump all available codecs:

  - **lg**: Decode and dump LG infrared codes.
  - **nec**: Decode and dump NEC infrared codes.
  - **panasonic**: Decode and dump Panasonic infrared codes.
  - **pioneer**: Decode and dump Pioneer infrared codes.
  - **jvc**: Decode and dump JVC infrared codes.
  - **samsung**: Decode and dump Samsung infrared codes.
  - **samsung36**: Decode and dump Samsung36 infrared codes.
  - **sony**: Decode and dump Sony infrared codes.
  - **rc_switch**: Decode and dump RCSwitch RF codes.
  - **rc5**: Decode and dump RC5 IR codes.
  - **raw**: Print all remote codes in their raw form. Useful for using arbitrary protocols.

- **tolerance** (*Optional*, int): The percentage that the remote signal lengths can deviate in the
  decoding process. Defaults to ``25%``.
- **buffer_size** (*Optional*, int): The size of the internal buffer for storing the remote codes. Defaults to ``10kB``
  on the ESP32 and ``1kB`` on the ESP8266.
- **memory_blocks** (*Optional*, int): The number of RMT memory blocks used. Only used on ESP32 platform. Defaults to
  ``3``.
- **filter** (*Optional*, :ref:`time <config-time>`): Filter any pulses that are shorter than this. Useful for removing
  glitches from noisy signals. Defaults to ``10us``.
- **idle** (*Optional*, :ref:`time <config-time>`): The amount of time that a signal should remain stable (i.e. not
  change) for it to be considered complete. Defaults to ``10ms``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation. Use this if you have
  multiple remote receivers.

Automations:

- **on_jvc** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  JVC remote code has been decoded. A variable ``x`` of type :apiclass:`remote_base::JVCData`
  is passed to the automation for use in lambdas.
- **on_lg** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  LG remote code has been decoded. A variable ``x`` of type :apiclass:`remote_base::LGData`
  is passed to the automation for use in lambdas.
- **on_nec** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  NEC remote code has been decoded. A variable ``x`` of type :apiclass:`remote_base::NECData`
  is passed to the automation for use in lambdas.
- **on_sony** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  Sony remote code has been decoded. A variable ``x`` of type :apiclass:`remote_base::SonyData`
  is passed to the automation for use in lambdas.
- **on_raw** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  raw remote code has been decoded. A variable ``x`` of type ``std::vector<int>``
  is passed to the automation for use in lambdas.
- **on_rc5** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  RC5 remote code has been decoded. A variable ``x`` of type :apiclass:`remote_base::RC5Data`
  is passed to the automation for use in lambdas.
- **on_rc_switch** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  RCSwitch RF code has been decoded. A variable ``x`` of type :apiclass:`remote_base::RCSwitchData`
  is passed to the automation for use in lambdas.
- **on_samsung** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  Samsung remote code has been decoded. A variable ``x`` of type :apiclass:`remote_base::SamsungData`
  is passed to the automation for use in lambdas.
- **on_samsung36** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  Samsung36 remote code has been decoded. A variable ``x`` of type :apiclass:`remote_base::Samsung36Data`
  is passed to the automation for use in lambdas.  
- **on_panasonic** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  Panasonic remote code has been decoded. A variable ``x`` of type :apiclass:`remote_base::PanasonicData`
  is passed to the automation for use in lambdas.
- **on_pioneer** (*Optional*, :ref:`Automation <automation>`): An automation to perform when a
  pioneer remote code has been decoded. A variable ``x`` of type :apiclass:`remote_base::PioneerData`
  is passed to the automation for use in lambdas.

.. _remote-receiver-binary-sensor:

Binary Sensor
-------------

The ``remote_receiver`` binary sensor lets you track when a button on a remote control is pressed.

Each time the pre-defined signal is received, the binary sensor will briefly go ON and
then immediately OFF.

.. code-block:: yaml

    # Example configuration entry
    remote_receiver:
      pin: GPIO32
      dump: all

    binary_sensor:
      - platform: remote_receiver
        name: "Panasonic Remote Input"
        panasonic:
          address: 0x4004
          command: 0x100BCBD

Configuration variables:
************************

- **name** (**Required**, string): The name for the binary sensor.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.

Remote code selection (exactly one of these has to be included):

- **jvc**: Trigger on a decoded JVC remote code with the given data.

  - **data** (**Required**, int): The JVC code to trigger on, see dumper output for more info.

- **lg**: Trigger on a decoded LG remote code with the given data.

  - **data** (**Required**, int): The LG code to trigger on, see dumper output for more info.
  - **nbits** (*Optional*, int): The number of bits of the remote code. Defaults to ``28``.

- **nec**: Trigger on a decoded NEC remote code with the given data.

  - **address** (**Required**, int): The address to trigger on, see dumper output for more info.
  - **command** (**Required**, int): The NEC command to listen for.

- **sony**: Trigger on a decoded Sony remote code with the given data.

  - **data** (**Required**, int): The Sony code to trigger on, see dumper output for more info.
  - **nbits** (*Optional*, int): The number of bits of the remote code. Defaults to ``12``.

- **raw**: Trigger on a raw remote code with the given code.

  - **code** (**Required**, list): The code to listen for, see :ref:`remote_transmitter-transmit_raw`
    for more info. Usually you only need to copy this directly from the dumper output.

- **rc5**: Trigger on a decoded RC5 remote code with the given data.

  - **address** (**Required**, int): The address to trigger on, see dumper output for more info.
  - **command** (**Required**, int): The RC5 command to listen for.

- **samsung**: Trigger on a decoded Samsung remote code with the given data.

  - **data** (**Required**, int): The data to trigger on, see dumper output for more info.
  - **nbits** (*Optional*, int): The number of bits of the remote code. Defaults to ``32``.

- **samsung36**: Trigger on a decoded Samsung36 remote code with the given data.

  - **address** (**Required**, int): The address to trigger on, see dumper output for more info.
  - **command** (**Required**, int): The command.

- **panasonic**: Trigger on a decoded Panasonic remote code with the given data.

  - **address** (**Required**, int): The address to trigger on, see dumper output for more info.
  - **command** (**Required**, int): The command.

- **pioneer**: Trigger on a decoded Pioneer remote code with the given data.

  - **rc_code_1** (**Required**, int): The remote control code trigger on, see dumper output for more details.

- **rc_switch_raw**: Trigger on a decoded RC Switch raw remote code with the given data.

  - **code** (**Required**, string): The remote code to listen for, copy this from the dumper output. To ignore a bit
    in the received data, use ``x`` at that place in the **code**.
  - **protocol** (*Optional*): The RC Switch protocol to use, see :ref:`remote_transmitter-rc_switch-protocol` for more info.

- **rc_switch_type_a**: Trigger on a decoded RC Switch Type A remote code with the given data.

  - **group** (**Required**, string): The group, binary string.
  - **device** (**Required**, string): The device in the group, binary string.
  - **state** (**Required**, boolean): The on/off state to trigger on.
  - **protocol** (*Optional*): The RC Switch protocol to use, see :ref:`remote_transmitter-rc_switch-protocol` for more info.

- **rc_switch_type_b**: Trigger on a decoded RC Switch Type B remote code with the given data.

  - **address** (**Required**, int): The address, int from 1 to 4.
  - **channel** (**Required**, int): The channel, int from 1 to 4.
  - **state** (**Required**, boolean): The on/off state to trigger on.
  - **protocol** (*Optional*): The RC Switch protocol to use, see :ref:`remote_transmitter-rc_switch-protocol` for more info.

- **rc_switch_type_c**: Trigger on a decoded RC Switch Type C remote code with the given data.

  - **family** (**Required**, string): The family. Range is ``a`` to ``p``.
  - **group** (**Required**, int): The group. Range is 1 to 4.
  - **device** (**Required**, int): The device. Range is 1 to 4.
  - **state** (**Required**, boolean): The on/off state to trigger on.
  - **protocol** (*Optional*): The RC Switch protocol to use, see :ref:`remote_transmitter-rc_switch-protocol` for more info.

- **rc_switch_type_d**: Trigger on a decoded RC Switch Type D remote code with the given data.

  - **group** (**Required**, int): The group. Range is 1 to 4.
  - **device** (**Required**, int): The device. Range is 1 to 3.
  - **state** (**Required**, boolean): The on/off state to trigger on.
  - **protocol** (*Optional*): The RC Switch protocol to use, see :ref:`remote_transmitter-rc_switch-protocol` for more info.

.. note::

    For the Sonoff RF Bridge you can use `this hack <https://github.com/xoseperez/espurna/wiki/Hardware-Itead-Sonoff-RF-Bridge---Direct-Hack>`__
    created by the GitHub user wildwiz. Then use this configuration for the remote receiver/transmitter hubs:

    .. code-block:: yaml

        remote_receiver:
          pin: 4
          dump: all

        remote_transmitter:
          pin: 5
          carrier_duty_percent: 100%

.. note::

    To caputure the codes more effectively with directly connected receiver like tsop38238 you can try to use ``INPUT_PULLUP``:

    .. code-block:: yaml

        remote_receiver:
          pin:
            number: D4
            inverted: True
            mode: INPUT_PULLUP
          dump: all


See Also
--------

- :doc:`index`
- :doc:`/components/remote_transmitter`
- `RCSwitch <https://github.com/sui77/rc-switch>`__ by `Suat Özgür <https://github.com/sui77>`__
- `IRRemoteESP8266 <https://github.com/markszabo/IRremoteESP8266/>`__ by `Mark Szabo-Simon <https://github.com/markszabo>`__
- :apiref:`remote/remote_receiver.h`
- :ghedit:`Edit`
