WireGuard Latest Handshake
==========================

This sensor can be used to track the *timestamp*
of the latest completed handshake.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: wireguard
        latest_handshake:
          name: 'WireGuard Latest Handshake'

Remember to setup the :doc:`/components/wireguard`.

Configuration variables
------------------------
- **name** (**Required**, string): The name of the sensor.
- All other options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :doc:`/components/wireguard`
- :doc:`/components/binary_sensor/wireguard`
- :ghedit:`Edit`

