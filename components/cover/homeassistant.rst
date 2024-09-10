Home Assistant Cover
====================

.. seo::
    :description: Instructions for setting up Home Assistant Cover with ESPHome that import states and allows control via your Home Assistant instance.
    :image: home-assistant.svg

The ``homeassistant`` Cover platform allows you to create Cover that **import**
states and allow **control** via your Home Assistant instance using the :doc:`native API </components/api>`.

.. code-block:: yaml

    # Example configuration entry
    cover:
      - platform: homeassistant
        name: "Input Boolean From Home Assistant"
        entity_id: cover.my_cool_cover

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the binary sensor.
- **entity_id** (**Required**, string): The entity ID to import / control from Home Assistant.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-cover>`.

See Also
--------

- :ref:`automation`
- :apiref:`homeassistant/cover/homeassistant_cover.h`
- :ghedit:`Edit`
