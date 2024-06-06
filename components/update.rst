Managed Updates Component
=========================

.. seo::
    :description: Instructions for using the Update component to manage updates on your ESPHome devices.
    :image: system-update.svg
    :keywords: Updates, OTA, ESP8266, ESP32

This component allows you to manage the deployment of updates to your ESPHome devices. It works by reading a YAML
manifest file and using it to determine the presence of an update; it leverages the :doc:`ota_http_request`--which
must be present in your device's configuration--to download and install the update on the device.

.. code-block:: yaml

    # Example configuration entry
    update:
      - platform: http_request
        name: Firmware Update
        url: http://example.com/manifest.yaml

.. _update-configuration_variables:

Configuration variables:
------------------------

- **url** (**Required**, string, :ref:`templatable <config-templatable>`): The URL of the YAML manifest file containing
  the firmware metadata.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _update-on_update:

``on_update`` Trigger
---------------------

This trigger is activated when an update is available.

.. code-block:: yaml

    update:
      # ...
      on_update:
        - switch.turn_on: switch1


See Also
--------

- :doc:`ota_http_request`
- :apiref:`update/update_component.h`
- :ghedit:`Edit`
