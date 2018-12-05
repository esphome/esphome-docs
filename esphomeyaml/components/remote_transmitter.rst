Remote Transmitter Component
============================

.. seo::
    :description: Instructions for setting up remote transmitters in esphomelib
    :image: remote.png
    :keywords: RF, infrared

The ``remote_transmitter`` component lets you send infrared messages to control
devices in your home. First, you need to setup a global hub that specifies which pin your remote
sender is connected to. Afterwards you can create :doc:`individual
switches </esphomeyaml/components/switch/remote_transmitter>` that each send a pre-defined remote signal to a device.

Use-cases are for example infrared remotes or 433MHz signals.

.. note::

    This component is *much* more accurate on the ESP32, since that chipset has a dedicated
    peripheral for sending exact signal sequences.

.. code-block:: yaml

    # Example configuration entry
    remote_transmitter:
      pin: GPIO32
      carrier_duty_percent: 50%

    # Individual switches
    switch:
      - platform: remote_transmitter
        name: "Panasonic TV Off"
        panasonic:
          address: 0x4004
          command: 0x100BCBD

Configuration variables:
------------------------

-  **pin** (**Required**, :ref:`config-pin`): The pin to transmit the remote signal on.
-  **carrier_duty_percent** (*Optional*, int): How much of the time the remote is on. For example, infrared
   protocols modulate the signal using a carrier signal. Set this is ``50%`` if you're working with IR leds and to
   ``100%`` if working with a other things like 433MHz transmitters.
-  **id** (*Optional*, :ref:`config-id`): Manually specify
   the ID used for code generation. Use this if you have multiple remote transmitters.

.. note::

    See :ref:`finding_remote_codes` for a guide for setting this up.

See Also
--------

- `RCSwitch <https://github.com/sui77/rc-switch>`__ by `Suat Özgür <https://github.com/sui77>`__
- `IRRemoteESP8266 <https://github.com/markszabo/IRremoteESP8266/>`__ by `Mark Szabo-Simon <https://github.com/markszabo>`__
- :doc:`API Reference </api/switch/remote_transmitter>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/remote_transmitter.rst>`__

.. disqus::
