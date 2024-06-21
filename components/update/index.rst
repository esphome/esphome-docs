Update Core
===========

.. seo::
    :description: Instructions for using Update entities to manage updates on your ESPHome devices.
    :image: system-update.svg
    :keywords: Updates, OTA, ESP32, ESP8266

The `update` component allows your ESPHome devices to install updates from a remote source; instead of
:doc:`"pushing" an update to your device </components/ota/index>`, the device can retrieve an update and
install it on its own.

.. code-block:: yaml

    # Example configuration entry
    update:
      - platform: ...

.. _config-update:

Configuration variables:
------------------------

- **name** (*Optional*, string): The name to use for the update component.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **device_class** (*Optional*, string): The device class for the update entity. See
  https://www.home-assistant.io/integrations/binary_sensor/#device-class for a list of available options.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI). Defaults to ``false``.
- **entity_category** (*Optional*, string): The category of the update entity. See
  https://developers.home-assistant.io/docs/core/entity/#generic-properties for a list of available options.
- **icon** (*Optional*, icon): The icon to use for the update entity in the frontend.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Specifying an ``id`` without a ``name`` will
  implicitly set this to true.

See Also
--------

.. toctree::
    :maxdepth: 1
    :glob:

    *

- :ghedit:`Edit`
