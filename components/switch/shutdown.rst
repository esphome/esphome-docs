Shutdown Switch
===============

.. seo::
    :description: Instructions for setting up switches that can remotely shut down the ESP.
    :image: power_settings.svg

The ``shutdown`` switch platform allows you to shutdown your node remotely
through Home Assistant. It does this by putting the node into deep sleep mode with no
wakeup source selected. After enabling, the only way to startup the ESP again is by
pressing the reset button or restarting the power supply.

.. figure:: images/shutdown-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    switch:
      - platform: shutdown
        name: "Living Room Shutdown"

Configuration variables:
------------------------

- All options from :ref:`Switch <config-switch>`.

See Also
--------

- :doc:`restart`
- :doc:`safe_mode`
- :doc:`factory_reset`
- :doc:`/components/button/shutdown`
- :doc:`template`
- :apiref:`shutdown/shutdown_switch.h`
- :ghedit:`Edit`
