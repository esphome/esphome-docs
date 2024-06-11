Managed Updates via HTTP Request
================================

.. seo::
    :description: Instructions for using ESPHome's http_request update platform to manage updates on your devices.
    :image: system-update.svg
    :keywords: Updates, OTA, ESP32, ESP8266

This platform allows you to manage the deployment of updates to your ESPHome devices. It works by reading a YAML
manifest file and using it to determine the presence of an update. To use it, the following components are required in
your device's configuration:

- :doc:`/components/http_request`
- :doc:`/components/ota_http_request`

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
- **source** (**Required**, string): The URL of the YAML manifest file containing the firmware metadata.
- All other options from :ref:`Update <config-update>`.

See Also
--------

- :doc:`http_request`
- :doc:`/components/ota_http_request`
- :doc:`/components/ota`
- :apiref:`update/update_entity.h`
- :ghedit:`Edit`
