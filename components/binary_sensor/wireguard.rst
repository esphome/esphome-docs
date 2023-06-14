WireGuard Status
================

This binary sensor can be used to check if the remote peer is online.

.. code-block:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: wireguard
        status:
          name: 'WireGuard Status'

Remember to setup the :doc:`/components/wireguard`.

Configuration variables
------------------------
- **name** (**Required**, string): The name of the binary sensor.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.

See Also
--------

- :doc:`/components/wireguard`
- :doc:`/components/sensor/wireguard`
- :ghedit:`Edit`

