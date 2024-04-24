Home Assistant Binary Sensor
============================

.. seo::
    :description: Instructions for setting up Home Assistant binary sensors with ESPHome that import states from your Home Assistant instance.
    :image: home-assistant.svg

The ``homeassistant`` binary sensor platform allows you to create binary sensors that **import**
states from your Home Assistant instance using the :doc:`native API </components/api>`.

.. code-block:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: homeassistant
        name: "Input Boolean From Home Assistant"
        entity_id: input_boolean.state_home

With Home Assistant 2021.6 or newer, entity state attributes can also be imported.

.. code-block:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: homeassistant
        id: muted
        entity_id: media_player.mega_speakers
        attribute: is_volume_muted

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the binary sensor.
- **entity_id** (**Required**, string): The entity ID to import from Home Assistant.
- **attribute** (*Optional*, string): The name of the state attribute to import from the
  specified entity. The entity state is used when this option is omitted.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.

See Also
--------

- :ref:`automation`
- :apiref:`homeassistant/binary_sensor/homeassistant_binary_sensor.h`
- :ghedit:`Edit`
