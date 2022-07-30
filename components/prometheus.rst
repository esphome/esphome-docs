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

Metric Filters
-------------------

ESPHome allows you to do some basic relabeling of Prometheus metrics.
This is for example useful if you want to have different metric names than those shown in the web interface.

There is currently only support for the ``map`` filter. You define it by adding a ``filters`` block in the ``prometheus`` configuration,
and then adding a ``map`` block to the ``filters`` block.


``map``
*******

Lookup the current value of the metric name or ID in a list, and return the matching item if found.
Does not change the value of the metric name or ID if the current value wasn't found.

.. code-block:: yaml

    # Example configuration entry
    prometheus:
      filters:
        map:
          - Wifi Signal -> RSSI
          - wifi_signal -> rssi
          - "Status: Light -> Light"
          - status_light -> light

The arguments are a list of substitutions, each in the form ``LOOKUP -> REPLACEMENT``.

See Also
--------

- :apiref:`prometheus/prometheus_handler.h`
- :ghedit:`Edit`
