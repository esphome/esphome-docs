Home Assistant Sensor
=====================

.. seo::
    :description: Instructions for setting up Home Assistant sensors with ESPHome that import states from your Home Assistant instance.
    :image: home-assistant.png

The ``homeassistant`` sensor platform allows you to create sensors that import
states from your Home Assistant instance using the :doc:`native API </components/api>`.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: homeassistant
        name: "Temperature Sensor From Home Assistant"
        entity_id: sensor.temperature_sensor

With Home Assistant 2021.6 or newer, entity state attributes can also be imported.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: homeassistant
        id: current_temperature
        entity_id: climate.living_room
        attribute: current_temperature

.. note::

    This component is only for numeral states. If you want to import arbitrary text states
    from Home Assistant, use the :doc:`Home Assistant Text Sensor </components/text_sensor/homeassistant>`.
    
    Albeit you might not plan to __export__ states from the node and you do not need an entity of the node
    in Home Assistant, this component still requires you to register the node under Home Assistant. See:
    :doc:`Getting started with Home Assistant </guides/getting_started_hassio>`

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **entity_id** (**Required**, string): The entity ID to import from Home Assistant.
- **attribute** (*Optional*, string): The name of the state attribute to import from the
  specified entity. The entity state is used when this option is omitted.
  Requires Home Assistant 2021.6 or newer.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>`.

See Also
--------

- :ref:`sensor-filters`
- :ref:`automation`
- :apiref:`homeassistant/sensor/homeassistant_sensor.h`
- :ghedit:`Edit`
