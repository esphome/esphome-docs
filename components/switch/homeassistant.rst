Home Assistant Switch
====================

.. seo::
    :description: Instructions for setting up Home Assistant Switch with ESPHome that import states and allows control via your Home Assistant instance.
    :image: home-assistant.svg

The ``homeassistant`` Switch platform allows you to create Switch that **import**
states and allow **control** via your Home Assistant instance using the :doc:`native API </components/api>`.

.. code-block:: yaml

    # Example configuration entry
    switch:
      - platform: homeassistant
        name: "Switch from Home Assistant"
        entity_id: switch.my_cool_switch

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the binary sensor.
- **entity_id** (**Required**, string): The entity ID to import / control from Home Assistant.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Switch <config-switch>`.

See Also
--------

- :ref:`automation`
- :apiref:`homeassistant/switch/homeassistant_switch.h`
- :ghedit:`Edit`
