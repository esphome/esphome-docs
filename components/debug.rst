Debug Component
===============

.. seo::
    :description: Instructions for setting up the debug component in ESPHome
    :image: bug-report.png

The ``debug`` component can be used to debug problems with ESPHome. At startup, it prints
a bunch of useful information like reset reason, free heap size, ESPHome version and so on.

.. figure:: images/debug.png
    :align: center

    Example debug component output.

.. code-block:: yaml

    # Example configuration entry
    debug:

    # Logger must be at least debug (default)
    logger:
      level: debug

No configuration variables.

See Also
--------

- :doc:`logger`
- :apiref:`debug/debug_component.h`
- :ghedit:`Edit`
