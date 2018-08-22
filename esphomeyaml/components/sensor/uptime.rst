Uptime Sensor
=============

The ``uptime`` sensor allows you to track the time the ESP has stayed up for in seconds.
Time rollovers are automatically handled.

.. code:: yaml

    # Example configuration entry
    sensor:
      - platform: uptime
        name: Uptime Sensor

Configuration variables:
------------------------

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``15s``.
  See :ref:`sensor-default_filter`.
- **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
- All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.
