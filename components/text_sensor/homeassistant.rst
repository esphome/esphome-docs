Home Assistant Text Sensor
==========================

.. seo::
    :description: Instructions for setting up Home Assistant text sensors with ESPHome that import states from your Home Assistant instance.
    :image: home-assistant.svg

The ``homeassistant`` text sensor platform allows you to create a sensors that import
states from your Home Assistant instance using the :doc:`native API </components/api>`.

.. code-block:: yaml

    # Example configuration entry
    text_sensor:
      - platform: homeassistant
        name: "Weather Forecast From Home Assistant"
        entity_id: sensor.weather_forecast

Entity state attributes can also be imported:

.. code-block:: yaml

    # Example configuration entry
    text_sensor:
      - platform: homeassistant
        id: effect
        entity_id: light.led_strip
        attribute: effect

Configuration variables:
------------------------

- **name** (*Optional*, string): The name of the text sensor.
- **entity_id** (**Required**, string): The entity ID to import from Home Assistant.
- **attribute** (*Optional*, string): The name of the state attribute to import from the
  specified entity. The entity state is used when this option is omitted.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Text Sensor <config-text_sensor>`.

See Also
--------

- :ref:`sensor-filters`
- :ref:`automation`
- :apiref:`homeassistant/text_sensor/homeassistant_text_sensor.h`
- :ghedit:`Edit`
