Update Core
===========

.. seo::
    :description: Instructions for using Update entities to manage updates on your ESPHome devices.
    :image: system-update.svg
    :keywords: Updates, OTA, ESP32, ESP8266

The `update` component allows your ESPHome devices to install updates from a remote source; instead of
:doc:`"pushing" an update to your device </components/ota>`, the device can retrieve an update and install it on its own.

.. code-block:: yaml

    # Example configuration entry
    update:
      - platform: ...

.. _config-update:

See Also
--------

.. toctree::
    :maxdepth: 1
    :glob:

    *

- :ghedit:`Edit`
