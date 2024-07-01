Uptime Sensor
=============

.. seo::
    :description: Instructions for setting up a sensor that tracks the uptime of the ESP.
    :image: timer.svg

The ``uptime`` sensor allows you to track the time the ESP has stayed up for in seconds.
Time rollovers are automatically handled.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: uptime
        name: Uptime Sensor

Configuration variables:
------------------------

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``60s``.

- **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
- All other options from :ref:`Sensor <config-sensor>`.

Example
-------
To get a human readable uptime

.. code-block:: yaml

    sensor:
      - platform: uptime
        name: Uptime Sensor
        id: uptime_seconds
        internal: true
        on_value:
          then: 
            - lambda: |-
                char buffer[25];
                int seconds = (id(uptime_seconds).state);
                int days = seconds / (24 * 3600);
                seconds = seconds % (24 * 3600);
                int hours = seconds / 3600;
                seconds = seconds % 3600;
                int minutes = seconds /  60;
                seconds = seconds % 60;
                sprintf(buffer, "%d days %d:%d:%d", days, hours, minutes, seconds);
                id(uptime_human).publish_state(to_string(buffer));
    
    text_sensor:
      - platform: template
        name: ${device_name} Uptime Human Readable
        id: uptime_human
        icon: mdi:clock-start
        disabled_by_default: true

See Also
--------

- :ref:`sensor-filters`
- :apiref:`uptime/uptime_sensor.h`
- :ghedit:`Edit`
