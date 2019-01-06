Restart Switch
==============

.. seo::
    :description: Instructions for setting up switches that can remotely reboot the ESP in esphomelib.
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
- All other options from :ref:`Switch <config-switch>` and :ref:`MQTT Component <config-mqtt-component>`.

See Also
--------

- :doc:`shutdown`
- :doc:`template`
- :doc:`API Reference </api/switch/restart>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/switch/restart.rst>`__

.. disqus::
