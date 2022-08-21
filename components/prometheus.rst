Prometheus Component
====================

.. seo::
    :description: Instructions for setting up a prometheus exporter with ESPHome.
    :image: prometheus.svg

The ``prometheus`` component enables an HTTP endpoint for the
:doc:`web_server` in order to integrate a `Prometheus <https://prometheus.io/>`__ installation.

This can be used to scrape data directly into your Prometheus-based monitoring and alerting-system,
without the need of any other software.

The list of available metrics can be found by directly browsing your node under
``<ip or node_name.local>/metrics``, and may be increased in the future.

.. code-block:: yaml

    # Example configuration entry
    web_server:

    # Activates prometheus /metrics endpoint
    prometheus:


Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **include_internal** (*Optional*, boolean): Whether ``internal`` entities should be displayed on the
  web interface. Defaults to ``false``.

.. note::

    Example integration into the configuration of your prometheus:

    .. code-block:: yaml

        scrape_configs:
          - job_name: esphome
            static_configs:
              - targets: [<ip or node_name.local>]

Metric Relabeling
-----------------

ESPHome allows you to do some basic relabeling of Prometheus metrics.
This is useful if you want to have different metric names or IDs than those shown in Home Assistant or the web interface.

You can relabel metric names or IDs it by adding a ``relabel`` block in the ``prometheus`` configuration,
and then adding key-value pairs with the string to be replaced and its replacement string.


``relabel``
***********

Lookup the current value of the metric name or ID, and return the replacement if found.
Does not change the value of the metric name or ID if the current value wasn't found.

.. code-block:: yaml

    # Example configuration entry
    prometheus:
      relabel:
        "Wifi Signal": RSSI
        wifi_signal: rssi
        "Status: Light": Light
        status_light: light


See Also
--------

- :apiref:`prometheus/prometheus_handler.h`
- :ghedit:`Edit`
