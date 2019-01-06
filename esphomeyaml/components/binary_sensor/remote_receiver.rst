Remote Receiver Binary Sensor
=============================

.. seo::
    :description: Instructions for setting up remote receiver binary sensors for infrared and RF codes.
    :image: remote.png

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
------------------------

- **name** (**Required**, string): The name for the binary sensor.
- The remote code, see :ref:`remote_transmitter-codes`. Only one
  of them can be specified per binary sensor.
- **remote_receiver_id** (*Optional*, :ref:`config-id`): The id of the :doc:`/esphomeyaml/components/remote_receiver`.
  Defaults to the first hub in your configuration.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`
  and :ref:`MQTT Component <config-mqtt-component>`.

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

    Supporting the RF Bridge chip directly is currently only a long-term goal for esphomelib.


See Also
--------

- :doc:`index`
- :doc:`/esphomeyaml/components/remote_receiver`
- :doc:`/esphomeyaml/components/remote_transmitter`
- `RCSwitch <https://github.com/sui77/rc-switch>`__ by `Suat Özgür <https://github.com/sui77>`__
- `IRRemoteESP8266 <https://github.com/markszabo/IRremoteESP8266/>`__ by `Mark Szabo-Simon <https://github.com/markszabo>`__
- :doc:`API Reference </api/binary_sensor/remote_receiver>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/binary_sensor/remote_receiver.rst>`__

.. disqus::
