Managed Updates
===============

.. seo::
    :description: Instructions for using the Update component to manage updates on your ESPHome devices.
    :image: system-update.svg
    :keywords: Updates, OTA, ESP8266, ESP32

This component allows you to manage the deployment of updates to your ESPHome devices. It works by reading a YAML
manifest file and using it to determine the presence of an update. To use it, the following components are required in
your device's configuration:

- :doc:`http_request`
- :doc:`ota_http_request`

.. code-block:: yaml

    # Example configuration entry
    update:
      - platform: http_request
        name: Firmware Update
        source: http://example.com/manifest.yaml

.. _update-configuration_variables:

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (*Optional*, string): The name for the update component.
- **source** (**Required**, string): The URL of the YAML manifest file containing
  the firmware metadata.

.. _update-on_update_available:

``on_update_available`` Trigger
-------------------------------

This trigger is activated when an update is available.

.. code-block:: yaml

    update:
      # ...
      on_update_available:
        - switch.turn_on: switch1

.. _update-update_is_available:

``update.is_available`` Condition
---------------------------------

This condition will be true when an update is available.

.. code-block:: yaml

    on_...:
      if:
        condition:
          update.is_available:
        then: # ...

See Also
--------

- :doc:`http_request`
- :doc:`ota_http_request`
- :apiref:`update/update_entity.h`
- :ghedit:`Edit`
