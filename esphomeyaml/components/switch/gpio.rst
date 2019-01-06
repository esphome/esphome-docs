GPIO Switch
===========

.. seo::
    :description: Instructions for setting up GPIO pin switches in esphomelib that control GPIO outputs.
    :image: pin.png

The ``gpio`` switch platform allows you to use any pin on your node as a
switch. You can for example hook up a relay to a GPIO pin and use it
through this platform.

.. figure:: images/gpio-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    switch:
      - platform: gpio
        pin: 25
        name: "Living Room Dehumidifier"

Configuration variables:
------------------------

- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The
  GPIO pin to use for the switch.
- **name** (**Required**, string): The name for the switch.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Switch <config-switch>` and :ref:`MQTT Component <config-mqtt-component>`.

.. note::

    esphomelib will attempt to restore the state of the switch on boot-up and write the value
    very early in the boot process.

    Please note that certain pins can have pull-up/down resistors that activate/deactivate a pin before
    esphomelib can initialize them. Please check with a multimeter and use another pin if necessary.

See Also
--------

- :doc:`index`
- :doc:`/esphomeyaml/components/output/gpio`
- :doc:`API Reference </api/switch/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/switch/gpio.rst>`__

.. disqus::
