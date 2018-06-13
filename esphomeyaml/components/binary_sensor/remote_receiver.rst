Remote Receiver Binary Sensor
=============================

The ``remote_receiver`` binary sensor lets you track when a button on a remote control is pressed.

Each time the pre-defined signal is received, the binary sensor will briefly go ON and
then immediately OFF.

.. code:: yaml

    # Example configuration entry
    remote_receiver:
      pin: GPIO32
      dump: all

    binary_sensor:
      - platform: remote_receiver
        panasonic:
          address: 0x4004
          command: 0x100BCBD

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

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

See Also
--------

- :doc:`index`
- :doc:`/esphomeyaml/components/remote_receiver`
- :doc:`/esphomeyaml/components/remote_transmitter`
- :doc:`API Reference </api/binary_sensor/remote_receiver>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/binary_sensor/remote_receiver.rst>`__
