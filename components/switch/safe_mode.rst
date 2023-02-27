Safe Mode Switch
================

.. seo::
    :description: Instructions for setting up switches that can remotely reboot the ESP in ESPHome into safe mode.
    :image: restart.svg

The ``safe_mode`` switch allows you to remotely reboot your node into :ref:`Safe Mode <config-ota>`. This is useful in certain situations where a misbehaving component is preventing Over-The-Air updates from completing successfully which can cause a "Retry" error message to be displayed after an unsuccessful update.  Can also help with certain OTA update scenarios that complete very slowly, sometimes pausing several times during the update. Certain low RAM situations can also cause slow or failed OTA updates and safe_mode may help OTA updates complete.

This component requires :ref:`OTA <config-ota>` to be configured.

.. figure:: images/safemode-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    switch:
      - platform: safe_mode
        name: "Living Room Restart (Safe Mode)"

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the switch.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Switch <config-switch>`.

See Also
--------

- :doc:`shutdown`
- :doc:`restart`
- :doc:`factory_reset`
- :doc:`/components/button/safe_mode`
- :doc:`template`
- :apiref:`safe_mode/safe_mode_switch.h`
- :ghedit:`Edit`
