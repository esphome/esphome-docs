Generic Output Switch
=====================

.. esphome:component-definition::
   :alias: output
   :category: switch-components
   :friendly_name: Generic Output Switch
   :toc_group: Switch Components
   :toc_image: upload.svg

.. seo::
    :description: Instructions for setting up generic output switches in ESPHome that control an output component.
    :image: upload.svg

The ``output`` switch platform allows you to use any output component as a switch.

.. figure:: images/output-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

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
- **restore_mode** (*Optional*): Control how the switch attempts to restore state on bootup.
  For restoring on ESP8266s, also see ``esp8266_restore_from_flash`` in the
  :doc:`esphome section </components/esphome>`.

    - ``RESTORE_DEFAULT_OFF`` (Default) - Attempt to restore state and default to OFF if not possible to restore.
    - ``RESTORE_DEFAULT_ON`` - Attempt to restore state and default to ON.
    - ``RESTORE_INVERTED_DEFAULT_OFF`` - Attempt to restore state inverted from the previous state and default to OFF.
    - ``RESTORE_INVERTED_DEFAULT_ON`` - Attempt to restore state inverted from the previous state and default to ON.
    - ``ALWAYS_OFF`` - Always initialize the pin as OFF on bootup.
    - ``ALWAYS_ON`` - Always initialize the pin as ON on bootup.

- All other options from :ref:`Switch <config-switch>`.

See Also
--------

- :doc:`/components/output/index`
- :apiref:`output/switch/output_switch.h`
- :ghedit:`Edit`
