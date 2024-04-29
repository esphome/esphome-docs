.. _statsd:

StatsD
========

.. seo::
    :description: Instructions for setting up a StatsD
    :keywords: StatsD, metrics

StatsD is a `protocol <https://github.com/statsd/statsd/blob/master/docs/metric_types.md>`_ to send metrics to a Daemon to store and aggregate them.
Today there are many monitoring solutions that support receiving metrics via the StatsD protocol.

.. note::

    This component will only work with Arduino for the ESP8266 since the `esphome::socket` implementation does not support UDP.
    ESP32 will work fine with or without Arduino as Framework.

.. code-block:: yaml

    # Example configuration entry
    statsd:
      host: 192.168.178.20
      prefix: esphome
      sensors:
        id: wlan_signal
        name: test1.wifi.signal

    sensor:
      platform: wifi_signal
      id: wlan_signal
      name: "WiFi Signal"
      update_interval: 10s


This example will generate a metric named `esphome.test1.wifi.signal` with the value of the `wifi_signal` sensor.


Configuration variables:
------------------------

- **host** (**Required**, ip): The Host IP of your StatsD Server.
- **post** (*Optional*, uint16): The Port of your StatsD Server. Defaults to ``8125``.
- **prefix** (*Optional*, string): The prefix to automatically prepend every metric with.  Defaults to ``""``.
- **update_interval** (*Optional*, uint16): How often to send the metrics. Defaults to ``10s``.
- **sensor** (*Optional*, :ref:`sensors`): A list of sensors to generate metrics for.
- **binary_sensor** (*Optional*, :ref:`sensors`): A list of binary sensors to generate metrics for.

.. _sensors:

Sensor list
-----------

- **id** (**Required**, id): The ID of the sensor.
- **name** (**Required**, name): The Name of the metric the sensor value is send as. (Prefix is added to this name).
