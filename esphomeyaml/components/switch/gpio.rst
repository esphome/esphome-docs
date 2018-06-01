GPIO Switch
===========

The ``gpio`` switch platform allows you to use any pin on your node as a
switch. You can for example hook up a relay to a GPIO pin and use it
through this platform.

.. figure:: images/gpio-ui.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    switch:
      - platform: gpio
        pin: 25
        name: "Living Room Dehumidifier"

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The
  GPIO pin to use for the switch.
- **name** (**Required**, string): The name for the switch.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Switch <config-switch>` and :ref:`MQTT Component <config-mqtt-component>`.

See Also
^^^^^^^^

- :doc:`index`
- :doc:`/esphomeyaml/components/output/gpio`
- :doc:`API Reference </api/switch/index>`
