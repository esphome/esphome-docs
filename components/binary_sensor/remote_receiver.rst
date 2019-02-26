Remote Receiver
===============

.. seo::
    :description: Instructions for setting up remote receiver binary sensors for infrared and RF codes.
    :image: remote.png
    :keywords: RF, infrared

.. _remote-receiver-component:

Component/Hub
-------------

The ``remote_receiver`` component lets you receive and decode any remote signal, these can
for example be infrared remotes or 433MHz signals.

The component is split up into two parts: the remote receiver hub which can be used to
receive, decode and dump all remote codes, and individual
:ref:`remote receiver binary sensors <remote-receiver-binary-sensor>` which will trigger when they
hear their own configured signal.

.. code-block:: yaml

    # Example configuration entry
    remote_receiver:
      pin: GPIO32
      dump: all


Configuration variables:
************************

- **pin** (**Required**, :ref:`config-pin`): The pin to receive the remote signal on.
- **dump** (*Optional*, list): Decode and dump these remote codes in the logs. Set to ``all`` to
  dump all available codecs:

  - **lg**: Decode and dump LG infrared codes.
  - **nec**: Decode and dump NEC infrared codes.
  - **panasonic**: Decode and dump Panasonic infrared codes.
  - **jvc**: Decode and dump JVC infrared codes.
  - **samsung**: Decode and dump Samsung infrared codes.
  - **sony**: Decode and dump Sony infrared codes.
  - **rc_switch**: Decode and dump RCSwitch RF codes.
  - **rc5**: Decode and dump RC5 IR codes.
  - **raw**: Print all remote codes in their raw form. Useful for using arbitrary protocols.

- **tolerance** (*Optional*, int): The percentage that the remote signal lengths can deviate in the
  decoding process. Defaults to ``25%``.
- **buffer_size** (*Optional*, int): The size of the internal buffer for storing the remote codes. Defaults to ``10kb``
  on the ESP32 and ``1kb`` on the ESP8266.
- **filter** (*Optional*, :ref:`time <config-time>`): Filter any pulses that are shorter than this. Useful for removing
  glitches from noisy signals. Defaults to ``10us``.
- **idle** (*Optional*, :ref:`time <config-time>`): The amount of time that a signal should remain stable (i.e. not
  change) for it to be considered complete. Defaults to ``10ms``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation. Use this if you have
  multiple remote transmitters.

.. note::

    See :ref:`finding_remote_codes` for a guide for setting this up.

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
- The remote code, see :ref:`remote_transmitter-codes`. Only one
  of them can be specified per binary sensor.
- **remote_receiver_id** (*Optional*, :ref:`config-id`): The id of the :ref:`remote-receiver-component`.
  Defaults to the first hub in your configuration.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.

.. note::

    See :ref:`finding_remote_codes` for a guide for setting this up.

.. note::

    For the Sonoff RF Bridge you can use `this hack <https://github.com/xoseperez/espurna/wiki/Hardware-Itead-Sonoff-RF-Bridge---Direct-Hack>`__
    created by the Github user wildwiz. Then use this configuration for the remote receiver/transmitter hubs:

    .. code-block:: yaml

        remote_receiver:
          pin: 4
          dump: all

        remote_transmitter:
          pin: 5
          carrier_duty_percent: 100%

    Supporting the RF Bridge chip directly is currently only a long-term goal for ESPHome.


See Also
--------

- :doc:`index`
- :doc:`/components/remote_transmitter`
- `RCSwitch <https://github.com/sui77/rc-switch>`__ by `Suat Özgür <https://github.com/sui77>`__
- `IRRemoteESP8266 <https://github.com/markszabo/IRremoteESP8266/>`__ by `Mark Szabo-Simon <https://github.com/markszabo>`__
- :apiref:`remote/remote_receiver.h`
- :ghedit:`Edit`

.. disqus::
