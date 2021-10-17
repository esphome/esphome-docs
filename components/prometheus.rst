Prometheus Component
====================

.. seo::
    :description: Instructions for setting up a prometheus exporter with ESPHome.
    :image: prometheus.png

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

.. note::

    Example integration into the configuration of your prometheus:

    .. code-block:: yaml

        scrape_configs:
          - job_name: esphome
            static_configs:
              - targets: [<ip or node_name.local>]

See Also
--------

- :apiref:`prometheus/prometheus_handler.h`
- :ghedit:`Edit`
