Generic Output Switch
=====================

The ``output`` switch platform allows you to use any output component as a switch.

.. figure:: images/output-ui.png
    :align: center
    :width: 80.0%

.. code:: yaml

    # Example configuration entry
    output:
      - platform: gpio
        pin: 25
        id: 'generic_out'
    switch:
      - platform: output
        name: "Generic Output"
        output: 'generic_out'

Configuration variables:
------------------------

- **output** (**Required**, :ref:`config-id`): The ID of the output component to use.
- **name** (**Required**, string): The name for the switch.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Switch <config-switch>` and :ref:`MQTT Component <config-mqtt-component>`.

See Also
--------

- :doc:`/esphomeyaml/components/output/index`
- :doc:`API Reference </api/switch/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/switch/output.rst>`__
