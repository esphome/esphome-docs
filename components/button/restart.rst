Restart Button
==============

.. seo::
    :description: Instructions for setting up buttons that can remotely reboot the ESP in ESPHome.
    :image: restart.svg

The ``restart`` button platform allows you to restart your node remotely
through Home Assistant.

.. code-block:: yaml

    # Example configuration entry
    button:
      - platform: restart
        name: "Living Room Restart"

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the button.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Button <config-button>`.

See Also
--------

- :doc:`/components/switch/restart`
- :doc:`template`
- :apiref:`restart/button/restart_button.h`
- :ghedit:`Edit`
