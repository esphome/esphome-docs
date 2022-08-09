Restart Switch
==============

.. esphome:component-definition::
   :alias: restart
   :category: switch-components
   :friendly_name: Restart Switch
   :toc_group: Switch Components
   :toc_image: restart.svg

.. seo::
    :description: Instructions for setting up switches that can remotely reboot the ESP in ESPHome.
    :image: restart.svg

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

- :doc:`/components/button/restart`
- :doc:`shutdown`
- :doc:`safe_mode`
- :doc:`template`
- :apiref:`restart/switch/restart_switch.h`
- :ghedit:`Edit`
