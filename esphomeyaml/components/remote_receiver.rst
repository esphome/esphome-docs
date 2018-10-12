Remote Receiver Component
=========================

The ``remote_receiver`` component lets you receive and decode any remote signal, these can
for example be infrared remotes or 433MHz signals.

The component is split up into two parts: the remote receiver hub which can be used to
receive, decode and dump all remote codes, and individual
:doc:`remote receiver binary sensors <binary_sensor/remote_receiver>` which will trigger when they
hear their own configured signal.

.. code:: yaml

    # Example configuration entry
    remote_receiver:
      pin: GPIO32
      dump: all


Configuration variables:
------------------------

- **pin** (**Required**, :ref:`config-pin`): The pin to receive the remote signal on.
- **dump** (*Optional*, list): Decode and dump these remote codes in the logs. Set to ``all`` to
  dump all available codecs:

  - **lg**: Decode and dump LG infrared codes.
  - **nec**: Decode and dump NEC infrared codes.
  - **panasonic**: Decode and dump Panasonic infrared codes.
  - **sony**: Decode and dump Sony infrared codes.
  - **rc_switch**: Decode and dump RCSwitch RF codes.
  - **raw**: Print all remote codes in their raw form. Useful for using arbitrary protocols.

- **tolerance** (*Optional*, int): The percentage that the remote signal lengths can devicate in the
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

See Also
--------

- `RCSwitch <https://github.com/sui77/rc-switch>`__ by `Suat Özgür <https://github.com/sui77>`__
- `IRRemoteESP8266 <https://github.com/markszabo/IRremoteESP8266/>`__ by `Mark Szabo-Simon <https://github.com/markszabo>`__
- :doc:`API Reference </api/switch/remote_transmitter>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/remote_transmitter.rst>`__

.. disqus::
