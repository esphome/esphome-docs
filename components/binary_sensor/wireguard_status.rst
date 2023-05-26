WireGuard Status
================

This binary sensor can be used to check if the remote peer is online.

.. code-block:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: wireguard_status
        name: 'WireGuard Status'

Remember to setup the :doc:`/components/wireguard`.

Configuration variables
------------------------
- **name** (**Required**, string): The name of the binary sensor.
- **update_interval** (*Optional*, :ref:`config-time`): The amount of time
  to wait between two checks. Default to ``10s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.

See Also
--------

- :doc:`/components/wireguard`
- :doc:`/components/sensor/wireguard_handshake`
- :ghedit:`Edit`

