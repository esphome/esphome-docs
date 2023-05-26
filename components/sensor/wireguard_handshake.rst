WireGuard Latest Handshake
==========================

This sensor can be used to track the *timestamp*
of the latest completed handshake.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: wireguard_handshake
        name: 'WireGuard Latest Handshake'

Remember to setup the :doc:`/components/wireguard`.

Configuration variables
------------------------
- **name** (**Required**, string): The name of the sensor.
- **update_interval** (*Optional*, :ref:`config-time`): The amount of time
  to wait between two refresh of the latest value as reported by the
  underlying library. Default to ``60s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :doc:`/components/wireguard`
- :doc:`/components/binary_sensor/wireguard_status`
- :ghedit:`Edit`

