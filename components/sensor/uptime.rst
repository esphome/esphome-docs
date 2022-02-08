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

Human readable sensor
---------------------

The sensor reports uptime in seconds which is good for automations
but is hard to read for humans, this example creates a text sensor
with human readable output.

.. code-block:: yaml

    # Example configuration entry
    text_sensor:
      - platform: template
        name: Uptime Human Readable
        id: uptime_human
        icon: mdi:clock-start
    sensor:
      - platform: uptime
        name: Uptime Sensor
        id: uptime_sensor
        update_interval: 60s
        on_raw_value:
          then:
            - text_sensor.template.publish:
                id: uptime_human
                state: !lambda |-
                  int seconds = round(id(uptime_sensor).raw_state);
                  int days = seconds / (24 * 3600);
                  seconds = seconds % (24 * 3600);
                  int hours = seconds / 3600;
                  seconds = seconds % 3600;
                  int minutes = seconds /  60;
                  seconds = seconds % 60;
                  return (
                    (days ? to_string(days) + "d " : "") +
                    (hours ? to_string(hours) + "h " : "") +
                    (minutes ? to_string(minutes) + "m " : "") +
                    (to_string(seconds) + "s") 
                  ).c_str();

See Also
--------

- :ref:`sensor-filters`
- :apiref:`uptime/uptime_sensor.h`
- :ghedit:`Edit`
