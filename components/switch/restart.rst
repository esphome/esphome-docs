Restart Switch
==============

.. seo::
    :description: Instructions for setting up switches that can remotely reboot the ESP in ESPHome.
    :image: restart.png

The ``restart`` switch platform allows you to restart your node remotely
through Home Assistant.

.. figure:: images/restart-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    switch:
      - platform: restart
        name: "Living Room Restart"

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the switch.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Switch <config-switch>`.

See Also
--------

- :doc:`shutdown`
- :doc:`safe_mode`
- :doc:`template`
- :apiref:`restart/restart_switch.h`
- :ghedit:`Edit`
