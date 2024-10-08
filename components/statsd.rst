.. _statsd:

StatsD
========

.. seo::
    :description: Instructions for setting up a StatsD
    :keywords: StatsD, metrics

StatsD is a `protocol <https://github.com/statsd/statsd/blob/master/docs/metric_types.md>`_ to send metrics to a Daemon to store and aggregate them.
Today there are many monitoring solutions that support receiving metrics via the StatsD protocol.


.. code-block:: yaml

    # Example configuration entry
    statsd:
      host: REPLACEME
      sensors:
        id: some_sensor
        name: test1.sensor

    sensor:
      platform: ...
      id: some_sensor


This example will generate a metric named `test1.sensor` with the value of the `some_sensor` sensor.


Configuration variables:
------------------------

- **host** (**Required**, ip): The Host IP of your StatsD Server.
- **port** (*Optional*, uint16): The Port of your StatsD Server. Defaults to ``8125``.
- **prefix** (*Optional*, string): The prefix to automatically prepend every metric with.  Defaults to ``""``.
- **update_interval** (*Optional*, uint16): How often to send the metrics. Defaults to ``10s``.
- **sensor** (*Optional*, :ref:`sensors`): A list of sensors to generate metrics for.
- **binary_sensor** (*Optional*, :ref:`sensors`): A list of binary sensors to generate metrics for.

.. _sensors:

Sensor list
-----------

- **id** (**Required**, :ref:`config-id`): The ID of the sensor.
- **name** (**Required**, name): The Name of the metric the sensor value is send as. (Prefix is added to this name).

See Also
--------

- :apiref:`statsd/statsd.h`
- :ghedit:`Edit`
